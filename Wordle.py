# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS

def wordle():

    def enter_action(s):
        gw.show_message("You have to implement this method.")

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)
    # Milestone 1: Choosing a random word and having it appear in the first row of the window 
   
    N_ROWS = 6
    N_COLS = 5

    ColumnDecrement = 5
    random_word = random.choice(FIVE_LETTER_WORDS).upper()
    for char in random_word:
        gw.set_square_letter(N_ROWS - 6, N_COLS - ColumnDecrement, char)
        ColumnDecrement = ColumnDecrement - 1
    

# Startup code

if __name__ == "__main__":
    wordle()



