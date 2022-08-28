"""Module desc goes here"""
from random import randint
import os


def read_int(prompt, min_val, max_val):
    """prompts player for input and returns a response integer
    between min and max values.  All player input will go through
    this function."""
    while True:
        player_input = input(prompt)
        try:
            entry = int(player_input)
            if entry > max_val:
                print("The number you entered is too large. Please try again!")
            elif entry < min_val:
                print("The number you entered is too small.  Please try again")
            else:
                return entry
        except ValueError:
            print("Ooops, you didn't enter a number dummy!")
            print(f"Please enter a number between {min_val} & {max_val}")


class Battlegrid:
    """create a battleship board grid"""
    def __init__(
        self,
        size: int,
        ships: int,
        player_name: str,
        num_guess: int
    ):
        self.size = size
        self.board = [["O" for x in range(size)] for y in range(size)]
        self.ships = ships
        self.player_name = player_name
        self.type = type
        self.guesses = []
        self.ship_locations = []
        self.num_guess = num_guess

    def print_grid(self):
        """print the grid"""
        for row in self.board:
            print(" ".join(row))

    def generate_ships(self):
        """generate a list of random co-ordinates stored in the ship_locations
        class array"""
        loops = 0
        while loops < self.ships:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            loops += 1
            self.ship_locations.append((row, col))

    def display_ships(self):
        """Display an S for every ship co-ordinate in the ship_locations
        array on the printed board"""
        for ship in self.ship_locations:
            self.board[ship[0]][ship[1]] = "S"

    def display_guess(self):
        """Display appropriate symbol on the board depending on if
        guess is a hit or miss"""
        for guess in self.guesses:
            for ship in self.ship_locations:
                if ship == guess:
                    self.board[ship[0]][ship[1]] = "H"
                    return
                self.board[guess[0]][guess[1]] = "M"


def custom_settings(player_name: str):
    """Allows the player to set the size of the board,
    the number of guesses, and win conditions"""
    grid_size = read_int("Enter grid size between 5 and 20: \n", 5, 20)
    num_ships = read_int("Enter number of ships between 1 and 10: \n", 1, 10)
    num_guesses = read_int(
        "Enter number of guesses between 5 and 100: \n",
        5,
        100
    )
    player_grid = Battlegrid(grid_size, num_ships, player_name, num_guesses)
    computer_grid = Battlegrid(grid_size, num_ships, player_name, num_guesses)
    print("-----CUSTOM SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def default_settings():
    """Sets the default game settings"""
    player_grid = Battlegrid(5, 4, "player", 100)
    computer_grid = Battlegrid(5, 4, "computer", 100)
    print("-----DEFAULT SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def make_guess(size: int, grid):
    """Prompts player to enter guesses and saves to instance guesses list"""
    row_guess = read_int("Guess a row: ", 0, size - 1)
    col_guess = read_int("Guess a column: ", 0, size - 1)
    grid.guesses.append((row_guess, col_guess))


def welcome() -> int:
    """Greeting message and choose game mode"""
    print("Welcome to Btlshps! Time to play the game!")
    print("Sink all your opponent's ships before they sink yours!")
    while True:
        print("Enter 1 for default game mode")
        print("Enter 2 for custom game mode ")
        print("Enter 3 for explanation of game modes\n")
        choice = read_int(
            "Would you like to play default or custom mode?\n",
            min_val=1,
            max_val=3
            )
        if choice == 1:
            return 1
        if choice == 2:
            return 2
        print("DEFAULT SETTINGS:")
        print("Grid size: 5 by 5 with 4 ships each")
        print("Unlimited Guesses")
        print("Winner is first to hit all opponents ships!")
        print("CUSTOM MODE: choose your own settings")


def the_game():
    """Run the game"""
    choice = welcome()
    if choice == 1:
        player_grid, computer_grid = default_settings()
    elif choice == 2:
        player_grid, computer_grid = custom_settings("mark")
    os.system("clear")

    player_grid.generate_ships()
    player_grid.display_ships()
    make_guess(5, player_grid)

    print(computer_grid.print_grid())
    print("_" * 30, "\n")
    print(player_grid.print_grid())


the_game()
