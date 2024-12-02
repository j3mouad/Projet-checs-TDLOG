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

def evaluate_piece(piece) : 
    s = 0
    if (piece[1]=='N') : 
        s = 300
    if (piece[1]=='Q') :
        s = 900
    if (piece[1]=='P') : 
        s = 100
    if (piece[1]=='R') :
        s = 500
    if (piece[1] == 'B') :
        s = 320 
    if (piece[1]=='K') :
        s = 10000
    if (piece[0]=='b') : 
        s*=-1
    return s

def evaluate(game) :
    result = 0 
    for x in range(8) :
        for y in range(8) :
            result += evaluate_piece(game.chess_board[x][y]) 
    return result 
def AI(game):
    score = 1e9  # Initialize with a very low score
    start = None  # Best move start position
    end = None  # Best move end position
    # Iterate over black pieces and their possible moves
    for start_pos, possible_moves in game.black_moves.items():
        # If there are no possible moves for this piece, continue
        if not possible_moves:
            continue
        
        # Loop through each move for the current piece
        random.shuffle(possible_moves)
        for end_pos in possible_moves:
            # Save the current game state (for move reversion)
            if (len(end_pos)<2) :
                continue 
            copy_game = game.copy_game()
            
            # Perform the move
            copy_game.move_piece(start_pos, end_pos[0],end_pos[1])
            
            # Evaluate the move
            current_score = evaluate(copy_game)
            
            # If this move results in a better score, update the best move
            if current_score < score:
                score = current_score
                start = start_pos
                end = end_pos
            if (current_score==score and random.randint(0,1)==1) :
                score = current_score
                start = start_pos
                end = end_pos

    return start, end