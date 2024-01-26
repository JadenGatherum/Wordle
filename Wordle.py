# File: Wordle.py

"""
This module is the starter file for the Wordle assignment.
BE SURE TO UPDATE THIS COMMENT WHEN YOU WRITE THE CODE.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR

def wordle():

    # Milestone 1: Choosing a random word and having it appear in the first row of the window 
   
    # N_ROWS = 6
    # N_COLS = 5

    # ColumnDecrement = 5
    # random_word = random.choice(FIVE_LETTER_WORDS).upper()
    # for char in random_word:
    #     gw.set_square_letter(N_ROWS - 6, N_COLS - ColumnDecrement, char)
    #     ColumnDecrement = ColumnDecrement - 1

    # Choose a random word and store it as a variable
    random_word = random.choice(FIVE_LETTER_WORDS).upper()
    # random_word = "JOLLY"
    

    # Print the random word to the console for debugging                                       DELETE LATER
    print("Debug: The chosen word is", random_word)

    def enter_action(userGuess):
        # Remove spaces
        
        userGuess = userGuess.strip().lower()
        

        # Make sure word is in word list
        if len(userGuess) != 5:
            gw.show_message("Not enough letters")
            return
        elif userGuess not in FIVE_LETTER_WORDS:
            gw.show_message("Not in word list")
            return
        

        userGuess = userGuess.upper()
        userList = list(userGuess)
        countLetterList = []

        # counts how many times a letter appears in the word of the day
        for letter in random_word:
            letterCount = 0
            for letter2 in random_word:
                if (letter == letter2):
                    letterCount = letterCount + 1
            countLetterList.append(letterCount)    
        # print(countLetterList)
        
        randPosition = 0
        for letter in random_word:
            # print("The current position for " + random_word + " is " + str(randPosition) + " which is letter " + str(letter))
            foundLetter = False     

            # this allows for comparison to start at the exact same spot 
            userPosition = randPosition

            # this allows for the one letter of the word of the day to be compared to every letter in the user's guess by resetting it to the first column, once it hits the 4th
            for i in range(0, 5, 1):
                if userPosition >= 5:
                    userPosition = 0 
                # print("The current position for " + userGuess + " is " + str(userPosition) + " which is letter " + str(userList[userPosition]))
                color = gw.get_square_color(N_ROWS - 6, userPosition)
                
                # the foundLetter allows us to move on to the next letter of the random word once it gets a green OR if every letter is unique in the word of the day 
                # this color thing is for a double letter in the random_word, without this it would replace a green square with a yellow one which is not what we want
                if not foundLetter and (color != CORRECT_COLOR):
                    if (letter == userList[userPosition]):
                        gw.set_square_color(N_ROWS - 6, userPosition, PRESENT_COLOR)
                        
                        # makes sure that every letter is unique in the word of the day
                        # if not, then it will move onto the next letter in word of the day
                        # this fixes the double letters of a guess 
                        if countLetterList[randPosition] < 2:
                            foundLetter = True
                        # print("The letter " + str(userList[userPosition]) + " is yellow")
                        
                        # if the letter matches another one AND is in the same exact spot, then it will turn green
                        # it will also move onto the next letter in the "word of the day" sequence
                        if (userPosition == randPosition):
                            gw.set_square_color(N_ROWS - 6, userPosition, CORRECT_COLOR)
                            foundLetter = True
                            # print("The letter " + str(userList[userPosition]) + " is green")    
                
                userPosition = userPosition + 1 # helps us keep track of which letter we are on in the user's guess
            randPosition = randPosition + 1 # helps us keep track of which letter we are on in the word of the day
        
        # this fills in all the unknown squares to missing
        for x in range(5):
            color = gw.get_square_color(N_ROWS - 6, x)
            if (color == UNKNOWN_COLOR):
                gw.set_square_color(N_ROWS - 6, x, MISSING_COLOR)

        
    

    
    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
