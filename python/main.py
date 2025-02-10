from test_pygame import ensure_pygame_installed
ensure_pygame_installed()
import socket
import subprocess

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
    HOST = '127.0.0.1'  # Localhost
    PORT = 8080         # Port to listen on
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening for connections...")
        cpp_executable = "build/Projet-echecs-TDLOG.exe" 
        print(1)
        subprocess.Popen(cpp_executable)
        print(1)
        conn, addr = s.accept()
        print('conns is ',conn)
        with conn:
            print(f"Connected by {addr}")
            
            while rematch and game_count < max_games:
                
                    rematch = run(conn)
                    if not isinstance(rematch, bool):  # Ensure a valid boolean return value
                            print("Error: run() did not return a boolean. Exiting loop.")
                            break  
                    rematch = rematch
                    if (rematch) :
                        break
                    game_count += 1

                