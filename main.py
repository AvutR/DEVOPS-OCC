#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from slot_engine import SlotEngine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import stats_collection, users_collection
from datetime import datetime
from passlib.context import CryptContext
import secrets
from typing import Optional

app = FastAPI(title="Vegas Slot Machine API", version="3.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory sessions (username -> token)
sessions = {}
user_engines = {}  # username -> SlotEngine instance


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class SpinRequest(BaseModel):
    bet_amount: int = 5


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """Validate session token and return username"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    username = None
    
    for user, user_token in sessions.items():
        if user_token == token:
            username = user
            break
    
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return username


def get_user_engine(username: str) -> SlotEngine:
    """Get or create SlotEngine for user"""
    if username not in user_engines:
        # Load user's current balance from DB
        user_doc = users_collection.find_one({"username": username})
        balance = user_doc.get("balance", 100) if user_doc else 100
        user_engines[username] = SlotEngine(starting_balance=balance)
    return user_engines[username]


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# ------------------ AUTH ------------------

@app.post("/register")
def register(user: UserRegister):
    """Register a new user"""
    if len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    
    if len(user.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")
    
    # Check if user exists
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password and create user
    hashed_password = pwd_context.hash(user.password)
    
    users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "balance": 100,
        "created_at": datetime.utcnow()
    })
    
    # Create session
    token = secrets.token_urlsafe(32)
    sessions[user.username] = token
    
    # Initialize engine
    user_engines[user.username] = SlotEngine(starting_balance=100)
    
    return {
        "message": "User registered successfully",
        "token": token,
        "username": user.username,
        "balance": 100
    }


@app.post("/login")
def login(user: UserLogin):
    """Login existing user"""
    user_doc = users_collection.find_one({"username": user.username})
    
    if not user_doc or not pwd_context.verify(user.password, user_doc["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create new session
    token = secrets.token_urlsafe(32)
    sessions[user.username] = token
    
    # Load user's balance
    balance = user_doc.get("balance", 100)
    user_engines[user.username] = SlotEngine(starting_balance=balance)
    
    return {
        "message": "Login successful",
        "token": token,
        "username": user.username,
        "balance": balance
    }


@app.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    """Logout current user"""
    username = get_current_user(authorization)
    
    # Save balance before logout
    if username in user_engines:
        engine = user_engines[username]
        users_collection.update_one(
            {"username": username},
            {"$set": {"balance": engine.balance}}
        )
        del user_engines[username]
    
    if username in sessions:
        del sessions[username]
    
    return {"message": "Logout successful"}


# ------------------ SPIN ------------------

@app.post("/spin")
def spin(request: SpinRequest, authorization: Optional[str] = Header(None)):
    username = get_current_user(authorization)
    engine = get_user_engine(username)
    
    bet_amount = request.bet_amount

    if engine.balance <= 0:
        raise HTTPException(status_code=400, detail="Game Over - Reset Required")

    if not engine.place_bet(bet_amount):
        raise HTTPException(status_code=400, detail="Insufficient balance")

    reel1, reel2, reel3 = engine.spin()
    winnings = engine.check_win(reel1, reel2, reel3)

    if winnings > 0:
        engine.add_winnings(winnings)

    spin_doc = {
        "username": username,
        "timestamp": datetime.utcnow(),
        "reels": [reel1, reel2, reel3],
        "bet": bet_amount,
        "winnings": winnings,
        "balance_after": engine.balance,
        "is_winner": winnings > 0
    }

    stats_collection.insert_one(spin_doc)
    
    # Update user balance in DB
    users_collection.update_one(
        {"username": username},
        {"$set": {"balance": engine.balance}}
    )

    return {
        "reel1": reel1,
        "reel2": reel2,
        "reel3": reel3,
        "bet_amount": bet_amount,
        "winnings": winnings,
        "new_balance": engine.balance,
        "is_winner": winnings > 0,
    }


# ------------------ RESET ------------------

@app.post("/reset")
def reset_game(authorization: Optional[str] = Header(None)):
    username = get_current_user(authorization)
    
    # Reset user's balance to 100
    user_engines[username] = SlotEngine(starting_balance=100)
    
    users_collection.update_one(
        {"username": username},
        {"$set": {"balance": 100}}
    )
    
    # Clear only this user's stats
    stats_collection.delete_many({"username": username})

    return {"message": "Game reset to $100", "balance": 100}


# ------------------ STATS ------------------

@app.get("/stats")
def get_stats(authorization: Optional[str] = Header(None)):
    username = get_current_user(authorization)
    
    total_spins = stats_collection.count_documents({"username": username})
    total_wins = stats_collection.count_documents({"username": username, "is_winner": True})

    total_amount_won = 0
    highest_win = 0
    current_streak = 0
    max_streak = 0

    for doc in stats_collection.find({"username": username}).sort("timestamp", 1):
        total_amount_won += doc["winnings"]

        if doc["winnings"] > highest_win:
            highest_win = doc["winnings"]

        if doc["is_winner"]:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            current_streak = 0

    win_rate = (total_wins / total_spins * 100) if total_spins > 0 else 0

    last_5_spins = list(
        stats_collection.find({"username": username}).sort("timestamp", -1).limit(5)
    )

    formatted_last_5 = [
        {
            "reels": doc["reels"],
            "winnings": doc["winnings"]
        }
        for doc in last_5_spins
    ]

    return {
        "total_spins": total_spins,
        "total_wins": total_wins,
        "total_amount_won": total_amount_won,
        "win_rate": round(win_rate, 2),
        "highest_win": highest_win,
        "max_win_streak": max_streak,
        "last_5_spins": formatted_last_5
    }


# ------------------ LEADERBOARD ------------------

@app.get("/leaderboard")
def get_leaderboard():
    """Get top 10 players by balance"""
    leaderboard = list(
        users_collection.find(
            {},
            {"username": 1, "balance": 1, "_id": 0}
        ).sort("balance", -1).limit(10)
    )
    
    # Add rank
    for idx, entry in enumerate(leaderboard):
        entry["rank"] = idx + 1
    
    return {"leaderboard": leaderboard}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)