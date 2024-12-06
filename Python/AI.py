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
    [ 0,  0,  0,  0,  0,  0,  0,  0],  # 8th rank
    [30, 30, 30, 30, 30, 30, 30, 30],  # 7th rank (promotion potential)
    [10, 10, 20, 30, 30, 20, 10, 10],  # 6th rank (advanced pawns gain value)
    [ 5,  5, 10, 40, 25, 10,  5,  5],  # 5th rank (central control is valuable)
    [ 0,  0,  0, 20, 20,  0,  0,  0],  # 4th rank (encourage centralization)
    [ 5, -5, -10,  0,  0, -10, -5,  5], # 3rd rank (discourage premature pushes)
    [ 5, 10, 10, -20, -20, 10, 10,  5], # 2nd rank (initial pawn moves)
    [ 0,  0,  0,  0,  0,  0,  0,  0],  # 1st rank (no pawns here)
]

KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-30, 0, 50, 15, 15, 50, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 50, 15, 15, 50, 0, -30],
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
    [0, -5, 5, 10, 10, 5, -5, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 5, 5, 5, 5, 5, 5, 0],
    [0, 10, 10, 10, 10, 10, 10, 0],
    [0, -5, 5, 10, 10, 5, -5, 0]
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
    'P': 100,
    'N': 300,
    'B': 320,
    'R': 500,
    'Q': 900,
    'K': 100000
}
def coeffs(x,y) :
    if (abs(x-3)+abs(y-3)<=3) :
        return 1.5
    if (abs(x-3)+abs(y-3)<=5) :
        return 1
    return 0.8
def evaluate_piece(turn, piece, x, y):
    """Evaluates the score of a piece based on its type, position, and game phase."""
    my = y if turn == 'white' else 7 - y
    tables = {
        'N': (300, KNIGHT_TABLE),
        'Q': (900, QUEEN_TABLE),
        'P': (100, PAWN_TABLE),
        'R': (500, ROOK_TABLE),
        'B': (320, BISHOP_TABLE),
        'K': (10000, KING_TABLE)
    }
    if piece[1] in tables:
        base, table = tables[piece[1]]
        piece_position_score = table[my][x] 
        coeff = coeffs(x,y)
        coeff = 1 if (piece[1]=='P' or piece[1]=='K' or piece[1]=='B') else coeff
        # For white pieces, return positive value, for black return negative
        score = base + piece_position_score
        return score if piece[0] == 'w' else -score
    return 0
def evaluate_material(game):
    material_score = 0
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[y][x]
            if piece != '--':  # not an empty square
                material_score += evaluate_piece(game.turn,piece,x,y) 
    return material_score
def evaluate(game):
    """Calculates the total evaluation score for the game based on various factors."""
    total_score = 0 

    # King Safety: Add extra evaluation for the safety of the kings
    white_king_position = find_king_position(game, 'white')
    black_king_position = find_king_position(game, 'black')
    total_score += king_safety(game.turn, white_king_position, black_king_position)

    # Pawn Structure Evaluation: Check for doubled, isolated, or passed pawns
    # Add a bit of evaluation for central control and mobility
    total_score += evaluate_control_and_mobility(game) + evaluate_material(game)
    if (game.len_list_of_boards<10) :
        total_score += evaluate_opening(game)

    return total_score 

def find_king_position(game, color):
    """Returns the position of the king for a given color."""
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[y][x]
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
        return 0 if ((x ==0) or (x==7)) else -100
    return 0



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
    return score


def evaluate_opening(game):
    score = 0
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]

    # Central control
    for x, y in center_squares:
        piece = game.chess_board[y][x]
        if piece == 'wp':
            score += 30
        elif piece == 'bp':
            score -= 30

    # Piece development
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[y][x]
            if piece.startswith('w') and y > 3 and y <6 and abs(y-x)<4 and (piece[1]=='N' or piece[1]=='Q') :  # Encourage white pieces to advance
                score += 40
            elif piece.startswith('b') and y < 6 and y>2 and abs(y-x)<4 and (piece[1]=='N' or piece[1]=='Q'):  # Encourage black pieces to advance
                score -= 40

    return score

def minimax(game, depth, alpha, beta):
    if depth == 0 or not game.running:
        return evaluate(game)
    if  game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        for move in game.white_moves.values():
            for end_pos in move:
                next_game = game.copy_game()
                next_game.move_piece(move[0], end_pos[0], end_pos[1])
                next_game.change_player()
                eval = minimax(next_game, depth - 1,alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta+10 <= alpha:
                    break
        return max_eval
    else:  # Minimizing for black
        min_eval = float('inf')
        for move in game.black_moves.values():
            for end_pos in move:
                next_game = game.copy_game()
                next_game.move_piece(move[0], end_pos[0], end_pos[1])
                next_game.change_player()
                eval = minimax(next_game, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta+10 <= alpha:
                    break
        return min_eval


def AI(game, depth=4):
    moves_scores = []
    # Determine moves based on whose turn it is
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    
    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            next_game = game.copy_game()
            next_game.move_piece(start_pos, end_pos[0], end_pos[1])
            next_game.change_player()
            # Evaluate the move using minimax
            score = minimax(next_game, depth - 1, alpha=-1000000, beta=10000000)
            moves_scores.append(((start_pos, end_pos), score))
    
    # Sort moves based on the score
    moves_scores.sort(key=lambda x: x[1], reverse=(game.turn == 'white'))
    
    # Return the move with the best score
    if moves_scores:
        best_move, best_score = moves_scores[0]
        return best_move  # You could also return the score if needed
    return None
