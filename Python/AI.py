import os
import sys
import random
new_dir = '/home/hassene/Desktop/Projet-echecs-TDLOG/build'
os.chdir(new_dir)
# Add to sys.path
if new_dir not in sys.path:
    sys.path.append(new_dir)
#import libAI
#a,b = libAI.generator()
PAWN_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # 1st rank
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # 2nd rank
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # 3rd rank
    [ 0,  0,  0, 10, 10,  0,  0,  0],   # 4th rank (center)
    [ 0,  0,  0, 10, 10,  0,  0,  0],   # 5th rank (center)
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # 6th rank
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # 7th rank
    [ 0,  0,  0,  0,  0,  0,  0,  0]    # 8th rank
]


KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20,   0,   0,   0,   0, -20, -40],
    [-30,   0,  100,  15,  15,  100,   0, -30],
    [-30,   5,  15,  20,  20,  15,   5, -30],
    [-30,   0,  15,  20,  20,  15,   0, -30],
    [-30,   5,  100,  15,  15,  100,   5, -30],
    [-40, -20,   0,   5,   5,   0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP_TABLE = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10,   5,   0,   0,   0,   0,   5, -10],
    [-10,  10,  10,  10,  10,  10,  10, -10],
    [-10,   0,  10,  10,  10,  10,   0, -10],
    [-10,   5,   5,  10,  10,   5,   5, -10],
    [-10,   0,   5,  10,  10,   5,   0, -10],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]
ROOK_TABLE = [
    [  0,   0,   5,  10,  10,   5,   0,   0],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [  5,  10,  10,  10,  10,  10,  10,   5],
    [  0,   0,   0,   0,   0,   0,   0,   0]
]
KING_TABLE = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [ 20,  20,   0,   0,   0,   0,  20,  20],
    [ 20,  30,  10,   0,   0,  10,  30,  20]
]
QUEEN_TABLE = [
    [-20, -10, -10,  -5,  -5, -10, -10, -20],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-10,   0,   5,   5,   5,   5,   0, -10],
    [ -5,   0,   5,   5,   5,   5,   0,  -5],
    [  0,   0,   5,   5,   5,   5,   0,  -5],
    [-10,   5,   5,   5,   5,   5,   0, -10],
    [-10,   0,   5,   0,   0,   0,   0, -10],
    [-20, -10, -10,  -5,  -5, -10, -10, -20]
]
def centrality_coefficient(x, y):
    # Manhattan distance from the center (4,4)
    center_x, center_y = 3, 3
    dist = abs(x - center_x) + abs(y - center_y)
    
    # Map the distance to a coefficient (smaller distance, higher coefficient)
    # The closer to the center, the larger the coefficient
    if dist == 0: 
        return 1.5  # Center
    elif dist == 1: 
        return 1.2  # Near center
    elif dist == 2: 
        return 1.0  # Mid-range
    elif dist == 3: 
        return 0.8  # Closer to edges
    else: 
        return 0.5  # Corners and far edges

def evaluate_piece(turn,piece,x,y) : 
    s = 0
    mx = x if turn=='white' else 7-x 
    my = y 
    coeff = centrality_coefficient(mx, my)  # Get the position-based coefficient

    if (piece[1]=='N') : 
        s = 300 + KNIGHT_TABLE[mx][my] * 5*coeff
    if (piece[1]=='Q') :
        s = 900 + QUEEN_TABLE[mx][my] * coeff
    if (piece[1]=='P') : 
        s = 50  + PAWN_TABLE[mx][my]
    if (piece[1]=='R') :
        s = 500 + ROOK_TABLE[mx][my] 
    if (piece[1] == 'B') :
        s = 320 + BISHOP_TABLE[mx][my] 
    if (piece[1]=='K') :
        s = 10000 + KING_TABLE[mx][my] 
    if (piece[0]=='b') : 
        s*=-1 
    return s

def evaluate(game) :
    result = 0 
    for x in range(8) :
        for y in range(8) :
            result += evaluate_piece(game.turn,game.chess_board[x][y],x,y) 
    return result 
def minimax(game, depth, maximizing_player, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Parameters:
        - game: Current game state object.
        - depth: Depth of the search tree.
        - maximizing_player: Boolean indicating whether the current player is maximizing.
        - alpha: Alpha value for pruning.
        - beta: Beta value for pruning.
        
        Returns:
        - Evaluation score of the current game state.
        """
        if depth == 0 or not game.running:
            return evaluate(game)

        if not maximizing_player:
            max_eval = -1e9
            for start_pos, moves in game.black_moves.items():
                if not moves:
                    continue
                for end_pos in moves:
                    if len(end_pos) < 2:
                        continue
                    next_game = game.copy_game()
                    next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                    eval_score = minimax(next_game, depth - 1, True, alpha, beta)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha+2:
                        break
            return max_eval
        else:
            min_eval = 1e9
            for start_pos, moves in game.white_moves.items():
                if not moves:
                    continue
                for end_pos in moves:
                    if len(end_pos) < 2:
                        continue
                    next_game = game.copy_game()
                    next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                    eval_score = minimax(next_game, depth - 1,False, alpha, beta)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha+2:
                        break
            return min_eval
        

def AI(game, depth=4):
    """
    AI function to determine the best move for the current player (black or white).
    
    Parameters:
    - game: Current game state object.
    - depth: Depth of the search tree for minimax evaluation.

    Returns:
    - best_move: Tuple containing the start and end positions of the best move.
    """
    

    best_score = 1e9 if game.turn == 'black' else -1e9
    best_move = None
    moves = game.black_moves if game.turn == 'black' else game.white_moves

    for start_pos, possible_moves in moves.items():
        if not possible_moves:
            continue
        for end_pos in possible_moves:
            if len(end_pos) < 2:
                continue
            copy_game = game.copy_game()
            copy_game.move_piece(start_pos, end_pos[0], end_pos[1])
            move_score = minimax(copy_game, depth - 1, game.turn == 'white', -1e9, 1e9)

            if game.turn == 'black' and (move_score < best_score) or (move_score == best_score ):
                best_score = move_score
                best_move = (start_pos, end_pos)
            elif game.turn == 'white' and (move_score > best_score) or (move_score == best_score ):
                best_score = move_score
                best_move = (start_pos, end_pos)

    return best_move
