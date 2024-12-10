import chess
import chess.engine
import numpy as np

def minimax(game, depth, alpha=float('-inf'), beta=float('inf')):
    if not game.running:
        if game.winner == 'Stalemate':
            return 0
        if game.winner == 'white':
            return 1e9
        return -1e9

    if depth == 0:
        print('I am doing evalutation')
        return game.evaluate()

    if game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        white_moves = list(game.white_moves.items())
        for start_pos, possible_moves in white_moves:
            for end_pos in possible_moves:
                next_game = game.copy_game()
                next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                next_game.change_player()
                eval_score = minimax(next_game, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:  # Minimizing for black
        min_eval = float('inf')
        black_moves = list(game.black_moves.items())
        for start_pos, possible_moves in black_moves:
            for end_pos in possible_moves:
                next_game = game.copy_game()
                next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                next_game.change_player()
                eval_score = minimax(next_game, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval


def AI(game, depth=2):
    """
    AI for determining the best move using heuristics and minimax evaluation.
    Returns the best move as a tuple (start_pos, end_pos).
    """
    print ('I am in AI now')
    moves_scores = []
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    for start_pos, possible_moves_0 in moves.items():
        # Evaluate all possible moves that are not excluded
        for start_pos, possible_moves_0 in moves.items():
            for end_pos in possible_moves_0:
 
                next_game = game.copy_game()
                next_game.move_piece(start_pos, end_pos[0], end_pos[1])
                next_game.change_player()
                # Evaluate the move using minimax
                score = minimax(next_game, depth - 1)
                moves_scores.append((score, (start_pos, end_pos)))

        moves_scores.sort(reverse=True, key=lambda x: x[0])

        # Return the move with the best score
        if moves_scores:
            return moves_scores[0][1]
        return None
