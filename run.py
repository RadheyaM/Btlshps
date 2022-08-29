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


def print_screen(plr, com):
    """Prints the game to terminal"""
    print("-------COMPUTER'S BOARD-------")
    com.display_ships()
    com.print_grid()
    print("_" * 30, "\n", "\n")
    print("----------YOUR BOARD----------")
    plr.display_ships()
    plr.print_grid()


class Battlegrid:
    """create a battleship board grid"""
    def __init__(
        self,
        grid_size: int,
        num_of_ships: int,
        guess_id: str,
        guesses_allowed: int,
    ):
        self.size = grid_size
        self.board = [
            ["_" for rows in range(grid_size)] for cols in range(grid_size)
        ]
        self.ships = num_of_ships
        self.guess_id = guess_id
        self.guesses = []
        self.ship_locations = []
        self.guesses_allowed = guesses_allowed
        self.guesses_made = 0

    def print_grid(self):
        """print the grid"""
        for row in self.board:
            print(" ".join(row))

    def generate_ships(self):
        """generate a list of random co-ordinates stored to
        ship_locations and used to generate ships on the board"""
        loops = 0
        while loops < self.ships:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            loops += 1
            self.ship_locations.append((row, col))

    def generate_guess(self):
        """Generates and saves computer guess co-ordinates to the Battlegrid
        instance guesses array"""
        row = randint(0, self.size - 1)
        col = randint(0, self.size - 1)
        self.guesses.append((row, col))
        self.guesses_made += 1

    def display_ships(self):
        """Display an S for every ship co-ordinate in the ship_locations
        array on the printed board"""
        for ship in self.ship_locations:
            self.board[ship[0]][ship[1]] = "S"


def custom_settings():
    """Allows the player to set the size of the board,
    the number of guesses, and win conditions"""
    grid_size = read_int("Enter grid size between 5 and 20: \n", 5, 20)
    num_ships = read_int("Enter number of ships between 1 and 10: \n", 1, 10)
    num_guess = read_int(
        "Enter number of guesses between 5 and 100: \n",
        5,
        100
    )
    player_grid = Battlegrid(grid_size, num_ships, "The Computer", num_guess)
    computer_grid = Battlegrid(grid_size, num_ships, "You", num_guess)
    os.system("clear")
    print("-----CUSTOM SETTINGS CHOSEN-----")
    print_screen(player_grid, computer_grid)
    return player_grid, computer_grid


def default_settings():
    """Sets the default game settings"""
    player_grid = Battlegrid(5, 4, "The Computer", 100)
    computer_grid = Battlegrid(5, 4, "You", 100)
    os.system("clear")
    print("-----DEFAULT SETTINGS CHOSEN-----")
    print_screen(player_grid, computer_grid)
    return player_grid, computer_grid


def display_guess(guessing, target):
    """Display appropriate symbol on the board depending on if
    guess is a hit or miss."""
    for guess in guessing.guesses:
        for ship in target.ship_locations:
            if ship == guess:
                target.board[guess[0]][guess[1]] = "H"
            target.board[guess[0]][guess[1]] = "M"


def outcome_message(guessing, target):
    """Generates turn feedback message"""
    if guessing.guesses[-1] == target.ship_locations[-1]:
        return print(f"{guessing.guess_id} hit a ship!")
    return print(f"{guessing.guess_id} missed!")


def make_guess_player(player_grid):
    """Prompts player to enter guesses and saves to instance guesses list"""
    row_guess = read_int("Guess a row: ", 0, player_grid.size - 1)
    col_guess = read_int("Guess a column: ", 0, player_grid.size - 1)
    player_grid.guesses.append((row_guess, col_guess))


def welcome() -> int:
    """Greeting message and choose game mode"""
    print("Welcome to Btlshps! Time to play the game!")
    print("Sink all your opponent's ships before they sink yours!")
    print("To quit just refresh page at any time.")
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


def game_loop(plr, com):
    """Run the game loop"""

    os.system("clear")
    print_screen(plr, com)
    print(plr.ship_locations)
    print(com.ship_locations)


def main():
    """start the game and apply settings"""
    choice = welcome()
    if choice == 1:
        plr, com = default_settings()
    elif choice == 2:
        plr, com = custom_settings()

    plr.generate_ships()
    com.generate_ships()

    game_loop(plr, com)


main()
