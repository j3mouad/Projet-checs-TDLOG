from random import shuffle, sample, choice

def shuffle_fischer_row():
    """
    Generates a shuffled row of chess pieces representing a Fischer random (960) chess setup.

    The function arranges chess pieces in a row according to the rules of Fischer random chess,
    where the bishops are placed on opposite-colored squares, the king is placed between two rooks,
    and the remaining pieces (queen and knights) are placed randomly in the available positions.

    The following pieces are placed:
        - Two bishops ('B') on opposite-colored squares
        - A king ('K') placed between two rooks ('R')
        - Two rooks ('R')
        - One queen ('Q')
        - Two knights ('N')

    Returns:
        list: A list of 8 elements representing the row of pieces, where each element is a string
              representing the piece ('B' for bishop, 'K' for king, 'R' for rook, 'Q' for queen, and 'N' for knight).
    """
    # Start with empty row
    row = [''] * 8

    # Place the bishops on opposite-colored squares
    bishop_positions = sample([0, 2, 4, 6], 1) + sample([1, 3, 5, 7], 1)
    row[bishop_positions[0]] = 'B'
    row[bishop_positions[1]] = 'B'

    # Place the king between two rooks
    open_positions = [i for i in range(8) if row[i] == '']
    king_position = choice(open_positions[1:-1])
    row[king_position] = 'K'

    # Rooks on either side of the king
    left_rook_position = choice([pos for pos in open_positions if pos < king_position])
    row[left_rook_position] = 'R'
    right_rook_position = choice([pos for pos in open_positions if pos > king_position])
    row[right_rook_position] = 'R'

    # Fill remaining positions with queen and knights
    remaining_positions = [i for i in range(8) if row[i] == '']
    pieces = ['Q', 'N', 'N']
    shuffle(pieces)
    for pos, piece in zip(remaining_positions, pieces):
        row[pos] = piece

    return row
