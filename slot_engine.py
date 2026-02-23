#!/usr/bin/env python3
"""
SLOT ENGINE - Core slot machine logic
Handles reel spinning, win checking, and game state
"""

import random
from typing import Tuple


class SlotEngine:
    """Core slot machine engine"""
    
    # Reel symbols
    SYMBOLS = ['@', '#', '$', '*', '7', 'BAR', 'CHERRY', 'LEMON']
    
    # Payout table
    PAYOUTS = {
        ('7', '7', '7'): 1000,
        ('*', '*', '*'): 500,
        ('#', '#', '#'): 250,
        ('$', '$', '$'): 200,
        ('@', '@', '@'): 150,
    }
    
    def __init__(self, starting_balance: int = 100):
        """Initialize the slot engine with a starting balance"""
        self.balance = starting_balance
        self.starting_balance = starting_balance
        self.last_spin = None
        self.last_winnings = 0
    
    def spin(self) -> Tuple[str, str, str]:
        """Spin the reels and return the result"""
        reel1 = random.choice(self.SYMBOLS)
        reel2 = random.choice(self.SYMBOLS)
        reel3 = random.choice(self.SYMBOLS)
        
        self.last_spin = (reel1, reel2, reel3)
        return self.last_spin
    
    def check_win(self, reel1: str, reel2: str, reel3: str) -> int:
        """Check if the spin is a winning combination and return winnings"""
        result = (reel1, reel2, reel3)
        winnings = self.PAYOUTS.get(result, 0)
        return winnings
    
    def place_bet(self, amount: int) -> bool:
        """Place a bet, return True if successful"""
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def add_winnings(self, amount: int) -> None:
        """Add winnings to balance"""
        self.balance += amount
        self.last_winnings = amount
    
    def get_state(self) -> dict:
        """Get current game state"""
        return {
            'balance': self.balance,
            'starting_balance': self.starting_balance,
            'last_spin': self.last_spin,
            'last_winnings': self.last_winnings,
        }
