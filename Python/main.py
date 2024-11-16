from chess import ChessGame
import pygame
from copy import deepcopy
pygame.init()

# Load sounds
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")
click_sound_chess = pygame.mixer.Sound("chess_move_soundf.mp3")

# Screen and colors setup
screen_width, screen_height, added_screen_width = 500, 500, 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))

# Define colors
white, grey, red = (255, 255, 255), (128, 128, 128), (255, 0, 0)
brown, light_brown, highlight_color = (118, 150, 86), (238, 238, 210), (200, 200, 0)
square_size = screen_width // 8

# Load piece images
pieces_images = {piece: pygame.image.load(f'{color}_{name}.png') 
                 for color, name, piece in [('black', 'rook', 'bR'), ('black', 'knight', 'bN'), 
                                            ('black', 'bishop', 'bB'), ('black', 'queen', 'bQ'), 
                                            ('black', 'king', 'bK'), ('black', 'pawn', 'bP'),
                                            ('white', 'rook', 'wR'), ('white', 'knight', 'wN'),
                                            ('white', 'bishop', 'wB'), ('white', 'queen', 'wQ'),
                                            ('white', 'king', 'wK'), ('white', 'pawn', 'wP')]}



# Main function
if __name__ == "__main__":
    game = ChessGame()
    game.last_move, selected_piece, possible_moves = [], None, []
    white_time, black_time = game.choose_game()  # Initialize game mode selection
    screen = pygame.display.set_mode((screen_width + added_screen_width ,  screen_height))
    
    game.time_reg(white_time, black_time)
    pygame.time.delay(100)
    game.list_of_boards.append(game.chess_board)
    game.list_of_times.append((game.white_time, game.black_time))
    x_king, y_king = -1, -1  # Initialize king's position in check
    k = 0
    
    while game.running:
        game.draw_timer()
        game.draw_add_time_button()
        game.handle_add_time_button()
        game.draw_move_back_button()
        game.draw_board()  # Draw the board
        l = game.len_list_of_boards
        # Ensure the list_of_boards contains independent deep copies of the board (3D list)
        if game.list_of_boards[l-1] != game.chess_board:
            game.list_of_boards[l] = deepcopy(game.chess_board)
            game.list_of_times[l] = [game.white_time, game.black_time]
            game.len_list_of_boards += 1
        
        # Highlight last move
        if len(game.last_move) > 1:
            x, y = game.last_move[0]
            mx, my = game.last_move[1]
            pygame.draw.rect(screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
            
        # Highlight king if in check
        if (x_king, y_king) != (-1, -1):
            pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))

        # Highlight possible moves for selected piece
        if game.selected_piece:
            x, y = game.selected_piece
            if game.turn[0] == game.chess_board[y][x][0]:  # Ensure selected piece belongs to current player
                pygame.draw.rect(screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                for mx, my in possible_moves:
                    pygame.draw.rect(screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))

        # Draw pieces, timer, and additional buttons
        game.draw_pieces()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Check if left click
                    x, y = event.pos
                    x_square, y_square = x // square_size, y // square_size
                    
                    # Ensure within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if game.selected_piece and (x_square, y_square) in possible_moves:
                            game.is_king_in_check()
                            game.move_piece(game.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            game.last_move = [[game.selected_piece[0], game.selected_piece[1]], [x_square, y_square]]
                            
                            # Check if the move results in a check
                            x_king, y_king = -1, -1  # Reset king position
                            for i in range(8):
                                for j in range(8):
                                    check_pos = game.check(i, j)
                                   #"" if check_pos != [-1, -1]:  # Update if a check is found
                                    x_king, y_king = check_pos
                                    if (x_king !=-1) : 
                                        break 
                                if x_king != -1:
                                    break
                            
                            
                            game.change_player()
                            game.selected_piece, possible_moves = None, []
                        elif game.chess_board[y_square][x_square][0]==game.turn[0]:
                            game.selected_piece = (x_square, y_square)
                            possible_moves = game.get_valid_moves(x_square, y_square)  # Only get valid moves
                            #print(possible_moves)
        pygame.display.flip()
    
        game.update_timers()
        if k == 0:
            game.time_reg(white_time, black_time)
            k += 1
            pygame.time.delay(100)
        game.show_winner()

    pygame.quit()
      #################        color = 'b' if self.turn=='white' else 'w'
#######
      
 