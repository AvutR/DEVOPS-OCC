#!/usr/bin/env python3

import random
from typing import Tuple


class SlotEngine:

    SYMBOLS = ['@', '#', '$', '*', '7', 'BAR', 'CHERRY', 'LEMON']

    PAYOUTS = {
        ('7', '7', '7'): 1000,
        ('*', '*', '*'): 500,
        ('#', '#', '#'): 250,
        ('$', '$', '$'): 200,
        ('@', '@', '@'): 150,
    }

    def __init__(self, starting_balance: int = 100):
        self.balance = starting_balance
        self.starting_balance = starting_balance
        self.last_spin = None
        self.last_winnings = 0

    def spin(self) -> Tuple[str, str, str]:
        reel1 = random.choice(self.SYMBOLS)
        reel2 = random.choice(self.SYMBOLS)
        reel3 = random.choice(self.SYMBOLS)

        self.last_spin = (reel1, reel2, reel3)
        return self.last_spin

    def check_win(self, reel1: str, reel2: str, reel3: str) -> int:
        result = (reel1, reel2, reel3)
        return self.PAYOUTS.get(result, 0)

    def place_bet(self, amount: int) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def add_winnings(self, amount: int) -> None:
        self.balance += amount
        self.last_winnings = amount

    def get_state(self) -> dict:
        return {
            'balance': self.balance,
            'starting_balance': self.starting_balance,
            'last_spin': self.last_spin,
            'last_winnings': self.last_winnings,
        }