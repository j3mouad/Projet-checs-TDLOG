import pygame
import sys
from copy import deepcopy

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
screen_width = 500
screen_height = 500
added_screen_width = 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
button_color = (100, 200, 100)  # Green color for the button
button_hover_color = (150, 250, 150)  # Lighter green for hover

# Taille de la case
square_size = screen_width // 8

# Charger les images des pièces (les fichiers doivent être présents dans le même répertoire)
pieces = {
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

# Fonction pour dessiner l'échiquier
def draw_board():
    for row in range(8):
        for col in range(8):
            color = light_brown if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Fonction pour placer les pièces sur l'échiquier
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--':
                resized_piece = pygame.transform.scale(pieces[piece], (square_size, square_size))
                screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Fonction pour afficher le timer
def draw_timer(white_time, black_time):
    font = pygame.font.Font(None, 36)
    white_timer_surface = font.render(f'White: {white_time // 60}:{white_time % 60:02}', True, black)
    black_timer_surface = font.render(f'Black: {black_time // 60}:{black_time % 60:02}', True, black)

    pygame.draw.rect(screen, white, (screen_width, 0, added_screen_width, screen_height))  # White background for the timer area
    screen.blit(white_timer_surface, (screen_width + 20, 450))
    screen.blit(black_timer_surface, (screen_width + 20, 50))

# Fonction pour dessiner le bouton d'ajout de temps
def draw_add_time_button():
    button_rect = pygame.Rect(screen_width + 20, 200, 250, 80)  # Position and size of the button
    mouse_pos = pygame.mouse.get_pos()

    # Change the color of the button based on mouse hover
    if button_rect.collidepoint(mouse_pos):  # Check if mouse is over the button
        pygame.draw.rect(screen, (150, 150, 150), button_rect)  # Lighter color for hover
    else:
        pygame.draw.rect(screen, black, button_rect)  # Original color

    # Create the button text
    font = pygame.font.Font(None, 36)
    button_text = font.render('+ 5 seconds', True, white)

    # Center the text on the button
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)  # Draw the text centered on the button


# Fonction pour gérer le clic sur le bouton
# Fonction pour gérer le clic sur le bouton
def handle_add_time_button(white_time, black_time, turn):
    button_rect = pygame.Rect(screen_width + 20, 200, 250, 80)  # Define the button rectangle
    mouse_pos = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
        if button_rect.collidepoint(mouse_pos):  # Check if mouse is over the button
            if turn == 'white':
                black_time += 5  # Add 5 seconds to black's timer
            else:
                white_time += 5  # Add 5 seconds to white's timer

    return white_time, black_time


# Fonction pour afficher le gagnant dans une nouvelle fenêtre
def show_winner(winner):
    winner_window = pygame.display.set_mode((300, 150))
    winner_window.fill(white)
    font = pygame.font.Font(None, 48)
    winner_text = font.render(f'{winner} won!', True, black)
    winner_window.blit(winner_text, (50, 50))
    def display_rematch_button(window, font, button_x=50, button_y=300, button_width=200, button_height=50):
        """
        Display a rematch button on the Pygame window.
        """
        # Create the button rectangle
        button_rematch = pygame.Rect(button_x, button_y, button_width, button_height)

        # Set button color based on hover
        button_color = white if not button_rematch.collidepoint(pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(window, button_color, button_rematch)

        # Render the text for the button
        rematch_text = font.render("Rematch", True, black)
        text_x = button_x + (button_width - rematch_text.get_width()) // 2
        text_y = button_y + (button_height - rematch_text.get_height()) // 2
        window.blit(rematch_text, (text_x, text_y))

        pygame.display.flip()

        return button_rematch  # Return the button rectangle for click detection


    def is_rematch_clicked(button_rematch):
        """
        Check if the rematch button was clicked.

        Returns:
        - True if the rematch button was clicked, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and button_rematch.collidepoint(event.pos):
                return True  # Button was clicked
        return False  # Button was not clicked
    running = False
    pygame.display.flip()
    button_rematch=display_rematch_button(winner_window, font, button_x=50, button_y=300, button_width=200, button_height=50)
    if (is_rematch_clicked(button_rematch)):
        running=True        
    # Boucle pour attendre que l'utilisateur ferme la fenêtre
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    if (running):
        return True 
    pygame.quit()
    sys.exit()
    return False 
def display_rematch_button(window, font, button_x=50, button_y=300, button_width=200, button_height=50):
    """
    Display a rematch button on the Pygame window and check if it is clicked.

    Returns:
    - True if the button is clicked, False otherwise.
    """
    # Create the button rectangle
    button_rematch = pygame.Rect(button_x, button_y, button_width, button_height)

    # Set button color based on hover
    button_color = white if not button_rematch.collidepoint(pygame.mouse.get_pos()) else button_hover_color
    pygame.draw.rect(window, button_color, button_rematch)

    # Render the text for the button
    rematch_text = font.render("Rematch", True, black)
    text_x = button_x + (button_width - rematch_text.get_width()) // 2
    text_y = button_y + (button_height - rematch_text.get_height()) // 2
    window.blit(rematch_text, (text_x, text_y))

    pygame.display.flip()

    # Check for a click on the button
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and button_rematch.collidepoint(event.pos):
            return True  # Button was clicked

    return False  # Button was not clicked


def choose_game():
    window = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
    pygame.display.set_caption("Choisir une partie")
    font = pygame.font.Font(None, 28)
    text = font.render("Choisissez une partie :", True, black)
    window.blit(text, (50, 50))

    # Boutons pour les parties
    button_width = 200
    button_height = 50
    button_margin = 20
    button_x = 50
    button_y = 100

    # Rectangle des boutons
    button_black = pygame.Rect(button_x, button_y, button_width, button_height)
    button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)

    # Affichage des boutons
    pygame.draw.rect(window, white if not button_black.collidepoint(pygame.mouse.get_pos()) else button_hover_color, button_black)
    pygame.draw.rect(window, white if not button_white.collidepoint(pygame.mouse.get_pos()) else button_hover_color, button_white)

    # Texte des boutons
    black_text = font.render("Jouer avec Noirs", True, black)
    white_text = font.render("Jouer avec Blancs", True, black)
    window.blit(black_text, (button_x + 10, button_y + 10))
    window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + 10))

    pygame.display.flip()

    # Gestion des événements
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_black.collidepoint(event.pos):
                    choosing = False
                    return 'black'  # Return black choice
                elif button_white.collidepoint(event.pos):
                    choosing = False
                    return 'white'  # Return white choice
# Return white choice

# Disposition initiale des pièces sur l'échiquier
chess_board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]
initial_board=deepcopy(chess_board)
choose_game()

# Timer settings
initial_white_time=6
initial_black_time=6
white_time = 6  # 10 minutes for white (in seconds)
black_time = 6  # 10 minutes for black (in seconds)
turn = 'white'  # Track whose turn it is
last_time_update = pygame.time.get_ticks()

# Boucle principale
running = True
while running :
    current_time = pygame.time.get_ticks() // 1000  # Get time in seconds
    elapsed_time = current_time - last_time_update // 1000

    if turn == 'white':
        white_time -= elapsed_time
    else:
        black_time -= elapsed_time

    # Check for timer expiration
    if white_time <= 0 or black_time <= 0:
        running = False
        winner = "Black" if white_time <= 0 else "White"
        b=show_winner(winner)
        if (b):
            running = True
            chess_board=initial_board
            white_time=initial_white_time
            black_time=initial_black_time
    last_time_update = pygame.time.get_ticks()

    # Dessiner l'échiquier et les pièces
    draw_board()
    draw_pieces(chess_board)
    draw_timer(white_time, black_time)  # Afficher le timer
    draw_add_time_button()  # Afficher le bouton d'ajout de temps

    # Gérer le clic sur le bouton d'ajout de temps
    white_time, black_time = handle_add_time_button(white_time, black_time, turn)
    if (not running) : 
        
        chess_board=initial_board
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    pygame.display.flip()
    pygame.time.delay(100)  # Delay to limit CPU usage

pygame.quit()
sys.exit()