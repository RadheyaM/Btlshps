"""Module desc goes here"""
# from random import randint


def read_int(prompt, min_val: int, max_val: int) -> int:
    """prompts player for input and returns a response integer
    between min and max values"""
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
        except TypeError:
            print("Ooops, you didn't enter a number dummy!")
            print(f"Please enter a number between {min_val} & {max_val}")
 

class Battlegrid: 
    """create a battleship board grid"""
    def __init__(self, size: int, ships: int, player_name: str, type: str):
        self.size = size
        self.board = [["O" for x in range(size)] for y in range(size)]
        self.ships = ships
        self.player_name = player_name
        self.type = type
        self.guesses = []
        self.ships = []

    def print_grid(self):
        """print the grid"""
        for row in self.board:
            print(" ".join(row))


def welcome() -> int:
    """Greeting message and choose game modes"""
    print("Welcome to Btlshps! Time to play the game!")
    print("Sink all your opponent's ships before they sink yours!")
    print("Enter 1 for default game mode")
    print("Enter 2 for custom game mode ")
    print("Enter 3 for explanation of game modes")
    choice = read_int(
        "Would you like to play default or custom mode?\n",
        min_val=1,
        max_val=3
        )
    if choice == 1:
        return 1
    elif choice == 2:
        return 2
    else:
        return 3


def custom_settings():
    """Allows the player to set the size of the board,
    the number of guess, and win conditions"""
    pass


def default_settings():
    """Sets the default game settings"""
    size = 6
    ships = 5
    player_name = player_name
    computer = Battlegrid(size, ships, player_name, type)


def the_game() -> None:
    welcome()


the_game()
