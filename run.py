"""Module containing the board class used in run.py"""
import os
from board_class import Battlegrid


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


if __name__ == "__main__":
    main()
