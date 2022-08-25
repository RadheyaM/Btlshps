"""Module desc goes here"""
# from random import randint


def read_int(prompt, min_val: int, max_val: int):
    """prompts player for input and ensures a response of an integer
    between min and max values"""
    while True:
        entry = input(prompt)
        try:
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
    def __init__(self, size, ships, player_name, type):
        self. size = size
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


def welcome():
    print("Welcome to Btlshps! Time to play the game!")
    print("The object of the game is to sink all your opponents ships before they sink your's!")
    print("Enter 1 for default game mode")
    print("Enter 2 for custom game mode ")
    read_int("Would you like to play default or custom mode?\n", min_val=1, max_val=2)


def custom_choice()
    pass


def the_game() -> None:
    welcome()

the_game()
