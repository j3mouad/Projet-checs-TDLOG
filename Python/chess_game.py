import pygame
from copy import deepcopy
from random import shuffle
import chess
import chess.engine
from utils import *
import numpy as np
import copy
import os
from config import *
from promotion import Promotion_screen

new_dir = ('/home/hassene/Desktop/Projet-echecs-TDLOG/Python')
os.chdir(new_dir)
pygame.init()



class ChessGame:
    def __init__(self,screen):
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
        self.player= False
        self.white = False
        self.black = False
        self.last_move=[]
        self.last_move_draw = []
        self.possible_moves=[]
        self.winner = None
        self.white_time = -1  
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
        self.hard = False
        self.flipped = False
        self.white_king_position = None
        self.black_king_position = None
        self.rook_pos = [7,0,0,7]
        self.king_of_the_hill = False
    ##########################################First functions manage graphcis#############################################
    def time_reg(self,white_time,black_time):
        self.white_time=white_time
        self.black_time=black_time
    #########################################From here functions will manage logic of the game############################################

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

        self.all_moves()  # Update all moves for the current player
        self.change_player()  # Switch to the opponent
        self.all_moves()  # Update all moves for the opponent
        self.change_player()  # Switch back to the original player

            # Standard chess castling logic
        if self.white_king_check or self.white_king_moved:
                self.castle[0] = False  # White king-side castling not possible
                self.castle[1] = False  # White queen-side castling not possible
            
        if not self.white_king_check and not self.white_king_moved:
                # White king-side castling
                if self.rook_moved[0]:
                    self.castle[0] = False
                elif self.chess_board[7][5] == '--' and self.chess_board[7][6] == '--':
                    if not any((6, 7) in self.black_moves[key] or (5, 7) in self.black_moves[key] for key in self.black_moves):
                        self.castle[0] = True
                # White queen-side castling
                if self.rook_moved[1]:
                    self.castle[1] = False
                elif self.chess_board[7][1] == '--' and self.chess_board[7][2] == '--' and self.chess_board[7][3] == '--':
                    if not any((2, 7) in self.black_moves[key] or (3, 7) in self.black_moves[key] for key in self.black_moves):
                        self.castle[1] = True

            # Black king-side and queen-side castling (similar logic)
        if self.black_king_check or self.black_king_moved:
                self.castle[2] = False
                self.castle[3] = False
            
        if not self.black_king_check and not self.black_king_moved:
                if self.rook_moved[2]:
                    self.castle[2] = False
                elif self.chess_board[0][5] == '--' and self.chess_board[0][6] == '--':
                    if not any((5, 0) in self.white_moves[key] or (6, 0) in self.white_moves[key] for key in self.white_moves):
                        self.castle[2] = True

                if self.rook_moved[3]:
                    self.castle[3] = False
                elif self.chess_board[0][1] == '--' and self.chess_board[0][2] == '--' and self.chess_board[0][3] == '--':
                    if not any((1, 0) in self.white_moves[key] or (2, 0) in self.white_moves[key] or (3, 0) in self.white_moves[key] for key in self.white_moves):
                        self.castle[3] = True
        print(self.castle)
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
        # Ensure the piece belongs to the current player and the destination is valid
        if start_piece == '--' or end_piece[0] == start_piece[0]:
            return False  # Empty square or same color piece cannot be moved
        piece_type = start_piece[1]  # Type of the piece (e.g., 'P' for pawn, 'R' for rook)
        # Logic for different piece types
        # Pawn move rules
        if piece_type == 'P':
            direction = -1 if start_piece[0] == 'w' else 1  # White moves up, black moves down
            coef = -1 if self.flipped else 1
            direction *=coef
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
                if len(last_move)  and self.chess_board[last_move[1][1]][last_move[1][0]][1] == 'P' and abs(last_move[1][1] - last_move[0][1]) == 2:
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
        # Wazir move rules
        elif piece_type == 'W':
            if abs(mx - x) <= 1 and abs(my - y) <= 1:
                return True
        # Ferz move rules
        elif piece_type == 'F':
            if abs(mx-x) == 1 and abs(my-y) == 1:
                return True           
        elif piece_type == 'M' :
            from random import randint
            r = randint(1,10)
            if (r<=5) :
                if abs(mx - x) == abs(my - y) or x == mx or y == my:  # Diagonal, horizontal, or vertical move
                    step_x = 1 if mx > x else -1 if mx < x else 0
                    step_y = 1 if my > y else -1 if my < y else 0
                    for i in range(1, max(abs(mx - x), abs(my - y))):
                        if self.chess_board[y + i * step_y][x + i * step_x] != '--':  # Check if path is blocked
                            return False
                    return True
            else :
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
        #Camel move rules
        elif piece_type == 'C' :
            if (abs(mx - x) == 3 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 3) :
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
            
            if start_piece[0] == 'b' :
                if mx == 2 and my == 0 and self.castle[3]:
                    return True
                if mx == 6 and my == 0 and self.castle[2]:
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

    def find_rook_positions(self):
        """Find the positions of the rooks for both players."""
        rooks = []
        
        # Loop through the board to find rook positions
        for x in range(8):
            if self.chess_board[7][x] == 'wR':  # White rooks on the 8th row (index 7)
                rooks.append(x)
            
        return rooks
    def move_piece(self, start, x, y): 
        """Moves the piece from start to (x, y). Handles en passant captures."""
        mx, my = start
        moving_piece = self.chess_board[my][mx]
        direction = -1 if self.turn == 'black' else 1
        if ( moving_piece[1]=='K' and abs(mx-x)>=2 and my==y):
            if (my  == 7 and not self.white_king_moved and not self.white_king_check and self.turn=='white') :
                self.chess_board[y][x]=moving_piece
                self.chess_board[my][mx]='--'
                direction = int((mx-x)/2)
                if(x==6) :
                    self.chess_board[my][self.rook_pos[0]]='--'
                else :
                    self.chess_board[my][self.rook_pos[1]]='--'
                rook = moving_piece[0] + 'R'
                self.chess_board[y][x+direction]=rook
                self.white_king_moved=True

                return
            if (my==0 and not self.black_king_check and not self.black_king_moved and self.turn=='black' ) :
                self.chess_board[y][x]=moving_piece
                self.chess_board[my][mx]='--'
                direction = int((mx-x)/2)
                if(x==6) :
                    self.chess_board[my][self.rook_pos[0]]='--'
                else :
                    self.chess_board[my][self.rook_pos[1]]='--'
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
            

        
        if (self.chess_board[my][mx][1]=='P' and abs(mx-x)==1 and self.pion_passant ) :
            self.chess_board[y+direction][x] = '--'
        self.pion_passant = False
        if (self.chess_board[my][mx][1]=='P' and abs(my-y)==2) :
            self.pion_passant = True
        self.chess_board[y][x], self.chess_board[my][mx] = moving_piece, '--'
        
        if ((y==0 or y==7) and  self.chess_board[y][x][1]=='P') :
            color = self.turn
            piece = Promotion_screen(color)[0]
            if (piece=='K') :
                piece = 'N'

            self.chess_board[y][x] = self.chess_board[y][x][0] + piece
            
                    
            
        
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
    def game_ends(self):

        if self.white_time <= 0:
            self.running = False
            pygame.time.delay(1000)
            return -1  # Black wins
        if self.black_time <= 0:
            self.running = False
            pygame.time.delay(1000)
            return 1  # White wins

        if self.is_king_in_check():
            current_moves = self.white_moves if self.turn == 'white' else self.black_moves
            if not has_non_empty_list(current_moves):
                pygame.time.delay(1000)
                return -1 if self.turn == 'white' else 1  # Checkmate
        
        current_moves = self.white_moves if self.turn == 'white' else self.black_moves
        if not has_non_empty_list(current_moves):
            pygame.time.delay(1000)
            return 0  # Stalemate
        if (self.king_of_the_hill) :
            x_w,y_w = self.find_king_position('w')
            x_b,y_b = self.find_king_position('b')
            if (x_w in [3,4] and y_w in [3,4] and self.turn == 'black') :
                return 1
            if (x_b in [3,4] and y_b in [3,4] and self.turn == 'white'):
                return -1
        return None  # Game continues



    def convert_to_chess_board(self):
        board = chess.Board()
        board.clear()
        for row in range(8):
            for col in range(8):
                piece = self.chess_board[row][col]
                if piece != '--':
                    color = chess.WHITE if piece[0] == 'w' else chess.BLACK
                    piece_type = chess.Piece.from_symbol(piece[1].upper()).piece_type
                    square = chess.square(col, 7 - row)
                    board.set_piece_at(square, chess.Piece(piece_type, color))
        return board

    def evaluate0(self):
            # Use a chess engine to evaluate the position
            stockfish_path = "/usr/games/stockfish"  # Replace with the correct path
            with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
                board = self.convert_to_chess_board()
                try:
                    result = engine.analyse(board, chess.engine.Limit( depth=10))
                except chess.engine.EngineTerminatedError as e:
                    print(f"Engine crashed: {e}")
                    return 1e5  # Or handle it differently

                score = result["score"]
                
                # Convert PovScore to a float (positive for white, negative for black)
                return score.white().score(mate_score=1e6) if score.is_mate() else score.white().score()