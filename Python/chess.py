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
button_color = (100, 200, 100)  # Couleur verte pour le bouton
button_hover_color = (150, 250, 150)  # Vert plus clair pour le survol
selected_piece=None

# Taille de la case
square_size = screen_width // 8

# Charger les images des pièces
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
        self.white_time = 6  # 10 minutes en secondes
        self.black_time = 6
        self.initial_white_time = self.white_time
        self.initial_black_time = self.black_time
        self.last_time_update = pygame.time.get_ticks()
        self.running = True
        self.x_square_clicked=None
        self.y_square_clicked=None
        self.number_of_time_same_piece_clicked= 0

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
    def selected_piece(self,x,y):
        self.draw_pieces()
        pygame.display.flip()
        if self.number_of_time_same_piece_clicked == 1:
            color = brown if ((self.x_square_clicked // square_size)+(self.y_square_clicked // square_size)) % 2 == 1 else light_brown
            pygame.draw.rect(screen, color , pygame.Rect(self.x_square_clicked, self.y_square_clicked, square_size, square_size))
            self.number_of_time_same_piece_clicked = 0
        else:
            x_square = (x // square_size) * square_size
            y_square = (y // square_size) * square_size
            pygame.draw.rect(screen, (240, 240, 0) , pygame.Rect(x_square, y_square, square_size, square_size))
            self.number_of_time_same_piece_clicked = 1
            self.x_square_clicked,self.y_square_clicked=x_square,y_square
    def selected_piece_coloring():
        pass
    def show_moves(piece,possible_move):
        pass
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

        rematch_text = font.render("Rejouer", True, black)
        text_x = button_x + (button_width - rematch_text.get_width()) // 2
        text_y = button_y + (button_height - rematch_text.get_height()) // 2
        window.blit(rematch_text, (text_x, text_y))

    def choose_game(self):
        window = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
        pygame.display.set_caption("Choisir une partie")
        font = pygame.font.Font(None, 28)
        text = font.render("Choisissez une partie :", True, black)
        window.blit(text, (50, 50))

        button_width = 200
        button_height = 50
        button_margin = 20
        button_x = 50
        button_y = 100

        button_black = pygame.Rect(button_x, button_y, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)

        choosing = True
        while choosing:
            mouse_pos = pygame.mouse.get_pos()
            window.fill(white)
            window.blit(text, (50, 50))

            pygame.draw.rect(window, white if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, white if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)

            black_text = font.render("Jouer avec Noirs", True, black)
            white_text = font.render("Jouer avec Blancs", True, black)
            window.blit(black_text, (button_x + 10, button_y + 10))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_black.collidepoint(event.pos):
                        choosing = False
                        self.turn = 'black'
                    elif button_white.collidepoint(event.pos):
                        choosing = False
                        self.turn = 'white'

    def reset_game(self):
        self.chess_board = deepcopy(self.initial_board)
        self.white_time = self.initial_white_time
        self.black_time = self.initial_black_time
        self.turn = 'white'
        self.last_time_update = pygame.time.get_ticks()

    def update_timers(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time_update) // 1000

        if elapsed_time > 0:
            if self.turn == 'white':
                self.white_time -= elapsed_time
            else:
                self.black_time -= elapsed_time
            self.last_time_update = current_time

        if self.white_time <= 0 or self.black_time <= 0:
            winner = "Noir" if self.white_time <= 0 else "Blanc"
            self.show_winner(winner)

    def run(self):
        self.choose_game()
        while self.running:
            self.update_timers()
            self.draw_board()
            self.draw_pieces()
            self.draw_timer()
            self.draw_add_time_button()
            self.handle_add_time_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            pygame.time.delay(100)

        pygame.quit()
        sys.exit()
"""
if __name__ == "__main__":
    game = ChessGame()
    game.run()

if __name__ == "__main__":
    game = ChessGame()
    game_running = True
    game.draw_board()
    x_square_clicked,y_square_clicked=None,None
    number_of_time_same_piece_clicked= 0
    while game_running:
        game.draw_pieces()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if number_of_time_same_piece_clicked == 1:
                    color = brown if ((x_square_clicked // square_size)+(y_square_clicked // square_size)) % 2 == 1 else light_brown
                    pygame.draw.rect(screen, color , pygame.Rect(x_square_clicked, y_square_clicked, square_size, square_size))
                    number_of_time_same_piece_clicked = 0
                else:
                    x, y = event.pos
                    x_square = (x // square_size) * square_size
                    y_square = (y // square_size) * square_size
                    pygame.draw.rect(screen, (240, 240, 0) , pygame.Rect(x_square, y_square, square_size, square_size))
                    number_of_time_same_piece_clicked = 1
                    x_square_clicked,y_square_clicked=x_square,y_square
                
    pygame.quit()
"""
if __name__ == "__main__":
    game = ChessGame()
    game_running = True
    game.draw_board()
    while game_running:
        game.draw_pieces()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                game.selected_piece(x,y)

    pygame.quit()
