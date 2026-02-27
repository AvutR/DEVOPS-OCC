#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from slot_engine import SlotEngine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import stats_collection
from datetime import datetime

app = FastAPI(title="Vegas Slot Machine API", version="2.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

engine = SlotEngine(starting_balance=100)


class SpinRequest(BaseModel):
    bet_amount: int = 5


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# ------------------ SPIN ------------------

@app.post("/spin")
def spin(request: SpinRequest):

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
        "timestamp": datetime.utcnow(),
        "reels": [reel1, reel2, reel3],
        "bet": bet_amount,
        "winnings": winnings,
        "balance_after": engine.balance,
        "is_winner": winnings > 0
    }

    stats_collection.insert_one(spin_doc)

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
def reset_game():
    global engine
    engine = SlotEngine(starting_balance=100)

    # Clear DB stats for fresh game
    stats_collection.delete_many({})

    return {"message": "Game fully reset"}


# ------------------ STATS ------------------

@app.get("/stats")
def get_stats():

    total_spins = stats_collection.count_documents({})
    total_wins = stats_collection.count_documents({"is_winner": True})

    total_amount_won = 0
    highest_win = 0
    current_streak = 0
    max_streak = 0

    for doc in stats_collection.find().sort("timestamp", 1):
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
        stats_collection.find().sort("timestamp", -1).limit(5)
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)