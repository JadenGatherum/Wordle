# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR

def wordle():

    def enter_action(userGuess):
        # Call random word
        random_word = gw.current_word
        
        # Remove spaces
        userGuess = userGuess.strip().lower()

        # Make sure word is in word list
        if len(userGuess) != 5:
            gw.show_message("Not enough letters")
            return
        elif userGuess not in FIVE_LETTER_WORDS:
            gw.show_message("Not in word list")
            return
        
        # Increment guess number
        gw.num_guesses += 1

        userGuess = userGuess.upper()
        userList = list(userGuess)
        current_row = gw.get_current_row()

        # Initialize letter count
        letter_count = {}
        for letter in random_word:
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

        # Initialize a dictionary to track the most informative color for each key
        key_colors = {ch: UNKNOWN_COLOR for ch in userGuess}

        # First loop: Identify correct letters
        for i in range(len(random_word)):
            if userList[i] == random_word[i]:
                gw.set_square_color(current_row, i, CORRECT_COLOR)
                letter_count[userList[i]] -= 1
                key_colors[userList[i]] = CORRECT_COLOR  # Correct letters override any other color
            else:
                gw.set_square_color(current_row, i, UNKNOWN_COLOR)  # Temporarily set to UNKNOWN_COLOR

        # Second loop: Handle letters present but in the wrong position
        for i in range(len(random_word)):
            if gw.get_square_color(current_row, i) != CORRECT_COLOR:
                if userList[i] in random_word and letter_count[userList[i]] > 0:
                    gw.set_square_color(current_row, i, PRESENT_COLOR)
                    letter_count[userList[i]] -= 1
                    if key_colors[userList[i]] != CORRECT_COLOR:  # Don't override CORRECT_COLOR
                        key_colors[userList[i]] = PRESENT_COLOR
                else:
                    gw.set_square_color(current_row, i, MISSING_COLOR)
                    if key_colors[userList[i]] == UNKNOWN_COLOR:  # Only set to MISSING_COLOR if not already determined
                        key_colors[userList[i]] = MISSING_COLOR

        # Update the on-screen keyboard based on the accumulated key colors
        for ch, color in key_colors.items():
            current_key_color = gw.get_key_color(ch)
            # Ensure CORRECT_COLOR keys are not changed to PRESENT_COLOR
            if current_key_color != CORRECT_COLOR:
                gw.set_key_color(ch, color)
            elif color == MISSING_COLOR and current_key_color != CORRECT_COLOR:
                # Update the key to MISSING_COLOR only if it's not already set to a more informative color (CORRECT or PRESENT)
                gw.set_key_color(ch, MISSING_COLOR)

        if userGuess == random_word:
            # Update variables
            gw.games_won += 1
            gw.games_played += 1
            gw.current_streak += 1
            if(gw.current_streak > gw.max_streak):
                gw.max_streak = gw.current_streak

            # End game
            gw.show_message("Congratulations! You guessed the word.", CORRECT_COLOR)
            gw._root.after(2000, gw.end_screen)
            return
        else:
            gw.next_row()

        if current_row >= (N_ROWS - 1):
            # Update variables
            gw.games_played += 1
            gw.current_streak = 0

            # End game
            gw.show_message("Game over! The word was " + random_word)
            gw.num_guesses += 1
            gw._root.after(2000, gw.end_screen)
            return

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code
if __name__ == "__main__":
    wordle()
