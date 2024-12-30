import pygame
from Board import Board
from utils import *
from config import screen_width, screen_height, added_screen_width, square_size, white, grey, red, orange, brown, light_brown, highlight_color, black, button_color, button_hover_color
from chess_game import ChessGame
from first_screen import choose_game
# Main function
pygame.init()
# Main game loop
def run() :
    screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
    pygame.display.set_caption("Chess")
    # Draw and update the chessboard
    game = ChessGame()
    board = Board(game)

    white_time,black_time = choose_game(board)
    screen.fill(white)
    board.game.time_reg(white_time, black_time)
    board.game.list_of_boards.append(game.chess_board)
    board.game.list_of_times.append((game.white_time, game.black_time))
    k = 0
    p = 0 
    while board.game.running:
        print(board.game.white_time)
        board.draw_timer()
        pygame.time.delay(100)
        board.draw_add_time_button()
        board.handle_add_time_button()
        board.draw_move_back_button()
        board.draw_board()  # Draw the board
        board.game.update_list_of_boards()
        board.draw_last_move()
        board.draw_king_in_check()

        board.draw_selected_piece()
        board.draw_pieces()
        pygame.display.flip()
        board.game.castling()
        board.run()
        board.draw_move()
        board.game.all_moves()
        board.game.change_player()
        board.game.all_moves()
        board.game.change_player()
        board.update_timers()            
        if k == 0:
            board.game.time_reg(white_time, black_time)
            k += 1

        board.game.game_ends()

    pygame.quit()

    

