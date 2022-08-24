"""Module desc goes here"""
# from random import randint


class Battlegrid:
    """create a battleship board grid"""
    def __init__(self, size, ships, player_name, type):
        self. size = size
        self.board = [["0" for x in range(size)] for y in range(size)]
        self.ships = ships
        self.player_name = player_name
        self.type = type
        self.guesses = []
        self.ships = []

    def print_grid(self):
        """print the grid"""
        for row in self.board:
            print(" ".join(row))


player_board = Battlegrid(10, 2, "Radheya", "player")

player_board.print_grid()
