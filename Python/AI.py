import os
import sys

# Set up directory
new_dir = '/home/hassene/Desktop/Projet-echecs-TDLOG/build'
os.chdir(new_dir)

# Add to sys.path
if new_dir not in sys.path:
    sys.path.append(new_dir)

# Positional tables for pieces
PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 10, 10, 0, 0, 0],
    [0, 0, 0, 10, 10, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-30, 10, 15, 20, 20, 15, 10, -30],
    [-30, 10, 15, 20, 20, 15, 10, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 10, 15, 15, 10, 5, -10],
    [-10, 5, 10, 15, 15, 10, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

ROOK_TABLE = [
    [0, 0, 5, 10, 10, 5, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 5, 5, 5, 5, 5, 5, 0],
    [0, 10, 10, 10, 10, 10, 10, 0],
    [0, 0, 5, 10, 10, 5, 0, 0]
]

QUEEN_TABLE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 10, 10, 5, 0, -5],
    [0, 5, 5, 10, 10, 5, 5, 0],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

KING_TABLE = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]

PIECE_VALUES = {
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 10000
}

def evaluate_piece(turn, piece, x, y):
    """Evaluates the score of a piece based on its type, position, and game phase."""
    mx = x if turn == 'white' else 7 - x
    coeff = 1
    tables = {
        'N': (300, KNIGHT_TABLE),
        'Q': (900, QUEEN_TABLE),
        'P': (50, PAWN_TABLE),
        'R': (500, ROOK_TABLE),
        'B': (320, BISHOP_TABLE),
        'K': (10000, KING_TABLE)
    }

    if piece[1] in tables:
        base, table = tables[piece[1]]
        piece_position_score = table[mx][y] * coeff
        # For white pieces, return positive value, for black return negative
        score = base + piece_position_score
        return score if piece[0] == 'w' else -score
    return 0
def evaluate_material(game):
    material_score = 0
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[x][y]
            if piece != '--':  # not an empty square
                material_score += PIECE_VALUES.get(piece[1], 0) if piece[0] == 'w' else -PIECE_VALUES.get(piece[1], 0)
    return material_score
def evaluate(game):
    """Calculates the total evaluation score for the game based on various factors."""
    total_score = 0

    for x in range(8):
        for y in range(8):
            piece = game.chess_board[x][y]
            if piece != '--':  # Ignore empty squares
                total_score += evaluate_piece(game.turn, piece, x, y)

    # King Safety: Add extra evaluation for the safety of the kings
    white_king_position = find_king_position(game, 'white')
    black_king_position = find_king_position(game, 'black')
    total_score += king_safety(game.turn, white_king_position, black_king_position)

    # Pawn Structure Evaluation: Check for doubled, isolated, or passed pawns
    total_score += evaluate_pawn_structure(game)

    # Add a bit of evaluation for central control and mobility
    total_score += evaluate_control_and_mobility(game)

    return total_score + evaluate_material(game)

def find_king_position(game, color):
    """Returns the position of the king for a given color."""
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[x][y]
            if piece == f'{color[0]}K':  # White king or black king
                return (x, y)
    return None

def king_safety(turn, white_king_position, black_king_position):
    """Adds a bonus/penalty for king safety depending on its position."""
    if turn == 'white':
        return evaluate_king_position(white_king_position)
    else:
        return -evaluate_king_position(black_king_position)

def evaluate_king_position(position):
    """Evaluates the safety of the king's position."""
    if position:
        x, y = position
        # Add a bonus for a king closer to the center
        return 0 if x in range(2, 6) and y in range(2, 6) else -100
    return 0

def evaluate_pawn_structure(game):
    """Evaluates pawn structure considering doubled, isolated, and passed pawns."""
    score = 0
    # Loop through the board and evaluate pawns' structure
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[x][y]
            if piece == 'wp':
                score += evaluate_white_pawn(game, x, y)
            elif piece == 'bp':
                score -= evaluate_black_pawn(game, x, y)
    return score

def evaluate_white_pawn(game, x, y):
    """Evaluate the position of a white pawn (for passed pawns, isolated pawns, etc.)."""
    score = 0
    # Evaluate pawn's position in terms of passed and isolated pawns
    if is_passed_pawn(game, 'w', x, y):
        score += 20
    if is_isolated_pawn(game, 'w', x, y):
        score -= 10
    return score

def evaluate_black_pawn(game, x, y):
    """Evaluate the position of a black pawn (for passed pawns, isolated pawns, etc.)."""
    score = 0
    if is_passed_pawn(game, 'b', x, y):
        score -= 20
    if is_isolated_pawn(game, 'b', x, y):
        score += 10
    return score

def is_passed_pawn(game, color, x, y):
    """Checks if a pawn is a passed pawn."""
    direction = 1 if color == 'w' else -1
    # Check if there is no opposing pawn blocking the path ahead
    for i in range(x + direction, 8, direction):
        if game.chess_board[i][y] == f'bp' if color == 'w' else 'wp':
            return False
    return True

def is_isolated_pawn(game, color, x, y):
    """Checks if a pawn is isolated (no pawns of the same color on adjacent files)."""
    # Check adjacent files for the same color pawns
    if color == 'w':
        if (y > 0 and game.chess_board[x][y - 1] == 'wp') or (y < 7 and game.chess_board[x][y + 1] == 'wp'):
            return False
    else:
        if (y > 0 and game.chess_board[x][y - 1] == 'bp') or (y < 7 and game.chess_board[x][y + 1] == 'bp'):
            return False
    return True

def evaluate_control_and_mobility(game):
    """Evaluates central control and piece mobility."""
    score = 0
    # Evaluate central control (favor pieces in the center)
    center = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for x, y in center:
        piece = game.chess_board[x][y]
        if piece == 'wp':
            score += 10
        elif piece == 'bp':
            score -= 10

    # Evaluate piece mobility
    score += evaluate_piece_mobility(game)
    return score

def evaluate_piece_mobility(game):
    """Evaluates the mobility of pieces, rewarding those with more available moves."""
    score = 0
    # Count available moves for each piece (more moves = better mobility)
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[x][y]
            if piece != '--':
                score += count_available_moves(game, x, y)
    return score

def count_available_moves(game, x, y):
    """Counts the number of available moves for a piece at position (x, y)."""
    piece = game.chess_board[x][y]
    moves = 0
    # Simple move counting logic for different piece types
    if piece == 'wp' or piece == 'bp':  # Pawns
        # Consider pawn forward moves (simplified, ignoring en passant and captures)
        if 0 <= x + 1 < 8:
            moves += 1
    # Implement counting moves for other pieces similarly (knights, rooks, bishops, queens, kings)
    # For brevity, we assume other pieces' move logic is also implemented here
    return moves

def minimax(game, depth, maximizing_player, alpha, beta):
    if depth == 0 or not game.running:
        return evaluate(game)

    if  maximizing_player:  # Maximizing for white
        max_eval = float('-inf')
        for move in game.white_moves.values():
            for end_pos in move:
                next_game = game.copy_game()
                next_game.move_piece(move[0], end_pos[0], end_pos[1])
                eval = minimax(next_game, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:  # Minimizing for black
        min_eval = float('inf')
        for move in game.black_moves.values():
            for end_pos in move:
                next_game = game.copy_game()
                next_game.move_piece(move[0], end_pos[0], end_pos[1])
                eval = minimax(next_game, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


def AI(game, depth=4):
    print("evaluation is ", evaluate(game))
    best_score = float('-inf') if game.turn == 'white' else float('inf')
    best_move = None

    # Determine moves based on whose turn it is
    moves = game.white_moves if game.turn == 'white' else game.black_moves

    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            next_game = game.copy_game()
            next_game.move_piece(start_pos, end_pos[0], end_pos[1])
            
            # Recursively call minimax
            score = minimax(next_game, depth - 1, game.turn == 'white', float('-inf'), float('inf'))

            # Select the best move based on turn
            if (game.turn == 'white' and score > best_score) or (game.turn == 'black' and score < best_score):
                best_score = score
                best_move = (start_pos, end_pos)

    return best_move
