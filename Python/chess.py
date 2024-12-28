import pygame
import sys
from copy import deepcopy
import time
from random import shuffle
from utils import has_non_empty_list
import math
import numpy as np
import copy
sys.path.append('/home/hassene/Desktop/Projet-echecs-TDLOG/Python')
import os
from AI import AI
import sys
from button import Button
new_dir = ('/home/hassene/Desktop/Projet-echecs-TDLOG/Python')
os.chdir(new_dir)
# Initialisation de Pygame
pygame.init()
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")  # Ensure you have a click.wav file in the same directory
click_sound_chess=pygame.mixer.Sound("chess_move_soundf.mp3")
screen_width = 500
screen_height = 500
added_screen_width = 400
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
pygame.display.set_caption("Chess")
# Colors
# Define colors
white, grey, red, orange = (255, 255, 255), (128, 128, 128), (255, 0, 0), (255,165,0)
brown, light_brown, highlight_color = (118, 150, 86), (238, 238, 210), (200, 200, 0)
square_size = screen_width // 8
black = (0, 0, 0)
brown = (118, 150, 86)
light_brown = (238, 238, 210)
button_color = (100, 200, 100)  #green
button_hover_color = (150, 250, 150)  



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
        self.chess_board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ])

        self.chess_board_squares = np.array([
    ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
    ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
    ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
    ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
    ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
    ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
    ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
    ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
    ])
        
        self.list_of_boards=[self.chess_board for _ in range(1000)]
        self.len_list_of_boards=0 
        self.list_of_times=[[0,0] for _ in range(1000)]
        self.list_of_last_moves = [[(0,0),(0,0)] for _ in range(1000)]
        self.list_of_king_check  = [(False,False) for _ in range(1000)]
        self.list_of_rooks = [[0,0,0,0] for _ in range(1000)]
        self.list_of_castles = [[0,0,0,0] for _ in range(1000)]
        self.list_of_king_moves = [(False,False) for _ in range(1000)]
        self.list_of_passant = [False for _ in range(1000)]
        self.turn = 'white'
        self.player='white'
        self.last_move=[]
        self.last_move_draw = []
        self.possible_moves=[]
        self.winner = None
        self.cooldown=0.5
        self.white_time = -1  # 10 minutes en secondes
        self.black_time = -1
        self.white_king_moved=False
        self.black_king_moved=False
        self.initial_white_time = self.white_time
        self.initial_black_time = self.black_time
        self.last_time_update = pygame.time.get_ticks()
        self.running = True
        self.x_square_clicked=None
        self.y_square_clicked=None
        self.number_of_time_same_piece_clicked= 0
        self.last_click_time=0
        self.is_back_button_pressed=0
        self.white_king_check=False
        self.black_king_check=False
        self.classic=True
        self.selected_piece=[]
        self.pion_passant=False
        self.last_time_back_clicked=0
        self.x_king, self.y_king = -1, -1
        self.white_moves={(-1,-1):[(-1,-1)]}
        self.black_moves={(-1,-1):[(-1,-1)]}
        self.rook_moved=[0,0,0,0]
        self.castle=[0,0,0,0]
        self.one_v_one=False
        self.white=False
        self.black=False
        self.white_king_position = None
        self.black_king_position = None
    ##########################################First functions manage graphcis#############################################
    def time_reg(self,white_time,black_time):
        self.white_time=white_time
        self.black_time=black_time


    def draw_board(self):
        """
        Draws the chessboard on the screen.

        The chessboard is an 8x8 grid where each square is drawn as a rectangle.
        The color of each square alternates between light brown and brown, following 
        the standard pattern for a chessboard. The squares are drawn using the 
        `pygame.draw.rect` function.

        This method does not return any value.

        It assumes that the `pygame` library has been initialized, and the `screen` 
        attribute, which is the surface where the board is drawn, is already set up.
        """
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                pygame.draw.rect(self.screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

        
    def draw_move(self):
        """
        Animates the movement of a chess piece on the board.

        This method draws the chessboard and the moving piece, updating its position 
        step by step over 40 frames. It checks if the piece is valid and not an empty square.
        The animation is drawn by incrementally updating the piece's position and redrawing 
        the board on each frame.

        The function requires `last_move` to be set, and the piece images must be available 
        in `pieces_images`. The move is animated between the starting and ending positions.

        Returns:
            None
        """
        if (self.last_move and self.last_move != self.last_move_draw):
            self.last_move_draw = self.last_move
            x, y = self.last_move[0]
            mx, my = self.last_move[1]
            dx = (mx - x) / 40
            dy = (my - y) / 40
            piece = self.chess_board[my][mx]
            if (piece != '--'):
                resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                for i in range(40):
                    self.draw_board()
                    self.draw_pieces(mx, my)
                    col = y + i * dy
                    row = x + i * dx
                    self.screen.blit(resized_piece, pygame.Rect(row * square_size, col * square_size, square_size, square_size))
                    pygame.time.delay(1)
                    pygame.display.flip()

    def draw_pieces(self, mx=-1, my=-1):
        """
        Draws the chess pieces on the board.

        This method iterates through the chessboard, drawing each piece at its respective
        position. If `mx` and `my` are provided, it skips drawing the piece at that 
        particular position. The pieces are drawn from the `chess_board` state, and 
        text can also be rendered for the square labels.

        Args:
            mx (int, optional): The x-coordinate of a square to skip drawing a piece at. Default is -1.
            my (int, optional): The y-coordinate of a square to skip drawing a piece at. Default is -1.

        Returns:
            None
        """
        font = pygame.font.Font(None, 12)
        for row in range(8):
            for col in range(8):
                text = font.render(self.chess_board_squares[col][row], True, (0, 0, 255)) 
                screen.blit(text, (row * square_size, col * square_size))
                piece = self.chess_board[row][col]
                if piece != '--':
                    if (mx == col and my == row):
                        continue 
                    resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                    self.screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

    def draw_add_time_button(self):
        """
        Draws the 'Add Time' button on the screen.

        This method creates a button that allows the user to add 5 seconds to the opponent's 
        timer. The button changes color when hovered, and displays the text '+ 5 seconds'.

        Returns:
            None
        """
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
        """
        Handles the logic when the 'Add Time' button is clicked.

        This method checks if the left mouse button is pressed and whether enough time has 
        passed since the last click. When the button is clicked, 5 seconds are added to the 
        opponent's timer, depending on which player's turn it is.

        Returns:
            None
        """
        current_time = time.time()
        if pygame.mouse.get_pressed()[0]:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                if (self.number_of_time_same_piece_clicked == 0):
                    self.number_of_time_same_piece_clicked = 1
                    return 
                if current_time - self.last_click_time >= self.cooldown:
                    click_sound_add_time_button.play()
                    if self.turn == 'white':
                        self.black_time += 5
                    else:
                        self.white_time += 5
                    self.last_click_time = current_time

    def draw_timer(self):
        """
        Draws the timers for both players.

        This method displays the countdown timers for the white and black players, updating 
        them in minutes and seconds format. If a player's time is below 5 seconds, their 
        timer is displayed in red. The timers are drawn on the screen depending on whose 
        turn it is.

        Returns:
            None
        """
        font = pygame.font.Font(None, 36)
        white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, black)
        if self.white_time <= 5:
            white_timer_surface = font.render(f'White: {self.white_time // 60}:{self.white_time % 60:02}', True, red)
        if self.black_time <= 5:
            black_timer_surface = font.render(f'Black: {self.black_time // 60}:{self.black_time % 60:02}', True, red)

        if self.player == 'white':
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(white_timer_surface, (screen_width + 20, 450))
            self.screen.blit(black_timer_surface, (screen_width + 20, 50))
        if self.player == 'black':
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(black_timer_surface, (screen_width + 20, 450))
            self.screen.blit(white_timer_surface, (screen_width + 20, 50))

    def game_ends(self):
        """
        Checks if the game has ended.

        This method checks if either player has run out of time or if the game is in a stalemate 
        condition (when a player cannot make a valid move). If a player is in checkmate, 
        the other player wins. The game ends when one of these conditions is met.

        Returns:
            bool: True if the game has ended, False otherwise.
        """
        if self.white_time <= 0:
            self.winner = 'black'
            self.running = False
            return True
        if self.black_time <= 0:
            self.winner = 'white'
            self.running = False
            return True
        if not has_non_empty_list(self.white_moves) and self.turn == 'white':
            if self.white_king_check:
                self.winner = 'black'
                self.running = False
                return True
            else:
                self.winner = 'Stalemate'
                self.running = False
                return False
        if not has_non_empty_list(self.black_moves) and self.turn == 'black':
            if self.black_king_check:
                self.winner = 'white'
                self.running = False
                return True
            else:
                self.winner = 'Stalemate'
                self.running = False
                return False

    def draw_move_back_button(self):
        """
        Draws the 'Back' button on the screen.

        This method creates a button that allows the player to undo the last move. The button 
        changes color when hovered over, and displays the text "Back".

        Returns:
            None
        """
        button_width = 60
        button_height = 50
        button_x = screen_width + 150
        button_y = 300
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(self.screen, black if not button_rect.collidepoint(mouse_pos) else button_hover_color, button_rect)

        font = pygame.font.Font(None, 24)
        text = font.render("Back", True, white)
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

        if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.handle_back_button_click()

    def handle_back_button_click(self):
        """
        Handles the logic when the 'Back' button is clicked.

        This method handles the logic of undoing the last move by reverting the game state 
        to the previous one. It checks the cooldown to prevent multiple triggers and ensures 
        the state can only be reverted if there is a previous board to go back to.

        Returns:
            None
        """
        time = pygame.time.get_ticks()
        if (time - self.last_time_back_clicked) <= self.cooldown:
            return
        if self.len_list_of_boards == 0:
            return
        self.last_time_back_clicked = time
        self.len_list_of_boards -= 1
        l = self.len_list_of_boards
        self.white_time, self.black_time = self.list_of_times[l - 1]
        self.chess_board = deepcopy(self.list_of_boards[l - 1])
        self.last_move = self.list_of_last_moves[l - 1]
        self.castle = deepcopy(self.list_of_castles[l - 1])
        self.rook_moved = deepcopy(self.list_of_rooks[l - 1])
        self.white_king_check, self.black_king_check = self.list_of_king_check[l - 1]
        self.white_king_moved, self.black_king_moved = self.list_of_king_moves[l - 1]
        self.pion_passant = self.list_of_passant[l - 1]

        self.selected_piece = []
        self.draw_board()
        self.draw_pieces()
        self.turn = 'black' if self.turn == 'white' else 'white'
        pygame.display.flip()
        pygame.time.delay(100)

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
                self.winner = "black" if self.white_time <= 0 else "white"

    def choose_game(self):
        window = pygame.display.set_mode((screen_width + added_screen_width, screen_height),pygame.RESIZABLE)
        pygame.display.set_caption("Let's play Chess!")
        
        # Load the background image
        background_image = pygame.image.load("background_image.jpg")  # Update with your image path
        background_image = pygame.transform.scale(background_image, (screen_width + added_screen_width, screen_height))
        
        font = pygame.font.Font(None, 28)
        text = font.render("Choose color and time ", True, black)
        
        button_width = 250
        button_height = 50
        button_margin = 20
        button_x = 50
        button_y = 100

        button_black = pygame.Rect(button_x, button_y, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_2v2 = pygame.Rect(button_x+button_width+20, button_y +  (button_height + button_margin), button_width, button_height)
        button_random=pygame.Rect(button_x, button_y+4*button_height, button_width, button_height)
        button_white = pygame.Rect(button_x, button_y + button_height + button_margin, button_width, button_height)
        button_rapid = pygame.Rect(button_x, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_classic = pygame.Rect(button_x + button_width / 2 + button_margin, button_y + 2 * (button_height + button_margin), button_width / 2, button_height)
        button_blitz = pygame.Rect(button_x + button_width+40 , button_y + 2 * (button_height + button_margin), button_width/2, button_height)
        first_choosing=True
        second_choosing = True
        white_time=0
        black_time=0
        
        while first_choosing or second_choosing:
            mouse_pos = pygame.mouse.get_pos()
            # Draw the background image
            window.blit(background_image, (0, 0))
            window.blit(text, (50, 50))
            pygame.draw.rect(window, white if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, white if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)
            black_text = font.render("Black pieces", True, black)
            white_text = font.render("White pieces", True, black)
            window.blit(black_text, (button_x + 10, button_y + 10))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + 10))
            pygame.draw.rect(window, orange if not button_2v2.collidepoint(mouse_pos) else button_hover_color, button_2v2)
            pygame.draw.rect(window, orange if not button_black.collidepoint(mouse_pos) else button_hover_color, button_black)
            pygame.draw.rect(window, orange if not button_white.collidepoint(mouse_pos) else button_hover_color, button_white)
            pygame.draw.rect(window, orange if not button_rapid.collidepoint(mouse_pos) else button_hover_color, button_rapid)
            pygame.draw.rect(window, orange if not button_classic.collidepoint(mouse_pos) else button_hover_color, button_classic)
            pygame.draw.rect(window, orange if not button_blitz.collidepoint(mouse_pos) else button_hover_color, button_blitz) 
            pygame.draw.rect(window, orange if not button_random.collidepoint(mouse_pos) else button_hover_color, button_random)
            black_text = font.render("Jouer avec Noirs", True, black)
            white_text = font.render("Jouer avec Blancs", True, black)
            classic_text = font.render("Jeu classique",True, black) 
            blitz_text = font.render("Jeu blitz",True,black)
            rapid_text= font.render("Jeu rapide",True,black)
            twovtwo_text = font.render("Jeu 1 VS 1",True,black)
            random_text=font.render("Jeu de Fisher",True,black)
            window.blit(black_text, (button_x + 10, button_y + (button_height - black_text.get_height()) // 2))
            window.blit(white_text, (button_x + 10, button_y + button_height + button_margin + (button_height - white_text.get_height()) // 2))
            window.blit(classic_text, (button_x + button_width / 2 + button_margin + 10, button_y + 2 * (button_height + button_margin) + (button_height - classic_text.get_height()) // 2))
            window.blit(rapid_text, (button_x +10 , button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(blitz_text, (button_x + 50+button_width, button_y + 2 * (button_height + button_margin) + (button_height - rapid_text.get_height()) // 2))
            window.blit(random_text, (button_x +50, button_y + 4 * (button_height) + (button_height - random_text.get_height()) // 2))
            window.blit(twovtwo_text, (button_x+button_width+30, button_y +  (button_height + button_margin) + (button_height - random_text.get_height()) // 2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_black.collidepoint(event.pos):
                        first_choosing = False
                        self.turn = 'black'
                        self.black=True
                        self.flip_board()
                    
                    elif button_white.collidepoint(event.pos):
                        first_choosing = False
                        self.white=True
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
                    elif  button_2v2.collidepoint(event.pos) : 
                        first_choosing = False
                        self.one_v_one=True
                        self.player = 'white'
        self.list_of_boards[0]=[self.chess_board]
        self.len_list_of_boards+=1
        return (white_time,black_time)   
    def draw_king_in_check(self):
        """
        Draws a red square around the current player's king if it is in check.
        The function checks if the king is threatened by any opponent's piece.
        """
        if (self.turn == 'white'):
            self.white_king_position = self.find_king_position('white')
            x_king, y_king = self.white_king_position
            b = False
            # Check if the white king is in check by any black piece
            for key in self.black_moves:
                if (x_king, y_king) in self.black_moves[key]:
                    b = True
                    break
            self.white_king_check = b
            # If white king is in check, draw a red square around its position
            if self.white_king_check:
                pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))
        else:
            self.black_king_position = self.find_king_position('black')
            x_king, y_king = self.black_king_position
            b = False
            # Check if the black king is in check by any white piece
            for key in self.white_moves:
                if (x_king, y_king) in self.white_moves[key]:
                    b = True
                    break
            self.black_king_check = b
            # If black king is in check, draw a red square around its position
            if self.black_king_check:
                pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))


    def draw_selected_piece(self):
        """
        Draws a grey square around the currently selected piece and its possible moves.
        The function ensures that the selected piece belongs to the current player and highlights its valid moves.
        """
        if self.selected_piece:
            x, y = self.selected_piece
            # Ensure the selected piece belongs to the current player
            if self.turn[0] == self.chess_board[y][x][0]:
                # Highlight the selected piece
                pygame.draw.rect(screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                # Highlight all possible valid moves of the selected piece
                for mx, my in self.possible_moves:
                    pygame.draw.rect(screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))


    def draw_last_move(self):
        """
        Highlights the squares involved in the last move.
        It draws a special color on the starting and ending positions of the last move.
        """
        if len(self.last_move) > 1:
            x, y = self.last_move[0]
            mx, my = self.last_move[1]
            # Highlight the starting and ending squares of the last move
            pygame.draw.rect(screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))


    def run(self):
        """
        Main game loop. Handles player input, updates the game state, 
        checks for check conditions, and alternates turns.
        """
        self.white_king_position = self.find_king_position('white')
        self.black_king_position = self.find_king_position('black')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left click check
                    x, y = event.pos
                    x_square, y_square = x // square_size, y // square_size
                    
                    # Ensure the clicked position is within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if self.selected_piece and (x_square, y_square) in self.possible_moves:
                            self.all_moves()
                            self.is_king_in_check()
                            self.move_piece(self.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            # Update last move
                            self.last_move = [[self.selected_piece[0], self.selected_piece[1]], [x_square, y_square]]
                            # Check if the move results in a check
                            self.x_king, self.y_king = -1, -1  # Reset king position
                            for i in range(8):
                                for j in range(8):
                                    check_pos = self.check(i, j)
                                    self.x_king, self.y_king = check_pos
                                    if self.x_king != -1:  # If a check is found
                                        break
                                if self.x_king != -1:
                                    break
                            self.change_player()
                            self.selected_piece, self.possible_moves = None, []  # Reset selected piece and possible moves
                        elif self.chess_board[y_square][x_square][0] == self.turn[0]:
                            # Select a piece if it belongs to the current player
                            self.selected_piece = (x_square, y_square)
                            self.castling()
                            self.all_moves()
                            if self.turn == 'white':
                                self.possible_moves = deepcopy(self.white_moves[(x_square, y_square)])
                            else:
                                self.possible_moves = deepcopy(self.black_moves[(x_square, y_square)])
        pygame.display.flip()


    def find_king_position(self, color):
        """
        Returns the position (x, y) of the king of the specified color.
        Searches the chess board for the king piece.
        """
        for x in range(8):
            for y in range(8):
                piece = self.chess_board[y][x]
                if piece == f'{color[0]}K':  # Check for white or black king
                    return (x, y)
        return None


    def show_winner(self):
        """
        Displays the winner of the game in a new screen.
        Reinitializes the Pygame window and waits for user input before closing the game.
        """
        pygame.init()
        # Set up the new screen for displaying the winner
        screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
        pygame.display.set_caption("Winner Announcement")
        screen.fill(white)

        # Render winner text
        font = pygame.font.Font(None, 72)  # Use a larger font for visibility
        winner = "No one" if self.winner is None else self.winner
        winner_text = font.render(f'{winner} won!', True, black)
        text_rect = winner_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(winner_text, text_rect)

        # Update the display
        pygame.display.flip()

        # Wait for any user input to close the window
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Exit the game gracefully
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False  # Close the winner screen on any key or mouse press

        pygame.quit()


    #########################################From here functions will manage logic of the game############################################
    def flip_board(self):
        """Flip the chessboard upside down by reversing its rows."""
        # Create a new list of the chessboard by reversing the rows
        L = [[self.chess_board[i][j] for j in range(8)] for i in range(7, -1, -1)]
        # Update the chessboard with the flipped version
        self.chess_board = deepcopy(L)

    def change_player(self):
        """Switch the current player from white to black or vice versa."""
        if self.turn == 'white':
            self.turn = 'black'  # If current player is white, change to black
        else:
            self.turn = 'white'  # Otherwise, change to white

    def castling(self):
        """Check and update castling availability for both players."""
        if not self.classic: 
            return  # Return if the game is not in classic mode
        
        self.all_moves()  # Update all moves for the current player
        self.change_player()  # Switch to the opponent
        self.all_moves()  # Update all moves for the opponent
        self.change_player()  # Switch back to the original player
        
        # Check if castling is possible for the white king
        if self.white_king_check or self.white_king_moved:
            self.castle[0] = False  # White king cannot castle if in check or moved
            self.castle[1] = False  # White king cannot castle if in check or moved
        
        if not self.white_king_check and not self.white_king_moved:
            if self.rook_moved[0] == 1:
                self.castle[0] = False  # White rook moved, castling is no longer possible
            elif self.rook_moved[0] == 0 and self.chess_board[7][5] == '--' and self.chess_board[7][6] == '--':
                b = False
                for key in self.black_moves:
                    b = (6, 7) in self.black_moves[key] or (5, 7) in self.black_moves[key]
                    if b:
                        break
                self.castle[0] = not b  # If no black pieces threaten castling, allow castling
        
        # Repeat similar logic for black king and rook
        if self.black_king_check or self.black_king_moved:
            self.castle[2] = False
            self.castle[3] = False
        
        if not self.black_king_check and not self.black_king_moved:
            if self.rook_moved[2] == 1:
                self.castle[2] = False
            elif self.rook_moved[2] == 0 and self.chess_board[0][1] == '--' and self.chess_board[0][2] == '--' and self.chess_board[0][3] == '--':
                b = False
                for key in self.white_moves:
                    b = (1, 0) in self.white_moves[key] or (2, 0) in self.white_moves[key] or (3, 0) in self.white_moves[key]
                    if b:
                        break
                self.castle[2] = not b

            if self.rook_moved[3] == 1:
                self.castle[3] = False
            if self.rook_moved[3] == 0 and self.chess_board[0][6] == '--' and self.chess_board[0][5] == '--':
                b = False
                for key in self.white_moves:
                    b = (5, 0) in self.white_moves[key] or (6, 0) in self.white_moves[key]
                    if b:
                        break
                self.castle[3] = not b

    def copy_game(self):
        """Create and return a deep copy of the current game state."""
        new_game = copy.copy(self)  # Shallow copy the ChessGame object itself
        
        # Deep copy the chess board and other mutable attributes
        new_game.chess_board = np.copy(self.chess_board)  # Deep copy of the chess board
        new_game.white_moves = self.white_moves.copy()  # Copy the white player's moves
        new_game.black_moves = self.black_moves.copy()  # Copy the black player's moves
        
        # Copy other necessary mutable attributes
        new_game.white_time = self.white_time
        new_game.black_time = self.black_time
        new_game.turn = self.turn
        new_game.player = np.copy(self.player)
        new_game.last_move = np.copy(self.last_move[:])
        new_game.possible_moves = np.copy(self.possible_moves[:])
        new_game.rook_moved = deepcopy(self.rook_moved)  # Deep copy the rook moved status
        new_game.castle = deepcopy(self.castle)  # Deep copy the castling status
        
        # Return the copied game object
        return new_game

    def is_valid_move(self, start, end):
        """Check if a move from the start position to the end position is valid."""
        x, y = start  # Current position
        mx, my = end  # Target position
        start_piece = self.chess_board[y][x]  # Piece at the start position
        end_piece = self.chess_board[my][mx]  # Piece at the target position
        opponent_color = 'b' if self.turn == 'w' else 'w'  # Determine opponent's color
        
        # Ensure the piece belongs to the current player and the destination is valid
        if start_piece == '--' or end_piece[0] == start_piece[0]:
            return False  # Empty square or same color piece cannot be moved

        piece_type = start_piece[1]  # Type of the piece (e.g., 'P' for pawn, 'R' for rook)
        
        # Logic for different piece types
        # Pawn move rules
        if piece_type == 'P':
            direction = -1 if start_piece[0] == 'w' else 1  # White moves up, black moves down
            if mx == x:  # Moving straight
                if my == y + direction and end_piece == '--':  # Single step
                    return True
                if (y == 1 or y == 6) and my == y + 2 * direction and end_piece == '--' and \
                        self.chess_board[y + direction][x] == '--':  # Double step
                    return True
            elif abs(mx - x) == 1 and my == y + direction:  # Capture move
                if end_piece != '--':
                    return True
                # En passant capture
                last_move = self.last_move
                if len(last_move) > 0 and self.chess_board[last_move[1][1]][last_move[1][0]][1] == 'P' and abs(last_move[1][1] - last_move[0][1]) == 2:
                    if last_move[1][0] == mx and last_move[1][1] + direction == my:
                        self.pion_passant = True
                        return True

        # Rook move rules
        elif piece_type == 'R':
            if x == mx or y == my:  # Horizontal or vertical move
                step_x = 1 if mx > x else -1 if mx < x else 0
                step_y = 1 if my > y else -1 if my < y else 0
                for i in range(1, max(abs(mx - x), abs(my - y))):
                    if self.chess_board[y + i * step_y][x + i * step_x] != '--':  # Check if path is blocked
                        return False
                return True

        # Knight move rules
        elif piece_type == 'N':
            if (abs(mx - x) == 2 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 2):
                return True

        # Bishop move rules
        elif piece_type == 'B':
            if abs(mx - x) == abs(my - y):  # Diagonal move
                step_x = 1 if mx > x else -1
                step_y = 1 if my > y else -1
                for i in range(1, abs(mx - x)):
                    if self.chess_board[y + i * step_y][x + i * step_x] != '--':  # Check if path is blocked
                        return False
                return True

        # King move rules
        elif piece_type == 'K':
            if max(abs(mx - x), abs(my - y)) == 1:  # One square in any direction
                return True
            if start_piece[0] == 'w' and not self.white_king_moved:
                if mx == 6 and my == 7 and self.castle[0]:
                    return True
                if mx == 2 and my == 7 and self.castle[1]:
                    return True
            if start_piece[0] == 'b' and not self.black_king_moved:
                if mx == 2 and my == 0 and self.castle[2]:
                    return True
                if mx == 6 and my == 0 and self.castle[3]:
                    return True

        # Queen move rules
        elif piece_type == 'Q':
            if abs(mx - x) == abs(my - y) or x == mx or y == my:  # Diagonal, horizontal, or vertical move
                step_x = 1 if mx > x else -1 if mx < x else 0
                step_y = 1 if my > y else -1 if my < y else 0
                for i in range(1, max(abs(mx - x), abs(my - y))):
                    if self.chess_board[y + i * step_y][x + i * step_x] != '--':  # Check if path is blocked
                        return False
                return True

        # If no valid move is found, return False
        return False


    def get_possible_moves(self, x, y):
        """Returns moves for the piece at (x, y) that don't put its king in check."""
        return [(mx, my) for mx in range(8) for my in range(8) if self.is_valid_move((x, y), (mx, my))]



    def move_piece(self, start, x, y): 
        """Moves the piece from start to (x, y). Handles en passant captures."""
 
        mx, my = start
        moving_piece = self.chess_board[my][mx]
        direction = -1 if self.turn == 'black' else 1
        if (moving_piece[1]=='K' and abs(mx-x)==2 and self.classic and my==y):
            if (my  == 7 and not self.white_king_moved and not self.white_king_check and not self.white_king_check and self.turn=='white') :
                self.chess_board[y][x]=moving_piece
                self.chess_board[my][mx]='--'
                direction = int((mx-x)/2)
                if(x==6) :
                    self.chess_board[my][7]='--'
                else :
                    self.chess_board[my][0]='--'
                rook = moving_piece[0] + 'R'
                self.chess_board[y][mx-direction]=rook
                self.white_king_moved=True

                return
            if (my==0 and not self.black_king_check and not self.black_king_moved and self.turn=='black' and not self.black_king_check) :
                self.chess_board[y][x]=moving_piece
                self.chess_board[my][mx]='--'
                direction = int((mx-x)/2)
                if(x==6) :
                    self.chess_board[my][7]='--'
                else :
                    self.chess_board[my][0]='--'
                rook = moving_piece[0] + 'R'
                self.chess_board[y][mx-direction]=rook
                self.black_king_moved=True

                return
        if (self.chess_board[my][mx][1]=='K') :
            color = self.chess_board[my][mx][0] 
            if (color=='w') :
                self.white_king_moved=True
            else :
                self.black_king_moved=True
        # Move the piece from start to (x, y)
        
        if (self.chess_board[my][mx][1]=='R') :
            if (mx==7 and my==7) :
                self.rook_moved[0] = 1
            if (mx==0 and my==7) :
                self.rook_moved[1]== 1
            if (mx == 0 and my == 0) :
                self.rook_moved[2] = 1
            if (mx==7 and my == 0 ) :
                self.rook_moved[3] = 1
        self.chess_board[y][x], self.chess_board[my][mx] = moving_piece, '--'
        if ((y==0 or y==7) and  self.chess_board[y][x][1]=='P') :
            self.chess_board[y][x] = self.chess_board[y][x][0] + 'Q'
            
                    
            
        # Handle en passant capture
        if (self.pion_passant) :
            # Clear the square of the pawn captured via en passant
            self.chess_board[y+direction][x] = '--'
            # Reset en passant if no double-step pawn move occurred
        self.pion_passant = False

    def back_move_piece(self, start, final, piece): 
        """Reverts a move to restore board state."""
        mx, my = start
        x, y = final 
        self.chess_board[my][mx] = self.chess_board[y][x]
        self.chess_board[y][x] = piece
    def is_king_in_check(self):
        """Checks if the player's king is in check."""
        color=self.turn[0]
        king_position = self.get_king_position()
        if not king_position:
            # King not found, possibly captured
            self.running=False
            self.winner = 'black' if color=='w' else 'white'
            
            return True

        x_king, y_king = king_position
        opponent_color = 'b' if color == 'w' else 'w'
        # Check if any opponent piece can capture the king's position
        for y in range(8):
            for x in range(8):
                piece = self.chess_board[y][x]
                if piece[0] == opponent_color :
                    
                    if self.is_valid_move((x, y), (x_king, y_king)):
                        
                        return True

        return False

    def simulate_move_and_check(self, start, end):
        """Simulates a move and checks if it puts the player's king in check."""
        copy_game = self.copy_game()
        piece = self.chess_board[start[1]][start[0]]
        target_piece = self.chess_board[end[1]][end[0]]
        
        # Make the move temporarily
        copy_game.chess_board[end[1]][end[0]] = piece
        copy_game.chess_board[start[1]][start[0]] = "--"
        # Check if the king is in check after the move
        in_check = copy_game.is_king_in_check()

        # Undo the move
        copy_game.chess_board[start[1]][start[0]] = piece
        copy_game.chess_board[end[1]][end[0]] = target_piece

        return  not in_check

    def get_valid_moves(self, x_square, y_square):
        """Returns a list of valid moves that do not put the player's own king in check."""
        self.possible_moves = self.get_possible_moves(x_square, y_square)
        valid_moves = [move for move in self.possible_moves if self.simulate_move_and_check((x_square, y_square), move)]
        return valid_moves

    
    def get_king_position(self):
        """Finds and returns the position of the king of the given color."""
        color = self.turn[0]
        king = color + 'K'
        for y in range(8):
            for x in range(8):
                if self.chess_board[y][x] == king:
                    return (x, y)
        return None
    
    def check(self, x_square, y_square):
        """Checks if the move puts the opponent's king in check."""
        if (self.chess_board[y_square][x_square]=='--') :
            return (-1,-1)
        moves = self.get_valid_moves(x_square, y_square)
        color = 'b' if self.turn[0] == 'w' else 'w'
        king = color + 'K'

        for move in moves:
            if self.chess_board[move[1]][move[0]] == king:
                

                return move  # Returns the position of the king in check

        return (-1, -1)
    def all_moves(self):
        """
        Calculates and stores all valid moves for the current player (white or black) for all their pieces.

        This method updates the list of valid moves for white and black pieces separately, depending on whose turn it is.
        It checks each square on the board, and if the square contains a piece belonging to the current player, 
        it calculates and stores its valid moves.

        For white's turn, it updates the `white_moves` dictionary, and for black's turn, it updates the `black_moves` dictionary.
        The valid moves are stored in a dictionary where the keys are the coordinates of the pieces (x, y), 
        and the values are lists of valid moves for those pieces.

        Side effects:
            - Modifies the `white_moves` or `black_moves` attributes based on the current turn.
        """
        copy_game = self.copy_game()
        
        if self.turn == 'white':
            # Clear previous white moves and calculate valid moves for white pieces
            self.white_moves.clear()
            copy_game.white_moves.clear()
            for y in range(8):
                for x in range(8):
                    if copy_game.chess_board[y][x][0] == 'w':  # Check if the piece belongs to white
                        self.white_moves[(x, y)] = copy_game.get_valid_moves(x, y)

        if self.turn == 'black':
            # Clear previous black moves and calculate valid moves for black pieces
            self.black_moves.clear()
            copy_game.black_moves.clear()
            for y in range(8):
                for x in range(8):
                    if self.chess_board[y][x][0] == 'b':  # Check if the piece belongs to black
                        self.black_moves[(x, y)] = copy_game.get_valid_moves(x, y)


    def update_list_of_boards(self):
        """
        Updates the history of board states, storing deep copies of the current board state.

        This method ensures that the list of boards (`list_of_boards`) contains independent deep copies of the chessboard
        to maintain a history of all game states. The method also stores additional game-related information such as:
        - The remaining time for each player
        - The last move made
        - Castling rights
        - Rook movements
        - King check and king move status
        - En passant status

        If the current board state is different from the last state in `list_of_boards`, the method adds the current state 
        and the associated game data to the history.

        Side effects:
            - Updates the `list_of_boards`, `list_of_times`, `list_of_last_moves`, `list_of_castles`, 
            `list_of_rooks`, `list_of_king_check`, `list_of_king_moves`, and `list_of_passant`.
            - Increases `len_list_of_boards` by 1 to reflect the addition of a new game state.
        """
        l = self.len_list_of_boards

        # Ensure the list_of_boards contains independent deep copies of the board (3D list)
        if not np.array_equal(self.list_of_boards[l - 1], self.chess_board):
            self.list_of_boards[l] = deepcopy(self.chess_board)  # Deep copy the current board
            self.list_of_times[l] = [self.white_time, self.black_time]  # Store the current times for both players
            self.list_of_last_moves[l] = deepcopy(self.last_move)  # Store the last move made
            self.list_of_castles[l] = deepcopy(self.castle)  # Store the castling rights
            self.list_of_rooks[l] = deepcopy(self.rook_moved)  # Store the rook movement status
            self.list_of_king_check[l] = [self.white_king_check, self.black_king_check]  # Store the king check status
            self.list_of_king_moves[l] = [self.white_king_moved, self.black_king_moved]  # Store the king move status
            self.list_of_passant[l] = self.pion_passant  # Store the en passant status
            self.len_list_of_boards += 1  # Increment the board history counter
