from chess import ChessGame
import pygame
from chess import screen_width,screen_height,added_screen_width
pygame.init()
import sys
sys.path.append('/home/hassene/Desktop/Projet-echecs-TDLOG/build/libAI.so')
import sys
sys.path.append('/home/hasssene/Desktop/Projet-echecs-TDLOG/Python')
from Board import Board
from AI import evaluate
# Main function
white = (255,255,255)
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
pygame.display.set_caption("Chess")
# Main game loop
def run() :
    # Draw and update the chessboard
    game = ChessGame()
    board = Board(game)
    white_time,black_time = board.choose_game()
    screen.fill(white)
    board.game.time_reg(white_time, black_time)
    pygame.time.delay(100)
    board.game.list_of_boards.append(game.chess_board)
    board.game.list_of_times.append((game.white_time, game.black_time))
    k = 0
    p = 0 
    while board.game.running:
        board.draw_timer()
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
            pygame.time.delay(100)
        
        board.game.game_ends()

    pygame.quit()
    game.show_winner()

    

