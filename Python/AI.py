import os
import sys
import random 
# Set up directory
new_dir = '/home/hassene/Desktop/Projet-echecs-TDLOG/build'
os.chdir(new_dir)

# Add to sys.path
if new_dir not in sys.path:
    sys.path.append(new_dir)

# Positional tables for pieces
PAWN_TABLE = [
    [  0,   0,   0,   0,   0,   0,   0,   0],  
    [ 10,  10,  10, -10, -10,  10,  10,  10],  
    [  5,   5,  10,  20,  20,  10,   5,   5],  
    [  0,   0,   10,  30,  30,  10,   0,   0],  
    [  5,   5,  20,  40,  40,  20,   5,   5],  
    [ 10,  10,  20,  50,  50,  20,  10,  10],  
    [ 20,  20,  30,  60,  60,  30,  20,  20], 
    [  0,   0,   0,   0,   0,   0,   0,   0], 
]

KNIGHT_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [40, 20, 0, 5, 5, 0, 20, 40],
    [-30, 5, 30, 30, 30, 30, 5, -30],
    [10, 10, 60, 40, 40, 60, 10, 10],
    [10, 10, 60, 80, 80, 60, 10, 10],
    [-30, 5, 30, 30, 30, 30, 5, -30],
    [40, 20, 0, 5, 5, 0, 20, 40],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

BISHOP_TABLE = [
    [20, 10, 100, 10, 10, 100, 10, 20],
    [10, 0, 0, 0, 0, 0, 0, 10],
    [10, 0, 5, 10, 10, 5, 0, 10],
    [10, 5, 10, 15, 15, 10, 5, 10],
    [10, 5, 10, 15, 15, 10, 5, 10],
    [10, 0, 5, 10, 10, 5, 0, 10],
    [10, 0, 0, 0, 0, 0, 0, 10],
    [20, 10, 100, 10, 10, 100, 10, 20]
]
ROOK_TABLE = [
    [50, 0, 40, 10, 40, 40, 0, 50],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [100, 0, 0, 0, 0, 0, 0, 100],
    [100, 0, 0, 0, 0, 0, 0, 100],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [50, 0, 40, 10, 40, 40, 0, 50],
]

QUEEN_TABLE = [
    [20, 10, 10, 5, 5, 10, 10, 20],
    [10, 0, 0, 0, 0, 0, 0, 10],
    [10, 0, 50, 50, 50, 50, 0, 10],
    [5, 0, 50, 100, 100, 50, 0, 5],
    [0, 50, 50, 100, 100, 50, 50, 0],
    [10, 50, 50, 50, 50, 50, 0, 10],
    [10, 0, 50, 0, 0, 0, 0, 10],
    [20, 10, 10, 5, 5, 10, 10, 20]
]
KING_TABLE = [
    [30, 40, 40, 50, 50, 40, 40, 30],
    [30, 40, 40, 50, 50, 40, 40, 30],
    [30, 40, 40, 50, 50, 40, 40, 30],
    [30, 40, 40, 50, 50, 40, 40, 30],
    [20, 30, 30, 40, 40, 30, 30, 20],
    [10, 20, 20, 20, 20, 20, 20, 10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 1000, -40, 0, -40, 1000, 20]
]

tables = {
        'N': (300, KNIGHT_TABLE),
        'Q': (900, QUEEN_TABLE),
        'P': (100, PAWN_TABLE),
        'R': (500, ROOK_TABLE),
        'B': (300, BISHOP_TABLE),
        'K': (100000, KING_TABLE)
    }

def evaluate_piece(piece, x, y):
    """Evaluates the score of a piece based on its type, position, and game phase."""
    my = y if piece[0] == 'w' else 7 - y
    
    
    if piece[1] in tables:
        base, table = tables[piece[1]]
        piece_position_score = table[my][x] 
        coeff = 1
        black_score = 0
        white_score = 0 
        # For white pieces, return positive value, for black return negative
        score = base + piece_position_score * coeff
        if (piece[0]=='b') : black_score += score
        elif (piece[0]=='w') : white_score +=score  

        return score if piece[0] == 'w' else -score
    return 0
def evaluate_material(game):
    material_score = 0
    for x in range(8):
        for y in range(8):
            piece = game.chess_board[y][x]
            if piece != '--':  # not an empty square
                material_score += evaluate_piece(piece,x,y) 
    return material_score

def evaluate(game):
    """Calculates the total evaluation score for the game based on various factors."""
    total_score = 0 
    # Evaluate material
    material_score = evaluate_material(game)
    total_score += material_score

    # King safety
    king_safety_score = king_safety(game.turn, game.white_king_position, game.black_king_position)
    total_score += king_safety_score

    # Evaluate opening strategies if early in the game
    if game.len_list_of_boards < 20:
        opening_score = evaluate_opening(game)
        total_score += opening_score

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
        return 0 if ((x <=1) or (x>=5)) else -300
    return 0


def evaluate_opening(game):
    score = 0
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4),(2,4),(4,2),(3,2),(2,3)]
    
    # Central control
    for x, y in center_squares:
        piece = game.chess_board[y][x]
        if piece == 'wP':
            score += 100  # White pawn controlling the center
        elif piece == 'bP':
            score -= 100  # Black pawn controlling the center
        elif piece[1]=='N' : 
            if (piece[0]=='w') :
                score+=100
            else :
                score-=100
        elif piece[1]=='Q' :
            if (piece[0]=='w') :
                score+=70
            else :
                score-=70
    return score

def minimax(game, depth, alpha=float('-inf'), beta=float('inf')):
    if not game.running:
        if game.winner == 'Stalemate':
            return 0
        if game.winner == 'white':
            return 1e9
        return -1e9
    
    if depth == 0:
        return evaluate(game)
    
    if game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        white_moves = list(game.white_moves.items())  # Convert to list
        random.shuffle(white_moves)
        for start_pos, possible_moves in white_moves:
            for end_pos in possible_moves:
                next_game = game.copy_game()
                next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                next_game.change_player()
                eval = minimax(next_game, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                
                # Beta pruning
                if beta+100 <= alpha :
                    break
        return max_eval
    else:  # Minimizing for black
        min_eval = float('inf')
        black_moves = list(game.black_moves.items())  # Convert to list
        random.shuffle(black_moves)
        for start_pos, possible_moves in black_moves:
            for end_pos in possible_moves:
                next_game = game.copy_game()
                next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                next_game.change_player()
                eval = minimax(next_game, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                
                # Alpha pruning
                if beta +100<= alpha:
                    break
        return min_eval

def AI(game, depth=15):
    """
    AI for determining the best move using heuristics and minimax evaluation.
    Returns the best move as a tuple (start_pos, end_pos).
    """
    moves_scores = []
    exclude = set()  # Use a set to track excluded moves for better performance
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    b = game.len_list_of_boards < 40  # Depth heuristic

    # Immediate capture heuristic
    if b:
        for start_pos, possible_moves in moves.items():
            x, y = start_pos
            start_piece = game.chess_board[y][x][1]
            color = game.chess_board[y][x][0]
            for end_pos in possible_moves:
                mx, my = end_pos
                piece_end = game.chess_board[my][mx][1]
                color_end = game.chess_board[my][mx][0]
                if start_piece != '-' and piece_end != '-' and color_end != color and tables[piece_end] >= tables[start_piece]:
                    return start_pos, end_pos

    # Positional evaluation with exclusion logic
    if b:
        for start_pos, possible_moves in moves.items():
            for end_pos in possible_moves:
                copy_game = game.copy_game()
                mx, my = end_pos
                copy_game.move_piece(start_pos, mx, my)
                copy_game.all_moves()
                copy_game.change_player()
                pos_moves_0 = copy_game.white_moves if copy_game.turn == 'white' else copy_game.black_moves
                for start, possible_moves1 in pos_moves_0.items():
                    if end_pos in possible_moves1:  # Exclude moves leading to immediate threat
                        exclude.add((start_pos, end_pos))

    # Evaluate all possible moves
    print(exclude)
    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            if (start_pos, end_pos) in exclude:
                continue  # Skip excluded moves
            next_game = game.copy_game()
            next_game.move_piece(start_pos, end_pos[0], end_pos[1])
            next_game.change_player()
            # Evaluate the move using minimax
            score = minimax(next_game, depth - 1)
            moves_scores.append((score, (start_pos, end_pos)))

    # Sort moves based on scores in descending order
    moves_scores.sort(reverse=True, key=lambda x: x[0])

    print(f"Evaluation score: {evaluate(game)}")
    # Return the move with the best score
    if moves_scores:
        return moves_scores[0][1]
    return None
