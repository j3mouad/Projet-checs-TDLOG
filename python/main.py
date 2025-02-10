from test_pygame import ensure_pygame_installed
ensure_pygame_installed()

try:
    from game import run
except ImportError as e:
    print(f"Error: Failed to import 'run' from 'game'.\nDetails: {e}")
    exit(1)

"""
Main script to run the chess game.

It ensures that pygame is installed and then runs the game loop.
This script initializes the game loop, allowing for multiple matches if a rematch is selected.
The `run` function from the `game` module handles the execution of each game.

Attributes:
    rematch (bool): Flag to control the loop for rematches. Set to True to start or continue playing.
"""

if __name__ == "__main__":
    rematch = True
    max_games = 10  # Optional: Set a maximum number of matches to prevent infinite looping
    game_count = 0  

    while rematch and game_count < max_games:
        try:
            result = run()
            if not isinstance(result, bool):  # Ensure a valid boolean return value
                print("Error: run() did not return a boolean. Exiting loop.")
                break  
            rematch = result  
            game_count += 1
        except Exception as e:
            print(f"Unexpected error in game loop: {e}")
            break  # Exit loop on error
    print("Exiting game loop.")