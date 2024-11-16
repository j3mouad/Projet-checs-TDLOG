from chess import ChessGame
import pygame
from chess import screen_width,screen_height,added_screen_width,click_sound_chess,click_sound_add_time_button
from chess import screen
pygame.init()

# Main function
if __name__ == "__main__":
    game = ChessGame()
    white_time, black_time = game.choose_game()  # Initialize game mode selection
    screen = pygame.display.set_mode((screen_width + added_screen_width ,  screen_height))
    game.time_reg(white_time, black_time)
    pygame.time.delay(100)
    game.list_of_boards.append(game.chess_board)
    game.list_of_times.append((game.white_time, game.black_time))
    k = 0
    while game.running:
        game.draw_timer()
        game.draw_add_time_button()
        game.handle_add_time_button()
        game.draw_move_back_button()
        game.draw_board()  # Draw the board
        game.update_list_of_boards()
        # Highlight last move
        game.draw_last_move()
        # Highlight king if in check
        game.draw_king_in_check()
        # Highlight possible moves for selected piece
        game.draw_selected_piece()
        # Draw pieces, timer, and additional buttons
        game.draw_pieces()
        # Event handling
        pygame.display.flip()
        game.run()
        game.update_timers()
        if k == 0:
            game.time_reg(white_time, black_time)
            k += 1
            pygame.time.delay(100)
        game.show_winner()

    pygame.quit()
    
 