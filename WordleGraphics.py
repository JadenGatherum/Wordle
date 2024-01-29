# File: WordleGraphics.py

"""
This file implements the WordleGWindow class, which manages the
graphical display for the Wordle project.
"""

import atexit
import math
import time
import tkinter as tk
import random

from WordleDictionary import FIVE_LETTER_WORDS

# Constants

N_ROWS = 6			# Number of rows
N_COLS = 5			# Number of columns

CORRECT_COLOR = "#6AAA64"       # Light green for correct letters
PRESENT_COLOR = "#C9B458"       # Brownish yellow for misplaced letters
MISSING_COLOR = "#787C7E"       # Gray for letters that don't appear
UNKNOWN_COLOR = "#FFFFFF"       # Undetermined letters are white
KEY_COLOR = "#D3D6DA"           # Keys are colored light gray

CANVAS_WIDTH = 500		# Width of the tkinter canvas (pixels)
CANVAS_HEIGHT = 700		# Height of the tkinter canvas (pixels)

SQUARE_SIZE = 60		# Size of each square (pixels)
SQUARE_SEP = 5                  # Separation between squares (pixels)
TOP_MARGIN = 30    		# Top margin (pixels)
BOTTOM_MARGIN = 30    		# Bottom margin (pixels)
MESSAGE_SEP = 20                # Space between board and message center

SQUARE_FONT = ("Helvetica Neue", -44, "bold")
MESSAGE_FONT = ("Helvetica Neue", -20, "bold")
KEY_FONT = ("Helvetica Neue", -18)
ENTER_FONT = ("Helvetica Neue", -14)

KEY_WIDTH = 40
KEY_HEIGHT = 60
KEY_CORNER = 9
KEY_XSEP = 5
KEY_YSEP = 7

KEY_LABELS = [
    [ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P" ],
    [ "A", "S", "D", "F", "G", "H", "J", "K", "L" ],
    [ "ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE" ]
]

CLICK_MAX_DISTANCE = 2
CLICK_MAX_DELAY = 0.5

# Derived constants

SQUARE_DELTA = SQUARE_SIZE + SQUARE_SEP
BOARD_WIDTH = N_COLS * SQUARE_SIZE + (N_COLS - 1) * SQUARE_SEP
BOARD_HEIGHT = N_ROWS * SQUARE_SIZE + (N_ROWS - 1) * SQUARE_SEP
MESSAGE_X = CANVAS_WIDTH / 2
MESSAGE_Y = TOP_MARGIN + BOARD_HEIGHT + MESSAGE_SEP

class WordleGWindow:
    """This class creates the Wordle window."""

    def __init__(self):
        """Creates the Wordle window."""

        # Bind keys and clicks                                                          FIX LATER
        # self._root = tk.Tk()
        # self._root.bind("<Key>", self.key_action)
        # self._root.bind("<ButtonPress-1>", self.press_action)
        # self._root.bind("<ButtonRelease-1>", self.release_action)

        # Statistics variables to be used throughout the games
        self.games_played = 0
        self.games_won = 0
        self.current_streak = 0
        self.max_streak = 0

        self.num_guesses = 0

        self.guess_distribution = [0 for _ in range(N_ROWS)]

        # Random word variable
        self.current_word = ""
        self.random_word()

        def create_grid():
            return [
                [
                    WordleSquare(canvas, i, j) for j in range(N_COLS)
                ] for i in range(N_ROWS)
            ]

        def create_keyboard():
            keys = { }
            nk = len(KEY_LABELS[0])
            h = KEY_HEIGHT
            y0 = CANVAS_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
            for row in range(len(KEY_LABELS)):
                y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                x = (CANVAS_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                if row == 1:
                    x += (KEY_WIDTH + KEY_XSEP) / 2
                for col in range(len(KEY_LABELS[row])):
                    label = KEY_LABELS[row][col]
                    w = KEY_WIDTH
                    if len(label) > 1:
                        w += (KEY_WIDTH + KEY_XSEP) / 2
                    keys[label] = WordleKey(self._canvas, x, y, w, h, label)
                    x += w + KEY_XSEP
            return keys

        def create_message():
            return WordleMessage(self._canvas,
                                 CANVAS_WIDTH / 2,
                                 MESSAGE_Y)

        def key_action(tke):
            keysym = None
            if isinstance(tke, str):
                ch = tke.upper()
            else:
                ch = tke.char.upper()
                keysym = tke.keysym
            if keysym == "BackSpace" or ch == "\007" or ch == "\177" or ch == "\b" or ch == "DELETE":
                self.show_message("")
                if self._row < N_ROWS and self._col > 0:
                    self._col -= 1
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(" ")
            elif keysym == "Return" or ch == "\r" or ch == "\n" or ch == "ENTER":
                self.show_message("")
                s = ""
                for col in range(N_COLS):
                    s += self._grid[self._row][col].get_letter()
                for fn in self._enter_listeners:
                    fn(s)
            elif ch.isalpha():
                self.show_message("")
                if self._row < N_ROWS and self._col < N_COLS:
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(ch)
                    self._col += 1

        def press_action(tke):
            self._down_x = tke.x
            self._down_y = tke.y
            self._down_time = time.time()

        def release_action(tke):
            if abs(self._down_x - tke.x) <= CLICK_MAX_DISTANCE:
                if abs(self._down_y - tke.y) <= CLICK_MAX_DISTANCE:
                    t = time.time()
                    if t - self._down_time < CLICK_MAX_DELAY:
                        key = find_key(tke.x, tke.y)
                        if key:
                            key_action(key._label)

        def find_key(x, y):
            for key in self._keys.values():
                kx, ky, kw, kh = key._bounds
                if x >= kx and x <= kx + kw and y >= ky and y <= ky + kh:
                    return key
            return None

        def delete_window():
            """Closes the window and exits from the event loop."""
            self._root.destroy()

        def start_event_loop():
            """Starts the tkinter event loop when the program exits."""
            root.mainloop()

        root = tk.Tk()
        root.title("Wordle")
        root.protocol("WM_DELETE_WINDOW", delete_window)
        self._root = root
        canvas = tk.Canvas(root,
                                bg="White",
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                highlightthickness=0)
        canvas.pack()
        self._canvas = canvas
        self._grid = create_grid()
        self._message = create_message()
        self._keys = create_keyboard()
        self._enter_listeners = [ ]
        root.bind("<Key>", key_action)
        root.bind("<ButtonPress-1>", press_action)
        root.bind("<ButtonRelease-1>", release_action)
        self._row = 0
        self._col = 0
        atexit.register(start_event_loop)

    def get_square_letter(self, row, col):
        return self._grid[row][col].get_letter()

    def set_square_letter(self, row, col, ch):
        self._grid[row][col].set_letter(ch)

    def get_square_color(self, row, col):
        return self._grid[row][col].get_color()

    def set_square_color(self, row, col, color):
        self._grid[row][col].set_color(color)

    def get_key_color(self, ch):
        return self._keys[ch].get_color()

    def set_key_color(self, ch, color):
        self._keys[ch].set_color(color)

    def get_current_row(self):
        return self._row

    def set_current_row(self, row):
        self._row = row
        self._col = 0
        for col in range(N_COLS):
            self.set_square_letter(row, col, " ")
            self.set_square_color(row, col, UNKNOWN_COLOR)

    def add_enter_listener(self, fn):
        self._enter_listeners.append(fn)

    def show_message(self, msg, color="Black"):
        self._message.set_text(msg, color)

    def random_word(self):
        # Choose a random word and store it as a variable
        self.current_word = random.choice(FIVE_LETTER_WORDS).upper()

        # Filter out plural words
        while self.current_word.endswith('S') and self.current_word[-2] not in ['I', 'S', 'U']:
            self.current_word = random.choice(FIVE_LETTER_WORDS).upper()

        # Print the random word to the console for debugging                                       DELETE LATER
        print("Debug: The chosen word is", self.current_word)

    def next_row(self):
        """Advances to the next row and resets the squares for a new guess."""
        if self._row < N_ROWS - 1:  # Check to avoid exceeding the number of rows
            self._row += 1  # Move to the next row
            self._col = 0  # Reset column index to the start of the row

    def end_screen(self):
        """Displays the end screen with final message or options for the user."""
        
        # Create a new Toplevel window
        popup = tk.Toplevel(self._root)
        popup.title("Game Over")
        popup.geometry("450x350")  # Set the size of the pop-up (width x height)

        # Center the pop-up window over the main game window
        x = self._root.winfo_x()
        y = self._root.winfo_y()
        popup.geometry(f"+{x + 25}+{y + 175}")

        # Statistics Frame
        stats_frame = tk.Frame(popup, pady=5)
        stats_frame.pack(fill='x', padx=10)
        tk.Label(stats_frame, text="STATISTICS", font=("Helvetica", 14, "bold")).pack()
        
        # Actual Statistics
        win_percentage = round((self.games_won / self.games_played * 100)) if self.games_played > 0 else 0
        stats_text = f"{self.games_played} Played    {win_percentage} Win %    {self.current_streak} Current Streak    {self.max_streak} Max Streak"
        tk.Label(stats_frame, text=stats_text, font=("Helvetica", 10)).pack()

        # Guess Distribution Frame
        guess_dist_frame = tk.Frame(popup, pady=5)
        guess_dist_frame.pack(fill='x', padx=10)
        tk.Label(guess_dist_frame, text="GUESS DISTRIBUTION", font=("Helvetica", 14, "bold")).pack()
        
        # Actual Guess Distribution  
        if(self.num_guesses < 6):
            self.guess_distribution[self.num_guesses - 1] += 1  

        for i, count in enumerate(self.guess_distribution, start=1):
            row = tk.Frame(guess_dist_frame)
            row.pack(fill='x')
            tk.Label(row, text=f"{i}", width=2).pack(side='left')
            # Assuming max_guesses is the maximum number of guesses in a game for scaling the bar width
            max_guesses = max(self.guess_distribution) if self.guess_distribution else 1

            if max_guesses == 0:
                max_guesses = 1
                
            bar_width = (count / max_guesses) * 400
            tk.Canvas(row, height=20, width=bar_width, bg=KEY_COLOR).pack(side='left')

        # Buttons Frame
        buttons_frame = tk.Frame(popup, pady=10)
        buttons_frame.pack(fill='x', padx=10)
        share_button = tk.Button(buttons_frame, text="Share", bg=CORRECT_COLOR, fg="white", font=("Helvetica", 14, "bold"), command=self.share_results)
        share_button.pack(side='left', expand=True, fill='x', padx=5)
        new_game_button = tk.Button(buttons_frame, text="New Game", bg=CORRECT_COLOR, fg="white", font=("Helvetica", 14, "bold"), command=self.new_game)
        new_game_button.pack(side='left', expand=True, fill='x', padx=5)

        # Eventual "Copied to Clipboard" message
        self.share_message_label = tk.Label(popup, text="", fg="green")
        self.share_message_label.pack()

        # Make the pop-up window modal
        popup.transient(self._root)
        popup.grab_set()
        self._root.wait_window(popup)
    
    def share_results(self):

        """Copies the game results to the clipboard."""
        results_text = self.format_results_for_sharing()
        self.copy_to_clipboard(results_text)
        
        # Update the message label
        self.share_message_label.config(text="Results copied to clipboard!", fg="green")

        # Reset the message after some time
        self._root.after(3000, lambda: self.share_message_label.config(text=""))

    def format_results_for_sharing(self):

        """Formats the game results into a string that can be shared."""
        results_data = {
            'played': self.games_played,
            'win_percent': round((self.games_won / self.games_played * 100)) if self.games_played > 0 else 0,
            'current_streak': self.current_streak,
            'max_streak': self.max_streak
        }

        # Format the results into a string
        results_str = "My Wordle Stats:\n"
        results_str += f"Games Played: {results_data['played']}\n"
        results_str += f"Win %: {results_data['win_percent']}\n"
        results_str += f"Current Streak: {results_data['current_streak']}\n"
        results_str += f"Max Streak: {results_data['max_streak']}"
        return results_str

    def copy_to_clipboard(self, text):

        """Copies the given text to the system clipboard."""
        self._root.clipboard_clear()
        self._root.clipboard_append(text)

    def new_game(self):
        """Resets the game to start a new one."""
        # Reset the game board
        for row in range(N_ROWS):
            for col in range(N_COLS):
                self.set_square_letter(row, col, " ")
                self.set_square_color(row, col, UNKNOWN_COLOR)
        
        # Reset any necessary game state variables
        self._row = 0
        self._col = 0
        self.num_guesses = 0

        # Clear any displayed messages
        self.show_message("")

        # Generate a new target word for the next game (adjust based on your game's design)
        self.random_word()


class WordleSquare:

    def __init__(self, canvas, row, col):
        x0 = (CANVAS_WIDTH - BOARD_WIDTH) / 2 + col * SQUARE_DELTA
        y0 = TOP_MARGIN + row * SQUARE_DELTA
        x1 = x0 + SQUARE_SIZE
        y1 = y0 + SQUARE_SIZE
        self._canvas = canvas
        self._ch = " "
        self._color = UNKNOWN_COLOR
        self._frame = canvas.create_rectangle(x0, y0, x1, y1)
        self._text = canvas.create_text(x0 + SQUARE_SIZE / 2,
                                        y0 + SQUARE_SIZE / 2,
                                        text=self._ch,
                                        font=SQUARE_FONT)

    def get_letter(self):
        return self._ch

    def set_letter(self, ch):
        self._ch = ch
        self._canvas.itemconfigure(self._text, text=ch)

    def get_color(self):
        return self._color

    def set_color(self, color):
        color = color.upper()
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleKey:

    def __init__(self, canvas, x, y, width, height, label):
        self._canvas = canvas
        self._label = label
        self._bounds = [ x, y, width, height ]
        self._color = UNKNOWN_COLOR
        font = KEY_FONT
        if label == "ENTER":
            font = ENTER_FONT
        if label == "DELETE":
            label = "\u232B"
        points = [ x + KEY_CORNER, y,
                   x + KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width, y,
                   x + width, y + KEY_CORNER,
                   x + width, y + KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x, y + height,
                   x, y + height - KEY_CORNER,
                   x, y + height - KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y]
        self._frame = canvas.create_polygon(points,
                                            fill=KEY_COLOR,
                                            outline=KEY_COLOR,
                                            smooth=True)
        self._text = canvas.create_text(x + width / 2,
                                        y + height / 2,
                                        text=label,
                                        font=font)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleMessage:

    def __init__(self, canvas, x, y):
        self._canvas = canvas
        self._text = ""
        self._msg = canvas.create_text(x, y,
                                       text="",
                                       font=MESSAGE_FONT,
                                       anchor=tk.CENTER)

    def get_text(self):
        return self._text

    def set_text(self, text, color="Black"):
        self._text = text
        self._canvas.itemconfigure(self._msg, text=text, fill=color)
