#include "board.h"

/**
 * @brief Generates a random back rank configuration for Chess960.
 *
 * This function generates a randomized configuration for the back rank pieces,
 * ensuring that:
 * - The two bishops are placed on opposite-colored squares.
 * - The king is positioned between the two rooks.
 *
 * @return A vector of pairs where each pair consists of an integer (the original position)
 *         and a string (the name of the piece).
 */
vector<pair<int, string>> generateRandomBackRank()
{
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    mt19937 rng(seed);
    vector<pair<int, string>> pieces = {
        make_pair(0, "Rook"), make_pair(1, "Knight"), make_pair(2, "Bishop"),
        make_pair(3, "Queen"), make_pair(4, "King"), make_pair(5, "Bishop"),
        make_pair(6, "Knight"), make_pair(7, "Rook")};

    while (true)
    {
        shuffle(pieces.begin(), pieces.end(), rng);

        int bishop1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string> &p)
                                 { return p.second == "Bishop"; }) -
                         pieces.begin();
        int bishop2Pos = find_if(pieces.begin() + bishop1Pos + 1, pieces.end(), [](const pair<int, string> &p)
                                 { return p.second == "Bishop"; }) -
                         pieces.begin();

        // Ensure bishops are on opposite colored squares.
        if ((bishop1Pos % 2 == bishop2Pos % 2))
        {
            continue;
        }

        int kingPos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string> &p)
                              { return p.second == "King"; }) -
                      pieces.begin();
        int rook1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string> &p)
                               { return p.second == "Rook"; }) -
                       pieces.begin();
        int rook2Pos = find_if(pieces.begin() + rook1Pos + 1, pieces.end(), [](const pair<int, string> &p)
                               { return p.second == "Rook"; }) -
                       pieces.begin();

        // Ensure the king is between the two rooks.
        if (rook1Pos < kingPos && kingPos < rook2Pos)
        {
            break; // Valid configuration found.
        }
    }

    return pieces;
}

/**
 * @brief Transforms the board into a Fischer-Random (Chess960) configuration.
 *
 * This method generates a random back rank configuration using @ref generateRandomBackRank and
 * rearranges the board accordingly. To avoid overwriting pieces during the rearrangement, the
 * pieces are first moved to temporary positions (rows 2 and 5) and then placed into their new
 * positions on rows 0 and 7.
 */
void Board::transformToFisher()
{
    cout << 1 << endl;
    vector<pair<int, string>> backRank = generateRandomBackRank();

    for (pair<int, string> couple : backRank)
    {
        cout << couple.second << " : " << couple.first << endl;
    }
    cout << 2 << endl;

    // Temporarily move pieces to avoid collision.
    for (int i = 0; i < 8; ++i)
    {
        movePiece(Point(i, 0), Point(i, 2));
        movePiece(Point(i, 7), Point(i, 5));
    }

    // Reposition pieces to the new back rank configuration.
    for (int i = 0; i < 8; ++i)
    {
        movePiece(Point(backRank[i].first, 2), Point(i, 0));
        movePiece(Point(backRank[i].first, 5), Point(i, 7));
    }
}

/**
 * @brief Evaluates the score of the piece located at the given board coordinates.
 *
 * This function retrieves the piece at the specified (x, y) location and calculates its score.
 * The score is modified by a factor: +1 for white pieces and -1 for black pieces.
 * If the square is empty, the function returns 0.
 *
 * @param x The x-coordinate on the board.
 * @param y The y-coordinate on the board.
 * @return The evaluation score of the piece at (x, y).
 */
int Board::evaluatePiece(int x, int y)
{
    Piece piece = getPiece(Point(x, y));
    if (piece.getName() == "EmptyPlace")
    {
        return 0;
    }
    int factor = -1 + 2 * (piece.getColor() == "white");
    int value = scores[piece.getName()];
    // Optional: Add positional score contribution.
    // value += piece.getScore(x, (8 - 2 * y) * (piece.getColor() == "white") + y);
    value *= factor;
    return value;
}

/**
 * @brief Evaluates the entire board by summing the scores of all pieces.
 *
 * Iterates over every square on the board (8x8) and accumulates the score of each piece by calling
 * @ref evaluatePiece.
 *
 * @return The total evaluation score of the board.
 */
int Board::evaluateBoard()
{
    int value = 0;

    for (int x = 0; x < 8; x++)
    {
        for (int y = 0; y < 8; y++)
        {
            value += evaluatePiece(x, y);
        }
    }

    return value;
}

#include "board.h"

/**
 * @brief Constructs a new Board object using an initial board array.
 *
 * This constructor initializes the board from a one-dimensional array of 64 Piece
 * objects. The pieces are copied into the board’s two-dimensional array, row by row.
 *
 * @param initial__board Pointer to an array of 64 Pieces representing the initial board.
 * @param Turn A string representing which side moves first (e.g., "white" or "black").
 */
Board::Board(Piece *initial__board, string Turn)
{
    turn = Turn;

    for (int idxY = 0; idxY < 8; idxY++)
    {
        for (int idxX = 0; idxX < 8; idxX++)
        {
            board[idxY][idxX] = initial__board[idxX + 8 * idxY];
        }
    }
}

/**
 * @brief Copy constructor for the Board class.
 *
 * Creates a deep copy of an existing Board object. All board state variables,
 * including the turn, king positions, castling rights, en passant square, move history,
 * and evaluation state, are copied from the provided object.
 *
 * @param other The Board object from which to create a copy.
 */
Board::Board(const Board &other)
{
    turn = other.turn;
    WhiteKingPos = other.WhiteKingPos;
    BlackKingPos = other.BlackKingPos;
    LeftCastleBlack = other.LeftCastleBlack;
    RightCastleBlack = other.RightCastleBlack;
    LeftCastleWhite = other.LeftCastleWhite;
    RightCastleWhite = other.RightCastleWhite;
    enPassant = other.enPassant;
    Hashmap = other.Hashmap;
    isMinimaxCalculated = other.isMinimaxCalculated;
    Minimaxscore = other.Minimaxscore;
    depthMap = other.depthMap;

    for (int idx1 = 0; idx1 < 8; idx1++)
    {
        for (int idx2 = 0; idx2 < 8; idx2++)
        {
            board[idx1][idx2] = other.board[idx1][idx2];
        }
    }

    moves = other.moves;
}

/*
bool testCopyConstructor()
{
    Board secondBoard = initial_board;
    secondBoard.movePiece(Point(0, 1), Point(0, 3));
    return initial_board.getPiece(Point(0, 3)).getName() == "EmptyPlace";
}
this function was already tested;
*/

/**
 * @brief Changes the turn from the current player to the other.
 *
 * If the current turn is "white", it is switched to "black", and vice versa.
 */
void Board::changeTurn()
{
    if (turn == "white")
    {
        turn = "black";
    }
    else
    {
        turn = "white";
    }
}

/**
 * @brief Retrieves the piece located at a specific point on the board.
 *
 * @param point A Point object specifying the (x, y) coordinates on the board.
 * @return The Piece object at the specified board position.
 */
Piece Board::getPiece(Point point)
{
    return board[point.getY()][point.getX()];
}

/**
 * @brief Places a piece at the specified position on the board.
 *
 * @param point A Point object specifying the (x, y) coordinates on the board.
 * @param piece The Piece object to be placed at the given position.
 */
void Board::setPiece(Point point, Piece piece)
{
    board[point.getY()][point.getX()] = piece;
}

/**
 * @brief Computes all possible moves for the piece at the given board position.
 *
 * This function examines the piece located at the specified position and calculates
 * all the legal moves it can make. It takes into account the piece's movement set,
 * whether it moves by sliding or in fixed steps, and any obstacles or enemy pieces that
 * might block its path or be captured.
 *
 * @param position A Point object representing the current location of the piece.
 * @return A vector of Point objects, each representing a valid destination for the move.
 */
vector<Point> Board::getPossibleMoves(Point position)
{
    int movex, movey;
    int piecePositionX, piecePositionY;
    int currPosX, currPosY;
    int multiplier;
    vector<Point> VectOfMoves;
    
    piecePositionX = position.getX();
    piecePositionY = position.getY();
    Piece piece = board[piecePositionY][piecePositionX];

    // Only consider moves for the piece whose color matches the current turn.
    if (piece.getColor() != turn)
    {
        return VectOfMoves;
    }

    const Point *elemMoves = piece.getElemMoveSet();

    // If the piece uses the move set as its attack set.
    if (piece.isMoveSetAttackMoveSet())
    {
        for (int idx = 0; idx < piece.numberOfElemMoves(); idx++)
        {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true)
            {
                // For non-sliding pieces, only allow one step.
                if (multiplier == 2 && piece.hasInfiniteMoves() == false)
                {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 &&
                    currPosY >= 0 && currPosY < 8 &&
                    board[currPosY][currPosX].getColor() != turn)
                {
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX, currPosY));
                    if (board[currPosY][currPosX].getName() != "EmptyPlace")
                    {
                        break;
                    }
                }
                else
                {
                    break;
                }
            }
        }
    }
    else
    {
        // If the piece has a separate attack move set.
        const Point *attackMoves = piece.getAttackMoveSet();
        for (int idx = 0; idx < piece.numberOfElemMoves(); idx++)
        {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true)
            {
                if (multiplier == 2 && piece.hasInfiniteMoves() == false)
                {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 &&
                    currPosY >= 0 && currPosY < 8 &&
                    board[currPosY][currPosX].getName() == "EmptyPlace")
                {
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX, currPosY));
                }
                else
                {
                    break;
                }
            }
        }
        for (int idx = 0; idx < piece.numberOfAttackMoves(); idx++)
        {
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
            currPosY = piecePositionY + movey;
            if (currPosX >= 0 && currPosX < 8 &&
                currPosY >= 0 && currPosY < 8 &&
                board[currPosY][currPosX].getColor() != turn &&
                board[currPosY][currPosX].getColor() != "none")
            {
                multiplier++;
                VectOfMoves.push_back(Point(currPosX, currPosY));
            }
        }
    }
    return VectOfMoves;
}

/**
 * @brief Computes all possible attack moves for the piece at a given position.
 *
 * This function calculates and returns a vector of potential attack destinations for the
 * piece located at the specified board position. It distinguishes between pieces that use
 * their standard move set as their attack set and those that have a separate attack move set.
 *
 * @param position The current position of the piece.
 * @return A vector of Point objects representing valid attack destinations.
 */
 vector<Point> Board::getPossibleAttacks(Point position)
 {
     int movex, movey;
     int piecePositionX, piecePositionY;
     int currPosX, currPosY;
     int multiplier;
     vector<Point> VectOfMoves;
     
     piecePositionX = position.getX();
     piecePositionY = position.getY();
     Piece piece = board[piecePositionY][piecePositionX];
     
     // Only compute attacks for pieces that match the current turn.
     if (piece.getColor() != turn)
     {
         return VectOfMoves;
     }
     
     const Point *elemMoves = piece.getElemMoveSet();
     
     if (piece.isMoveSetAttackMoveSet())
     {
         for (int idx = 0; idx < piece.numberOfElemMoves(); idx++)
         {
             movex = elemMoves[idx].getX();
             movey = elemMoves[idx].getY();
             multiplier = 1;
             while (true)
             {
                 if (multiplier == 2 && piece.hasInfiniteMoves() == false)
                 {
                     break;
                 }
                 currPosX = piecePositionX + multiplier * movex;
                 currPosY = piecePositionY + multiplier * movey;
                 if (currPosX >= 0 && currPosX < 8 &&
                     currPosY >= 0 && currPosY < 8 &&
                     board[currPosY][currPosX].getColor() != turn)
                 {
                     multiplier++;
                     if (board[currPosY][currPosX].getName() != "EmptyPlace")
                     {
                         VectOfMoves.push_back(Point(currPosX, currPosY));
                         break;
                     }
                 }
                 else
                 {
                     break;
                 }
             }
         }
     }
     else
     {
         const Point *attackMoves = piece.getAttackMoveSet();
         for (int idx = 0; idx < piece.numberOfAttackMoves(); idx++)
         {
             movex = attackMoves[idx].getX();
             movey = attackMoves[idx].getY();
             currPosX = piecePositionX + movex;
             currPosY = piecePositionY + movey;
             if (currPosX >= 0 && currPosX < 8 &&
                 currPosY >= 0 && currPosY < 8 &&
                 board[currPosY][currPosX].getColor() != turn &&
                 board[currPosY][currPosX].getColor() != "none")
             {
                 multiplier++;
                 VectOfMoves.push_back(Point(currPosX, currPosY));
             }
         }
     }
     return VectOfMoves;
 }
 
 /**
  * @brief Updates the board state and caches calculated data.
  *
  * This function recalculates important board state information such as whether the current
  * side is in check, all possible moves, and the board evaluation. It uses a hash of the
  * board state to check for and reuse previously computed data, which helps avoid redundant
  * calculations.
  */
 void Board::updateBoard(){
     string key = hashBoard();
     if ((*Hashmap).find(key) != (*Hashmap).end()){
         *this = (*Hashmap)[key];
     } else {
         isBoardDataCalculated = true;
         // The order of function calls is important.
         inCheck = isInCheckinternal();
         moves = getAllPossibleMoves();
         boardEvaluation = evaluateGameinternal();
         isMinimaxCalculated = false;
         Minimaxscore = 0;
         (*Hashmap)[key] = *this;
     }
 }
 
 /**
  * @brief Moves a piece from one position to another, updating castling rights as needed.
  *
  * This function moves a piece from the starting position (Position1) to the destination (Position2).
  * If the moved piece is a king or rook, it updates the castling rights accordingly. If the destination
  * square contains the enemy king, the function sets a flag indicating that the game is won.
  *
  * @param Position1 The starting position of the piece.
  * @param Position2 The destination position for the piece.
  * @param changeCastling Boolean flag indicating whether castling rights should be updated.
  * @return True if the move results in capturing a king (winning the game), false otherwise.
  */
 bool Board::movePiece(Point Position1, Point Position2, bool changeCastling)
 {
     bool winningTheGame = false;
     Piece piece = getPiece(Position1);
 
     if (piece.getName() == "King")
     {
         if (piece.getColor() == "white")
         {
             if (changeCastling)
             {
                 LeftCastleWhite = false;
                 RightCastleWhite = false;
             }
             WhiteKingPos = Position2;
         }
         else
         {
             if (changeCastling)
             {
                 LeftCastleBlack = false;
                 RightCastleBlack = false;
             }
             BlackKingPos = Position2;
         }
     }
 
     if (piece.getName() == "Rook" && changeCastling)
     {
         if (Position1.getX() == 7 && Position1.getY() == 0)
         {
             RightCastleWhite = false;
         }
         else if (Position1.getX() == 0 && Position1.getY() == 0)
         {
             LeftCastleWhite = false;
         }
         else if (Position1.getX() == 0 && Position1.getY() == 7)
         {
             LeftCastleBlack = false;
         }
         else if (Position1.getX() == 7 && Position1.getY() == 7)
         {
             RightCastleBlack = false;
         }
     }
     if (changeCastling)
     {
         if (Position2.getX() == 7 && Position2.getY() == 0)
         {
             RightCastleWhite = false;
         }
         else if (Position2.getX() == 0 && Position2.getY() == 0)
         {
             LeftCastleWhite = false;
         }
         else if (Position2.getX() == 0 && Position2.getY() == 7)
         {
             LeftCastleBlack = false;
         }
         else if (Position2.getX() == 7 && Position2.getY() == 7)
         {
             RightCastleBlack = false;
         }
     }
     setPiece(Position1, Empty);
     if (getPiece(Position2).getName() == "King")
     {
         winningTheGame = true;
     }
     setPiece(Position2, piece);
     return winningTheGame;
 }
 
 /**
  * @brief Performs a full move, including special move updates and pawn promotion.
  *
  * This function moves a piece from Position1 to Position2 while updating castling rights,
  * handling en passant captures, and managing pawn promotion (with different handling for
  * human and AI moves). After the move is completed, the turn is changed and the board state
  * is updated.
  *
  * @param Position1 The starting position of the piece.
  * @param Position2 The destination position.
  * @param IsPlayer Boolean flag indicating if the move was made by a human player (affecting pawn promotion).
  * @return True if the move results in capturing a king, false otherwise.
  */
 bool Board::movePieceoff(Point Position1, Point Position2, bool IsPlayer)
 {
     bool winningTheGame = false;
     Piece piece = getPiece(Position1);
 
     updatecastling(piece, Position1, Position2);
     updateEnPassant(piece, Position1, Position2);
 
     setPiece(Position1, Empty);
     if (getPiece(Position2).getName() == "King")
     {
         winningTheGame = true;
     }
     setPiece(Position2, piece);
     if (IsPlayer) {
         choosePawnHuman(Position2);
     } else {
         choosePawnAi(Position2);
     }
     string turn = getTurn();
     changeTurn();
     updateBoard();
     return winningTheGame;
 }
 
 /**
  * @brief Updates castling rights and executes rook movement when castling.
  *
  * This function updates the board's castling rights when a king or rook is moved.
  * For a king move, it disables both castling rights and updates the king's position.
  * For a rook move, it disables the corresponding castling right. Additionally, if a king move
  * indicates castling (two-square horizontal move), the appropriate rook is moved to complete the castling.
  *
  * @param piece The piece being moved.
  * @param Position1 The starting position of the piece.
  * @param Position2 The destination position of the piece.
  */
 void Board::updatecastling(Piece piece, Point Position1, Point Position2)
 {
     if (piece.getName() == "King")
     {
         if (piece.getColor() == "white")
         {
             LeftCastleWhite = false;
             RightCastleWhite = false;
             WhiteKingPos = Position2;
         }
         else
         {
             LeftCastleBlack = false;
             RightCastleBlack = false;
             BlackKingPos = Position2;
         }
     }
 
     if (piece.getName() == "Rook")
     {
         if (Position1.getX() == 7 && Position1.getY() == 0)
         {
             RightCastleWhite = false;
         }
         else if (Position1.getX() == 0 && Position1.getY() == 0)
         {
             LeftCastleWhite = false;
         }
         else if (Position1.getX() == 0 && Position1.getY() == 7)
         {
             LeftCastleBlack = false;
         }
         else if (Position1.getX() == 7 && Position1.getY() == 7)
         {
             RightCastleBlack = false;
         }
     }
 
     if(getPiece(Position2).getName() == "Rook")
     {
         if (Position2.getX() == 7 && Position2.getY() == 0)
         {
             RightCastleWhite = false;
         }
         else if (Position2.getX() == 0 && Position2.getY() == 0)
         {
             LeftCastleWhite = false;
         }
         else if (Position2.getX() == 0 && Position2.getY() == 7)
         {
             LeftCastleBlack = false;
         }
         else if (Position2.getX() == 7 && Position2.getY() == 7)
         {
             RightCastleBlack = false;
         }
     }
 
     if (getPiece(Position1).getName() == "King")
     {
         if (Position2.getX() - Position1.getX() == 2)
         {
             Piece rook = getPiece(Point(7, Position1.getY()));
             setPiece(Point(7, Position1.getY()), Empty);
             setPiece(Point(Position1.getX() + 1, Position1.getY()), rook);
         }
         else if (Position2.getX() - Position1.getX() == -2)
         {
             Piece rook = getPiece(Point(0, Position1.getY()));
             setPiece(Point(0, Position1.getY()), Empty);
             setPiece(Point(Position1.getX() - 1, Position1.getY()), rook);
         }
     }
 }
 

/**
 * @brief Updates the en passant target square and performs en passant capture if applicable.
 *
 * This function first checks if the destination square of a move equals the current en passant square.
 * If so, it removes the captured pawn (located just behind the en passant square, depending on the turn).
 * Then, the en passant square is reset. If the moved piece is a pawn that moves two squares from its
 * starting position, a new en passant square is set.
 *
 * @param piece The piece being moved.
 * @param Position1 The starting position of the moving piece.
 * @param Position2 The destination position of the moving piece.
 */
 void Board::updateEnPassant(Piece piece, Point Position1, Point Position2)
 {
     if (Position2 == enPassant)
     {
         if (getTurn() == "white")
         {
             setPiece(Point(enPassant.getX(), enPassant.getY() - 1), Empty);
         }
         else
         {
             setPiece(Point(enPassant.getX(), enPassant.getY() + 1), Empty);
         }
     }
     enPassant = Point(-1, -1);
 
     if (getPiece(Position1).getName() == "Pawn" &&
        ((Position2.getY() - Position1.getY()) == 2 || (Position2.getY() - Position1.getY()) == -2))
     {
         enPassant = Point(Position1.getX(), (Position2.getY() + Position1.getY()) / 2);
     }
 }
 
 /**
  * @brief Renders the board graphically.
  *
  * This function iterates over each board square and draws its corresponding image using a gray image
  * rendering function (e.g., for a GUI). The board is drawn with row 7 at the top and row 0 at the bottom.
  */
 void Board::show()
 {
     for (int idxY = 7; idxY >= 0; idxY--)
     {
         for (int idxX = 0; idxX < 8; idxX++)
         {
             putGreyImage(60 * idxX, 480 - (60 * (idxY + 1)),
                           getPiece(Point(idxX, idxY)).getImage(), 60, 60);
         }
     }
 }
 
 /**
  * @brief Prints a textual representation of the board to the standard output.
  *
  * This function iterates over the board rows (from row 7 down to 0) and columns (from 0 to 7)
  * and prints the name of each piece. Each row is ended with a newline.
  */
 void Board::print()
 {
     for (int idxY = 7; idxY >= 0; idxY--)
     {
         for (int idxX = 0; idxX < 8; idxX++)
         {
             cout << getPiece(Point(idxX, idxY)).getName();
         }
         cout << endl;
     }
 }
 
 /**
  * @brief Computes the legal moves for a piece at a given position by simulation.
  *
  * This function obtains the basic possible moves for the piece at the specified position, then
  * adds pawn-specific moves (such as double-step and en passant) via @ref addPawnMoves. For each
  * candidate move, the function simulates the move, checks whether the move leaves the king in check,
  * and then undoes the move. Finally, castling moves are added via @ref addCastleMoves.
  *
  * @param position The starting position of the piece.
  * @return A vector of Point objects representing all legal moves for the piece.
  */
 vector<Point> Board::getPossibleMovesComp(Point position)
 {
     vector<Point> moves = getPossibleMoves(position);
     addPawnMoves(moves, position);
     int x = position.getX();
     int y = position.getY();
     vector<Point> trueMoves;
     for (int idx = 0; idx < moves.size(); idx++)
     {
         Point destination = moves[idx];
         Piece piece = getPiece(destination);
         movePiece(position, destination);
         if (!isInCheckinternal())
         {
             trueMoves.push_back(destination);
         }
         movePiece(destination, position);
         setPiece(destination, piece);
     }
     addCastleMoves(trueMoves, position);
     return trueMoves;
 }
 
 /**
  * @brief Adds valid castling moves to a list of moves for the king at the given position.
  *
  * This function checks whether castling is available for the king (based on castling rights, the king's color,
  * and whether the king is currently in check). If the adjacent squares required for castling are empty and
  * the simulated move does not place the king in check, the corresponding castling move is added to the list.
  *
  * @param trueMoves A reference to the vector of legal moves that will be updated with castling moves.
  * @param position The current position of the king.
  */
 void Board::addCastleMoves(vector<Point> &trueMoves, Point position)
 {
     if (getPiece(position).getName() == "King" && !(isInCheck()))
     {
         int x_castle = position.getX();
         int y_castle = position.getY();
         if (getPiece(position).getColor() == "white" && getTurn() == "white")
         {
             if (RightCastleWhite)
             {
                 if (getPiece(Point(x_castle + 1, y_castle)).getName() == "EmptyPlace" &&
                     getPiece(Point(x_castle + 2, y_castle)).getName() == "EmptyPlace")
                 {
                     movePiece(position, Point(x_castle + 1, y_castle));
                     if (!(isInCheckinternal()))
                     {
                         movePiece(Point(x_castle + 1, y_castle), Point(x_castle + 2, y_castle));
                         if (!(isInCheckinternal()))
                         {
                             trueMoves.push_back(Point(x_castle + 2, y_castle));
                         }
                         movePiece(Point(x_castle + 2, y_castle), position);
                     }
                     else
                     {
                         movePiece(Point(x_castle + 1, y_castle), position);
                     }
                 }
             }
             if (LeftCastleWhite)
             {
                 if (getPiece(Point(x_castle - 1, y_castle)).getName() == "EmptyPlace" &&
                     getPiece(Point(x_castle - 2, y_castle)).getName() == "EmptyPlace" &&
                     getPiece(Point(x_castle - 3, y_castle)).getName() == "EmptyPlace")
                 {
                     movePiece(position, Point(x_castle - 1, y_castle));
                     if (!(isInCheckinternal()))
                     {
                         movePiece(Point(x_castle - 1, y_castle), Point(x_castle - 2, y_castle));
                         if (!(isInCheckinternal()))
                         {
                             trueMoves.push_back(Point(x_castle - 2, y_castle));
                         }
                         movePiece(Point(x_castle - 2, y_castle), position);
                     }
                     else
                     {
                         movePiece(Point(x_castle - 1, y_castle), position);
                     }
                 }
             }
         }
         else if (getPiece(position).getColor() == "black" && getTurn() == "black")
         {
             if (RightCastleBlack)
             {
                 if (getPiece(Point(x_castle + 1, y_castle)).getName() == "EmptyPlace" &&
                     getPiece(Point(x_castle + 2, y_castle)).getName() == "EmptyPlace")
                 {
                     movePiece(position, Point(x_castle + 1, y_castle));
                     if (!(isInCheckinternal()))
                     {
                         movePiece(Point(x_castle + 1, y_castle), Point(x_castle + 2, y_castle));
                         if (!(isInCheckinternal()))
                         {
                             trueMoves.push_back(Point(x_castle + 2, y_castle));
                         }
                         movePiece(Point(x_castle + 2, y_castle), position);
                     }
                     else
                     {
                         movePiece(Point(x_castle + 1, y_castle), position);
                     }
                 }
             }
             if (LeftCastleBlack)
             {
                 if (getPiece(Point(x_castle - 1, y_castle)).getName() == "EmptyPlace" &&
                     getPiece(Point(x_castle - 2, y_castle)).getName() == "EmptyPlace" &&
                     getPiece(Point(x_castle - 3, y_castle)).getName() == "EmptyPlace")
                 {
                     movePiece(position, Point(x_castle - 1, y_castle));
                     if (!isInCheckinternal())
                     {
                         movePiece(Point(x_castle - 1, y_castle), Point(x_castle - 2, y_castle));
                         if (!isInCheckinternal())
                         {
                             trueMoves.push_back(Point(x_castle - 2, y_castle));
                         }
                         movePiece(Point(x_castle - 2, y_castle), position);
                     }
                     else
                     {
                         movePiece(Point(x_castle - 1, y_castle), position);
                     }
                 }
             }
         }
     }
 }
 
 /**
  * @brief Adds pawn-specific moves such as the initial double-step and en passant captures.
  *
  * For a pawn at the given position, this function checks whether it can move two squares forward
  * from its starting rank (if both squares are empty) or perform an en passant capture. Any valid move
  * discovered is added to the provided vector.
  *
  * @param moves A reference to the vector of moves to be updated.
  * @param position The current position of the pawn.
  */
 void Board::addPawnMoves(vector<Point> &moves, Point position)
 {
     int x = position.getX();
     int y = position.getY();
     if (getPiece(position).getName() == "Pawn")
     {
         if (getPiece(position).getColor() == "white" && getTurn() == "white")
         {
             if (y == 1)
             {
                 if (getPiece(Point(x, y + 2)).getName() == "EmptyPlace" &&
                     getPiece(Point(x, y + 1)).getName() == "EmptyPlace")
                 {
                     moves.push_back(Point(x, y + 2));
                 }
             }
             else if (((Point(x + 1, y + 1) == enPassant) || (Point(x - 1, y + 1) == enPassant)))
             {
                 moves.push_back(enPassant);
             }
         }
         else if (getPiece(position).getColor() == "black" && getTurn() == "black")
         {
             if (y == 6)
             {
                 if (getPiece(Point(x, y - 2)).getName() == "EmptyPlace" &&
                     getPiece(Point(x, y - 1)).getName() == "EmptyPlace")
                 {
                     moves.push_back(Point(x, y - 2));
                 }
             }
             else if (((Point(x + 1, y - 1) == enPassant) || (Point(x - 1, y - 1) == enPassant)))
             {
                 moves.push_back(enPassant);
             }
         }
     }
 }
 /**
 * @brief Computes all possible moves for every piece on the board.
 *
 * This function iterates through every square on the board (8×8) and, for each square,
 * computes the legal moves using @ref getPossibleMovesComp. If any moves are found, they are
 * stored in a map keyed by the originating square.
 *
 * @return A map with each key as a Point representing a square, and its value as a vector of Points representing legal move destinations.
 */
map<Point, vector<Point>> Board::getAllPossibleMoves()
{
    map<Point, vector<Point>> possibleMoves;
    for (int x = 0; x < 8; x++)
    {
        for (int y = 0; y < 8; y++)
        {
            Point point(x, y);
            vector<Point> movees = getPossibleMovesComp(point);
            if (movees.size() != 0)
                possibleMoves[point] = movees;
        }
    }
    return possibleMoves;
}

/**
 * @brief Returns all possible moves for the white pieces.
 *
 * If it is currently white's turn, this function simply calls @ref getAllPossibleMoves.
 * Otherwise, it temporarily switches the turn to white, computes the moves, and then restores the turn.
 *
 * @return A map of Points to vectors of Points representing white's legal moves.
 */
map<Point, vector<Point>> Board::getAllPossibleWhiteMoves()
{
    if (getTurn() == "white")
    {
        return getAllPossibleMoves();
    }
    else
    {
        changeTurn();
        map<Point, vector<Point>> possibleMoves = getAllPossibleMoves();
        changeTurn();
        return possibleMoves;
    }
}

/**
 * @brief Returns all possible moves for the black pieces.
 *
 * If it is currently black's turn, this function simply calls @ref getAllPossibleMoves.
 * Otherwise, it temporarily switches the turn to black, computes the moves, and then restores the turn.
 *
 * @return A map of Points to vectors of Points representing black's legal moves.
 */
map<Point, vector<Point>> Board::getAllPossibleBlackMoves()
{
    if (getTurn() == "black")
    {
        return getAllPossibleMoves();
    }
    else
    {
        changeTurn();
        map<Point, vector<Point>> possibleMoves = getAllPossibleMoves();
        changeTurn();
        return possibleMoves;
    }
}

/**
 * @brief Generates a string hash representing the current board state.
 *
 * The hash is constructed by concatenating the hash of each piece (as provided by the piece's
 * @ref hashPiece method) on the board, followed by flags for castling rights, the current turn,
 * and the en passant square coordinates.
 *
 * @return A string uniquely representing the board state.
 */
string Board::hashBoard(){
    string hashedBoard = "";
    for (int x = 0; x < 8; x++){
        for (int y = 0; y < 8; y++){
            hashedBoard += board[x][y].hashPiece();
        }
    }
    if(LeftCastleBlack){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    if(RightCastleBlack){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    if(LeftCastleWhite){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    if(RightCastleWhite){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    hashedBoard += to_string(turn == "white");
    hashedBoard += to_string(enPassant.getX());
    hashedBoard += to_string(enPassant.getY());
    return hashedBoard;
}

/**
 * @brief Determines if the current side's king is in check.
 *
 * This internal function simulates potential enemy attacks on the king's square and, by temporarily
 * changing the king's piece type, checks for threats from sliding and leaping pieces.
 *
 * @return True if the king is under attack; false otherwise.
 */
bool Board::isInCheckinternal()
{
    vector<Point> test;
    int x, y;
    if (getTurn() == "white")
    {
        x = WhiteKingPos.getX();
        y = WhiteKingPos.getY();
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "King")
            {
                return true;
            }
        }
        if (getPiece(Point(x + 1, y + 1)).getName() == "Pawn" &&
            getPiece(Point(x + 1, y + 1)).getColor() == "black")
        {
            return true;
        }
        if (getPiece(Point(x - 1, y + 1)).getName() == "Pawn" &&
            getPiece(Point(x - 1, y + 1)).getColor() == "black")
        {
            return true;
        }
        setPiece(WhiteKingPos, WhiteBishop);
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" ||
                getPiece(test[idx]).getName() == "Bishop")
            {
                setPiece(WhiteKingPos, WhiteKing);
                return true;
            }
        }
        setPiece(WhiteKingPos, WhiteRook);
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" ||
                getPiece(test[idx]).getName() == "Rook")
            {
                setPiece(WhiteKingPos, WhiteKing);
                return true;
            }
        }
        setPiece(WhiteKingPos, WhiteKnight);
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Knight")
            {
                setPiece(WhiteKingPos, WhiteKing);
                return true;
            }
        }
        setPiece(WhiteKingPos, WhiteKing);
    }
    else
    {
        x = BlackKingPos.getX();
        y = BlackKingPos.getY();
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "King")
            {
                return true;
            }
        }
        if (getPiece(Point(x + 1, y - 1)).getName() == "Pawn" &&
            getPiece(Point(x + 1, y - 1)).getColor() == "white")
        {
            return true;
        }
        if (getPiece(Point(x - 1, y - 1)).getName() == "Pawn" &&
            getPiece(Point(x - 1, y - 1)).getColor() == "white")
        {
            return true;
        }
        setPiece(BlackKingPos, BlackBishop);
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" ||
                getPiece(test[idx]).getName() == "Bishop")
            {
                setPiece(BlackKingPos, BlackKing);
                return true;
            }
        }
        setPiece(BlackKingPos, BlackRook);
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" ||
                getPiece(test[idx]).getName() == "Rook")
            {
                setPiece(BlackKingPos, BlackKing);
                return true;
            }
        }
        setPiece(BlackKingPos, BlackKnight);
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Knight")
            {
                setPiece(BlackKingPos, BlackKing);
                return true;
            }
        }
        setPiece(BlackKingPos, BlackKing);
    }
    return false;
}

/**
 * @brief Checks whether the current side is in check.
 *
 * This function ensures the board data is up-to-date before returning the value of the in-check flag.
 *
 * @return True if the current side is in check; false otherwise.
 */
bool Board::isInCheck(){
    if (!isBoardDataCalculated){
        updateBoard();
    }
    return inCheck;
}

/**
 * @brief Returns the current evaluation score of the board.
 *
 * This function updates the board data if necessary, and then returns the board evaluation
 * computed by @ref evaluateGameinternal.
 *
 * @return The board evaluation score.
 */
int Board::evaluateGame(){
    if (!isBoardDataCalculated){
        updateBoard();
    }
    return boardEvaluation;
}

/**
 * @brief Determines the game outcome when no legal moves remain.
 *
 * If no moves are available, this function checks whether the current side is in check (indicating checkmate)
 * or not (indicating stalemate). Otherwise, it returns "NONE".
 *
 * @return A string indicating the game outcome: either a win (with the winning side), "stalemate", or "NONE".
 */
string Board::gameOver()
{
    if (!isBoardDataCalculated)
    {
        updateBoard();
    }
    if (moves.size() == 0)
    {
        if (isInCheck())
        {
            return getTurn() + " won";
        }
        else
        {
            return "stalemate";
        }
    }
    else
    {
        return "NONE";
    }
}

/**
 * @brief Computes the game phase based on the total material on the board.
 *
 * The game phase is represented as a float between 0.0 and 1.0, where a lower value indicates
 * an opening phase and a higher value indicates an endgame. The value is computed from the sum of
 * the initial scores of the remaining pieces.
 *
 * @return A float representing the game phase.
 */
float Board::getGamePhase()
{
    int whitePieces = 0;
    int blackPieces = 0;
    int val;
    float total, phase;
    for (int y = 0; y < 8; y++)
    {
        for (int x = 0; x < 8; x++)
        {
            Piece piece = getPiece(Point(x, y));
            if (piece.getName() != "EmptyPlace")
            {
                int val = initialScores[piece.getName()];
                if (piece.getColor() == "white")
                {
                    whitePieces += val;
                }
                else
                {
                    blackPieces += val;
                }
            }
        }
    }
    total = whitePieces + blackPieces;
    phase = max(0.0, min(1.0, (5600.0 - total) / 3600.0));
    return phase;
}

/**
 * @brief Evaluates the control of the four key central squares.
 *
 * This function checks the occupancy of the four center squares (3,3), (3,4), (4,3), and (4,4)
 * and assigns a score: +20 for each square occupied by a white piece and -20 for each square occupied
 * by a black piece.
 *
 * @return The control score for the central squares.
 */
int Board::evaluateControlOfKeySquares()
{
    Point centerSquares[4] = {Point(3, 3), Point(3, 4), Point(4, 3), Point(4, 4)};
    int score = 0;
    for (int idx = 0; idx < 4; idx++)
    {
        Piece piece = getPiece(centerSquares[idx]);
        if (piece.getColor() == "white")
        {
            score += 20;
        }
        else if (piece.getColor() == "black")
        {
            score -= 20;
        }
    }
    return score;
}

/**
 * @brief Determines if the king is active (i.e., centralized) based on its color.
 *
 * For the specified color, the function checks whether the king's coordinates lie within the central
 * region of the board (between 2 and 5 for both x and y).
 *
 * @param color The color of the king ("white" or "black").
 * @return True if the king is active (centralized); false otherwise.
 */
bool Board::isKingActive(string color)
{
    if (color == "white")
    {
        int x = WhiteKingPos.getX();
        int y = WhiteKingPos.getY();
        return (2 < x && x < 5) && (2 < y && y < 5);
    }
    else
    {
        int x = BlackKingPos.getX();
        int y = BlackKingPos.getY();
        return (2 < x && x < 5) && (2 < y && y < 5);
    }
}

/**
 * @brief Computes a score representing control over the central board area.
 *
 * This function sums up contributions from all legal moves by both white and black pieces that target
 * the center squares (with x between 3 and 4 and y between 3 and 4). Moves by white add to the score,
 * while moves by black subtract.
 *
 * @return The central control score.
 */
int Board::centerControl()
{
    int score = 0;
    for (const auto &pair : getAllPossibleWhiteMoves())
    {
        for (const auto &point : pair.second)
        {
            int x = point.getX();
            int y = point.getY();
            if (x > 2 && x < 5 && y > 2 && y < 5)
            {
                score += 1;
            }
        }
    }
    for (const auto &pair : getAllPossibleBlackMoves())
    {
        for (const auto &point : pair.second)
        {
            int x = point.getX();
            int y = point.getY();
            if (x > 2 && x < 5 && y > 2 && y < 5)
            {
                score -= 1;
            }
        }
    }
    return score;
}

/**
 * @brief Evaluates the game position by combining various features.
 *
 * Currently, this function returns only the material evaluation from @ref evaluateBoard.
 * (Additional evaluation components, such as center control, king safety, and pawn structure,
 * are hinted at in commented code.)
 *
 * @return The evaluation score for the current position.
 */
int Board::evaluateGameinternal()
{
    int materialScore = evaluateBoard();
    /*
    int centerScore = centerControl();
    // Pawn structure

    int kingSafetyScore = 0;
    int pieceCoordinationScore = 0;
    int controlScore = evaluateControlOfKeySquares();
    int endGameScore = evaluateEndGameFeatures();

    int phase = getGamePhase();
    // opening_weight ~ (1 - phase)
    // endgame_weight ~ phase
    int openingWeight = 1 - phase;
    int endGameWeight = phase;
    int totalScore = (materialScore * 1 +
                      kingSafetyScore * 1.0 +
                      pieceCoordinationScore * 0.6 +
                      controlScore * (0.6 * openingWeight + 0.3 * endGameWeight) +
                      endGameScore * endGameWeight);
    */
    return materialScore;
}

/**
 * @brief Allows a human player to choose a promotion piece when a pawn reaches the last rank.
 *
 * If a pawn reaches the first or last rank, this function prompts the user to choose a piece (Queen,
 * Rook, Bishop, or Knight) for promotion.
 *
 * @param point The position of the pawn to be promoted.
 */
void Board::choosePawnHuman(Point point){
    int idx_piece_chosen;
    if ((getPiece(point).getName() == "Pawn") && (point.getY()==0 || point.getY()==7)){
        cout << "choose a piece to change your pawn into" << endl;
        cout << "0: Queen    1: Rook    2: Bishop    3: Knight" << endl;
        while(true){
            cin >> idx_piece_chosen;
            if (idx_piece_chosen>=0 && idx_piece_chosen<4){
                break;
            }
            cout << "choose a valid index between 0 and 3" << endl;
        }
        if (getTurn() == "white"){
            switch(idx_piece_chosen){
                case 0:
                    setPiece(point,WhiteQueen);
                    break;
                case 1:
                    setPiece(point,WhiteRook);
                    break;
                case 2:
                    setPiece(point,WhiteBishop);
                    break;
                case 3:
                    setPiece(point,WhiteKnight);
                    break;
            }
        }
        if (getTurn() == "black"){
            switch(idx_piece_chosen){
                case 0:
                    setPiece(point,BlackQueen);
                    break;
                case 1:
                    setPiece(point,BlackRook);
                    break;
                case 2:
                    setPiece(point,BlackBishop);
                    break;
                case 3:
                    setPiece(point,BlackKnight);
                    break;
            }
        }
    }
}

/**
 * @brief Automatically promotes a pawn for an AI move.
 *
 * When a pawn reaches the first or last rank, this function automatically promotes it to a queen.
 *
 * @param point The position of the pawn to be promoted.
 */
void Board::choosePawnAi(Point point){
    if ((getPiece(point).getName() == "Pawn") && (point.getY()==0 || point.getY()==7)){
        if (getTurn() == "white"){
            setPiece(point,WhiteQueen);
        } else{
            setPiece(point,BlackQueen);
        }
    }
}

/**
 * @brief Global initial board configuration.
 *
 * The board is initialized in the standard chess starting position.
 * The board is represented as a one-dimensional array of 64 Pieces.
 */
Piece initialBoard[64] = {
    WhiteRook, WhiteKnight, WhiteBishop, WhiteQueen, WhiteKing, WhiteBishop, WhiteKnight, WhiteRook,
    WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn,
    BlackRook, BlackKnight, BlackBishop, BlackQueen, BlackKing, BlackBishop, BlackKnight, BlackRook
};

/**
 * @brief Global Board object initialized with the standard chess starting position.
 */
Board initial_board(initialBoard, "white");

