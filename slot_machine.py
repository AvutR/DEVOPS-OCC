#!/usr/bin/env python3
"""
VEGAS STYLE SLOT MACHINE
A simple, archaic text-based slot machine game
"""

import random

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


def print_banner():
    """Print the slot machine banner"""
    print("\n" + "=" * 50)
    print("      *** VEGAS STYLE SLOT MACHINE ***")
    print("=" * 50)


def spin_reel():
    """Spin a single reel and return a symbol"""
    return random.choice(SYMBOLS)


def display_result(reel1, reel2, reel3):
    """Display the spinning reels in ASCII art"""
    print("\n")
    print("     +-------+-------+-------+")
    print(f"     |  {reel1:^3}  |  {reel2:^3}  |  {reel3:^3}  |")
    print("     +-------+-------+-------+")
    print()


def check_win(reel1, reel2, reel3):
    """Check if the spin is a winning combination"""
    result = (reel1, reel2, reel3)
    return PAYOUTS.get(result, 0)


def play_game():
    """Main game loop"""
    balance = 100
    
    print_banner()
    print(f"\nStarting Balance: ${balance}")
    print("\nPress ENTER to SPIN... (bet = $5)")
    print("Type 'quit' to exit\n")
    
    while balance > 0:
        user_input = input(">>> ").strip().lower()
        
        if user_input == 'quit':
            print(f"\nFinal Balance: ${balance}")
            print("Thanks for playing!")
            break
        
        if user_input != '':
            continue
            
        # Take bet
        balance -= 5
        
        if balance < 0:
            balance += 5
            print("Not enough balance!")
            continue
        
        # Spin the reels
        print("\nSPINNING...")
        reel1 = spin_reel()
        reel2 = spin_reel()
        reel3 = spin_reel()
        
        # Display result
        display_result(reel1, reel2, reel3)
        
        # Check for win
        winnings = check_win(reel1, reel2, reel3)
        
        if winnings > 0:
            balance += winnings
            print(f"*** YOU WIN ${winnings}!!! ***\n")
        else:
            print("SORRY... BETTER LUCK NEXT TIME!\n")
        
        print(f"Balance: ${balance}")
        
        if balance <= 0:
            print("\nGAME OVER - NO BALANCE LEFT!")
            break


if __name__ == "__main__":
    play_game()
