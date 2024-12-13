import traceback
import sys
import chess
import chess.engine
import numpy as np
def hash_game(game):
    """
    Hash the current game state. This should return a unique identifier
    for the current board position and turn.
    """
    # For simplicity, you can hash the chessboard and current player
    board_state = ''.join([str(piece) for row in game.chess_board for piece in row])
    turn = game.turn  # Assuming 'white' or 'black' for the turn
    return hash(board_state + turn)
transposition_table = {}

def minimax(game, depth, alpha=float('-inf'), beta=float('inf')):
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
        eval_score = game.evaluate()
        transposition_table[game_hash] = eval_score  # Store evaluation result
        return eval_score

    if game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        for start_pos, possible_moves in game.white_moves.items():
            for end_pos in possible_moves:
                x, y = end_pos
                piece = game.chess_board[y][x]
                game.move_piece(start_pos, x, y)
                game.change_player()
                eval_score = minimax(game, depth - 1, alpha, beta)
                game.back_move_piece(start_pos, end_pos, piece)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune inner loop
        # Store the evaluation result in the transposition table
        transposition_table[game_hash] = max_eval
        return max_eval
    else:  # Minimizing for black
        min_eval = float('inf')
        for start_pos, possible_moves in game.black_moves.items():
            for end_pos in possible_moves:
                x, y = end_pos
                piece = game.chess_board[y][x]
                game.move_piece(start_pos, x, y)
                game.change_player()
                eval_score = minimax(game, depth - 1, alpha, beta)
                game.back_move_piece(start_pos, end_pos, piece)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune inner loop
        # Store the evaluation result in the transposition table
        transposition_table[game_hash] = min_eval
        return min_eval


def AI(game, depth=2):
    """
    AI for determining the best move using minimax evaluation.
    Returns the best move as a tuple (start_pos, end_pos).
    """
    moves_scores = []
    moves = game.white_moves if game.turn == 'white' else game.black_moves

    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            # Create a copy of the game to simulate the move
            
            x, y = end_pos
            piece = game.chess_board[y][x]
            game.move_piece(start_pos, x, y)
            game.change_player()
            eval_score = minimax(game, depth - 1)
            game.back_move_piece(start_pos, end_pos, piece)
            score = minimax(game, depth - 1)
            moves_scores.append((score, (start_pos, end_pos)))
            print(f"Move: {start_pos} -> {end_pos}, Score: {score}")

    # Sort moves by score (higher is better for white, lower for black)
    moves_scores.sort(reverse=(game.turn == 'white'), key=lambda x: x[0])

    # Return the move with the best score
    if moves_scores:
        print(f"Best move: {moves_scores[0][1]} with score {moves_scores[0][0]}")
        return moves_scores[0][1]
    print("No valid moves found")
    return None
