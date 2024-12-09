import os
import sys
import random

# Set up directory if needed (adjust as necessary)
new_dir = '/home/hassene/Desktop/Projet-echecs-TDLOG/build'
os.chdir(new_dir)
if new_dir not in sys.path:
    sys.path.append(new_dir)

# Positional tables for pieces
PAWN_TABLE = [
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [ 10,  10,  10, -10, -10,  10,  10,  10],
    [  5,   5,  10,  20,  20,  10,   5,   5],
    [  0,   0,  10,  30,  30,  10,   0,   0],
    [  5,   5,  20,  40,  40,  20,   5,   5],
    [ 10,  10,  20,  50,  50,  20,  10,  10],
    [ 20,  20,  30,  60,  60,  30,  20,  20],
    [  0,   0,   0,   0,   0,   0,   0,   0],
]

KNIGHT_TABLE = [
    [0,   0,   0,   0,   0,   0,   0,  0],
    [40, 20,   0,   5,   5,   0,  20, 40],
    [-30, 5,  30,  30,  30,  30,   5, -30],
    [10, 10,  60,  40,  40,  60,  10, 10],
    [10, 10,  60,  80,  80,  60,  10, 10],
    [-30, 5,  30,  30,  30,  30,   5, -30],
    [40, 20,   0,   5,   5,   0,  20, 40],
    [0,   0,   0,   0,   0,   0,   0,  0],
]

BISHOP_TABLE = [
    [20,  10, 100,  10,  10, 100, 10, 20],
    [10,   0,   0,   0,   0,   0,  0, 10],
    [10,   0,   5,  10,  10,   5,  0, 10],
    [10,   5,  10,  15,  15,  10,  5, 10],
    [10,   5,  10,  15,  15,  10,  5, 10],
    [10,   0,   5,  10,  10,   5,  0, 10],
    [10,   0,   0,   0,   0,   0,  0, 10],
    [20,  10, 100,  10,  10, 100, 10, 20],
]

ROOK_TABLE = [
    [50,   0,  40,  10,  40,  40,   0, 50],
    [50,   0,   0,   0,   0,   0,   0, 50],
    [50,   0,   0,   0,   0,   0,   0, 50],
    [100,  0,   0,   0,   0,   0,   0,100],
    [100,  0,   0,   0,   0,   0,   0,100],
    [50,   0,   0,   0,   0,   0,   0, 50],
    [50,   0,   0,   0,   0,   0,   0, 50],
    [50,   0,  40,  10,  40,  40,   0, 50],
]

QUEEN_TABLE = [
    [20, 10, 10,   5,   5, 10, 10, 20],
    [10,  0,  0,   0,   0,  0,  0, 10],
    [10,  0, 50,  50,  50, 50,  0, 10],
    [ 5,  0, 50, 100, 100, 50,  0,  5],
    [ 0, 50, 50, 100, 100, 50, 50,  0],
    [10, 50, 50,  50,  50, 50,  0, 10],
    [10,  0, 50,   0,   0,  0,  0, 10],
    [20, 10, 10,   5,   5, 10, 10, 20],
]

KING_TABLE = [
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [20, 30, 30, 40,  40, 30, 30, 20],
    [10, 20, 20, 20,  20, 20, 20, 10],
    [20, 20,  0,  0,   0,  0, 20, 20],
    [20, 30,1000,-40,   0,-40,1000,20],
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
    material_score = 0
    for y in range(8):
        for x in range(8):
            piece = game.chess_board[y][x]
            if piece != '--':
                material_score += evaluate_piece(piece, x, y)
    return material_score


# ---------- NEW / IMPROVED HELPER FUNCTIONS ----------

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


def evaluate_mobility(game):
    """Evaluate how many moves each side has. More mobility = better position."""
    white_mobility = sum(len(m) for m in game.white_moves.values())
    black_mobility = sum(len(m) for m in game.black_moves.values())
    # Give a small bonus based on mobility difference
    return (white_mobility - black_mobility) * 0.1


def is_isolated_pawn(x, y, game):
    """Check if a pawn is isolated (no friendly pawns on adjacent files)."""
    piece = game.chess_board[y][x]
    if piece == '--' or piece[1] != 'P':
        return False
    color = piece[0]
    file_offsets = [-1, 1]
    for offset in file_offsets:
        nx = x + offset
        if 0 <= nx < 8:
            for ny in range(8):
                p = game.chess_board[ny][nx]
                if p != '--' and p[1] == 'P' and p[0] == color:
                    return False
    return True




def evaluate_pawn_structure(game):
    """Evaluate pawn structure (isolated, passed pawns)."""
    score = 0
    for y in range(8):
        for x in range(8):
            piece = game.chess_board[y][x]
            if piece != '--' and piece[1] == 'P':
                color = piece[0]
                base = 1 if color == 'w' else -1
                if is_isolated_pawn(x, y, game):
                    score -= base * 30

    return score





def evaluate_control_of_key_squares(game):
    """Evaluate control of central and other important squares."""
    # Already considered a bit in your opening evaluation. Let's extend it:
    # Add more squares (e.g., outposts) that are valuable in mid/endgame.

    # As a simple example, still emphasize center squares but now variable based on phase:
    center_squares = [(3,3),(3,4),(4,3),(4,4)]
    score = 0
    for (x, y) in center_squares:
        piece = game.chess_board[y][x]
        if piece != '--':
            if piece[0] == 'w':
                score += 20
            else:
                score -= 20
    return score


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


def evaluate(game):
    """Calculates the total evaluation score for the game based on various factors."""
    # Base material and position evaluation
    material_score = evaluate_material(game)

    # Mobility
    mobility_score = evaluate_mobility(game)

    # Pawn structure
    pawn_structure_score = evaluate_pawn_structure(game)

    # King safety
    king_safety_score = 0

    # Piece coordination
    piece_coordination_score = 0

    # Control of key squares
    control_score = evaluate_control_of_key_squares(game)

    # Endgame features
    endgame_score = evaluate_endgame_features(game)

    # Determine game phase and interpolate
    phase = get_game_phase(game)  
    # opening_weight ~ (1 - phase)
    # endgame_weight ~ phase
    opening_weight = 1 - phase
    endgame_weight = phase

    # Combine scores
    # Material remains essential throughout, but other factors change importance over time.
    total_score = (
        material_score +
        mobility_score * 0.5 +
        pawn_structure_score * 0.5 +
        king_safety_score * 1.0 +
        piece_coordination_score * 0.5 +
        control_score * (0.5 * opening_weight + 0.2 * endgame_weight) +
        endgame_score * endgame_weight
    )

    return total_score


# ---------------- MINIMAX AND AI --------------------

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
        white_moves = list(game.white_moves.items())
        random.shuffle(white_moves)
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
        random.shuffle(black_moves)
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


def AI(game, depth=4):
    """
    AI for determining the best move using heuristics and minimax evaluation.
    Returns the best move as a tuple (start_pos, end_pos).
    """
    moves_scores = []
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    b = game.len_list_of_boards < 25  # Depth heuristic

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
                # Attempt immediate beneficial capture
                if (start_piece != '-' and piece_end != '-' and
                    color_end != color and tables.get(piece_end, (0,[]))[0] >= tables.get(start_piece,(0,[]))[0]):
                    return start_pos, end_pos

    # Positional evaluation with exclusion logic
    exclude = set()

    for start_pos, possible_moves_0 in moves.items():
        for end_pos in possible_moves_0:
            copy_game = game.copy_game()
            mx, my = end_pos
            copy_game.move_piece(start_pos, mx, my)
            copy_game.all_moves()
            copy_game.change_player()

                # Get opponent's possible moves
            pos_moves_0 = copy_game.white_moves if copy_game.turn == 'white' else copy_game.black_moves

            threatened = False
            end_piece = copy_game.chess_board[my][mx]
            if end_piece != '--':
                end_piece_val = tables[end_piece[1]][0] if end_piece[1] in tables else 0
                for st, pmoves1 in pos_moves_0.items():
                    if end_pos in pmoves1:
                        sx, sy = st
                        start_piece_at = copy_game.chess_board[sy][sx]
                        if start_piece_at != '--':
                            start_piece_val = tables[start_piece_at[1]][0] if start_piece_at[1] in tables else 0
                            # If the opponent can capture back with equal or greater value piece, risky move
                            if end_piece_val >= start_piece_val :
                                threatened = True
                                break
                            if (b) :
                                threatened = True

                if threatened:
                    exclude.add((start_pos, end_pos))

    # Evaluate all possible moves that are not excluded
    for start_pos, possible_moves_0 in moves.items():
        for end_pos in possible_moves_0:
            if (start_pos, end_pos) in exclude:
                continue
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