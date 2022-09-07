"""Module Desc"""
from random import randint


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
