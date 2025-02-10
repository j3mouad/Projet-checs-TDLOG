import pygame
from board import Board
from utils import *
from config import WHITE
from chess_game import ChessGame
from first_screen import choose_game
from rematch import Rematch_screen
pygame.init()
def run():
    """
    Initializes and runs the main chess game loop.

    This function sets up the game window, initializes the chessboard, and manages the game loop.
    It continuously updates the board, handles user interactions, and checks for game-ending conditions.
    When a game ends, it displays a rematch screen and resets the game if the player chooses to play again.

    The game loop performs the following tasks:
    - Initializes the game screen and board.
    - Handles drawing elements such as pieces, moves, timers, and scores.
    - Updates game states and checks for game-ending conditions.
    - Displays the rematch screen when a game ends.
    - Allows restarting the game with a new setup.

    The loop runs until the player exits the game.

    Returns:
        None
    """
    screen_width = 1600
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Chess")

    # Initialize game components
    game = ChessGame(screen)
    board = Board(game, screen)
    white_time, black_time, screen_width, screen_height = choose_game(board)
    board.screen_width = screen_width
    board.screen_height = screen_height
    board.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    screen.fill(WHITE)

    board.game.time_reg(white_time, black_time)
    board.game.list_of_boards.append(game.chess_board)
    board.game.list_of_times.append((game.white_time, game.black_time))

    k = 0
    while board.game.running:
        board.draw_timer()
        board.draw_move_back_button()
        board.draw_board()
        board.draw_score()
        board.draw_add_time_button()
        board.draw_last_move()
        board.draw_king_in_check()
        board.draw_selected_piece()
        board.draw_pieces()
        board.run()
        board.update_score()
        board.draw_move()
        board.update_moves()
        board.update_screen()
        pygame.display.flip()
        result = board.game.game_ends()
        board.update_timers()
        board.draw_timer()
        if k == 0:
            board.game.time_reg(white_time, black_time)
            k += 1
        if result is not None:
            rematch = Rematch_screen(result)  # Display the rematch screen
            if not rematch:  # If rematch is False, exit the game
                break

            # Reset the game for a rematch
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Chess")
            game = ChessGame(screen)
            board = Board(game, screen)
            white_time, black_time = choose_game(board)
            screen.fill(WHITE)
            board.game.time_reg(white_time, black_time)
            board.game.list_of_boards.append(game.chess_board)
            board.game.list_of_times.append((game.white_time, game.black_time))
            k = 0  # Reset any variables as needed

    pygame.quit()
