"""Code to run the game in the terminal"""
from random import randint


def read_input(prompt, min_val: int, max_val: int):
    """prompts the player for input and returns a response integer
    between min and max values.  All player input will go through
    this function."""
    while True:
        player_input = input(prompt).strip()
        # option to refresh the game within the terminal
        if player_input.lower() == "n":
            return main()
        if player_input.lower() == "h":
            help_me()
            continue
        try:
            entry = int(player_input)
            if entry > max_val:
                print("**************************************************")
                print("--Oops...The number you entered is too large!...Oops")
                print(
                    f"--Please enter a number between {min_val} & {max_val}."
                    )
                print("**************************************************\n")
            elif entry < min_val:
                print("**************************************************")
                print("--Ooops...The number you entered is too small!...Ooops")
                print(
                    f"--Please enter a number between {min_val} & {max_val}."
                    )
                print("**************************************************\n")
            else:
                return entry
        except ValueError:
            print("**************************************************\n")
            print("--Ooops... you didn't enter a number!...Ooops")
            print(f"--Please enter a number between {min_val} & {max_val}.")
            print("**************************************************\n")


def print_screen(plr, com):
    """Print both grids with symbols"""
    com.grid_symbols()
    plr.grid_symbols()
    com.print_grid()
    plr.print_grid()


class Battlegrid:
    """A class defining the battleship board grid for the player
    and computer"""
    def __init__(
        self,
        opponent_name: str,
        grid_size=5,
        num_of_ships=4,
        hits_to_win=4,
        guesses_allowed=100, 
        game_status="in-play"
    ):
        self.size = grid_size
        self.board = [
            ["___" for rows in range(grid_size)] for cols in range(grid_size)
        ]
        self.ships = num_of_ships
        self.hits_to_win = hits_to_win
        self.guesses_allowed = guesses_allowed
        self.game_status = game_status
        self.ship_locations = []
        # id of the opposing player
        self.opponent = opponent_name
        # guesses made by the other player/computer
        self.guesses = []
        # hits on this board made by opponent
        self.hits = []

    def print_grid(self):
        """print grid to the terminal"""
        if self.opponent == "You":
            # board is spelled as bored, which is deliberate.
            print(">>>>>>>>>>THE COMPUTER's BOARD<<<<<<<<<<<\n")
        else:
            print(">>>>>>>>>>>>>AND YOU'RE BORED<<<<<<<<<<<<\n")
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def generate_ships(self):
        """generate a list of unique random co-ordinates used to place ships
        on the grid"""
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
        """Display appropriate symbols on the board while the
        game is in progress"""
        for ship in self.ship_locations:
            # display the player's ships but not the computer's
            if self.opponent == "The Computer":
                self.board[ship[0]][ship[1]] = "SHP"
        for hit in self.hits:
            self.board[hit[0]][hit[1]] = "###"
        for guess in self.guesses:
            if guess not in self.hits:
                self.board[guess[0]][guess[1]] = "_X_"

    def grid_symbols_game_over(self):
        """Display appropriate symbols on the board when the game ends"""
        for ship in self.ship_locations:
            self.board[ship[0]][ship[1]] = "SHP"
        for hit in self.hits:
            self.board[hit[0]][hit[1]] = "###"
        for guess in self.guesses:
            if guess not in self.hits:
                self.board[guess[0]][guess[1]] = "_X_"

    def player_guess(self) -> int:
        """Get a guess from the player, not allowing duplicate entries"""
        while True:
            row = read_input(">>Guess a row: \n", 1, self.size) - 1
            col = read_input(">>Guess a column: \n", 1, self.size) - 1
            if (row, col) in self.guesses:
                print(
                    f"--Ooops...You already guessed {(row+1, col+1)}...Ooops"
                )
            elif (row, col) in self.ship_locations:
                self.hits.append((row, col))
                self.guesses.append((row, col))
                return
            else:
                self.guesses.append((row, col))
                return

    def computer_guess(self):
        """Generates a unique random computer guess"""
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
        """Generates the appropriate feedback based outcome of a guess"""
        if self.guesses[-1] in self.ship_locations:
            return print(f"--AND ... {self.opponent} hit a ship!")
        return print(f"--AND ... {self.opponent} missed...")


def custom_settings():
    """Allows the player to set the size of the board,
    the number of guesses, and first to hit certain number
    of ships wins.

    Returns:
        The player and computer Battlegrid instances with appropriate
        settings.
    """
    num_ships = read_input(
        ">>Enter number of ships between 1 and 10: \n", 1, 10
        )
    hits_to_win = read_input(
        f">>Enter number of the {num_ships} ships hit to win: \n", 1, num_ships
        )
    guesses_allowed = read_input(
        ">>Enter number of guesses allowed between 1 and 100: \n", 1, 100
        )
    player_grid = Battlegrid(
         "The Computer", 5, num_ships, hits_to_win, guesses_allowed
        )
    computer_grid = Battlegrid(
         "You", 5, num_ships, hits_to_win, guesses_allowed
        )
    print("-----CUSTOM SETTINGS CHOSEN-----")
    return player_grid, computer_grid


def help_me():
    """Prints helpful information for the player. Can
    be accessed by pressing h at any time or 3 in the
    start-up menu."""
    print("**************************************************")
    print("DEFAULT MODE SETTINGS:")
    print("--Grid size of 5 by 5 with 4 ships.")
    print("--100 guesses each.")
    print("--First to hit all the opponents ships wins.")
    print("--Grid starts top left at co-ordinates: (1, 1)\n")
    print("CUSTOM MODE SETTINGS:")
    print("--Choose your own settings.\n")
    print("GRID SYMBOLS:")
    print("'SHP' --> A Ship.")
    print("'###' --> A Hit!")
    print("'_X_' --> A Miss!\n")
    print("**************************************************\n")


def game_start_options():
    """Greets the player at the start of the game
    and prompts them to make a game mode choice or
    see game mode details.

    Returns:
        An int depending on what choice the player made.

    """
    print("Welcome-to-boredome -- Welcome-to-boredome -- Welcome ...\n")
    print("--Welcome to the kingdom of Boredome, where we play Btlshps!")
    print("--Sink your opponent's ships before they sink yours!")
    print("--To RESTART the game press 'n' at any time.")
    print("--For HELP press 'h' at any time.\n")
    while True:
        print("****************************************")
        print(">>>Option '1' for default game mode.")
        print(">>>Option '2' for custom game mode. ")
        print(">>>Option '3' for game mode details.")
        print("****************************************\n")
        choice = read_input(
            ">>Please enter option number: \n",
            min_val=1,
            max_val=3
            )
        if choice == 1:
            return 1
        if choice == 2:
            return 2
        if choice == 3:
            help_me()


def game_loop(plr, com):
    """Run the game loop and print the boards.
    Check if win conditions have been met after each round of guessing.
    Display the turn log and guess outcomes.

    Args:
        plr: the player instance of the Battlegrid class.
        com: the computer instance of the Battlegrid class.

    Returns:
        Runs in a loop until a win condition is met then returns
        the appropriate end of game screen.
    """
    new_turn = True
    guesses_made = 0

    while new_turn:
        print_screen(plr, com)

        com.player_guess()
        plr.computer_guess()
        guesses_made += 1

        # computer wins by hit number
        if len(plr.hits) == plr.hits_to_win:
            new_turn = False
            com.grid_symbols_game_over()
            print("***LOSER***LOSER***LOSER***LOSER***LOSER\n")
            print_screen(plr, com)

        # player wins by hit number
        if len(com.hits) == plr.hits_to_win:
            new_turn = False
            com.grid_symbols_game_over()
            print("***WIN***WIN***WIN***WIN***WIN***WIN\n")
            print_screen(plr, com)

        # most ships hit with limited guesses endings
        if guesses_made == plr.guesses_allowed:
            new_turn = False
            com.grid_symbols_game_over()
            if len(plr.hits) > len(com.hits):
                print("***LOSER***LOSER***LOSER***LOSER***LOSER\n")
                print("The computer hit more ships. YOU LOSE!\n")
                print_screen(plr, com)
            if len(plr.hits) < len(com.hits):
                print("***WIN***WIN***WIN***WIN***WIN***WIN\n")
                print("YOU WIN!!! You hit the most ships!\n")
                print_screen(plr, com)
            if len(plr.hits) == len(com.hits):
                print("IN BOREDOME A YAWN IS THE HIGHEST ACHIEVABLE HONOUR")
                print("ON BEHALF OF ALL BOORES PLEASE ACCEPT A HEARTFELT YAWN")
                print(
                    "***CONGRATS!***YAWN***YOU DREW***YAWN***CONGRATS!***\n"
                    )
                print_screen(plr, com)

        # turn summary prints below the boards
        print(
            f">>Your guess: {(com.guesses[-1][0]+1, com.guesses[-1][1]+1)}"
            )
        com.outcome_message()
        print(
            f">>Computer guess: {(plr.guesses[-1][0]+1, plr.guesses[-1][1]+1)}"
        )
        plr.outcome_message()


def main():
    """start the game and apply settings based on player
    choice. Generate ships on each board according to settings
    choices. Start the game loop."""
    choice = game_start_options()
    if choice == 1:
        plr, com = Battlegrid("The Computer"), Battlegrid("You")
    elif choice == 2:
        plr, com = custom_settings()

    plr.generate_ships()
    com.generate_ships()

    game_loop(plr, com)


if __name__ == "__main__":
    main()
