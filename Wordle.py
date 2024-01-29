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
        countLetterList = []

        # Counts how many times a letter appears in the random word
        for letter in random_word:
            letterCount = 0
            for letter2 in random_word:
                if (letter == letter2):
                    letterCount = letterCount + 1
            countLetterList.append(letterCount)   

        current_row = gw.get_current_row() 
        
        randPosition = 0
        for letter in random_word:
            foundLetter = False     

            # This allows for comparison to start at the exact same spot 
            userPosition = randPosition

            # This allows for the one letter of the random word to be compared to every letter in the user's guess by resetting it to the first column, once it hits the 4th
            for i in range(0, 5, 1):
                if userPosition >= 5:
                    userPosition = 0 
                color = gw.get_square_color(current_row, userPosition)
                
                # The foundLetter allows us to move on to the next letter of the random word once it gets a green OR if every letter is unique in the word of the day 
                # This color thing is for a double letter in the random_word, without this it would replace a green square with a yellow one which is not what we want
                if not foundLetter and (color != CORRECT_COLOR):
                    if (letter == userList[userPosition]):
                        gw.set_square_color(current_row, userPosition, PRESENT_COLOR)
                        
                        # Makes sure that every letter is unique in the random word
                        # If not, then it will move onto the next letter in random word
                        # This fixes the double letters of a guess 
                        if countLetterList[randPosition] < 2:
                            foundLetter = True
                        
                        # If the letter matches another one AND is in the same exact spot, then it will turn green
                        # It will also move onto the next letter in the random word sequence
                        if (userPosition == randPosition):
                            gw.set_square_color(current_row, userPosition, CORRECT_COLOR)
                            foundLetter = True    
                
                userPosition = userPosition + 1     # Helps us keep track of which letter we are on in the user's guess
            randPosition = randPosition + 1         # Helps us keep track of which letter we are on in the random word

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
            # This fills in all the unknown squares to missing
            for x in range(5):
                color = gw.get_square_color(current_row, x)
                if (color == UNKNOWN_COLOR):
                    gw.set_square_color(current_row, x, MISSING_COLOR)

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
