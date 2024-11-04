import pygame
import sys
from copy import deepcopy
import time
from random import shuffle
# Initialisation de Pygame
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
button_color = (100, 200, 100)  # Couleur verte pour le bouton
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

class ChessGame:
    def __init__(self):
        self.screen = screen
        self.chess_board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.initial_board = deepcopy(self.chess_board)
        self.turn = 'white'
        self.player='white'
        self.winner = None
        self.cooldown=0.5
        self.white_time = -1  # 10 minutes en secondes
        self.black_time = -1
        self.initial_white_time = self.white_time
        self.initial_black_time = self.black_time
        self.last_time_update = pygame.time.get_ticks()
        self.running = True
        self.x_square_clicked=None
        self.y_square_clicked=None
        self.number_of_time_same_piece_clicked= 0
        self.last_click_time=0
    def time_reg(self,white_time,black_time):
        self.white_time=white_time
        self.black_time=black_time
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                pygame.draw.rect(self.screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.chess_board[row][col]
                if piece != '--':
                    resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                    self.screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
    
  

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, black)

        pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
        self.screen.blit(white_timer_surface, (screen_width + 20, 450))
        self.screen.blit(black_timer_surface, (screen_width + 20, 50))

    def draw_add_time_button(self):
        self.button_rect = pygame.Rect(screen_width + 20, 200, 250, 80)
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (150, 150, 150), self.button_rect)
        else:
            pygame.draw.rect(self.screen, black, self.button_rect)

        font = pygame.font.Font(None, 36)
        button_text = font.render('+ 5 seconds', True, white)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_add_time_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.button_rect.collidepoint(mouse_pos):
                if self.turn == 'white':
                    self.black_time += 5
                else:
                    self.white_time += 5

    def show_winner(self, winner):
        winner_window = pygame.display.set_mode((300, 150))
        winner_window.fill(white)
        font = pygame.font.Font(None, 48)
        winner_text = font.render(f'{winner} a gagné!', True, black)
        winner_window.blit(winner_text, (50, 50))
        self.x_square_clicked = None
        self.y_square_clicked = None
        self.number_of_time_same_piece_clicked= 0
        self.last_click_time = 0
        self.clicked = 0
        self.cooldown = 1  # Cooldown period in seconds
        self.font = pygame.font.Font(None, 36)  # Default font and size

        self.display_rematch_button(winner_window, font)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rematch_button_rect.collidepoint(event.pos):
                        self.reset_game()
                        waiting = False
                        return
        pygame.quit()
        sys.exit()

    def display_rematch_button(self, window, font, button_x=50, button_y=100, button_width=200, button_height=50):
        self.rematch_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color_current = white if not self.rematch_button_rect.collidepoint(pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(window, button_color_current, self.rematch_button_rect)

    def selected_piece(self, x, y):
        

        # Calculate the current square based on the clicked position
        x_square = (x // square_size) * square_size
        y_square = (y // square_size) * square_size
        
    # Toggle selection based on the number of times the same piece is clicked
        if self.number_of_time_same_piece_clicked == 1:
        # Color the previously selected square
            color = brown if ((self.x_square_clicked // square_size) + (self.y_square_clicked // square_size)) % 2 == 1 else light_brown
            pygame.draw.rect(self.screen, color, pygame.Rect(self.x_square_clicked, self.y_square_clicked, square_size, square_size))

        # Reset click count after coloring the previous square
            self.number_of_time_same_piece_clicked = 0
        else:
        # Highlight the newly selected square
            pygame.draw.rect(self.screen, (240, 240, 0), pygame.Rect(x_square, y_square, square_size, square_size))

        # Update clicked position and increment click count
            self.number_of_time_same_piece_clicked = 1
            self.x_square_clicked, self.y_square_clicked = x_square, y_square


    def selected_piece_coloring(self, x_square, y_square, color):
        """
    Color a selected piece's square on the chessboard.
    
    Args:
        x_square (int): The x-coordinate of the square to be colored.
        y_square (int): The y-coordinate of the square to be colored.
        color (tuple): The RGB color value for the square.
    """
    # Draw the square with the specified color
        
        pygame.draw.rect(self.screen, color, pygame.Rect(x_square, y_square, square_size, square_size))

    

    def handle_add_time_button(self):
        current_time = time.time()  # Get the current time
        
        if pygame.mouse.get_pressed()[0]: 
            # Check if the left mouse button is pressed
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                if (self.number_of_time_same_piece_clicked==0) :
                    self.number_of_time_same_piece_clicked=1
                    return 
                # Check if enough time has passed since the last click
                if current_time - self.last_click_time >= self.cooldown:
                    # Play click sound
                    click_sound_add_time_button.play()

                    if self.player == 'white':
                        self.black_time += 5  # Add 5 seconds to black's time
                        print("Added 5 seconds to black's time.")
                    else:
                        self.white_time += 5  # Add 5 seconds to white's time
                        print("Added 5 seconds to white's time.")

                    self.last_click_time = current_time  # Update the last click time fix this code so it gets to add time in the left mouse click

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, black)
        if (self.white_time<=5):
            white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, red)
        if (self.black_time<=5):
            black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, red)

        if (self.player=='white') :
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(white_timer_surface, (screen_width + 20, 450))
            self.screen.blit(black_timer_surface, (screen_width + 20, 50))
        if (self.player=='black'):
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(black_timer_surface, (screen_width + 20, 450))
            self.screen.blit(white_timer_surface, (screen_width + 20, 50))
    def game_ends(self):
        if (self.white_time<=0 ):
            self.running=False
            self.winner = 'black'
            return True
        if (self.black_time<=0):
            self.running = False
            self.winner = 'white'
            return True
        return False
    def flip_board(self):
        L= [[self.chess_board[i][j] for j in range(8)] for i in range(7,-1,-1)]
        self.chess_board=deepcopy(L)
    def show_winner(self):
        self.game_ends()
        if (self.running):
            return 
        screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
        winner = self.winner
        screen.fill(white)
        font = pygame.font.Font(None, 48)
        winner_text = font.render(f'{winner} a gagné!', True, black)
        screen.blit(winner_text, (50, 50))
        self.display_rematch_button(screen, font)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rematch_button_rect.collidepoint(event.pos):
                        self.reset_game()
                        waiting = False
                        return
        pygame.quit()
        sys.exit()

    def display_rematch_button(self, window, font, button_x=50, button_y=100, button_width=200, button_height=400):
        self.rematch_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color_current = white if not self.rematch_button_rect.collidepoint(pygame.mouse.get_pos()) else button_hover_color
        pygame.draw.rect(window, button_color_current, self.rematch_button_rect)

        rematch_text = font.render("Rejouer", True, black)
        text_x = button_x + (button_width - rematch_text.get_width()) // 2
        text_y = button_y + (button_height - rematch_text.get_height()) // 2
        window.blit(rematch_text, (text_x, text_y))
    def draw_move_back_button(self):
        # Define button properties
        button_width = 60
        button_height = 50
        button_x = screen_width + 150
        button_y = 300
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Darker outline color for a button effect

  
    def handle_back_button_click(self):
        # Logic for what happens when the button is clicked
        print("Back button clicked!")
        # Add your back action here
    def choose_game(self):
        window = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
        pygame.display.set_caption("Let's play Chess!")
        font = pygame.font.Font(None, 28)
        text = font.render("Choisissez une partie: Un couleur et un temps de jeu ", True, black)
        window.blit(text, (50, 50))
        
        button_width = 250
        button_height = 50
        button_margin = 20
        button_x = 50
        button_y = 100

        button_black = pygame.Rect(button_x, button_y, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)

        
        button_random=pygame.Rect(button_x, button_y+4*button_height, button_width, button_height)
        button_black = pygame.Rect(button_x, button_y, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_rapid = pygame.Rect(button_x, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_classic = pygame.Rect(button_x + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_blitz = pygame.Rect(button_x + button_width+40 , button_y + 2 * (button_height + button_margin), button_width/2, button_height)
        first_choosing=True
        second_choosing = True
        white_time=0
        black_time=0
        while first_choosing or second_choosing:
            print('bla bla')
            mouse_pos = pygame.mouse.get_pos()
            window.fill(white)
            window.blit(text, (50, 50))

            pygame.draw.rect(window, white if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, white if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)

            black_text = font.render("Jouer avec Noirs", True, black)
            white_text = font.render("Jouer avec Blancs", True, black)
            window.blit(black_text, (button_x + 10, button_y + 10))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + 10))


            pygame.draw.rect(window, grey if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, grey if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)
            pygame.draw.rect(window, grey if not button_rapid.collidepoint(mouse_pos) else button_hover_color, button_rapid)
            pygame.draw.rect(window, grey if not button_classic.collidepoint(mouse_pos) else button_hover_color, button_classic)
            pygame.draw.rect(window, grey if not button_blitz.collidepoint(mouse_pos) else button_hover_color, button_blitz) 
            pygame.draw.rect(window, grey if not button_random.collidepoint(mouse_pos) else button_hover_color, button_random)


            black_text = font.render("Jouer avec Noirs", True, black)
            white_text = font.render("Jouer avec Blancs", True, black)
            classic_text = font.render("Jeu classic",True,black) 
            blitz_text = font.render("Jeu blitz",True,black)
            rapid_text= font.render("Jeu rapid",True,black)
            random_text=font.render("Jeu de Fisher",True,black)
            window.blit(black_text, (button_x + 10, button_y + (button_height - black_text.get_height()) // 2))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + (button_height - white_text.get_height()) // 2))
            window.blit(classic_text, (button_x + button_width / 2 + button_margin + 10, button_y + 2 * (button_height + button_margin) + (button_height - classic_text.get_height()) // 2))
            window.blit(rapid_text, (button_x +10 , button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(blitz_text, (button_x + 50+button_width, button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(random_text, (button_x +50, button_y + 4 * (button_height) + (button_height - random_text.get_height()) // 2))

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_black.collidepoint(event.pos):
                        first_choosing = False
                        self.turn = 'black'
                        self.flip_board()
                    
                    elif button_white.collidepoint(event.pos):
                        first_choosing = False
                        self.player = 'white'
                    elif button_classic.collidepoint(event.pos) :
                        second_choosing=False
                        self.time_reg(3600,3600)
                        white_time=3600
                        black_time=3600
                    elif button_rapid.collidepoint(event.pos) : 
                        second_choosing=False
                        self.time_reg(600,600)
                        white_time=600
                        black_time=600
                    elif button_blitz.collidepoint(event.pos) :
                        second_choosing = False
                        self.time_reg(60,60)
                        white_time=60
                        black_time=60
                    elif button_random.collidepoint(event.pos) :
                        shuffle(self.chess_board[0])
                        shuffle(self.chess_board[7])
                        
        return (white_time,black_time)    

   

    def update_timers(self,click):
        if (click):
            return 
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time_update) // 1000

        if elapsed_time > 0:
            if self.turn == 'white':
                self.white_time -= elapsed_time
            else:
                self.black_time -= elapsed_time
            self.last_time_update = current_time

        if self.white_time <= 0 or self.black_time <= 0:
            self.winner = "black" if self.white_time <= 0 else "white"
        


    
