from chess import ChessGame
import pygame

pygame.init()
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")  # Ensure you have a click.wav file in the same directory
click_sound_chess=pygame.mixer.Sound("chess_move_soundf.mp3")

# Screen and colors setup
screen_width = 500
screen_height = 500
added_screen_width = 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))

white = (255, 255, 255)
grey = (128, 128, 128)
red = (255, 0, 0)
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
highlight_color = (200, 200, 0)  # Color for highlighting possible moves

square_size = screen_width // 8

# Load piece images
pieces_images = {
    'bR': pygame.image.load('black_rook.png'),
    'bN': pygame.image.load('black_knight.png'),
    'bB': pygame.image.load('black_bishop.png'),
    'bQ': pygame.image.load('black_queen.png'),
    'bK': pygame.image.load('black_king.png'),
    'bP': pygame.image.load('black_pawn.png'),
    'wR': pygame.image.load('white_rook.png'),
    'wN': pygame.image.load('white_knight.png'),
    'wB': pygame.image.load('white_bishop.png'),
    'wQ': pygame.image.load('white_queen.png'),
    'wK': pygame.image.load('white_king.png'),
    'wP': pygame.image.load('white_pawn.png')
}
if __name__ == "__main__":
    game = ChessGame()
    last_move = []
    t = pygame.time.get_ticks()
    white_time, black_time = game.choose_game()  # Initialize game mode selection
    k = 0
    screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))

    pygame.time.delay(100)
    game.time_reg(white_time, black_time)

    selected_piece = None
    x_king = -1 
    y_king  = -1 
    while game.running:
        # Draw board and highlight moves
        game.draw_board()  # Draw the board
        if len(game.last_move)>1  :
            x,y=game.last_move[0]
            mx,my=game.last_move[1]
            pygame.draw.rect(screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
            
        if selected_piece:
            x,y=selected_piece
            if (game.turn[0]==game.chess_board[y][x][0]):
                pygame.draw.rect(screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                print(possible_moves)
                for mx, my in possible_moves:
                    pygame.draw.rect(screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
        
        if (x_king>-1 and y_king>-1) :
            pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))

        game.draw_pieces()  # Draw pieces on top of highlighted squares
        game.draw_timer()
        game.draw_add_time_button()
        game.handle_add_time_button()
        game.draw_move_back_button()
        
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_clicked = pygame.mouse.get_pressed()[0]
                if not left_clicked:
                    continue
                
                x, y = event.pos
                x_square = x // square_size
                y_square = y // square_size
                
                if 0 <= x_square < 8 and 0 <= y_square < 8:  # Check if within board bounds
                    if selected_piece is not None: # Deselect if same piece clicked
                        if ((x_square,y_square) in possible_moves) :
                            game.move_piece(selected_piece,x_square, y_square)
                            game.last_move=[]
                            game.last_move.append([selected_piece[0],selected_piece[1]])
                            game.last_move.append([x_square,y_square])
                            x_king,y_king=game.check(x_square,y_square)
                            game.change_player()
                        selected_piece = None
                        possible_moves = []
                    else:
                        
                        selected_piece = (x_square, y_square)  # Select the new piece
                        #click_sound_chess.play()
                        
                        # Retrieve possible moves for the selected piece
                        possible_moves = game.get_possible_moves(x_square, y_square)
        
        pygame.display.flip()
        game.update_timers()
        if k == 0:
            game.time_reg(white_time, black_time)
            k = 1

        game.show_winner()

    pygame.quit()
