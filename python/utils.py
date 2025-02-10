def has_non_empty_list(map_data):
    """
    Checks if a dictionary has any value that is a non-empty list.

    :param map_data: dict
        The dictionary to check.
    :return: bool
        True if any value is a non-empty list, False otherwise.
    """
    
    for value in map_data.values():
        if isinstance(value, list) and len(value) > 0:
            return True
    return False


def check_list(L, x, y,color='white'):
    # Determine the start and end of the range
    start = min(x, y)
    end = max(x, y)
    piece = color[0]+'R'
    # Check if L[7][i] is '--' for all i in the range [start, end]
    for i in range(start, end + 1):
        if L[7][i] != '--' and L[7][i]!=piece:
            return False
    return True

def find_king_position(chess_board, color):

    """ Args:
            chess_board (list of list of str): A 2D list representing the chess board.
            color (str): The color of the king to find ('white' or 'black').

        Returns:
            tuple: A tuple (x, y) representing the position of the king on the board.
                   Returns None if the king is not found.
    """

    for x in range(8):
        for y in range(8):
            piece = chess_board[y][x]
            if piece == f'{color[0]}K':  # Check for white or black king
                return (x, y)
    return None