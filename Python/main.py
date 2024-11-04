from chess import ChessGame
import pygame
pygame.init()
click_sound_add_time_button = pygame.mixer.Sound("/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/chess_add_time_sound.wav")  # Ensure you have a click.wav file in the same directory
clcik_sound_chess=pygame.mixer.Sound("/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/chess_move_soundf.mp3")
# Taille de la fenêtre
screen_width = 500
screen_height = 500
added_screen_width = 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))

# Couleurs
white = (255, 255, 255)
grey=(128,128,128)
red = (255,0,0)
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
button_color = (100, 0, 100)  # Couleur verte pour le bouton
button_hover_color = (150, 250, 150)  # Vert plus clair pour le survol
selected_piece=None
# Taille de la case
square_size = screen_width // 8

# Charger les images des pièces
pieces_images = {
    'bR': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/black_rook.png'),
    'bN': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/black_knight.png'),
    'bB': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/black_bishop.png'),
    'bQ': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/black_queen.png'),
    'bK': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/black_king.png'),
    'bP': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/black_pawn.png'),
    'wR': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/white_rook.png'),
    'wN': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/white_knight.png'),
    'wB': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/white_bishop.png'),
    'wQ': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/white_queen.png'),
    'wK': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/white_king.png'),
    'wP': pygame.image.load('/home/hassenekallala/Desktop/projet/Projet-echecs-TDLOG/Python/white_pawn.png')
}

if __name__ == "__main__":
    game = ChessGame()
    white_time,black_time=game.choose_game()  # Initialize game mode selection
    game.white_time=white_time
    game.black_time=black_time
    screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))

    if game.player == 'black' :
        game.flip_board()
    pygame.time.delay(100)
    game_running = True
    game.draw_board()

    # Initialize click tracking variables
    number_of_time_same_piece_clicked = 0
    x_square_clicked = None
    y_square_clicked = None

    while game_running:
        game.update_timers(1)
        game.draw_board()  # Draw the board
        
        # Draw the timer and add time button
        game.draw_timer()
        game.draw_add_time_button()
        game.handle_add_time_button()
        game.draw_move_back_button()

        # Highlight the selected square if a piece is selected
        if number_of_time_same_piece_clicked == 1 and x_square_clicked is not None and y_square_clicked is not None :
            color = (128, 128, 128)  # Highlight color
            pygame.draw.rect(game.screen, color, pygame.Rect(x_square_clicked, y_square_clicked, square_size, square_size))
        game.draw_pieces()  # Draw the pieces

        pygame.display.flip()  # Update the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN  :
        # Get the mouse position
                left_clicked = pygame.mouse.get_pressed()[0]  # [0] is for left button
                if not (left_clicked):
                    continue
                x, y = event.pos
                x_square = (x // square_size) * square_size
                y_square = (y // square_size) * square_size

    # Check if the square is empty using the instance method
                
                # Check if the click is within the board area
                if 0 <= x_square < screen_width-square_size and 0 <= y_square < screen_height-square_size :
                    if number_of_time_same_piece_clicked == 1:
                        # Recolor the previously selected square
                        color = grey if ((x_square_clicked // square_size) + (y_square_clicked // square_size)) % 2 == 1 else brown
                        pygame.draw.rect(game.screen, color, pygame.Rect(x_square_clicked, y_square_clicked, square_size, square_size))
                        number_of_time_same_piece_clicked = 0  # Reset click count
                    else:
                        # Highlight the newly selected square
                        number_of_time_same_piece_clicked = 1  # Increment click count
                        x_square_clicked, y_square_clicked = x_square, y_square# Update clicked position
                        clcik_sound_chess.play()
                        game.selected_piece(x, y)
        game.show_winner()

    pygame.quit()
