# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS

def wordle():

    # Choose a random word and store it as a variable
    random_word = random.choice(FIVE_LETTER_WORDS).upper()

    def enter_action(s):
        # Remove spaces
        s = s.strip().lower()

        # Make sure word is in word list
        if len(s) != 5:
            gw.show_message("Not enough letters")
            return
        elif s not in FIVE_LETTER_WORDS:
            gw.show_message("Not in word list")
            return
        
        gw.show_message("You need to implement this method")

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
