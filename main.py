#!/usr/bin/env python3
"""
SLOT MACHINE API - FastAPI Backend
Provides REST endpoints for slot machine operations
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from slot_engine import SlotEngine

app = FastAPI(title="Vegas Slot Machine API", version="1.0.0")

# Global engine instance
engine = SlotEngine(starting_balance=100)


# Request/Response Models
class SpinRequest(BaseModel):
    bet_amount: int = 5


class SpinResponse(BaseModel):
    reel1: str
    reel2: str
    reel3: str
    bet_amount: int
    winnings: int
    new_balance: int
    total_won: int
    is_winner: bool


class GameStateResponse(BaseModel):
    balance: int
    starting_balance: int
    last_spin: tuple | None
    last_winnings: int


@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Vegas Slot Machine API",
        "endpoints": {
            "GET /state": "Get current game state",
            "POST /spin": "Spin the reels",
            "POST /reset": "Reset the game",
        }
    }


@app.get("/state")
def get_state() -> GameStateResponse:
    """Get current game state"""
    state = engine.get_state()
    return GameStateResponse(
        balance=state['balance'],
        starting_balance=state['starting_balance'],
        last_spin=state['last_spin'],
        last_winnings=state['last_winnings'],
    )


@app.post("/spin")
def spin(request: SpinRequest = SpinRequest()) -> SpinResponse:
    """Spin the reels and calculate winnings"""
    bet_amount = request.bet_amount
    
    # Check if player has enough balance
    if not engine.place_bet(bet_amount):
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Spin the reels
    reel1, reel2, reel3 = engine.spin()
    
    # Check for win
    winnings = engine.check_win(reel1, reel2, reel3)
    
    # Add winnings to balance
    if winnings > 0:
        engine.add_winnings(winnings)
    
    return SpinResponse(
        reel1=reel1,
        reel2=reel2,
        reel3=reel3,
        bet_amount=bet_amount,
        winnings=winnings,
        new_balance=engine.balance,
        total_won=engine.last_winnings,
        is_winner=winnings > 0,
    )


@app.post("/reset")
def reset_game() -> GameStateResponse:
    """Reset the game to initial state"""
    global engine
    engine = SlotEngine(starting_balance=100)
    state = engine.get_state()
    return GameStateResponse(
        balance=state['balance'],
        starting_balance=state['starting_balance'],
        last_spin=state['last_spin'],
        last_winnings=state['last_winnings'],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
