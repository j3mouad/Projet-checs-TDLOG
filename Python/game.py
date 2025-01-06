import pygame
from Board import Board
from utils import *
from config import screen_width, screen_height, square_size, white, grey, red, orange, brown, light_brown, highlight_color, black, button_color, button_hover_color
from chess_game import ChessGame
from first_screen import choose_game
from rematch import Rematch_screen
# Main function
pygame.init()

# Main game loop
def run() :
    screen = pygame.display.set_mode((screen_width , screen_height))
    pygame.display.set_caption("Chess")
    # Draw and update the chessboard
    game = ChessGame(screen)
    board = Board(game,screen)

    white_time,black_time = choose_game(board)
    screen.fill(white)
    board.game.time_reg(white_time, black_time)
    board.game.list_of_boards.append(game.chess_board)
    board.game.list_of_times.append((game.white_time, game.black_time))
    k = 0
    while board.game.running:
        board.draw_timer()
        #board.handle_add_time_button()
        board.draw_move_back_button()
        board.draw_board()  # Draw the board
        board.draw_add_time_button()
        board.draw_last_move() 
        board.draw_king_in_check()
        board.draw_selected_piece()
        board.draw_pieces()
        board.run()
        board.draw_move()
        board.update_moves()

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
                        break  # Exit the game loop
                    screen = pygame.display.set_mode((screen_width , screen_height))
                    pygame.display.set_caption("Chess")
                    # Draw and update the chessboard
                    game = ChessGame(screen)
                    board = Board(game,screen)
                    white_time,black_time = choose_game(board)
                    screen.fill(white)
                    board.game.time_reg(white_time, black_time)
                    board.game.list_of_boards.append(game.chess_board)
                    board.game.list_of_times.append((game.white_time, game.black_time))
                    k = 0  # Reset any variables as needed

    pygame.quit()

    

