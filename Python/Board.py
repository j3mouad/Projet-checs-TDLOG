import pygame
from copy import deepcopy
import time
from random import shuffle
import os
from utils import *
from Button import Button,squares
from AI import AI,AI_hard
# Set the new directory and change the working directory
new_dir = ('/home/hassene/Desktop/Projet-echecs-TDLOG/Python')
os.chdir(new_dir)
from config import *
# Initialize Pygame
pygame.init()
from numba import njit

def find_king_position(chess_board, color):
    """
    Returns the position (x, y) of the king of the specified color.
    Searches the chess board for the king piece.
    """
    for x in range(8):
        for y in range(8):
            piece = chess_board[y][x]
            if piece == f'{color[0]}K':  # Check for white or black king
                return (x, y)
    return None

class Board:

    def __init__(self, game,screen):


        # Initial screen width and height

        # Create a resizable window
        self.screen = screen
        pygame.display.set_caption("Chess")
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
        for row in range(8):
            for col in range(8):
                squares[col][row].draw(self.screen)

    def draw_move(self):
        """
        Animates the movement of a chess piece on the board.
        """
        if (self.game.last_move and self.game.last_move != self.game.last_move_draw):
            self.game.last_move_draw = self.game.last_move
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            dx = (mx - x) / 20
            dy = (my - y) / 20
            piece = self.game.chess_board[my][mx]
            if (piece != '--'):
                resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                for i in range(1,21):
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
        font = pygame.font.Font(None, 12)
        for row in range(8):
            for col in range(8):
                text = font.render(self.game.chess_board_squares[col][row], True, (0, 0, 255)) 
                self.screen.blit(text, (row * square_size, col * square_size))
                piece = self.game.chess_board[row][col]
                if piece != '--':
                    if (mx == col and my == row):
                        continue 
                    resized_piece = pygame.transform.scale(pieces_images[piece], (square_size, square_size))
                    self.screen.blit(resized_piece, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
    def draw_add_time_button(self):
        """
        Draws the 'Add Time' button on the screen using the Button class.

        This method uses the Button class to create and manage a button 
        that allows the user to add 5 seconds to the opponent's timer.

        Returns:
            None
        """
        # Create the button instance
        self.add_time_button = Button(
            text="+ 5 seconds",
            x=screen_width + 20,
            y=200,
            width=250,
            height=80,
            color=grey

        )
        self.add_time_button.draw(self.screen)

        

    def handle_add_time_button(self,event):
        # Draw the button
        current_time = time.time()
        if self.add_time_button.is_clicked(event) and current_time - self.last_click_time >= self.cooldown:
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

        if self.game.turn == 'white':
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(white_timer_surface, (screen_width + 20, 450))
            self.screen.blit(black_timer_surface, (screen_width + 20, 50))
        if self.game.turn == 'black':
            pygame.draw.rect(self.screen, white, (screen_width, 0, added_screen_width, screen_height))
            self.screen.blit(black_timer_surface, (screen_width + 20, 450))
            self.screen.blit(white_timer_surface, (screen_width + 20, 50))
    def draw_move_back_button(self):
        """
        Draws the 'Back' button on the screen using the Button class.

        This method uses the Button class to create and manage a button 
        that allows the player to undo the last move.

        Returns:
            None
        """
        # Create the button instance
        self.back_button = Button(
            text="Back",
            x=screen_width + 150,
            y=300,
            width=60,
            height=50,
        )

        # Draw the button
        self.back_button.draw(self.screen)

        # Handle button click
       

    def handle_back_button_click(self, event):
        """
        Handles the logic when the 'Back' button is clicked.

        This method restores the game state to the previous one if available, adhering to a cooldown
        to prevent rapid triggers. It also redraws the game UI to reflect the restored state.

        Returns:
            None
        """
        # Enforce cooldown to prevent rapid triggers

        current_time = pygame.time.get_ticks()
        if (current_time - self.game.last_time_back_clicked) <= self.cooldown:
            return

        # Check if a previous state is available
        if self.game.len_list_of_boards == 0:
            return

        # Update cooldown tracker
        if (self.back_button.is_clicked(event)) :
            self.game.last_time_back_clicked = current_time

            # Revert to the previous state
            self.game.len_list_of_boards -= 1
            previous_index = self.game.len_list_of_boards

            # Restore game attributes
            self.game.white_time, self.game.black_time = self.game.list_of_times[previous_index - 1]
            self.game.chess_board = deepcopy(self.game.list_of_boards[previous_index - 1])
            self.game.last_move = self.game.list_of_last_moves[previous_index - 1]
            self.game.castle = deepcopy(self.game.list_of_castles[previous_index - 1])
            self.game.rook_moved = deepcopy(self.game.list_of_rooks[previous_index - 1])
            self.game.white_king_check, self.game.black_king_check = self.game.list_of_king_check[previous_index - 1]
            self.game.white_king_moved, self.game.black_king_moved = self.game.list_of_king_moves[previous_index - 1]
            self.game.pion_passant = self.game.list_of_passant[previous_index - 1]
            self.game.selected_piece = []

            # Redraw game board and pieces
            self.draw_board()
            self.draw_pieces()

            # Toggle the turn
            self.game.turn = 'black' if self.game.turn == 'white' else 'white'

            # Update the display
            pygame.display.flip()

            # Add a short delay for smooth transition
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
            self.game.white_king_position = find_king_position(self.game.chess_board,'white')
            x_king, y_king = self.game.white_king_position
            b = False
            # Check if the white king is in check by any black piece
            for key in self.game.black_moves:
                if (x_king, y_king) in self.game.black_moves[key]:
                    b = True
                    break
            self.game.white_king_check = b
            # If white king is in check, draw a red square around its position
            if self.game.white_king_check:
                pygame.draw.rect(self.screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))
        else:
            self.game.black_king_position = find_king_position(self.game.chess_board,'black')
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
                pygame.draw.rect(self.screen, red, pygame.Rect(x_king * square_size, y_king * square_size, square_size, square_size))

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
                pygame.draw.rect(self.screen, grey, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
                # Highlight all possible valid moves of the selected piece
                for mx, my in self.game.possible_moves:
                    pygame.draw.rect(self.screen, grey, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def draw_last_move(self):
        """
        Highlights the squares involved in the last move.
        It draws a special color on the starting and ending positions of the last move.
        """
        if len(self.game.last_move) > 1:
            x, y = self.game.last_move[0]
            mx, my = self.game.last_move[1]
            # Highlight the starting and ending squares of the last move
            pygame.draw.rect(self.screen, highlight_color, pygame.Rect(x * square_size, y * square_size, square_size, square_size))
            pygame.draw.rect(self.screen, highlight_color, pygame.Rect(mx * square_size, my * square_size, square_size, square_size))
    def update_moves(self) :
        self.game.all_moves()
        self.game.change_player()
        self.game.all_moves()
        self.game.change_player()
    def run(self):
        """
        Main game loop. Handles player input, updates the game state, 
        checks for check conditions, and alternates turns.
        """
        self.game.white_king_position = find_king_position(self.game.chess_board,'white')
        self.game.black_king_position = find_king_position(self.game.chess_board,'black')
        
        for event in pygame.event.get():
            self.handle_add_time_button(event)
            self.handle_back_button_click( event)
            if (self.game.player) :
                
                if (self.game.white and self.game.turn == 'black') :
                            self.game.all_moves()
                            if (self.game.hard) :
                                start,end = AI_hard(self.game)
                            else :
                                start,end = AI(self.game)
                            x,y = start 
                            mx,my = end 
                            self.game.move_piece(start,end[0],end[1])
                            self.game.last_move = [start,end]
                            self.draw_last_move()
                            self.update_timers()
                            self.game.change_player()
                            self.game.all_moves()
                if (self.game.black and self.game.turn=='white') :
                            self.game.all_moves()
                            if (self.game.hard) :
                                start,end = AI_hard(self.game)
                            else :
                                start,end = AI(self.game)
                            x,y = start 
                            mx,my = end 
                            self.game.move_piece(start,mx,my)
                            self.game.last_move = [start,end]
                            self.draw_last_move()
                            self.update_timers()
                            self.game.change_player()
                            self.game.all_moves()

            if event.type == pygame.QUIT:
                self.game.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left click check
                    x, y = event.pos
                    x_square, y_square = x // square_size, y // square_size
                    
                    # Ensure the clicked position is within board bounds
                    if 0 <= x_square < 8 and 0 <= y_square < 8:
                        if (x_square,y_square) == (self.game.selected_piece) :
                            continue
                        if (self.game.selected_piece and (x_square,y_square) not in self.game.possible_moves) :
                            self.game.selected_piece = None
                            self.game.possible_moves = []
                        if self.game.selected_piece and (x_square, y_square) in self.game.possible_moves:
                            self.game.all_moves()
                            self.game.is_king_in_check()
                            self.game.move_piece(self.game.selected_piece, x_square, y_square)
                            click_sound_chess.play()
                            # Update last move
                            self.game.last_move = [[self.game.selected_piece[0], self.game.selected_piece[1]], [x_square, y_square]]
                            # Check if the move results in a check
                            self.game.update_list_of_boards()

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

        self.game.all_moves()
        self.game.change_player()
        self.game.all_moves()
        self.game.change_player()
        pygame.display.flip()
       