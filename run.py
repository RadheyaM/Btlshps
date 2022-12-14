"""Code to run a battleships game in a simulated terminal on Heroku"""
from random import randint


class Battlegrid:
    """A class defining the battleship board/grid for the player
    and computer"""
    def __init__(
        self,
        opponent_name: str,
        grid_size=5,
        num_of_ships=4,
        hits_to_win=4,
        guesses_allowed=100,
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
        self.opponent = opponent_name
        # guesses made by the other player/computer
        self.guesses = []
        # hits on this board made by opponent
        self.hits = []

    def print_grid(self):
        """print grid to the terminal"""
        if self.opponent == "You":
            print(">>>>>>>>>>THE COMPUTER's BOARD<<<<<<<<<<<\n")
        else:
            # board is spelled as bored deliberately.
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
            # screen for duplicates
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
        """Get a guess from the player, screening for duplicate entries"""
        while True:
            row = read_input(">>Guess a row: \n", 1, self.size) - 1
            col = read_input(">>Guess a column: \n", 1, self.size) - 1
            if (row, col) in self.guesses:
                print(
                    f"--Ooops, you already guessed {(row+1, col+1)}, try again"
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
        """Generates the appropriate feedback based on guess outcome"""
        if self.guesses[-1] in self.ship_locations:
            return print(f"--AND ... {self.opponent} hit a ship!")
        return print(f"--AND ... {self.opponent} missed...")


def read_input(
    prompt,
    min_val: int,
    max_val: int,
    game_over=False
) -> int:
    """prompts the player for input and returns a response integer
    between min and max values.  All player input goes through
    this function.

    Args:
        prompt: str: context for player input.
        min_val: int: the minimum value that can be entered.
        max_val: The maximum value that can be entered.
        game_over: bool: triggers custom printout on game over.

    Returns:
        When guessing during the game returns int within certain params.
        Otherwise triggers other in-terminal actions such as printing
        help_me and starting a new game.
    """
    while True:
        # remove spaces surrounding input if any
        player_input = input(prompt).strip()
        # restart and help
        if player_input.lower() == "r":
            main()
        if player_input.lower() == "h":
            help_me()
            continue
        try:
            entry = int(player_input)
            if game_over:
                if entry == 1:
                    main()
                elif entry == 2:
                    break
            if entry > max_val:
                print("**************************************************")
                print("--Oops...The number you entered is too large!...")
                print(
                    f"--Please enter a number between {min_val} & {max_val}."
                )
                print("**************************************************\n")
            elif entry < min_val:
                print("**************************************************")
                print("--Ooops...The number you entered is too small!...")
                print(
                    f"--Please enter a number between {min_val} & {max_val}."
                )
                print("**************************************************\n")
            else:
                return entry
        except ValueError:
            print("**************************************************")
            print("--Ooops... you didn't enter a number!...")
            print(f"--Please enter a number between {min_val} & {max_val}.")
            print("**************************************************\n")


def print_screen(plr, com, game_over) -> None:
    """Print both grids with symbols.

    Args:
        player and computer instances of the Battlegrid Class.
        game_over: bool: is the game over True or False.

    Returns:
        None: prints to the terminal.
    """
    if game_over:
        com.grid_symbols_game_over()
        plr.grid_symbols_game_over()
        com.print_grid()
        plr.print_grid()
        return
    com.grid_symbols()
    plr.grid_symbols()
    com.print_grid()
    plr.print_grid()


def custom_settings():
    """Allows the player to set the size of the board,
    the number of guesses, and first to hit certain number
    of ships wins.

    Returns:
        The player and computer Battlegrid instances with appropriate
        settings applied.
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


def help_me() -> None:
    """Prints helpful information for the player. Can
    be accessed by pressing 'H' in-game or '3' in the
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


def game_start_options() -> int:
    """Greets the player at the start of the game
    and prompts them to make a game mode choice or
    see game mode details.

    Returns:
        An int depending on what choice the player made.

    """
    print("Welcome-to-boredome -- Welcome-to-boredome -- Welcome ...\n")
    print(
        "--Welcome to the kingdom of Boredome, where we play Btlshps!"
        )
    print("--Sink your opponent's ships before they sink yours!")
    print("--To RESTART the game press 'R'")
    print("--For HELP press 'H'\n")
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


def game_log(plr, com) -> None:
    """Description for how a turn of guessing went, co-ordinates guessed
    by computer and player and the outcome of the guess, hit or miss.

    Args:
        computer and player class instances.

    Returns:
        Prints out a game log in the terminal.

    """
    print(
        f">>Your guess: {(com.guesses[-1][0]+1, com.guesses[-1][1]+1)}"
    )
    com.outcome_message()
    print(
        f">>Computer guess: {(plr.guesses[-1][0]+1, plr.guesses[-1][1]+1)}"
    )
    plr.outcome_message()
    print_screen(plr, com, False)


def final_score(score_type, plr, com) -> None:
    """Prints the appropriate message and score at the end of a game

    Args:
        score_type: int: depends on which win condition is met.
        computer and player class instances.

    Returns:
        Prints to terminal.
    """
    loser = "***LOSER***LOSER***LOSER***LOSER***LOSER***LOSER***"
    winner = "***WIN!***WIN!***WIN!***WIN!***WIN!***WIN!***WIN!***"
    luck = "Aww that pesky computer did it again ... better luck next time!"
    com_hits = len(plr.hits)
    plr_hits = len(com.hits)
    print_screen(plr, com, True)
    if score_type == 1:
        print(loser)
        print(luck)
    elif score_type == 2:
        print(winner)
    elif score_type == 3:
        print(loser)
        print("The computer hit more ships within the guess limit!")
        print(luck)
    elif score_type == 4:
        print(winner)
        print("You hit more ships than the computer within the guess limit!")
    elif score_type == 5:
        print("IN BOREDOME A YAWN IS THE HIGHEST ACHIEVABLE HONOUR")
        print("ON BEHALF OF ALL BORES PLEASE ACCEPT A HEARTFELT YAWN")
        print(
            "***CONGRATS!***YAWN***YOU DREW***YAWN***CONGRATS!***YOU DREW***"
        )

    print("*********************************************************")
    print(f"-- Final Score is Computer: {com_hits}, Player: {plr_hits}")
    print("*********************************************************")
    print("Scroll up to see final board positions.")


def win_conditions(plr, com) -> bool:
    """Checks for win conditions after a guess is made.

    Args:
        computer and player class instances.

    Returns:
        bool: returns False if a win condition is met
        and interupts the game_loop to initiate game over
        printouts.
    """
    guesses = plr.guesses_allowed
    # abbreviated to fit in one line below
    c_guess_num = len(plr.guesses)
    p_guess_num = len(com.guesses)
    # computer wins by hit number
    if len(plr.hits) == plr.hits_to_win:
        final_score(1, plr, com)
        return False

    # player wins by hit number
    if len(com.hits) == plr.hits_to_win:
        com.grid_symbols_game_over()
        final_score(2, plr, com)
        return False

    # most ships hit with limited guess settings
    if guesses == c_guess_num and guesses == p_guess_num:
        com.grid_symbols_game_over()
        if len(plr.hits) > len(com.hits):
            final_score(3, plr, com)
            return False
        if len(plr.hits) < len(com.hits):
            final_score(4, plr, com)
            return False
        if len(plr.hits) == len(com.hits):
            final_score(5, plr, com)
            return False
    return True


def game_loop(plr, com) -> None:
    """Run the game loop and print the boards.

    Args:
        plr: the player instance of the Battlegrid class.
        com: the computer instance of the Battlegrid class.

    Returns:
        Runs in a loop until a win condition is met then returns
        the appropriate end of game message.
    """
    new_turn = True
    print_screen(plr, com, False)

    while new_turn:
        com.player_guess()
        new_turn = win_conditions(plr, com)
        if new_turn:
            plr.computer_guess()
            new_turn = win_conditions(plr, com)
            if new_turn:
                game_log(plr, com)
            else:
                read_input(
                    "Start a NEW GAME? '1' for Yes/'2' for No: \n", 1, 2, True
                )
        else:
            read_input(
                    "Start a NEW GAME? '1' for Yes/'2' for No: \n", 1, 2, True
            )


def main() -> None:
    """start the game and apply settings based on player
    choice. Generate ships on each board according to player
    choices. Initiate the game loop.

    Return:
        Initiates the game loop.

    """
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
