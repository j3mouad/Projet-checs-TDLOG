import pygame
from copy import deepcopy
import chess
import chess.engine
from utils import *
import numpy as np
import copy
from config import *
from random import randint
from promotion import Promotion_screen
from piece import PieceType

pygame.init()


class ChessGame:
    def __init__(self,screen):
        
        """Represents a chess game, managing the board state, player turns, time tracking, and game logic.

        Attributes:
        screen (pygame.Surface): The screen to render the game.
        chess_board (np.array): A 2D array representing the chess board with pieces.
        chess_board_squares (np.array): A 2D array of square labels for the chess board.
        list_of_boards (list): A list of previous board states.
        list_of_times (list): A list of the elapsed time for both players.
        list_of_last_moves (list): A list of the last moves made for each turn.
        list_of_king_check (list): A list of king check states for both players.
        list_of_rooks (list): A list representing rook movement history.
        list_of_castles (list): A list representing castle movement history.
        list_of_king_moves (list): A list representing king movement history.
        list_of_passant (list): A list indicating if en passant is available.
        turn (str): The current player's turn ('white' or 'black').
        player (bool): The player's identity (True for white, False for black).
        winner (str or None): The winner of the game ('white' or 'black'), or None if the game is ongoing.
        white_time (int): The remaining time for the white player.
        black_time (int): The remaining time for the black player.
        running (bool): A flag indicating if the game is still running.
        classic (bool): A flag indicating if the game follows classic chess rules.
        selected_piece (list): The coordinates of the selected piece.
        pion_passant (bool): A flag indicating if en passant is active.
        x_king, y_king (int): The coordinates of the kings on the board.
        white_moves (dict): A dictionary storing possible moves for the white player.
        black_moves (dict): A dictionary storing possible moves for the black player.
        rook_moved (list): A list indicating whether the rooks have moved.
        castle (list): A list indicating whether castling is possible for each side.
        hard (bool): A flag indicating if the game difficulty is set to hard.
        flipped (bool): A flag indicating if the board is flipped.
        white_king_position, black_king_position (tuple): The positions of the white and black kings.
        rook_pos (list): The positions of the rooks.
        king_of_the_hill (bool): A flag indicating if the King of the Hill rule is active."""
    
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
        
        self.list_of_boards=[self.chess_board for _ in range(5000)]
        self.len_list_of_boards=0 
        self.list_of_times=[[0,0] for _ in range(5000)]
        self.list_of_last_moves = [[(0,0),(0,0)] for _ in range(5000)]
        self.list_of_king_check  = [(False,False) for _ in range(5000)]
        self.list_of_rooks = [[0,0,0,0] for _ in range(5000)]
        self.list_of_castles = [[0,0,0,0] for _ in range(5000)]
        self.list_of_king_moves = [(False,False) for _ in range(5000)]
        self.list_of_passant = [False for _ in range(5000)]
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
    def time_reg(self,white_time,black_time):
        self.white_time=white_time
        self.black_time=black_time

    def flip_board(self):
        """
        Flip the chessboard upside down by reversing its rows.

        This method creates a new list representing the chessboard with its rows
        reversed, effectively flipping the board upside down. The original 
        chessboard is then updated with this flipped version.

        Returns:
            None
        """
        # Create a new list of the chessboard by reversing the rows
        L = [[self.chess_board[i][j] for j in range(8)] for i in range(7, -1, -1)]
        # Update the chessboard with the flipped version
        self.chess_board = deepcopy(L)

    def change_player(self):
        """
        Switch the current player from white to black or vice versa.

        This method toggles the `turn` attribute between 'white' and 'black'.
        If the current player is 'white', it changes to 'black', and if the 
        current player is 'black', it changes to 'white'.
        """
        if self.turn == 'white':
            self.turn = 'black'  # If current player is white, change to black
        else:
            self.turn = 'white'  # Otherwise, change to white
    def castling(self):
        """
        Check and update castling availability for both players.
        This method updates the castling rights for both white and black players based on the current state of the game.
        It considers whether the kings or rooks have moved, whether the kings are in check, and whether the squares between
        the kings and rooks are unoccupied and not under attack.
        Castling rights are stored in the `self.castle` list:
        - `self.castle[0]`: White king-side castling availability
        - `self.castle[1]`: White queen-side castling availability
        - `self.castle[2]`: Black queen-side castling availability
        - `self.castle[3]`: Black king-side castling availability
        The method performs the following steps:
        1. Updates all possible moves for the current player.
        2. Switches to the opponent and updates their possible moves.
        3. Switches back to the original player.
        4. Checks and updates castling rights for the white player.
        5. Checks and updates castling rights for the black player.
        Castling conditions:
        - The king and the chosen rook must not have moved.
        - There must be no pieces between the king and the chosen rook.
        - The king must not be in check, and the squares the king passes over must not be under attack.
        """

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





    def is_valid_move(self, start, end):
        """
        Determines if a move from the start position to the end position is valid according to chess rules.

        Parameters:
        start (tuple): A tuple (x, y) representing the starting position on the chessboard.
        end (tuple): A tuple (mx, my) representing the destination position on the chessboard.

        Returns:
        bool: True if the move is valid, False otherwise.

        The function checks:
        - If a valid piece is selected and if the destination square is not occupied by the player's own piece.
        - Movement rules based on the type of piece being moved, using an enumeration for clarity.
        - Special cases like castling, en passant, and pawn promotions are handled within their respective functions.

        The movement logic is delegated to helper functions stored in a dictionary `move_rules`,
        allowing clean separation of logic for each piece:
        - `PAWN`: Handles normal moves, double steps, captures, and en passant.
        - `ROOK`: Moves horizontally and vertically, ensuring no obstacles.
        - `WAZIR`: Moves to any adjacent square.
        - `FERZ`: Moves diagonally to adjacent squares.
        - `MYSTERIOUS`: Randomly chooses between rook and queen-like moves.
        - `KNIGHT`: Moves in an 'L' shape.
        - `CAMEL`: Moves in a (3,1) or (1,3) pattern.
        - `BISHOP`: Moves diagonally, ensuring no obstacles.
        - `KING`: Moves one square in any direction, handles castling.
        - `QUEEN`: Moves like both a rook and a bishop.

        If the piece type is unrecognized, the function returns False by default.
        """
        x, y = start  # Current position
        mx, my = end  # Target position
        start_piece = self.chess_board[y][x]  # Piece at start
        end_piece = self.chess_board[my][mx]  # Piece at destination
        
        # Ensure a valid piece is selected and destination is valid
        if start_piece == '--' or end_piece[0] == start_piece[0]:
            return False  

        piece_type = PieceType(start_piece[1])  # Convert to Enum for clarity

        # Define movement rules
        move_rules = {
            PieceType.PAWN: self._is_valid_pawn_move,
            PieceType.ROOK: self._is_valid_rook_move,
            PieceType.WAZIR: self._is_valid_wazir_move,
            PieceType.FERZ: self._is_valid_ferz_move,
            PieceType.MYSTERIOUS: self._is_valid_mysterious_move,
            PieceType.KNIGHT: self._is_valid_knight_move,
            PieceType.CAMEL: self._is_valid_camel_move,
            PieceType.BISHOP: self._is_valid_bishop_move,
            PieceType.KING: self._is_valid_king_move,
            PieceType.QUEEN: self._is_valid_queen_move
        }

        # Call the corresponding function for the piece type
        return move_rules.get(piece_type, lambda *_: False)(x, y, mx, my, start_piece, end_piece)


    # ==================================
    #    MOVEMENT FUNCTIONS (HELPERS)
    # ==================================

    def _is_valid_pawn_move(self, x, y, mx, my, start_piece, end_piece):
        """
        Validate a pawn's move from the starting position (x, y) to the target position (mx, my).

        The pawn's move is considered valid if one of the following conditions is met:
        - A single step forward into an empty square.
        - A double step forward from the starting rank (row 1 or 6) provided that both the target and
            the intermediate square are empty.
        - A diagonal capture if an opponent's piece occupies the target square.
        - An en passant capture, if the last move meets the en passant criteria.

        Parameters:
            x (int): Current x-coordinate of the pawn.
            y (int): Current y-coordinate of the pawn.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            start_piece (str): String representing the pawn at the starting square (e.g., 'wP' or 'bP').
            end_piece (str): String representing the piece at the target square ('--' indicates an empty square).

        Returns:
            bool: True if the pawn move is valid, False otherwise.
        """
        direction = -1 if start_piece[0] == 'w' else 1  # White moves up, black moves down
        coef = -1 if self.flipped else 1
        direction *= coef

        if mx == x:  # Moving straight
            if my == y + direction and end_piece == '--':  # Single step
                return True
            if (y == 1 or y == 6) and my == y + 2 * direction and end_piece == '--' and \
            self.chess_board[y + direction][x] == '--':  # Double step
                return True
        elif abs(mx - x) == 1 and my == y + direction:  # Diagonal capture move
            if end_piece != '--':
                return True
            # En passant capture
            last_move = self.last_move
            if len(last_move) and self.chess_board[last_move[1][1]][last_move[1][0]][1] == 'P' and \
            abs(last_move[1][1] - last_move[0][1]) == 2:
                if last_move[1][0] == mx and last_move[1][1] + direction == my:
                    self.pion_passant = True
                    return True
        return False


    def _is_valid_rook_move(self, x, y, mx, my, *_):
        """
        Validate a rook's move from (x, y) to (mx, my).

        The rook moves in a straight line either horizontally or vertically.
        In addition to the linear movement, the path from the starting square to the target square
        must be unobstructed.

        Parameters:
            x (int): Current x-coordinate of the rook.
            y (int): Current y-coordinate of the rook.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move is in a straight line and the path is clear, False otherwise.
        """
        if x == mx or y == my:
            step_x = 1 if mx > x else -1 if mx < x else 0
            step_y = 1 if my > y else -1 if my < y else 0
            for i in range(1, max(abs(mx - x), abs(my - y))):
                if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                    return False
            return True
        return False


    def _is_valid_wazir_move(self, x, y, mx, my, *_):
        """
        Validate a Wazir's move from (x, y) to (mx, my).

        The Wazir can move one square in any direction (horizontally, vertically, or diagonally).

        Parameters:
            x (int): Current x-coordinate of the Wazir.
            y (int): Current y-coordinate of the Wazir.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the target square is within one square in any direction, False otherwise.
        """
        return abs(mx - x) <= 1 and abs(my - y) <= 1


    def _is_valid_ferz_move(self, x, y, mx, my, *_):
        """
        Validate a Ferz's move from (x, y) to (mx, my).

        The Ferz moves exactly one square diagonally.

        Parameters:
            x (int): Current x-coordinate of the Ferz.
            y (int): Current y-coordinate of the Ferz.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move is exactly one square diagonally, False otherwise.
        """
        return abs(mx - x) == 1 and abs(my - y) == 1


    def _is_valid_mysterious_move(self, x, y, mx, my, *_):
        """
        Validate a Mysterious piece's move from (x, y) to (mx, my).

        The Mysterious piece behaves unpredictably:
        - With a 50% chance, it moves like a queen (diagonally, horizontally, or vertically).
        - Otherwise, it moves like a rook (only horizontally or vertically).

        Parameters:
            x (int): Current x-coordinate of the piece.
            y (int): Current y-coordinate of the piece.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move is valid based on the random behavior of the piece, False otherwise.
        """
        r = randint(1, 10)
        if r <= 5:  # Queen-like move
            return self._is_valid_queen_move(x, y, mx, my, *_)
        else:  # Rook-like move
            return self._is_valid_rook_move(x, y, mx, my, *_)


    def _is_valid_knight_move(self, x, y, mx, my, *_):
        """
        Validate a Knight's move from (x, y) to (mx, my).

        The Knight moves in an L-shape: either two squares in one direction and one square in the perpendicular direction.

        Parameters:
            x (int): Current x-coordinate of the Knight.
            y (int): Current y-coordinate of the Knight.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move matches the knight's L-shaped movement, False otherwise.
        """
        return (abs(mx - x) == 2 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 2)


    def _is_valid_camel_move(self, x, y, mx, my, *_):
        """
        Validate a Camel's move from (x, y) to (mx, my).

        The Camel moves in a (3, 1) or (1, 3) pattern.

        Parameters:
            x (int): Current x-coordinate of the Camel.
            y (int): Current y-coordinate of the Camel.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move follows the Camel's (3,1) or (1,3) pattern, False otherwise.
        """
        return (abs(mx - x) == 3 and abs(my - y) == 1) or (abs(mx - x) == 1 and abs(my - y) == 3)


    def _is_valid_bishop_move(self, x, y, mx, my, *_):
        """
        Validate a Bishop's move from (x, y) to (mx, my).

        The Bishop moves diagonally any number of squares, provided the path is unobstructed.

        Parameters:
            x (int): Current x-coordinate of the Bishop.
            y (int): Current y-coordinate of the Bishop.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move is diagonal and the path is clear, False otherwise.
        """
        if abs(mx - x) == abs(my - y):
            step_x = 1 if mx > x else -1
            step_y = 1 if my > y else -1
            for i in range(1, abs(mx - x)):
                if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                    return False
            return True
        return False


    def _is_valid_king_move(self, x, y, mx, my, start_piece, *_):
        """
        Validate a King's move from (x, y) to (mx, my).

        The King normally moves one square in any direction. In addition, castling is permitted if:
        - The king has not moved.
        - The corresponding castling flag is enabled.
        - The target castling square is reached (e.g., for white, (6,7) for kingside and (2,7) for queenside).

        Parameters:
            x (int): Current x-coordinate of the King.
            y (int): Current y-coordinate of the King.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            start_piece (str): String representing the King (e.g., 'wK' or 'bK').
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move is valid according to the King's movement or castling rules, False otherwise.
        """
        if max(abs(mx - x), abs(my - y)) == 1:
            return True
        if start_piece[0] == 'w' and not self.white_king_moved:
            if mx == 6 and my == 7 and self.castle[0]:
                return True
            if mx == 2 and my == 7 and self.castle[1]:
                return True
        if start_piece[0] == 'b':
            if mx == 2 and my == 0 and self.castle[3]:
                return True
            if mx == 6 and my == 0 and self.castle[2]:
                return True
        return False


    def _is_valid_queen_move(self, x, y, mx, my, *_):
        """
        Validate a Queen's move from (x, y) to (mx, my).

        The Queen may move diagonally, horizontally, or vertically any number of squares,
        as long as the path from the start to the target square is unobstructed.

        Parameters:
            x (int): Current x-coordinate of the Queen.
            y (int): Current y-coordinate of the Queen.
            mx (int): Target x-coordinate.
            my (int): Target y-coordinate.
            *_: Additional parameters (ignored).

        Returns:
            bool: True if the move is valid and the path is clear, False otherwise.
        """
        if abs(mx - x) == abs(my - y) or x == mx or y == my:
            step_x = 1 if mx > x else -1 if mx < x else 0
            step_y = 1 if my > y else -1 if my < y else 0
            for i in range(1, max(abs(mx - x), abs(my - y))):
                if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                    return False
            return True
        return False


    def _is_valid_queen_move(self, x, y, mx, my, *_):
        if abs(mx - x) == abs(my - y) or x == mx or y == my:
            step_x = 1 if mx > x else -1 if mx < x else 0
            step_y = 1 if my > y else -1 if my < y else 0
            for i in range(1, max(abs(mx - x), abs(my - y))):
                if self.chess_board[y + i * step_y][x + i * step_x] != '--':
                    return False
            return True
        return False

    def copy_game(self):
        """
        Create and return a deep copy of the current game state.
        This method performs a deep copy of the ChessGame object, ensuring that all mutable attributes
        are copied to prevent unintended modifications to the original game state.
        Returns:
            ChessGame: A new instance of ChessGame with the same state as the current game.
        """
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



    def get_possible_moves(self, x, y):
        """
        Returns a list of possible moves for the piece at the given coordinates (x, y) that do not put its king in check.

        Args:
            x (int): The x-coordinate of the piece.
            y (int): The y-coordinate of the piece.

        Returns:
            list of tuple: A list of tuples where each tuple represents a valid move (mx, my) for the piece.
        """
        return [(mx, my) for mx in range(8) for my in range(8) if self.is_valid_move((x, y), (mx, my))]


    def move_piece(self, start, x, y):
        """
        Moves a piece from the starting position to the target position (x, y).

        This method handles:
        - Normal piece movement.
        - Castling.
        - En passant captures.
        - Pawn promotion.
        - Updating game state (tracking king and rook movements).

        Args:
            start (tuple): A tuple (mx, my) representing the starting position.
            x (int): The target x-coordinate.
            y (int): The target y-coordinate.

        Returns:
            None
        """
        mx, my = start
        moving_piece = self.chess_board[my][mx]
        piece_type = moving_piece[1]
        color = moving_piece[0]
        direction = -1 if self.turn == 'black' else 1

        # --- Attempt Castling ---
        if self._try_castling(mx, my, x, y, piece_type, color):
            return

        # --- Update King and Rook Movements ---
        self._track_king_movement(piece_type, color)
        self._track_rook_movement(mx, my, piece_type)

        # --- Handle En Passant Capture ---
        self._handle_en_passant(piece_type, mx, x, y, direction)
        self._update_en_passant_status(piece_type, my, y)

        # --- Execute the Move ---
        self._execute_move(mx, my, x, y, moving_piece)

        # --- Handle Pawn Promotion ---
        self._handle_pawn_promotion(piece_type, x, y, color)


    def _try_castling(self, mx, my, x, y, piece_type, color):
        """
        Attempts to perform a castling move if all conditions are met.

        Args:
            mx (int): King's initial x-coordinate.
            my (int): King's initial y-coordinate.
            x (int): King's target x-coordinate.
            y (int): King's target y-coordinate.
            piece_type (str): The type of the moving piece.
            color (str): The color of the piece ('w' for white, 'b' for black).

        Returns:
            bool: True if castling was executed, False otherwise.
        """
        if piece_type == 'K' and abs(mx - x) == 2 and my == y:
            if color == 'w' and not self.white_king_moved and not self.white_king_check and my == 7:
                self._castle(mx, my, x, y, color)
                self.white_king_moved = True
                return True
            elif color == 'b' and not self.black_king_moved and not self.black_king_check and my == 0:
                self._castle(mx, my, x, y, color)
                self.black_king_moved = True
                return True
        return False


    def _track_king_movement(self, piece_type, color):
        """
        Updates the game state to indicate that the king has moved.

        Args:
            piece_type (str): The type of the moving piece.
            color (str): The color of the king ('w' or 'b').

        Returns:
            None
        """
        if piece_type == 'K':
            if color == 'w':
                self.white_king_moved = True
            else:
                self.black_king_moved = True


    def _track_rook_movement(self, mx, my, piece_type):
        """
        Updates the game state for rook movements, which affect castling rights.

        Args:
            mx (int): Rook's initial x-coordinate.
            my (int): Rook's initial y-coordinate.
            piece_type (str): The type of the moving piece.

        Returns:
            None
        """
        if piece_type == 'R':
            # Mapping of rook starting positions to their indices in self.rook_moved.
            rook_positions = {(7, 7): 0, (0, 7): 1, (0, 0): 2, (7, 0): 3}
            if (mx, my) in rook_positions:
                self.rook_moved[rook_positions[(mx, my)]] = 1


    def _handle_en_passant(self, piece_type, mx, x, y, direction):
        """
        Processes an en passant capture if the move qualifies.

        Args:
            piece_type (str): The type of the moving piece.
            mx (int): Pawn's starting x-coordinate.
            x (int): Pawn's target x-coordinate.
            y (int): Pawn's target y-coordinate.
            direction (int): Direction of pawn movement (-1 or 1).

        Returns:
            None
        """
        if piece_type == 'P' and abs(mx - x) == 1 and self.pion_passant:
            self.chess_board[y + direction][x] = '--'


    def _update_en_passant_status(self, piece_type, my, y):
        """
        Updates the en passant status after a pawn move.

        Args:
            piece_type (str): The type of the moving piece.
            my (int): Pawn's starting y-coordinate.
            y (int): Pawn's target y-coordinate.

        Returns:
            None
        """
        self.pion_passant = (piece_type == 'P' and abs(my - y) == 2)


    def _execute_move(self, mx, my, x, y, moving_piece):
        """
        Moves the piece on the board from its initial to target position.

        Args:
            mx (int): The initial x-coordinate of the piece.
            my (int): The initial y-coordinate of the piece.
            x (int): The target x-coordinate.
            y (int): The target y-coordinate.
            moving_piece (str): The piece being moved.

        Returns:
            None
        """
        self.chess_board[y][x] = moving_piece
        self.chess_board[my][mx] = '--'


    def _handle_pawn_promotion(self, piece_type, x, y, color):
        """
        Promotes a pawn that has reached the far end of the board.

        Args:
            piece_type (str): The type of the moving piece.
            x (int): Pawn's target x-coordinate.
            y (int): Pawn's target y-coordinate.
            color (str): The color of the pawn ('w' or 'b').

        Returns:
            None
        """
        if piece_type == 'P' and y in (0, 7):
            promoted_piece = Promotion_screen(self, color)[0]
            # If the promotion choice is 'K', substitute it with 'N' as per game rules.
            self.chess_board[y][x] = color + ('N' if promoted_piece == 'K' else promoted_piece)


    def _castle(self, mx, my, x, y, color):
        """
        Handles castling by moving both the king and the appropriate rook.

        Args:
            mx (int): King's initial x-coordinate.
            my (int): King's initial y-coordinate.
            x (int): King's target x-coordinate.
            y (int): King's target y-coordinate.
            color (str): The color of the king ('w' for white, 'b' for black).

        Returns:
            None
        """
        # Move the king to the target square.
        self.chess_board[y][x] = self.chess_board[my][mx]
        self.chess_board[my][mx] = '--'
    
        # Determine the direction and the rook index based on the king's move.
        direction = (mx - x) // 2
        rook_idx = 0 if x == 6 else 1  # 0 for kingside, 1 for queenside castling.
    
        # Remove the rook from its original position and place it next to the king.
        self.chess_board[my][self.rook_pos[rook_idx]] = '--'
        self.chess_board[y][x + direction] = color + 'R'

    def is_king_in_check(self):
        """
        Checks if the current player's king is in check.
        This method determines if the king of the player whose turn it is currently
        is in check. It does so by checking if any of the opponent's pieces can move
        to the king's position.
        Returns:
            bool: True if the king is in check or has been captured, False otherwise.
        """
        color=self.turn[0]
        king_position = find_king_position(self.chess_board,color)
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
        """
        Simulates a move on the chess board and checks if it puts the player's king in check.
        Args:
            start (tuple): The starting position of the piece (column, row).
            end (tuple): The ending position of the piece (column, row).
        Returns:
            bool: True if the move does not put the player's king in check, False otherwise.
        """
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
        """
        Get a list of valid moves for a piece at the given coordinates.

        This method calculates all possible moves for the piece located at the 
        specified (x_square, y_square) coordinates and filters out any moves 
        that would put the player's own king in check.

        Args:
            x_square (int): The x-coordinate of the piece on the chessboard.
            y_square (int): The y-coordinate of the piece on the chessboard.

        Returns:
            list: A list of valid moves, where each move is represented by a 
                  tuple of coordinates (x, y).
        """
        self.possible_moves = self.get_possible_moves(x_square, y_square)
        valid_moves = [move for move in self.possible_moves if self.simulate_move_and_check((x_square, y_square), move)]
        return valid_moves
    
    def check(self, x_square, y_square):
        """
        Checks if the move at the given position puts the opponent's king in check.

        Args:
            x_square (int): The x-coordinate (column index) of the square from which the piece is moving.
            y_square (int): The y-coordinate (row index) of the square from which the piece is moving.

        Returns:
            tuple: A tuple (x, y) representing the position of the opponent's king if it is in check.
                Returns (-1, -1) if the move does not result in a check or if the square is empty.

        The function first verifies if the selected square contains a piece. If the square is empty ('--'),
        it returns (-1, -1). It then retrieves all valid moves for the piece at the given square. The color
        of the opponent is determined based on the current player's turn, and the opponent's king's identifier
        ('bK' for black king or 'wK' for white king) is set accordingly. The function iterates over the valid
        moves, checking if any of them capture the opponent's king. If the king is found in the path of a move,
        its position is returned. If no such move is found, the function returns (-1, -1).
        """
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
        """Checks if the game has ended based on time, checkmate, stalemate, or specific game rules.

        Returns:
        int: -1 if Black wins, 1 if White wins, 0 for stalemate, or None if the game continues.
        """
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
            x_w,y_w = find_king_position(self.chess_board,'w')
            x_b,y_b = find_king_position(self.chess_board,'b')
            if (x_w in [3,4] and y_w in [3,4] and self.turn == 'black') :
                return 1
            if (x_b in [3,4] and y_b in [3,4] and self.turn == 'white'):
                return -1
        return None  # Game continues



    def convert_to_chess_board(self):
    
        """Converts the internal chess board representation to a `chess.Board` object.

        Returns:
        chess.Board: A `chess.Board` object representing the current board state.
        """
        game = self.copy_game()
        board = chess.Board()
        if (game.turn=='black') :
            game.flip_board()
        board.clear()
        for row in range(8):
            for col in range(8):
                piece = game.chess_board[row][col]
                if piece != '--':
                    color = chess.WHITE if piece[0] == 'w' else chess.BLACK
                    piece_type = chess.Piece.from_symbol(piece[1].upper()).piece_type
                    square = chess.square(col, 7 - row)
                    board.set_piece_at(square, chess.Piece(piece_type, color))
        return board
    def evaluate_hard(self):
        """Evaluates the current chess position using the Stockfish engine.

        Returns:
        float: The evaluation score for the position, positive for white advantage,
            negative for black advantage. Returns a large number if the engine crashes.
        """
        stockfish_path = "/usr/games/stockfish"  # Replace with the correct path
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            board = self.convert_to_chess_board()
            print(board)
            
            try:
                result = engine.analyse(board, chess.engine.Limit(depth=9))
            except chess.engine.EngineTerminatedError as e:
                print(f"Engine crashed: {e}")
                return 1e5  # Return a large score if the engine crashes

            score = result["score"]

            # Evaluate the score from the perspective of the player whose turn it is
            if self.turn=='white':
                # It's White's turn: Use White's perspective
                print('white')
                evaluation = score.white().score(mate_score=1e6) if score.is_mate() else score.white().score()
            else:
                # It's Black's turn: Use Black's perspective
                print('black')
                evaluation = score.black().score(mate_score=-1e6) if score.is_mate() else score.black().score()

            print(f"Turn: {board.turn}, Evaluation: {evaluation}")
            return evaluation





