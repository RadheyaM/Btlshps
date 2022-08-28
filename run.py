"""Module desc goes here"""
from random import randint
import os


def read_int(prompt, min_val: int, max_val: int) -> int:
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


def generate_random_coordinates(qty: int, size: int) -> []:
    """generate a list of random co-ordinates for populating grids and
    so the computer can make guesses"""
    coordinates = []
    loops = 0
    while loops < qty:
        row = randint(0, size - 1)
        col = randint(0, size - 1)
        loops += 1
        coordinates.append((row, col))
    return coordinates


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
    co_ords = generate_random_coordinates(5, 5)
    co_ords2 = generate_random_coordinates(5, 5)
    for tup in co_ords:
        print(tup)
        player_grid.ship_locations.append(tup)
    for tup in co_ords2:
        computer_grid.ship_locations.append(tup)

    print(player_grid.print_grid())
    print("_" * 30, "\n")
    print(computer_grid.print_grid())


the_game()
