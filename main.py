# TIC TAC TOE game built using tkinter
import tkinter as tk
from tkinter import font
from typing import NamedTuple

# creating a class that represents a player
class Player(NamedTuple):
    # the label attribute stores what sign the player has: X or 0
    label: str

    # the label color is used to differentiate each player in particular
    color: str


#creating a class that represents the move a player makes
class Move(NamedTuple):
    row: int
    column: int

    # label attribute stores the sign a player has used to make a move
    label : str = ""



# creating a class to represent the game logic
class GameLogic:
    # creating the list of players
    _PLAYERS = [
        Player("X", "red"),
        Player("0", "green")
    ]
    _boolean_cycle = 0

    def __init__(self):
        # defining the current player
        # player with 0 always starts
        self.current_player = self._PLAYERS[0]

        # defining the typical tic-tac-toe board size: 3x3
        self.board_size = 3

        # list of all possible moves in a given game, regardless of the player color
        self._current_moves = [
            [Move(row, column) for row in range(self.board_size)]
            for column in range(self.board_size)
        ]

        # list of winning combinations of moves
        self._winning_combos = []

        # populating the list with all the possible winning situations
        # all three rows
        self._winning_combos.extend([(row, column) for column in range(self.board_size)]
                                    for row in range(self.board_size))

        # all three columns
        self._winning_combos.extend(list(move) for move in zip(*self._winning_combos))

        # both diagonals
        self._winning_combos.extend([[(row, row) for row in range(self.board_size)]])
        self._winning_combos.extend([[(row, self.board_size - row - 1) for row in range(self.board_size)]])


        # boolean to establish if the game has a winner or it is a draw
        self._has_winner = False
        self._winning_buttons = []

    # public functions

    # adding a function that verifies whether or not the current move is valid
    # it returns true if the move is valid and false otherwise

    def valid_move(self, move):
        # one move is valid if it satisfies 2 conditions:
            # 1. the current game doesn't have a winner yet
            # 2. the selected move hasn't already been played
        row, column = move.row, move.column

        # the current game doesn't have a winner,
        # it means that the attribut _has_winner is false
        no_winner = not self._has_winner

        # if a move hsn't been played yet,
        # it means that the coresponding label in current_moves array hasn't been filled
        move_was_not_played = self._current_moves[row][column].label == ""

        return no_winner and move_was_not_played


    # adding a function that processes the current move and checks if the game has a winner
    def playing_the_game(self, move):
        row, column = move.row, move.column
        # registering the move into _current_moves array
        self._current_moves[row][column] = move

        #checking if it is a win
        for combo in self._winning_combos:
            results = set(
                self._current_moves[i][j].label
                for i, j in combo
            )

            is_win = (len(results) == 1) and ("" not in results)

            if is_win:
                self._has_winner = True
                self._winning_buttons = combo

                break

    def has_winner(self):
        # returns true if the game has a winner and false otherwise
        return self._has_winner

    def is_tied(self):
        # returns true if the game is tied, false otherwise
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        # returns true if the game doeasn't have a winner and all the labels have been filled
        # meaning all the moves have been played
        return not self._has_winner and all(played_moves)

    def toggle_player(self):
        # returns the next player
        if self._boolean_cycle == 1:
            self.current_player = self._PLAYERS[0]
            self._boolean_cycle = 0

        else:
            self.current_player = self._PLAYERS[1]
            self._boolean_cycle = 1


# creating a class that represent the game board
class TicTacToe_board(tk.Tk):

    # initializing private board attribute: cells
    __cells = {}
    # constructors
    def __init__(self, game):
        # initialize the parent class tk
        super().__init__()

        # setting the title of the window as Tic Tac Toe Game
        self.title("Tic-Tac-Toe")

        self._game = game
        self._create_board_display()

    # creating the board display function
    def _create_board_display(self):
        # changing the geometry of the window to match the background photo dimensions
        # creating the background photo
        self._background = tk.PhotoImage(file="flower2.png")

        w = self._background.width()
        h = self._background.height()

        self.geometry(f"{w}x{h}")
        self.maxsize(w, h)
        self.minsize(w, h)

        # creating a canvas to use as a background
        display_frame = tk.Canvas(
            master=self,
            bg="#f3dba5",
        )
        display_frame.pack(
            side=tk.TOP,
            fill="both",
            expand="yes"
        )
        display_frame.create_image(0, 0, anchor="nw", image=self._background)

        # creating a label which will serve as a judge for the game
        self._judge = tk.Label(
            master=display_frame,
            text = "Ready?",
            font = font.Font(family = "Papyrus", size = 25, weight = "bold"),
            bg="#f3dba5",
            fg="#2b4700"
        )
        self._judge.pack(pady = (90, 0), padx = (0, 60))

        # creating the board grid
        grid_frame = tk.Frame(master = display_frame, bg = "#fff4cc")
        grid_frame.pack()

        for row in range(self._game.board_size):
            for column in range(self._game.board_size):
                button = tk.Button(
                    master = grid_frame,
                    text ="",
                    font = ("Papyrus", 30),
                    fg = "#2b4700",
                    bg = "#fff4cc",
                    highlightbackground = "white",

                    width = 3,
                    height = 1,

                    relief = tk.GROOVE
                )
                self.__cells[button] = (row, column)

                # binding the button to click event
                button.bind("<ButtonPress-1>", self.play)

                button.grid(
                    row = row,
                    column = column,
                    sticky="nsew",

                    padx = 2,
                    pady = 2
                )

        # creating a copy for the cells dictionary in order to still have the data later on
        # when a reset board action is needed
        self.__reset_cells = self.__cells

        # creating a menu for the board having exit and reset game options
        menu_game = tk.Menu(master=display_frame)
        self.config(menu=menu_game)
        menu_game.add_command(label="Exit", command=quit)

        menu_game.add_command(
            label="Wanna play again?",
            command=self.reset_board
        )

    # function that modifies the aspect of buttons when clicked
    def _update_button(self, button):
        button.config(text = self._game.current_player.label, fg = self._game.current_player.color)

    # function that modifies the aspect of the label on move
    def _update_display(self, message, color):
        self._judge.config(text = message, fg = color)

    # function that highlights the buttons pressed from the winning combo in case of a win
    def _party(self):
        for combo in self._game._winning_buttons:
            for button in self.__cells.keys():
                 if self.__cells[button] == combo:
                     button.config(bg = "#FFF5E4")

    # adding the engine of the game
    def play(self, event):
        # function that handles a player move
        clicked_button = event.widget
        row, column = self.__cells[clicked_button]

        move = Move(row, column, self._game.current_player.label)
        # checking if the move is valid
        if self._game.valid_move(move):

            # button display modifies accordingly
            self._update_button(clicked_button)

            self._game.playing_the_game(move)
            # checking for a tie
            if self._game.is_tied():
                self._update_display(message = "Tied Game!", color = "black")

            # checking for a win
            elif self._game.has_winner():
                self._update_display(message = f"Player {self._game.current_player.label} won!", color = self._game.current_player.color)
                self._party()
            # continue the game with the next player
            else:
                self._game.toggle_player()
                self._update_display(message = f"{self._game.current_player.label}'s turn", color = self._game.current_player.color)


    # creating a reset board function
    def reset_board(self):
        # reset the game first
        for row in range(self._game.board_size):
            for column in range(self._game.board_size):
                self._game._current_moves[row][column] = Move(row, column, "")
        self._game._has_winner = False

        # reset the board
        (self._judge).config(text = "Ready?", fg="#2b4700")
        for button in self.__cells.keys():
            button.config(text = "", bg = "#fff4cc")
        self.__cells = self.__reset_cells

def main():
    game = GameLogic()
    board = TicTacToe_board(game)
    board.mainloop()


if __name__ == "__main__":
    main()
