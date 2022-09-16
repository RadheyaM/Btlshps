# BTLSHPS: A Python Terminal battleships game

[Live Site](https://btlshps.herokuapp.com/)

## Overview

The player and computer make guesses (random in the computer's case) to try to hit the opponent's ships first, custom settings can be applied increasing or decreasing the number of ships on the grid, ships hit to win and a guess limit.

## Table of Contents

## Planning

## Features

### feature1
### feature2
### etc...

## Game Logic Overview
### Game Start and Choosing Settings
'main()' is initiated and calls 'game_start_options()' which prints the greeting and presents the player with three options.  
 - Option 1 returns '1' to main() which creates the computer and player class instances with default settings.  
  - Option 2 returns '2' to main() which calls custom_settings() and allows the player to choose number of ships, hits to win and total guesses allowed before game over. Player and computer intances are assigned the custom settings.
  - Option 3 prints out help_me() and prompts the player again to make a choice.
  - Once a choice has been made main() calls the generate_ships() class method on player and computer intances and then calls game_loop().

### Game Loop
 - The game loop starts by printing the boards using the print_screen() function. While the 'new_turn' variable is equal to 'True' the loop calls the player_guess() class method prompting the player to input guess co-ordinates, guesses are saved in a class array.  
 - With win_conditions() the co-ordinates are then checked against ship locations, hits to win etc.  If win conditions are met it sets 'new_turn' to 'False' which will end the game_loop().  If win conditions are not met it returns 'True' and the game continues by calling computer_guess() and generating a random computer guess which follow the same checks as the player guess.
 - After both guesses are made and 'new_turn' still equals 'True' a game log with guess results is printed along with a board with updated symbols representing a miss or a hit as appropriate.
 - If win conditions are met a fitting message will be printed to the player along with a final board showing the computer ship locations and the final scores.  The player will be prompted to hit '1' for a new game or '2' to close the program.


## Technologies Used

## Testing

## Deployment

## Credits