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


def print_screen(plr, com, game_status):
    """Prints the game to terminal"""
    game = game_status
    # show or don't show computer's ships
    if game == "over":
        plr.grid_symbols_game_over()
        com.grid_symbols_game_over()
    elif game == "in-play":
        plr.grid_symbols()
        com.grid_symbols()
    print("\n")
    print("----THE COMPUTER'S BORED----", "\n")
    com.print_grid()
    print("\n")
    print("------AND YOUR BORED-------", "\n")
    plr.print_grid()
    print("\n")
    if game == "over":
        print("Click 'Run Program' button for new game.")


class Battlegrid:
    """create a battleship board grid"""
    def __init__(
        self,
        guess_id: str,
        grid_size=5,
        num_of_ships=4,
        hits_to_win=5,
        guesses_allowed=100
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
        """Display appropriate symbols on the board in-play"""
        for ship in self.ship_locations:
            # display the player's ships but not the computer's
            if self.guess_id == "The Computer":
                self.board[ship[0]][ship[1]] = "SHP"
        for hit in self.hits:
            self.board[hit[0]][hit[1]] = "###"
        for guess in self.guesses:
            if guess not in self.hits:
                self.board[guess[0]][guess[1]] = "_X_"

    def grid_symbols_game_over(self):
        """Display appropriate symbols on the board on game over"""
        for ship in self.ship_locations:
            self.board[ship[0]][ship[1]] = "SHP"
        for hit in self.hits:
            self.board[hit[0]][hit[1]] = "###"
        for guess in self.guesses:
            if guess not in self.hits:
                self.board[guess[0]][guess[1]] = "_X_"

    def player_guess(self) -> int:
        """Get a guess from the player avoiding duplicates"""
        while True:
            row = read_int("Guess a row: ", 1, self.size) - 1
            col = read_int("Guess a column: ", 1, self.size) - 1
            if (row, col) in self.guesses:
                print(
                    f"You already guessed {(row+1, col+1)}. Try again..."
                )
            elif (row, col) in self.ship_locations:
                self.hits.append((row, col))
                self.guesses.append((row, col))
                return
            else:
                self.guesses.append((row, col))
                return

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
         "The Computer", 5, num_ships, hits_to_win, guesses_allowed
        )
    computer_grid = Battlegrid(
         "You", 5, num_ships, hits_to_win, guesses_allowed
        )
    os.system("clear")
    print("-----CUSTOM SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def welcome() -> int:
    """Greeting message and choose game mode"""
    print("Welcome to Btlshps!")
    print("Sink your opponent's ships before they sink yours!")
    print("To quit just refresh the page at any time.\n")
    while True:
        print("--Enter '1' for default game mode.")
        print("--Enter '2' for custom game mode. ")
        print("--Enter '3' for game mode details.\n")
        choice = read_int(
            "Please enter option number: \n",
            min_val=1,
            max_val=3
            )
        if choice == 1:
            return 1
        if choice == 2:
            return 2
        os.system("clear")
        print("DEFAULT MODE SETTINGS:")
        print("Grid size of 5 by 5 with 4 ships each")
        print("100 guesses each")
        print("First to hit all the opponents ships wins\n")
        print("CUSTOM MODE SETTINGS:")
        print("Choose your own settings\n")
        print("GRID SYMBOLS:")
        print("'SHP' --> A Ship.")
        print("'###' --> A Hit!")
        print("'_X_' --> A Miss!\n")


def game_loop(plr, com):
    """Run the game loop"""
    new_turn = True
    guesses_made = 0
    print_screen(plr, com, "in-play")

    while new_turn:

        com.player_guess()
        plr.computer_guess()
        guesses_made += 1

        # computer wins by hit number
        if len(plr.hits) == plr.hits_to_win:
            new_turn = False
            os.system("clear")
            print("YOU LOSE!!! THE COMPUTER BEAT YOU TO IT!!!")
            print_screen(plr, com, "over")
            return

        # player wins by hit number
        if len(com.hits) == plr.hits_to_win:
            new_turn = False
            os.system("clear")
            print("YOU WIN!!!YOU WIN!!!YOU WIN!!!")
            print_screen(plr, com, "over")
            return

        # most ships hit with limited guesses endings
        if guesses_made == plr.guesses_allowed:
            if len(plr.hits) > len(com.hits):
                os.system("clear")
                print("The computer hit more ships. YOU LOSE!")
            if len(plr.hits) < len(com.hits):
                os.system("clear")
                print("YOU WIN!!! You hit the most ships!")
            if len(plr.hits) == len(com.hits):
                os.system("clear")
                print("It's a draw...yawn...")
            return print_screen(plr, com, "over")

        os.system("clear")
        print_screen(plr, com, "in-play")

        # turn summary prints below the boards
        print(
            f"Your guess: {(com.guesses[-1][0]+1, com.guesses[-1][1]+1)}"
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
        plr, com = Battlegrid("The Computer"), Battlegrid("You")
    elif choice == 2:
        plr, com = custom_settings()

    plr.generate_ships()
    com.generate_ships()

    game_loop(plr, com)


main()
