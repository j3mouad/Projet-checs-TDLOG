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
    [  0,   0,   0,   0,   0,   0,   0,   0],  
    [ 10,  10,  10, -10, -10,  10,  10,  10],  
    [ 10,  10,  20,  20,  20,  20,  10,  10],  
    [  5,  10,  10,  25,  25,  10,  10,   5],  
    [  0,   0,   0,  20,  20,   0,   0,   0],  
    [  5,  -5, -10,   0,   0, -10,  -5,   5],  
    [  5,  10,  10, -20, -20,  10,  10,   5], 
    [  0,   0,   0,   0,   0,   0,   0,   0], 
]
KNIGHT_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [40, 20, 0, 5, 5, 0, 20, 40],
    [-30, 5, 200, 30, 30, 200, 5, -30],
    [30, 10, 60, 80, 80, 60, 10, 30],
    [30, 10, 60, 80, 80, 60, 10, 30],
    [-30, 5, 200, 30, 30, 200, 5, -30],
    [40, 20, 0, 5, 5, 0, 20, 40],
    [0, 00, 0, 0, 0, 0, 00, 0],
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
    [50, 0, 90, 100, 100, 90, 00, 50],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [100, 0, 0, 0, 0, 0, 0, 100],
    [100, 0, 0, 0, 0, 0, 0, 100],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [50, 0, 0, 0, 0, 0, 0, 50],
    [50, 00, 90, 100, 100, 90, 0, 50]
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
    [20, 30, 100, -40, 0, -40, 100, 20]
]


PIECE_VALUES = {
    'P': 1000,
    'N': 3000,
    'B': 3000,
    'R': 5000,
    'Q': 9000,
    'K': 1000000
}

def evaluate_piece(piece, x, y):
    """Evaluates the score of a piece based on its type, position, and game phase."""
    my = y if piece[0] == 'w' else 7 - y
    
    tables = {
        'N': (3000, KNIGHT_TABLE),
        'Q': (9000, QUEEN_TABLE),
        'P': (1000, PAWN_TABLE),
        'R': (5000, ROOK_TABLE),
        'B': (3000, BISHOP_TABLE),
        'K': (100000, KING_TABLE)
    }
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
def evaluate_capture(attacking_piece, target_piece):
    PIECE_VALUES = {
        'P': 100,
        'N': 300,
        'B': 300,
        'R': 500,
        'Q': 900,
        'K': 20000
    }
    if (target_piece=='--') :
        return 0 
    if (attacking_piece=='--') :
        return 0 
    if (target_piece[0]==attacking_piece[0]) :
        return 0 
    coeff = 1 if (target_piece[0]=='w') else -1
    return (PIECE_VALUES[target_piece[1]] - PIECE_VALUES[attacking_piece[1]])*coeff
def evaluate_captures(game):
    """Evaluates the score for potential captures on the board."""
    capture_score = 0
    game0 = game.copy_game()
    game0.all_moves() 
    for key, value in game0.white_moves.items():
        x,y = key 
        attacking_piece = game0.chess_board[y][x]
        if (len(value)>0) :
            for move in value :

                if len(move)>0 and move[0]!=-1:  
                    mx,my= move
                    target_piece = game0.chess_board[my][mx]
                    capture_score+=evaluate_capture(attacking_piece,target_piece)
    
    for key, value in game0.black_moves.items():
        x,y = key 
        attacking_piece = game0.chess_board[y][x]
        if (len(value)>0):
            for move in value : 
                if (len(move)>0 and move[0]!=-1) :
                    mx,my= move
                    target_piece = game0.chess_board[my][mx]
                    capture_score+=evaluate_capture(attacking_piece,target_piece)

    return capture_score

def evaluate(game):
    """Calculates the total evaluation score for the game based on various factors."""
    total_score = 0 

    # Evaluate material
    material_score = evaluate_material(game)
    total_score += material_score

    # Evaluate central control and mobility
    #central_control_score = evaluate_control_and_mobility(game)
    #total_score += central_control_score

    # Evaluate capturing opportunities
    #capture_score = evaluate_captures(game)
    #total_score += capture_score

    # King safety

    #king_safety_score = king_safety(game.turn, game.white_king_position, game.black_king_position)
    #total_score += king_safety_score

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


def evaluate_control_and_mobility(game):
    """Evaluates central control and piece mobility."""
    score = 0
    # Evaluate central control (favor pieces in the center)
    center = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for x, y in center:
        piece = game.chess_board[x][y]
        if piece == 'wP':
            score += 10
        elif piece == 'bP':
            score -= 10

    # Evaluate piece mobility
    return score

def evaluate_opening(game):
    score = 0
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    
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

def minimax(game, depth):
    if (not game.running) :
        if (game.winner=='Stalemate') :
            return 0
        if (game.winner=='white') :
            return 1e9
        return -1e9
    if depth == 0 :
        return evaluate(game)
    if  game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        for move in game.white_moves.values():
            for end_pos in move:
                next_game = game.copy_game()
                next_game.move_piece(move[0], end_pos[0], end_pos[1])
                next_game.change_player()
                eval = minimax(next_game, depth - 1)
                max_eval = max(max_eval, eval)

        return max_eval
    else:  # Minimizing for black
        min_eval = float('inf')
        for move in game.black_moves.values():
            for end_pos in move:
                next_game = game.copy_game()
                next_game.move_piece(move[0], end_pos[0], end_pos[1])
                next_game.change_player()
                eval = minimax(next_game, depth - 1)
                min_eval = min(min_eval, eval)

        return min_eval


def AI(game, depth=3):
    
    moves_scores = []
    # Determine moves based on whose turn it is
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    
    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            next_game = game.copy_game()
            next_game.move_piece(start_pos, end_pos[0], end_pos[1])
            next_game.change_player()
            # Evaluate the move using minimax
            score = minimax(next_game, depth - 1)
            moves_scores.append((score,(start_pos, end_pos)))
    
    # Sort moves based on the score
    moves_scores.sort()
    print(moves_scores)
    print(evaluate(game))
    # Return the move with the best score
    if moves_scores:
        score ,best_move = moves_scores[0]
        return best_move  # You could also return the score if needed
    return None
