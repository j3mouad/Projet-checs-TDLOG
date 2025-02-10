from enum import Enum

class PieceType(Enum):
    """
    Enumeration representing the various chess piece types used in the game.

    Each member of this enumeration corresponds to a specific chess piece,
    represented by a unique single-character code:

      - PAWN: Represents a Pawn, denoted by 'P'.
      - ROOK: Represents a Rook, denoted by 'R'.
      - WAZIR: Represents a Wazir (a fairy chess piece), denoted by 'W'.
      - FERZ: Represents a Ferz (a fairy chess piece), denoted by 'F'.
      - MYSTERIOUS: Represents a Mysterious piece with unpredictable behavior, denoted by 'M'.
      - KNIGHT: Represents a Knight, denoted by 'N'.
      - CAMEL: Represents a Camel (a fairy chess piece), denoted by 'C'.
      - BISHOP: Represents a Bishop, denoted by 'B'.
      - KING: Represents a King, denoted by 'K'.
      - QUEEN: Represents a Queen, denoted by 'Q'.
    """

    PAWN = 'P'
    ROOK = 'R'
    WAZIR = 'W'
    FERZ = 'F'
    MYSTERIOUS = 'M'
    KNIGHT = 'N'
    CAMEL = 'C'
    BISHOP = 'B'
    KING = 'K'
    QUEEN = 'Q'