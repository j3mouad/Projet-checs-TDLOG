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
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 100, 15, 15, 100, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 100, 15, 15, 100, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]
BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
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
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
QUEEN_TABLE = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
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

def centrality_coefficient(x, y):
    center_x, center_y = 3, 3
    dist = abs(x - center_x) + abs(y - center_y)
    if dist == 0:
        return 1.5
    elif dist == 1:
        return 1.2
    elif dist == 2:
        return 1.0
    elif dist == 3:
        return 0.8
    else:
        return 0.5

def evaluate_piece(turn, piece, x, y):
    mx = x if turn == 'white' else 7 - x
    coeff = centrality_coefficient(mx, y)
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
        score = base + table[mx][y] * coeff
        return score if piece[0] == 'w' else -score
    return 0

def evaluate(game):
    return sum(
        evaluate_piece(game.turn, game.chess_board[x][y], x, y)
        for x in range(8) for y in range(8)
    )

def minimax(game, depth, maximizing_player, alpha, beta):
    if depth == 0 or not game.running:
        return evaluate(game)

    if maximizing_player:
        max_eval = float('-inf')
        for move in game.black_moves.values():
            eval = minimax(game, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.white_moves.values():
            eval = minimax(game, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def AI(game, depth=4):
    best_score = float('-inf') if game.turn == 'white' else float('inf')
    best_move = None
    for start_pos, moves in (game.white_moves if game.turn == 'white' else game.black_moves).items():
        for end_pos in moves:
            next_game = game.copy_game()
            next_game.move_piece(start_pos, end_pos[0], end_pos[1])
            score = minimax(next_game, depth - 1, game.turn == 'black', float('-inf'), float('inf'))
            if (game.turn == 'white' and score > best_score) or (game.turn == 'black' and score < best_score):
                best_score = score
                best_move = (start_pos, end_pos)
    return best_move
