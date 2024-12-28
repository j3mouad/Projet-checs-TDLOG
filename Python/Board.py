import pygame
from copy import deepcopy
import time
from random import shuffle
import os
from chess import ChessGame
from utils import *
import sys
from AI import AI
# Set the new directory and change the working directory
new_dir = ('/home/hassene/Desktop/Projet-echecs-TDLOG/Python')
os.chdir(new_dir)

# Initialize Pygame
pygame.init()

# Load sound effects
click_sound_add_time_button = pygame.mixer.Sound("chess_add_time_sound.wav")
click_sound_chess = pygame.mixer.Sound("chess_move_soundf.mp3")

# Initial screen width and height

# Create a resizable window
screen = pygame.display.set_mode((screen_width + added_screen_width, screen_height))
pygame.display.set_caption("Chess")


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

class Board:
    def __init__(self, game):
        self.screen = screen
        self.game = game
        self.cooldown = 0.5
        self.number_of_time_same_piece_clicked = 0
        self.last_click_time = 0

    def draw_board(self):
        """
        Draws the chessboard on the screen.

        The chessboard is an 8x8 grid where each square is drawn as a rectangle.
        The color of each square alternates between light brown and brown, following 
        the standard pattern for a chessboard. The squares are drawn using the 
        `pygame.draw.rect` function.

        This method does not return any value.
        """
        square_size = min(screen.get_width(), screen.get_height()) // 8  # Dynamically adjust square size based on window size
        for row in range(8):
            for col in range(8):
                color = light_brown if (row + col) % 2 == 0 else brown
                pygame.draw.rect(self.screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

    def draw_move(self):
        """
        Animates the movement of a chess piece on the board.
        """
        if (self.game.last_move and self.game.last_move != self.game.last_move_draw):
            self.game.last_move_draw = self.game.last_move
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            dx = (mx - x) / 40
            dy = (my - y) / 40
            piece = self.game.chess_board[my][mx]
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
        """
        square_size = min(screen.get_width(), screen.get_height()) // 8  # Dynamically adjust square size based on window size
        font = pygame.font.Font(None, 12)
        for row in range(8):
            for col in range(8):
                text = font.render(self.game.chess_board_squares[col][row], True, (0, 0, 255)) 
                screen.blit(text, (row * square_size, col * square_size))
                piece = self.game.chess_board[row][col]
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
                if current_time - self.last_click_time >= self.cooldown:
                    
                    click_sound_add_time_button.play()
                    if self.game.turn == 'white':
                        self.game.black_time += 5
                    else:
                        self.game.white_time += 5
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
        white_timer_surface = font.render(f'White: {self.game.white_time // 60}:{self.game.white_time % 60:02}', True, black)
        black_timer_surface = font.render(f'Black: {self.game.black_time // 60}:{self.game.black_time % 60:02}', True, black)
        if self.game.white_time <= 5:
            white_timer_surface = font.render(f'White: {self.game.white_time // 60}:{self.game.white_time % 60:02}', True, red)
        if self.game.black_time <= 5:
            black_timer_surface = font.render(f'Black: {self.game.black_time // 60}:{self.game.black_time % 60:02}', True, red)

        if self.game.player == 'white':
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(white_timer_surface, (screen_width + 20, 450))
            self.screen.blit(black_timer_surface, (screen_width + 20, 50))
        if self.game.player == 'black':
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(black_timer_surface, (screen_width + 20, 450))
            self.screen.blit(white_timer_surface, (screen_width + 20, 50))
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
        if (time - self.game.last_time_back_clicked) <= self.cooldown:
            return
        if self.game.len_list_of_boards == 0:
            return
        self.game.last_time_back_clicked = time
        self.game.len_list_of_boards -= 1
        l = self.game.len_list_of_boards
        self.game.white_time, self.game.black_time = self.game.list_of_times[l - 1]
        self.game.chess_board = deepcopy(self.game.list_of_boards[l - 1])
        self.game.last_move = self.game.list_of_last_moves[l - 1]
        self.game.castle = deepcopy(self.game.list_of_castles[l - 1])
        self.game.rook_moved = deepcopy(self.game.list_of_rooks[l - 1])
        self.game.white_king_check, self.game.black_king_check = self.game.list_of_king_check[l - 1]
        self.game.white_king_moved, self.game.black_king_moved = self.game.list_of_king_moves[l - 1]
        self.game.pion_passant = self.game.list_of_passant[l - 1]
        self.game.selected_piece = []
        self.draw_board()
        self.draw_pieces()
        self.game.turn = 'black' if self.game.turn == 'white' else 'white'
        pygame.display.flip()
        pygame.time.delay(100)

    def update_timers(self):
        current_time = pygame.time.get_ticks()

        elapsed_time = (current_time - self.game.last_time_update) // 1000
        if elapsed_time > 0:
            if self.game.turn == 'white':
                    self.game.white_time -= elapsed_time
                    self.game.last_time_update = current_time

            else:
                self.game.black_time -= elapsed_time
                self.game.last_time_update = current_time
    def draw_king_in_check(self):
        """
        Draws a red square around the current player's king if it is in check.
        The function checks if the king is threatened by any opponent's piece.
        """
        if (self.game.turn == 'white'):
            self.game.white_king_position = self.game.find_king_position('white')
            x_king, y_king = self.game.white_king_position
            b = False
            # Check if the white king is in check by any black piece
            for key in self.game.black_moves:
                if (x_king, y_king) in self.game.black_moves[key]:
                    b = True
                    break
            self.white_king_check = b
            # If white king is in check, draw a red square around its position
            if self.game.white_king_check:
                pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))
        else:
            self.game.black_king_position = self.game.find_king_position('black')
            x_king, y_king = self.game.black_king_position
            b = False
            # Check if the black king is in check by any white piece
            for key in self.game.white_moves:
                if (x_king, y_king) in self.game.white_moves[key]:
                    b = True
                    break
            self.game.black_king_check = b
            # If black king is in check, draw a red square around its position
            if self.game.black_king_check:
                pygame.draw.rect(screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))

    def draw_last_move(self):
        """
        Highlights the squares involved in the last move.
        It draws a special color on the starting and ending positions of the last move.
        """
        if len(self.game.last_move) > 1:
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            # Highlight the starting and ending squares of the last move
            pygame.draw.rect(screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def draw_selected_piece(self):
        """
        Draws a grey square around the currently selected piece and its possible moves.
        The function ensures that the selected piece belongs to the current player and highlights its valid moves.
        """
        if self.game.selected_piece:
            x, y = self.game.selected_piece
            # Ensure the selected piece belongs to the current player
            if self.game.turn[0] == self.game.chess_board[y][x][0]:
                # Highlight the selected piece
                pygame.draw.rect(screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                # Highlight all possible valid moves of the selected piece
                for mx, my in self.game.possible_moves:
                    pygame.draw.rect(screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def draw_last_move(self):
        """
        Highlights the squares involved in the last move.
        It draws a special color on the starting and ending positions of the last move.
        """
        if len(self.game.last_move) > 1:
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            # Highlight the starting and ending squares of the last move
            pygame.draw.rect(screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def run(self):
        """
        Main game loop. Handles player input, updates the game state, 
        checks for check conditions, and alternates turns.
        """
        self.game.white_king_position = self.game.find_king_position('white')
        self.game.black_king_position = self.game.find_king_position('black')
        
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left click check
                    x, y = event.pos
                    x_square, y_square = x // square_size, y // square_size
                    if (self.game.turn=='black') :
                        start,end = AI(self.game,4)
                        self.game.move_piece(start,end[0],end[1])
                        self.game.last_move = [start,end]
                        self.draw_last_move()
                        self.game.change_player()

                    # Ensure the clicked position is within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if self.game.selected_piece and (x_square, y_square) in self.game.possible_moves:
                            self.game.all_moves()
                            self.game.is_king_in_check()
                            self.game.move_piece(self.game.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            # Update last move
                            self.game.last_move = [[self.game.selected_piece[0], self.game.selected_piece[1]], [x_square, y_square]]
                            # Check if the move results in a check
                            self.x_king, self.y_king = -1, -1  # Reset king position
                            for i in range(8):
                                for j in range(8):
                                    check_pos = self.game.check(i, j)
                                    self.x_king, self.y_king = check_pos
                                    if self.x_king != -1:  # If a check is found
                                        break
                                if self.x_king != -1:
                                    break
                            self.game.change_player()
                            self.game.selected_piece, self.game.possible_moves = None, []  # Reset selected piece and possible moves
                        elif self.game.chess_board[y_square][x_square][0] == self.game.turn[0]:

                            # Select a piece if it belongs to the current player
                            self.game.selected_piece = (x_square, y_square)
                            self.game.castling()
                            self.game.all_moves()
                            if self.game.turn == 'white':
                                self.game.possible_moves = deepcopy(self.game.white_moves[(x_square, y_square)])
                            else:
                                self.game.possible_moves = deepcopy(self.game.black_moves[(x_square, y_square)])
        pygame.display.flip()
       

