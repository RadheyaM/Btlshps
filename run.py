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
            print("Ooops, you didn't enter a number!")
            print(f"Please enter a number between {min_val} & {max_val}")


def print_screen(plr, com):
    """Prints the game to terminal"""
    plr.grid_symbols()
    com.grid_symbols()
    print("\n")
    print("----THE COMPUTER'S BOARD----", "\n")
    com.print_grid()
    print("\n")
    print("---------YOUR BOARD---------", "\n")
    plr.print_grid()
    print("\n")


class Battlegrid:
    """create a battleship board grid"""
    def __init__(
        self,
        grid_size: int,
        num_of_ships: int,
        guess_id: str,
        hits_to_win: int,
        guesses_allowed: int
    ):
        self.size = grid_size
        self.board = [
            ["___" for rows in range(grid_size)] for cols in range(grid_size)
        ]
        self.ships = num_of_ships
        self.hits_to_win = hits_to_win
        self.guesses_allowed = guesses_allowed
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
            self.board[ship[0]][ship[1]] = "_S_"
        for hit in self.hits:
            self.board[hit[0]][hit[1]] = "_H_"
        for guess in self.guesses:
            if guess not in self.hits:
                self.board[guess[0]][guess[1]] = "_M_"

    def player_guess(self):
        """Get a guess from the player avoiding duplicates"""
        row = read_int("Guess a row: ", 1, self.size) - 1
        col = read_int("Guess a column: ", 1, self.size) - 1
        if (row, col) in self.guesses:
            print(
                f"You already guessed {(row + 1, col + 1)}, try again"
            )
        if (row, col) in self.ship_locations:
            self.hits.append((row, col))
            self.guesses.append((row, col))
            return
        self.guesses.append((row, col))

    def computer_guess(self):
        """Generates and saves a unique computer guess to the player's
        Battlegrid instance guesses array"""
        loop = True
        while loop:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            if (row, col) in self.guesses:
                continue
            if (row, col) in self.ship_locations:
                self.hits.append((row, col))
                self.guesses.append((row, col))
                return
            self.guesses.append((row, col))
            loop = False

    def outcome_message(self):
        """Generates appropriate feedback based on outcome value"""
        if self.guesses[-1] in self.ship_locations:
            return print(f"{self.guess_id} hit a ship!")
        return print(f"{self.guess_id} missed...")


def custom_settings():
    """Allows the player to set the size of the board,
    the number of guesses, and win conditions"""
    os.system("clear")
    num_ships = read_int("Enter number of ships between 1 and 10: \n", 1, 10)
    hits_to_win = read_int(
        "Enter number of ships hit to win: \n", 1, num_ships
        )
    guesses_allowed = read_int(
        "Enter number of guesses allowed between 1 and 100: \n", 1, 100
        )
    player_grid = Battlegrid(
        5, num_ships, "The Computer", hits_to_win, guesses_allowed
        )
    computer_grid = Battlegrid(
        5, num_ships, "You", hits_to_win, guesses_allowed
        )
    os.system("clear")
    print("-----CUSTOM SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def default_settings():
    """Sets the default game settings"""
    player_grid = Battlegrid(5, 4, "The Computer", 4, 100)
    computer_grid = Battlegrid(5, 4, "You", 4, 100)
    os.system("clear")
    print("-----DEFAULT SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def welcome() -> int:
    """Greeting message and choose game mode"""
    print("Welcome to Btlshps!")
    print("Sink your opponent's ships before they sink yours!")
    print("To quit just refresh the page at any time.\n")
    while True:
        print("Enter 1 for default game mode")
        print("Enter 2 for custom game mode ")
        print("Enter 3 for explanation of game modes\n")
        choice = read_int(
            "What would you like to do?\n",
            min_val=1,
            max_val=3
            )
        if choice == 1:
            return 1
        if choice == 2:
            return 2
        print("DEFAULT SETTINGS:")
        print("Grid size of 5 by 5 with 4 ships each")
        print("100 guesses each")
        print("First to hit all the opponents ships wins")
        print("CUSTOM MODE:")
        print("Choose your own settings")


def game_loop(plr, com):
    """Run the game loop"""
    new_turn = True
    guesses_made = 0
    print_screen(plr, com)

    while new_turn:

        com.player_guess()
        plr.computer_guess()
        guesses_made += 1

        # computer wins by hit number
        if len(plr.hits) == plr.hits_to_win:
            new_turn = False
            os.system("clear")
            return print("hit no.! YOU LOSE!!!")

        # player wins by hit number
        if len(com.hits) == plr.hits_to_win:
            new_turn = False
            os.system("clear")
            return print("hit no! YOU WIN!!!")

        os.system("clear")
        print_screen(plr, com)

        print(
            f"You guessed {(com.guesses[-1][0]+1, com.guesses[-1][1]+1)}"
            )
        com.outcome_message()
        print(
            f"Computer guess: {(plr.guesses[-1][0]+1, plr.guesses[-1][1]+1)}"
        )
        plr.outcome_message()


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
