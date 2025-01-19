from game import run


"""
Main script to run the chess game.

This script initializes the game loop, allowing for multiple matches if a rematch is selected.
The `run` function from the `game` module handles the execution of each game.

Attributes:
    rematch (bool): Flag to control the loop for rematches. Set to True to start or continue playing.
"""

if __name__ == "__main__":
    rematch = True
    while rematch :
        rematch  = run()

