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
    plr.grid_symbols()
    com.grid_symbols()
    print("-------COMPUTER'S BOARD-------")
    com.print_grid()
    print("_" * 30, "\n", "\n")
    print("----------YOUR BOARD----------", "\n")
    plr.print_grid()


class Battlegrid:
    """create a battleship board grid"""
    def __init__(
        self,
        grid_size: int,
        num_of_ships: int,
        guess_id: str
    ):
        self.size = grid_size
        self.board = [
            ["_" for rows in range(grid_size)] for cols in range(grid_size)
        ]
        self.ships = num_of_ships
        self.ship_locations = []
        # id of the opposing player
        self.guess_id = guess_id
        # guesses made by the other player/computer
        self.guesses = []
        # hits on this board made by opponent
        self.hits = []

    def print_grid(self):
        """print the grid"""
        for row in self.board:
            print(" ".join(row))

    def generate_ships(self):
        """generate a list of unique random co-ordinates"""
        loops = 0
        locs = self.ship_locations
        while loops < self.ships:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            # check for duplicates, don't add if so
            if (row, col) in locs:
                continue
            locs.append((row, col))
            loops += 1

    def grid_symbols(self):
        """Display appropriate symbols on the board"""
        for ship in self.ship_locations:
            # display the player's ships but not the computer's
            # if self.guess_id == "The Computer":
            self.board[ship[0]][ship[1]] = "S"
        for hit in self.hits:
            self.board[hit[0]][hit[1]] = "H"
        for guess in self.guesses:
            if guess not in self.hits:
                self.board[guess[0]][guess[1]] = "M"

    def player_guess(self):
        """Get a guess from the player avoid duplicates"""
        row = read_int("Guess a row: ", 1, self.size) - 1
        col = read_int("Guess a column: ", 1, self.size) - 1
        if (row, col) in self.guesses:
            print(
                f"You already guessed {(row + 1, col + 1)}, try again"
            )
        self.guesses.append((row, col))

    def computer_guess(self):
        """Generates and saves a unique computer guess to the player's
        Battlegrid instance guesses array"""
        loops = 0
        while loops == 0:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            if (row, col) in self.guesses:
                continue
            self.guesses.append((row, col))
            loops += 1

    def outcome_message(self):
        """Generates appropriate feedback based on outcome value"""
        if self.guesses[-1] in self.ship_locations:
            return print(f"{self.guess_id} hit a ship!")
        return print(f"{self.guess_id} missed...")


def custom_settings():
    """Allows the player to set the size of the board,
    the number of guesses, and win conditions"""
    grid_size = read_int("Enter grid size between 5 and 20: \n", 5, 20)
    num_ships = read_int("Enter number of ships between 1 and 10: \n", 1, 10)
    player_grid = Battlegrid(grid_size, num_ships, "The Computer")
    computer_grid = Battlegrid(grid_size, num_ships, "You")
    os.system("clear")
    print("-----CUSTOM SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def default_settings():
    """Sets the default game settings"""
    player_grid = Battlegrid(5, 4, "The Computer")
    computer_grid = Battlegrid(5, 4, "You")
    os.system("clear")
    print("-----DEFAULT SETTINGS CHOSEN-----")
    return player_grid, computer_grid


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
