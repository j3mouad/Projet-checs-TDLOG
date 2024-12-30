import sys
import numpy as np
import os
import sys
import time
from random import randint
#Code explanation for Mouad

#The first part is implementing the heuristics(evaluation function and how it works)
#You should not really in depth how it works you could just copy past everything 
#The second part includes minimax and AI    
#it uses hashing to improve speed and avoid recalculations
#Here is some explanation of how functions work,
#game.all_moves() generate legal moves of a player 
#you should also see my copy constructor
#good luck for implementation
#I used depth 2 for testing which is really bad 
# note : depth should always be even (really important )
#tell me how much depth can you reach in c++
#if we could reach depth 6 then we could say we have an AI
#if you have questions send them to me on whatsap
# Set up directory if needed (adjust as necessary)
new_dir = '/home/hassene/Desktop/Projet-echecs-TDLOG/build'
os.chdir(new_dir)
if new_dir not in sys.path:
    sys.path.append(new_dir)

# Positional tables for pieces
PAWN_TABLE = np.array([
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [ 10,  10,  10, 10, 10,  10,  10,  10],
    [  5,   5,  10,  20,  20,  10,   5,   5],
    [  0,   0,  10,  30,  30,  10,   0,   0],
    [  5,   5,  20,  40,  40,  20,   5,   5],
    [ 10,  10,  20,  50,  50,  20,  10,  10],
    [ 20,  20,  30,  20,  20,  30,  20,  20],
    [  0,   0,   0,   0,   0,   0,   0,   0],
])

KNIGHT_TABLE = np.array([
    [0,   0,   0,   0,   0,   0,   0,  0],
    [10, 20,   0,   5,   5,   0,  20, 10],
    [-30, 5,  30,  30,  30,  30,   5, -30],
    [10, 10,  30,  30,  30,  30,  10, 10],
    [10, 10,  30,  30,  40,  30,  10, 10],
    [-30, 5,  30,  30,  30,  30,   5, -30],
    [10, 20,   0,   5,   5,   0,  20, 10],
    [0,   0,   0,   0,   0,   0,   0,  0],
])

BISHOP_TABLE = np.array([
    [20,  10, 10,  10,  10, 10, 10, 20],
    [10,  30,   0,   0,   0,   0,  30, 10],
    [10,   0,   5,  10,  10,   5,   0, 10],
    [10,   5,  10,  15,  15,  10,   5, 10],
    [10,   5,  10,  15,  15,  10,   5, 10],
    [10,   0,   5,  10,  10,   5,   0, 10],
    [10,  30,   0,   0,   0,   0,  30, 10],
    [20,  10, 10,  10,  10, 10, 10, 20],
])

ROOK_TABLE = np.array([
    [0,   -50,  10,  15,  15,  10,  -50,  0], 
    [5,   10,  15,  20,  20,  15,   10,  5],
    [10,  15,  20,  25,  25,  20,   15, 10],
    [15,  20,  25,  30,  30,  25,   20, 15],
    [20,  25,  30,  35,  35,  30,   25, 20],
    [15,  20,  25,  30,  30,  25,   20, 15],
    [10,  15,  20,  25,  25,  20,   15, 10],
    [0,   -50,  10,  15,  15,  10,  -50,  0],
])

QUEEN_TABLE = np.array([
    [20, 10, 10,   5,   5, 10, 10, 20],
    [10,  0,  0,   0,   0,  0,  0, 10],
    [10,  0, 50,  50,  50, 50,  0, 10],
    [ 5,  0, 50, 100, 100, 50,  0,  5],
    [ 0, 50, 50, 100, 100, 50, 50,  0],
    [10, 50, 50,  50,  50, 50,  0, 10],
    [10,  0, 50,   0,   0,  0,  0, 10],
    [20, 10, 10,   5,   5, 10, 10, 20],
])

KING_TABLE = np.array([
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [20, 30, 30, 40,  40, 30, 30, 20],
    [10, 20, 20, 20,  20, 20, 20, 10],
    [20, 20,  0,  0,   0,  0, 20, 20],
    [20, 30,100,-40,   0,-40,100,20],
])


tables = {
    'N': (300, KNIGHT_TABLE),
    'Q': (900, QUEEN_TABLE),
    'P': (100, PAWN_TABLE),
    'R': (500, ROOK_TABLE),
    'B': (300, BISHOP_TABLE),
    'K': (100000, KING_TABLE)
}

def evaluate_piece(piece, x, y):
    """Evaluate a single piece's score based on type, position, and color."""
    if piece == '--':
        return 0
    color = piece[0]
    ptype = piece[1]
    my = y if color == 'w' else 7 - y

    if ptype in tables:
        base, table = tables[ptype]
        piece_position_score = table[my][x]
        score = base + piece_position_score
        return score if color == 'w' else -score
    return 0


def evaluate_material(game):
    """Sum material and positional table values."""
    return sum(evaluate_piece(game.chess_board[y][x], x, y) 
               for y in range(8) for x in range(8) 
               if game.chess_board[y][x] != '--')


def get_game_phase(game):
    """
    Determine the game phase based on material.
    A simple heuristic:
    - Count total material (excluding kings).
    - The less material on the board, the closer to the endgame.
    Returns a value between 0 (opening) and 1 (endgame).
    """
    # Example heuristic: sum up material and normalize
    white_material = 0
    black_material = 0
    for y in range(8):
        for x in range(8):
            piece = game.chess_board[y][x]
            if piece != '--':
                p_color = piece[0]
                p_type = piece[1]
                if p_type in tables:
                    val, _ = tables[p_type]
                    if p_color == 'w':
                        white_material += val
                    else:
                        black_material += val

    total_material = white_material + black_material
    # Assuming starting total ~ (2*R=1000 + 2*N=600 + 2*B=600 + Q=1800 + pawns=1600) ~ 5600
    # Adjust these numbers as needed based on actual piece values
    # Let's say if total_material < 2000 -> endgame, else opening.
    phase = max(0, min(1, (5600 - total_material) / 3600))
    return phase


def get_legal_moves_for_color(game, color):
    """Utility to get all legal moves for a given color."""
    return game.white_moves if color == 'white' else game.black_moves

def evaluate_control_of_key_squares(game):
    """Evaluate control of central and other important squares."""
    # As a simple example, still emphasize center squares but now variable based on phase:
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    return sum(20 if game.chess_board[y][x][0] == 'w' else -20
               for x, y in center_squares
               if game.chess_board[y][x] != '--')



def is_in_endgame(game):
    """Heuristic to decide if in endgame."""
    # Use the get_game_phase function. If phase > 0.7, consider endgame.
    return get_game_phase(game) > 0.7


def king_is_active(king_pos):
    """Check if king is active (centralized) - relevant in endgame."""
    if king_pos is None:
        return False
    x, y = king_pos
    # Active if closer to center in endgame
    return (2 <= x <= 5 and 2 <= y <= 5)


def evaluate_endgame_features(game):
    """Evaluate features specific to the endgame."""
    score = 0
    if is_in_endgame(game):
        white_king_pos = find_king_position(game, 'white')
        black_king_pos = find_king_position(game, 'black')
        if king_is_active(white_king_pos):
            score += 50
        if king_is_active(black_king_pos):
            score -= 50
    return score


def find_king_position(game, color):
    """Returns the position of the king for a given color."""
    for y in range(8):
        for x in range(8):
            piece = game.chess_board[y][x]
            if piece == f'{color[0]}K':  # White king or black king
                return (x, y)
    return None
def center_control(game) :
    score = 0 
    for start_pos, possible_moves in game.white_moves.items():
        for end_pos in possible_moves :
            x,y = end_pos 
            if (x>2 and x<5 and y>2 and y<5) :
                score+=1
    for start_pos, possible_moves in game.black_moves.items():
        for end_pos in possible_moves :
            x,y = end_pos 
            if (x>2 and x<5 and y>2 and y<5) :
                score-=1
    return score

def evaluate(game,transposition_table):
    """Calculates the total evaluation score for the game based on various factors."""
    # Base material and position evaluation
    hash = hash_game(game)
    if (hash in transposition_table) :
        return transposition_table[hash] 
    material_score = evaluate_material(game)

    # Mobility


    # Control of key squares
    control_score = evaluate_control_of_key_squares(game)

    # Endgame features
    endgame_score = evaluate_endgame_features(game)

    # Determine game phase and interpolate
    phase = get_game_phase(game)  
    opening_weight = 1 - phase
    endgame_weight = phase

    # Combine scores
    # Material remains essential throughout, but other factors change importance over time.
    total_score = (
        material_score*1 +
        control_score * (0.6 * opening_weight + 0.3 * endgame_weight) +
        endgame_score * endgame_weight
    )

    return total_score

#-------------------------------------------------------------------------#
#This is second part 
def hash_game(game):
    """
    Hash the current game state. This should return a unique identifier
    for the current board position and turn.
    """
    # For simplicity, you can hash the chessboard and current player
    board_state = ''.join([str(piece) for row in game.chess_board for piece in row])
    turn = game.turn  # Assuming 'white' or 'black' for the turn
    return hash(board_state + turn)
def minimax(game, depth, transposition_table, alpha=float('-inf'), beta=float('inf')):

    # Get the hash of the current game state
    game_hash = hash_game(game)

    # Check if the current game state has already been evaluated
    if game_hash in transposition_table:
        return transposition_table[game_hash]

    if not game.running:
        if game.winner == 'Stalemate':
            return 0
        return 1e9 if game.winner == 'white' else -1e9

    if depth == 0:
        eval_score = evaluate(game,transposition_table)
        transposition_table[game_hash] = eval_score  # Store evaluation result
        return eval_score
    
    if game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        for start_pos, possible_moves in game.white_moves.items():
            i = 0
            for end_pos in possible_moves:
                if (i>0) :
                    s = randint(1,100)
                    if (s<95) :
                        continue 

                i+=1
                copy_game = game.copy_game()
                x, y = end_pos
                copy_game.move_piece(start_pos, x, y)
                copy_game.change_player()
                copy_game.all_moves()
                eval_score = minimax(copy_game, depth - 1, transposition_table, alpha, beta)
                game_hash = hash_game(game)
                transposition_table[game_hash] = eval_score
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune outer loop
            if beta <= alpha:
                break  # Prune outer loop
        # Store the evaluation result in the transposition table
        return max_eval

    else:  # Minimizing for black
        min_eval = float('inf')
        for start_pos, possible_moves in game.black_moves.items():
            i = 0
            for end_pos in possible_moves:
                if (i>0) :
                    s = randint(1,100)
                    if (s<95) :
                        continue 
                copy_game = game.copy_game()
                x, y = end_pos
                copy_game.move_piece(start_pos, x, y)
                copy_game.change_player()
                copy_game.all_moves()
                eval_score = minimax(copy_game, depth - 1, transposition_table, alpha, beta)
                min_eval = min(min_eval, eval_score)
                game_hash = hash_game(game)
                transposition_table[game_hash] = eval_score
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune outer loop
            if beta <= alpha:
                break  # Prune outer loop
        return min_eval

def AI(game, depth=4):
    """
    AI for determining the best move using minimax evaluation.
    Returns the best move as a tuple (start_pos, end_pos).
    depth must be pair so that it works
    """
    transposition_table={}
    game.all_moves()
    game.change_player()
    game.all_moves()        
    game.change_player()
    moves_scores = []
    s = 0 
    i = 0
    eval_score = evaluate(game,{})
    print(game.evaluate0())
    print(eval_score)
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    total_time = 0

    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            i+=1
            start_time = time.time()  # Record the start time
            # Create a copy of the game to simulate the move
            copy_game = game.copy_game()
            copy_game.all_moves()
            x, y = end_pos
            copy_game.move_piece(start_pos, x, y)
            copy_game.change_player()
            score = (minimax(copy_game,1,{}))
            print(score)
            if (game.black and score<=eval_score) :
                print('continue black')
                s+=1
                print(s,'  ',i)
                #continue
            if (game.white and score>=eval_score) :
                print('continue white')
                s+=1
                print(s,' ',i)
                #continue

            score = minimax(copy_game, depth - 1,transposition_table)
            moves_scores.append((score, (start_pos, end_pos)))
            print(f"Move: {start_pos} -> {end_pos}, Score: {score}")
            end_time = time.time()
            print(end_time-start_time)
            total_time += end_time - start_time
    # Sort moves by score (higher is better for white, lower for black)
    moves_scores.sort(reverse=(game.turn == 'white'), key=lambda x: x[0])

    # Return the move with the best score
    if moves_scores:
        print(f"Best move: {moves_scores[0][1]} with score {moves_scores[0][0]}")
        print(total_time)
        return moves_scores[0][1]
    print("No valid moves found")
    return None

def AI_hard(game) :
    game.all_moves()
    game.change_player()
    game.all_moves()        
    game.change_player()
    moves_scores = []

    moves = game.white_moves if game.turn == 'white' else game.black_moves
    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            copy_game = game.copy_game()
            copy_game.all_moves()
            x, y = end_pos
            copy_game.move_piece(start_pos, x, y)
            copy_game.change_player()
            score = copy_game.evaluate0()
            moves_scores.append((score, (start_pos, end_pos)))


    moves_scores.sort(reverse=True, key=lambda x: x[0])

    # Return the move with the best score
    print(moves_scores)
    if moves_scores:
        print(f"Best move: {moves_scores[0][1]} with score {moves_scores[0][0]}")
        return moves_scores[0][1]
    print("No valid moves found")
    return None


    