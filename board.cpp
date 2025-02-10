#include "board.h"
#include <cassert>
#include <chrono>
#include <random>
#include <algorithm>
#include <iostream>
#include <exception>

/**
 * @brief Generates a random back rank configuration for Fischer Random Chess.
 *
 * This function shuffles the pieces ensuring that bishops are placed on opposite-colored
 * squares and that the king is positioned between the rooks.
 *
 * @return std::vector<std::pair<int, std::string>> A vector of pairs containing the original index and piece name.
 */
vector<pair<int, string>> generateRandomBackRank() {
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    mt19937 rng(seed);
    vector<pair<int, string>> pieces = {
        make_pair(0, "Rook"), make_pair(1, "Knight"), make_pair(2, "Bishop"),
        make_pair(3, "Queen"), make_pair(4, "King"), make_pair(5, "Bishop"),
        make_pair(6, "Knight"), make_pair(7, "Rook")
    };

    while (true) {
        shuffle(pieces.begin(), pieces.end(), rng);

        int bishop1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string>& p) {
                             return p.second == "Bishop";
                         }) - pieces.begin();
        int bishop2Pos = find_if(pieces.begin() + bishop1Pos + 1, pieces.end(), [](const pair<int, string>& p) {
                             return p.second == "Bishop";
                         }) - pieces.begin();

        // Both bishops must be on opposite-colored squares.
        if ((bishop1Pos % 2 == bishop2Pos % 2)) {
            continue;
        }

        int kingPos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string>& p) {
                          return p.second == "King";
                      }) - pieces.begin();
        int rook1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string>& p) {
                           return p.second == "Rook";
                       }) - pieces.begin();
        int rook2Pos = find_if(pieces.begin() + rook1Pos + 1, pieces.end(), [](const pair<int, string>& p) {
                           return p.second == "Rook";
                       }) - pieces.begin();

        // The king must be between the two rooks.
        if (rook1Pos < kingPos && kingPos < rook2Pos) {
            break; // Valid configuration found.
        }
    }

    return pieces;
}

/**
 * @brief Transforms the board into a Fischer Random configuration.
 *
 * This function generates a random back rank and rearranges the pieces accordingly.
 */
void Board::transformToFisher() {
    try {
        cout << 1 << endl;
        vector<pair<int, string>> backRank = generateRandomBackRank();

        for (const pair<int, string>& couple : backRank) {
            cout << couple.second << " : " << couple.first << endl;
        }
        cout << 2 << endl;

        // Move the original pieces out of the way.
        for (int i = 0; i < 8; ++i) {
            movePiece(Point(i, 0), Point(i, 2));
            movePiece(Point(i, 7), Point(i, 5));
        }

        // Place the pieces into their new positions.
        for (int i = 0; i < 8; ++i) {
            movePiece(Point(backRank[i].first, 2), Point(i, 0));
            movePiece(Point(backRank[i].first, 5), Point(i, 7));
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in transformToFisher: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Evaluates the score of the piece at the given board coordinates.
 *
 * @param x The x-coordinate (column) on the board.
 * @param y The y-coordinate (row) on the board.
 * @return int The evaluation score for the piece.
 */
int Board::evaluatePiece(int x, int y) {
    assert(x >= 0 && x < 8 && "x coordinate out of range");
    assert(y >= 0 && y < 8 && "y coordinate out of range");

    Piece* piece = getPiece(Point(x, y));
    assert(piece != nullptr && "Null pointer returned by getPiece in evaluatePiece");

    if (piece->getName() == "EmptyPlace") {
        return 0;
    }
    int factor = -1 + 2 * (piece->getColor() == "white");
    int value = scores[piece->getName()];
    value += piece->getScore(x, (8 - 2 * y) * (piece->getColor() == "black") + y);
    value *= factor;
    return value;
}

/**
 * @brief Evaluates the entire board.
 *
 * Sums the evaluation of each piece on the board.
 *
 * @return int The overall evaluation score.
 */
int Board::evaluateBoard() {
    int value = 0;
    for (int x = 0; x < 8; x++) {
        for (int y = 0; y < 8; y++) {
            value += evaluatePiece(x, y);
        }
    }
    return value;
}

/**
 * @brief Constructs a Board from an initial configuration.
 *
 * @param initial_board A 2D array of pointers to Piece representing the starting board.
 * @param Turn The color ("white" or "black") of the player who is to move.
 */
Board::Board(Piece* initial_board[8][8], string Turn) {
    turn = Turn;
    for (int idxY = 0; idxY < 8; idxY++) {
        for (int idxX = 0; idxX < 8; idxX++) {
            board[idxY][idxX] = initial_board[idxY][idxX];
        }
    }
}

/**
 * @brief Copy constructor for Board.
 *
 * @param other The board to copy.
 */
Board::Board(const Board& other) {
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

    for (int idx1 = 0; idx1 < 8; idx1++) {
        for (int idx2 = 0; idx2 < 8; idx2++) {
            board[idx1][idx2] = other.board[idx1][idx2];
        }
    }
    moves = other.moves;
}

/**
 * @brief Changes the turn to the other player.
 */
void Board::changeTurn() {
    if (turn == "white") {
        turn = "black";
    }
    else {
        turn = "white";
    }
}

/**
 * @brief Returns the piece at the given board position.
 *
 * @param point The board position.
 * @return Piece* Pointer to the piece at that position.
 */
Piece* Board::getPiece(Point point) {
    assert(point.getX() >= 0 && point.getX() < 8 && "Point X coordinate out of range in getPiece");
    assert(point.getY() >= 0 && point.getY() < 8 && "Point Y coordinate out of range in getPiece");
    return board[point.getY()][point.getX()];
}

/**
 * @brief Places a piece at the given board position.
 *
 * @param point The board position.
 * @param piece Pointer to the piece to set.
 */
void Board::setPiece(Point point, Piece* piece) {
    assert(point.getX() >= 0 && point.getX() < 8 && "Point X coordinate out of range in setPiece");
    assert(point.getY() >= 0 && point.getY() < 8 && "Point Y coordinate out of range in setPiece");
    board[point.getY()][point.getX()] = piece;
}

/**
 * @brief Returns all possible moves for the piece at the given position.
 *
 * @param position The starting position.
 * @return std::vector<Point> A vector of possible destination points.
 */
vector<Point> Board::getPossibleMoves(Point position) {
    vector<Point> VectOfMoves;
    int piecePositionX = position.getX();
    int piecePositionY = position.getY();
    assert(piecePositionX >= 0 && piecePositionX < 8 && "piecePositionX out of range in getPossibleMoves");
    assert(piecePositionY >= 0 && piecePositionY < 8 && "piecePositionY out of range in getPossibleMoves");

    Piece* piece = board[piecePositionY][piecePositionX];
    if (piece->getColor() != turn) {
        return VectOfMoves;
    }
    const Point* elemMoves = piece->getElemMoveSet();
    int movex, movey, currPosX, currPosY, multiplier;

    if (piece->isMoveSetAttackMoveSet()) {
        for (int idx = 0; idx < piece->numberOfElemMoves(); idx++) {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true) {
                if (multiplier == 2 && !piece->hasInfiniteMoves()) {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 &&
                    currPosY >= 0 && currPosY < 8 &&
                    board[currPosY][currPosX]->getColor() != turn) {
                    VectOfMoves.push_back(Point(currPosX, currPosY));
                    multiplier++;
                    if (board[currPosY][currPosX]->getName() != "EmptyPlace") {
                        break;
                    }
                }
                else {
                    break;
                }
            }
        }
    }
    else {
        const Point* attackMoves = piece->getAttackMoveSet();
        for (int idx = 0; idx < piece->numberOfElemMoves(); idx++) {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true) {
                if (multiplier == 2 && !piece->hasInfiniteMoves()) {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 &&
                    currPosY >= 0 && currPosY < 8 &&
                    board[currPosY][currPosX]->getName() == "EmptyPlace") {
                    VectOfMoves.push_back(Point(currPosX, currPosY));
                    multiplier++;
                }
                else {
                    break;
                }
            }
        }
        for (int idx = 0; idx < piece->numberOfAttackMoves(); idx++) {
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
            currPosY = piecePositionY + movey;
            if (currPosX >= 0 && currPosX < 8 &&
                currPosY >= 0 && currPosY < 8 &&
                board[currPosY][currPosX]->getColor() != turn &&
                board[currPosY][currPosX]->getColor() != "none") {
                VectOfMoves.push_back(Point(currPosX, currPosY));
            }
        }
    }
    return VectOfMoves;
}

/**
 * @brief Returns all possible attack moves for the piece at the given position.
 *
 * @param position The starting position.
 * @return std::vector<Point> A vector of possible attack destination points.
 */
vector<Point> Board::getPossibleAttacks(Point position) {
    vector<Point> VectOfMoves;
    int piecePositionX = position.getX();
    int piecePositionY = position.getY();
    assert(piecePositionX >= 0 && piecePositionX < 8 && "piecePositionX out of range in getPossibleAttacks");
    assert(piecePositionY >= 0 && piecePositionY < 8 && "piecePositionY out of range in getPossibleAttacks");

    Piece* piece = board[piecePositionY][piecePositionX];
    if (piece->getColor() != turn) {
        return VectOfMoves;
    }
    const Point* elemMoves = piece->getElemMoveSet();
    int movex, movey, currPosX, currPosY, multiplier;

    if (piece->isMoveSetAttackMoveSet()) {
        for (int idx = 0; idx < piece->numberOfElemMoves(); idx++) {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true) {
                if (multiplier == 2 && !piece->hasInfiniteMoves()) {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 &&
                    currPosY >= 0 && currPosY < 8 &&
                    board[currPosY][currPosX]->getColor() != turn) {
                    if (board[currPosY][currPosX]->getName() != "EmptyPlace") {
                        VectOfMoves.push_back(Point(currPosX, currPosY));
                        break;
                    }
                    multiplier++;
                }
                else {
                    break;
                }
            }
        }
    }
    else {
        const Point* attackMoves = piece->getAttackMoveSet();
        for (int idx = 0; idx < piece->numberOfAttackMoves(); idx++) {
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
            currPosY = piecePositionY + movey;
            if (currPosX >= 0 && currPosX < 8 &&
                currPosY >= 0 && currPosY < 8 &&
                board[currPosY][currPosX]->getColor() != turn &&
                board[currPosY][currPosX]->getColor() != "none") {
                VectOfMoves.push_back(Point(currPosX, currPosY));
            }
        }
    }
    return VectOfMoves;
}

/**
 * @brief Updates the board’s internal state.
 *
 * This function recomputes the evaluation, legal moves, and other internal data.
 */
void Board::updateBoard() {
    try {
        string key = hashBoard();
        if ((*Hashmap).find(key) != (*Hashmap).end()) {
            *this = (*Hashmap)[key];
        }
        else {
            isBoardDataCalculated = true;
            // The order of these functions is important.
            inCheck = isInCheckinternal();
            moves = getAllPossibleMoves();
            boardEvaluation = evaluateGameinternal();
            isMinimaxCalculated = false;
            Minimaxscore = 0;
            (*Hashmap)[key] = *this;
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in updateBoard: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Moves a piece from one board position to another.
 *
 * Handles special cases such as castling by updating the appropriate flags.
 *
 * @param Position1 The source position.
 * @param Position2 The destination position.
 * @param changeCastling If true, updates castling rights.
 * @return bool True if the move results in capturing the king, false otherwise.
 */
bool Board::movePiece(Point Position1, Point Position2, bool changeCastling) {
    bool winningTheGame = false;
    try {
        assert(Position1.getX() >= 0 && Position1.getX() < 8 && "Position1 X coordinate out of range in movePiece");
        assert(Position1.getY() >= 0 && Position1.getY() < 8 && "Position1 Y coordinate out of range in movePiece");
        assert(Position2.getX() >= 0 && Position2.getX() < 8 && "Position2 X coordinate out of range in movePiece");
        assert(Position2.getY() >= 0 && Position2.getY() < 8 && "Position2 Y coordinate out of range in movePiece");

        Piece* piece = getPiece(Position1);
        assert(piece != nullptr && "Null piece pointer in movePiece");

        if (piece->getName() == "King") {
            if (piece->getColor() == "white") {
                if (changeCastling) {
                    LeftCastleWhite = false;
                    RightCastleWhite = false;
                }
                WhiteKingPos = Position2;
            }
            else {
                if (changeCastling) {
                    LeftCastleBlack = false;
                    RightCastleBlack = false;
                }
                BlackKingPos = Position2;
            }
        }

        if (piece->getName() == "Rook" && changeCastling) {
            if (Position1.getX() == 7 && Position1.getY() == 0) {
                RightCastleWhite = false;
            }
            else if (Position1.getX() == 0 && Position1.getY() == 0) {
                LeftCastleWhite = false;
            }
            else if (Position1.getX() == 0 && Position1.getY() == 7) {
                LeftCastleBlack = false;
            }
            else if (Position1.getX() == 7 && Position1.getY() == 7) {
                RightCastleBlack = false;
            }
        }
        if (changeCastling) {
            if (Position2.getX() == 7 && Position2.getY() == 0) {
                RightCastleWhite = false;
            }
            else if (Position2.getX() == 0 && Position2.getY() == 0) {
                LeftCastleWhite = false;
            }
            else if (Position2.getX() == 0 && Position2.getY() == 7) {
                LeftCastleBlack = false;
            }
            else if (Position2.getX() == 7 && Position2.getY() == 7) {
                RightCastleBlack = false;
            }
        }
        setPiece(Position1, &Empty);
        if (getPiece(Position2)->getName() == "King") {
            winningTheGame = true;
        }
        setPiece(Position2, piece);
    }
    catch (const std::exception& e) {
        std::cerr << "Error in movePiece: " << e.what() << std::endl;
        throw;
    }
    return winningTheGame;
}

/**
 * @brief Moves a piece with additional updates (e.g. en passant, pawn promotion).
 *
 * Updates castling rights and changes the turn after the move.
 *
 * @param Position1 The source position.
 * @param Position2 The destination position.
 * @param IsPlayer True if the move was made by a human player.
 * @return bool True if the move results in capturing the king.
 */
bool Board::movePieceoff(Point Position1, Point Position2, bool IsPlayer) {
    bool winningTheGame = false;
    try {
        Piece* piece = getPiece(Position1);
        assert(piece != nullptr && "Null piece pointer in movePieceoff");

        updatecastling(piece, Position1, Position2);
        updateEnPassant(piece, Position1, Position2);

        setPiece(Position1, &Empty);
        if (getPiece(Position2)->getName() == "King") {
            winningTheGame = true;
        }
        setPiece(Position2, piece);
        if (IsPlayer) {
            choosePawnHuman(Position2);
        }
        else {
            choosePawnAi(Position2);
        }
        changeTurn();
        updateBoard();
    }
    catch (const std::exception& e) {
        std::cerr << "Error in movePieceoff: " << e.what() << std::endl;
        throw;
    }
    return winningTheGame;
}

/**
 * @brief Updates castling rights and moves the rook if a castling move is performed.
 *
 * @param piece The moving piece.
 * @param Position1 The original position.
 * @param Position2 The destination position.
 */
void Board::updatecastling(Piece* piece, Point Position1, Point Position2) {
    try {
        if (piece->getName() == "King") {
            if (piece->getColor() == "white") {
                LeftCastleWhite = false;
                RightCastleWhite = false;
                WhiteKingPos = Position2;
            }
            else {
                LeftCastleBlack = false;
                RightCastleBlack = false;
                BlackKingPos = Position2;
            }
        }

        if (piece->getName() == "Rook") {
            if (Position1.getX() == 7 && Position1.getY() == 0) {
                RightCastleWhite = false;
            }
            else if (Position1.getX() == 0 && Position1.getY() == 0) {
                LeftCastleWhite = false;
            }
            else if (Position1.getX() == 0 && Position1.getY() == 7) {
                LeftCastleBlack = false;
            }
            else if (Position1.getX() == 7 && Position1.getY() == 7) {
                RightCastleBlack = false;
            }
        }

        if (getPiece(Position2)->getName() == "Rook") {
            if (Position2.getX() == 7 && Position2.getY() == 0) {
                RightCastleWhite = false;
            }
            else if (Position2.getX() == 0 && Position2.getY() == 0) {
                LeftCastleWhite = false;
            }
            else if (Position2.getX() == 0 && Position2.getY() == 7) {
                LeftCastleBlack = false;
            }
            else if (Position2.getX() == 7 && Position2.getY() == 7) {
                RightCastleBlack = false;
            }
        }

        if (getPiece(Position1)->getName() == "King") {
            if (Position2.getX() - Position1.getX() == 2) {
                Piece* rook = getPiece(Point(7, Position1.getY()));
                setPiece(Point(7, Position1.getY()), &Empty);
                setPiece(Point(Position1.getX() + 1, Position1.getY()), rook);
            }
            else if (Position2.getX() - Position1.getX() == -2) {
                Piece* rook = getPiece(Point(0, Position1.getY()));
                setPiece(Point(0, Position1.getY()), &Empty);
                setPiece(Point(Position1.getX() - 1, Position1.getY()), rook);
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in updatecastling: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Updates the board for en passant moves.
 *
 * If an en passant move is performed, this function removes the captured pawn.
 *
 * @param piece The pawn that just moved.
 * @param Position1 The original position.
 * @param Position2 The destination position.
 */
void Board::updateEnPassant(Piece* piece, Point Position1, Point Position2) {
    try {
        if (Position2 == enPassant) {
            if (getTurn() == "white") {
                setPiece(Point(enPassant.getX(), enPassant.getY() - 1), &Empty);
            }
            else {
                setPiece(Point(enPassant.getX(), enPassant.getY() + 1), &Empty);
            }
        }
        enPassant = Point(-1, -1);

        if (piece->getName() == "Pawn" && (abs(Position2.getY() - Position1.getY()) == 2)) {
            enPassant = Point(Position1.getX(), (Position2.getY() + Position1.getY()) / 2);
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in updateEnPassant: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Displays the board using the Imagine graphics library.
 */
void Board::show() {
    try {
        for (int idxY = 7; idxY >= 0; idxY--) {
            for (int idxX = 0; idxX < 8; idxX++) {
                Imagine::putGreyImage(60 * idxX, 480 - (60 * (idxY + 1)),
                                      getPiece(Point(idxX, idxY))->getImage(), 60, 60);
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in show: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Returns all legal moves for a piece, checking that moves do not leave the king in check.
 *
 * @param position The starting position.
 * @return std::vector<Point> A vector of legal destination points.
 */
vector<Point> Board::getPossibleMovesComp(Point position) {
    vector<Point> moves = getPossibleMoves(position);
    addPawnMoves(moves, position);
    int x = position.getX();
    int y = position.getY();
    vector<Point> trueMoves;
    for (int idx = 0; idx < moves.size(); idx++) {
        Point destination = moves[idx];
        Piece* piece = getPiece(destination);
        movePiece(position, destination);
        if (!isInCheckinternal()) {
            trueMoves.push_back(destination);
        }
        // Undo the move.
        movePiece(destination, position);
        setPiece(destination, piece);
    }
    addCastleMoves(trueMoves, position);
    return trueMoves;
}

/**
 * @brief Adds castling moves to the list of legal moves for the king.
 *
 * @param trueMoves The vector of legal moves to update.
 * @param position The king's current position.
 */
void Board::addCastleMoves(vector<Point> &trueMoves, Point position) {
    if (getPiece(position)->getName() == "King" && !isInCheck()) {
        int x_castle = position.getX();
        int y_castle = position.getY();
        if (getPiece(position)->getColor() == "white" && getTurn() == "white") {
            if (RightCastleWhite) {
                if (getPiece(Point(x_castle + 1, y_castle))->getName() == "EmptyPlace" &&
                    getPiece(Point(x_castle + 2, y_castle))->getName() == "EmptyPlace") {
                    movePiece(position, Point(x_castle + 1, y_castle));
                    if (!isInCheckinternal()) {
                        movePiece(Point(x_castle + 1, y_castle), Point(x_castle + 2, y_castle));
                        if (!isInCheckinternal()) {
                            trueMoves.push_back(Point(x_castle + 2, y_castle));
                        }
                        movePiece(Point(x_castle + 2, y_castle), position);
                    }
                    else {
                        movePiece(Point(x_castle + 1, y_castle), position);
                    }
                }
            }
            if (LeftCastleWhite) {
                if (getPiece(Point(x_castle - 1, y_castle))->getName() == "EmptyPlace" &&
                    getPiece(Point(x_castle - 2, y_castle))->getName() == "EmptyPlace" &&
                    getPiece(Point(x_castle - 3, y_castle))->getName() == "EmptyPlace") {
                    movePiece(position, Point(x_castle - 1, y_castle));
                    if (!isInCheckinternal()) {
                        movePiece(Point(x_castle - 1, y_castle), Point(x_castle - 2, y_castle));
                        if (!isInCheckinternal()) {
                            trueMoves.push_back(Point(x_castle - 2, y_castle));
                        }
                        movePiece(Point(x_castle - 2, y_castle), position);
                    }
                    else {
                        movePiece(Point(x_castle - 1, y_castle), position);
                    }
                }
            }
        }
        else if (getPiece(position)->getColor() == "black" && getTurn() == "black") {
            if (RightCastleBlack) {
                if (getPiece(Point(x_castle + 1, y_castle))->getName() == "EmptyPlace" &&
                    getPiece(Point(x_castle + 2, y_castle))->getName() == "EmptyPlace") {
                    movePiece(position, Point(x_castle + 1, y_castle));
                    if (!isInCheckinternal()) {
                        movePiece(Point(x_castle + 1, y_castle), Point(x_castle + 2, y_castle));
                        if (!isInCheckinternal()) {
                            trueMoves.push_back(Point(x_castle + 2, y_castle));
                        }
                        movePiece(Point(x_castle + 2, y_castle), position);
                    }
                    else {
                        movePiece(Point(x_castle + 1, y_castle), position);
                    }
                }
            }
            if (LeftCastleBlack) {
                if (getPiece(Point(x_castle - 1, y_castle))->getName() == "EmptyPlace" &&
                    getPiece(Point(x_castle - 2, y_castle))->getName() == "EmptyPlace" &&
                    getPiece(Point(x_castle - 3, y_castle))->getName() == "EmptyPlace") {
                    movePiece(position, Point(x_castle - 1, y_castle));
                    if (!isInCheckinternal()) {
                        movePiece(Point(x_castle - 1, y_castle), Point(x_castle - 2, y_castle));
                        if (!isInCheckinternal()) {
                            trueMoves.push_back(Point(x_castle - 2, y_castle));
                        }
                        movePiece(Point(x_castle - 2, y_castle), position);
                    }
                    else {
                        movePiece(Point(x_castle - 1, y_castle), position);
                    }
                }
            }
        }
    }
}

/**
 * @brief Adds pawn‐specific moves (double-step and en passant) to the provided moves vector.
 *
 * For a pawn at the given position, if it is its first move (or if an en passant capture is available),
 * this function adds the corresponding move(s) to the moves vector.
 *
 * @param moves Reference to the vector of destination Points.
 * @param position The current board position of the pawn.
 */
void Board::addPawnMoves(vector<Point> &moves, Point position) {
    try {
        int x = position.getX();
        int y = position.getY();
        Piece* piece = getPiece(position);
        assert(piece != nullptr && "Null piece pointer in addPawnMoves");
        if (piece->getName() == "Pawn") {
            if (piece->getColor() == "white" && getTurn() == "white") {
                if (y == 1) {
                    if (getPiece(Point(x, y + 2))->getName() == "EmptyPlace" &&
                        getPiece(Point(x, y + 1))->getName() == "EmptyPlace") {
                        moves.push_back(Point(x, y + 2));
                    }
                } else if ((Point(x + 1, y + 1) == enPassant) || (Point(x - 1, y + 1) == enPassant)) {
                    moves.push_back(enPassant);
                }
            } else if (piece->getColor() == "black" && getTurn() == "black") {
                if (y == 6) {
                    if (getPiece(Point(x, y - 2))->getName() == "EmptyPlace" &&
                        getPiece(Point(x, y - 1))->getName() == "EmptyPlace") {
                        moves.push_back(Point(x, y - 2));
                    }
                } else if ((Point(x + 1, y - 1) == enPassant) || (Point(x - 1, y - 1) == enPassant)) {
                    moves.push_back(enPassant);
                }
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in addPawnMoves: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Computes all possible moves for every piece on the board.
 *
 * Iterates over every board square and calls getPossibleMovesComp() for each position.
 * Only positions that have at least one legal move are added to the returned map.
 *
 * @return std::map<Point, vector<Point>> A map where each key is a starting Point and the value is a vector of legal destination Points.
 */
map<Point, vector<Point>> Board::getAllPossibleMoves() {
    map<Point, vector<Point>> possibleMoves;
    try {
        for (int x = 0; x < 8; x++) {
            for (int y = 0; y < 8; y++) {
                Point point(x, y);
                vector<Point> movees = getPossibleMovesComp(point);
                if (!movees.empty())
                    possibleMoves[point] = movees;
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in getAllPossibleMoves: " << e.what() << std::endl;
        throw;
    }
    return possibleMoves;
}

/**
 * @brief Returns all possible moves for the white pieces.
 *
 * If it is not white’s turn, the turn is temporarily changed to compute white’s moves.
 *
 * @return std::map<Point, vector<Point>> Map of white pieces’ positions and their legal moves.
 */
map<Point, vector<Point>> Board::getAllPossibleWhiteMoves() {
    map<Point, vector<Point>> possibleMoves;
    try {
        if (getTurn() == "white") {
            possibleMoves = getAllPossibleMoves();
        } else {
            changeTurn();
            possibleMoves = getAllPossibleMoves();
            changeTurn();
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in getAllPossibleWhiteMoves: " << e.what() << std::endl;
        throw;
    }
    return possibleMoves;
}

/**
 * @brief Returns all possible moves for the black pieces.
 *
 * If it is not black’s turn, the turn is temporarily changed to compute black’s moves.
 *
 * @return std::map<Point, vector<Point>> Map of black pieces’ positions and their legal moves.
 */
map<Point, vector<Point>> Board::getAllPossibleBlackMoves() {
    map<Point, vector<Point>> possibleMoves;
    try {
        if (getTurn() == "black") {
            possibleMoves = getAllPossibleMoves();
        } else {
            changeTurn();
            possibleMoves = getAllPossibleMoves();
            changeTurn();
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in getAllPossibleBlackMoves: " << e.what() << std::endl;
        throw;
    }
    return possibleMoves;
}

/**
 * @brief Generates a hash string representing the current board state.
 *
 * The hash is built by concatenating each piece’s hash, the castling rights, the current turn, and the en passant square.
 *
 * @return std::string The hash string.
 */
string Board::hashBoard() {
    string hashedBoard = "";
    try {
        for (int x = 0; x < 8; x++) {
            for (int y = 0; y < 8; y++) {
                assert(board[x][y] != nullptr && "Null pointer in board array during hashBoard");
                hashedBoard += board[x][y]->hashPiece();
            }
        }
        hashedBoard += (LeftCastleBlack ? "T" : "F");
        hashedBoard += (RightCastleBlack ? "T" : "F");
        hashedBoard += (LeftCastleWhite ? "T" : "F");
        hashedBoard += (RightCastleWhite ? "T" : "F");
        hashedBoard += to_string(turn == "white");
        hashedBoard += to_string(enPassant.getX());
        hashedBoard += to_string(enPassant.getY());
    }
    catch (const std::exception& e) {
        std::cerr << "Error in hashBoard: " << e.what() << std::endl;
        throw;
    }
    return hashedBoard;
}

/**
 * @brief Determines whether the current player's king is in check.
 *
 * Checks for direct attacks on the king’s position (including pawn, knight, bishop, rook, and queen threats).
 *
 * @return bool True if the king is in check, false otherwise.
 */
bool Board::isInCheckinternal() {
    try {
        vector<Point> test;
        int x, y;
        if (getTurn() == "white") {
            x = WhiteKingPos.getX();
            y = WhiteKingPos.getY();
            test = getPossibleAttacks(WhiteKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                if (getPiece(test[idx])->getName() == "King") {
                    return true;
                }
            }
            // Check for pawn attacks.
            if (getPiece(Point(x + 1, y + 1))->getName() == "Pawn" &&
                getPiece(Point(x + 1, y + 1))->getColor() == "black") {
                return true;
            }
            if (getPiece(Point(x - 1, y + 1))->getName() == "Pawn" &&
                getPiece(Point(x - 1, y + 1))->getColor() == "black") {
                return true;
            }
            // Simulate bishop attack.
            setPiece(WhiteKingPos, &WhiteBishop);
            test = getPossibleAttacks(WhiteKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                string name = getPiece(test[idx])->getName();
                if (name == "Queen" || name == "Bishop") {
                    setPiece(WhiteKingPos, &WhiteKing);
                    return true;
                }
            }
            // Simulate rook attack.
            setPiece(WhiteKingPos, &WhiteRook);
            test = getPossibleAttacks(WhiteKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                string name = getPiece(test[idx])->getName();
                if (name == "Queen" || name == "Rook") {
                    setPiece(WhiteKingPos, &WhiteKing);
                    return true;
                }
            }
            // Simulate knight attack.
            setPiece(WhiteKingPos, &WhiteKnight);
            test = getPossibleAttacks(WhiteKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                if (getPiece(test[idx])->getName() == "Knight") {
                    setPiece(WhiteKingPos, &WhiteKing);
                    return true;
                }
            }
            setPiece(WhiteKingPos, &WhiteKing);
        } else {
            x = BlackKingPos.getX();
            y = BlackKingPos.getY();
            test = getPossibleAttacks(BlackKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                if (getPiece(test[idx])->getName() == "King") {
                    return true;
                }
            }
            // Check for pawn attacks.
            if (getPiece(Point(x + 1, y - 1))->getName() == "Pawn" &&
                getPiece(Point(x + 1, y - 1))->getColor() == "white") {
                return true;
            }
            if (getPiece(Point(x - 1, y - 1))->getName() == "Pawn" &&
                getPiece(Point(x - 1, y - 1))->getColor() == "white") {
                return true;
            }
            // Simulate bishop attack.
            setPiece(BlackKingPos, &BlackBishop);
            test = getPossibleAttacks(BlackKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                string name = getPiece(test[idx])->getName();
                if (name == "Queen" || name == "Bishop") {
                    setPiece(BlackKingPos, &BlackKing);
                    return true;
                }
            }
            // Simulate rook attack.
            setPiece(BlackKingPos, &BlackRook);
            test = getPossibleAttacks(BlackKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                string name = getPiece(test[idx])->getName();
                if (name == "Queen" || name == "Rook") {
                    setPiece(BlackKingPos, &BlackKing);
                    return true;
                }
            }
            // Simulate knight attack.
            setPiece(BlackKingPos, &BlackKnight);
            test = getPossibleAttacks(BlackKingPos);
            for (size_t idx = 0; idx < test.size(); idx++) {
                if (getPiece(test[idx])->getName() == "Knight") {
                    setPiece(BlackKingPos, &BlackKing);
                    return true;
                }
            }
            setPiece(BlackKingPos, &BlackKing);
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in isInCheckinternal: " << e.what() << std::endl;
        throw;
    }
    return false;
}

/**
 * @brief Checks if the current player's king is in check.
 *
 * If board data have not yet been calculated, they are updated.
 *
 * @return bool True if in check, false otherwise.
 */
bool Board::isInCheck() {
    try {
        if (!isBoardDataCalculated) {
            updateBoard();
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in isInCheck while updating board: " << e.what() << std::endl;
        throw;
    }
    return inCheck;
}

/**
 * @brief Evaluates the current game state.
 *
 * Updates board data if necessary and then returns the board evaluation.
 *
 * @return int The evaluation score.
 */
int Board::evaluateGame() {
    try {
        if (!isBoardDataCalculated) {
            updateBoard();
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in evaluateGame while updating board: " << e.what() << std::endl;
        throw;
    }
    return boardEvaluation;
}

/**
 * @brief Determines if the game is over.
 *
 * If no legal moves are available, the turn is changed and the position is evaluated
 * to decide if it is a checkmate or stalemate.
 *
 * @return std::string A message indicating the outcome ("white won", "black won", "stalemate", or "NONE").
 */
string Board::gameOver() {
    try {
        if (!isBoardDataCalculated) {
            updateBoard();
        }
        if (moves.size() == 0) {
            changeTurn();
            if (isInCheck()) {
                return getTurn() + " won";
            } else {
                return "stalemate";
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in gameOver: " << e.what() << std::endl;
        throw;
    }
    return "NONE";
}

/**
 * @brief Computes the game phase based on remaining material.
 *
 * Uses the sum of the initial scores for the pieces to estimate the game phase,
 * returning a value between 0 (opening) and 1 (endgame).
 *
 * @return float The game phase.
 */
float Board::getGamePhase() {
    try {
        int whitePieces = 0;
        int blackPieces = 0;
        for (int y = 0; y < 8; y++) {
            for (int x = 0; x < 8; x++) {
                Piece* piece = getPiece(Point(x, y));
                if (piece->getName() != "EmptyPlace") {
                    int val = initialScores[piece->getName()];
                    if (piece->getColor() == "white") {
                        whitePieces += val;
                    } else {
                        blackPieces += val;
                    }
                }
            }
        }
        float total = whitePieces + blackPieces;
        float phase = max(0.0f, min(1.0f, (5600.0f - total) / 3600.0f));
        return phase;
    }
    catch (const std::exception& e) {
        std::cerr << "Error in getGamePhase: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Evaluates the control over the central four squares.
 *
 * Each center square controlled by a white piece adds 20 points,
 * and each controlled by a black piece subtracts 20 points.
 *
 * @return int The control score.
 */
int Board::evaluateControlOfKeySquares() {
    int score = 0;
    try {
        Point centerSquares[4] = {Point(3, 3), Point(3, 4), Point(4, 3), Point(4, 4)};
        for (int idx = 0; idx < 4; idx++) {
            Piece* piece = getPiece(centerSquares[idx]);
            if (piece->getColor() == "white") {
                score += 20;
            } else if (piece->getColor() == "black") {
                score -= 20;
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in evaluateControlOfKeySquares: " << e.what() << std::endl;
        throw;
    }
    return score;
}

/**
 * @brief Checks whether the specified king is active (in the central region).
 *
 * A king is considered active if it is positioned roughly in the center of the board.
 *
 * @param color The color of the king ("white" or "black").
 * @return bool True if the king is active, false otherwise.
 */
bool Board::isKingActive(string color) {
    try {
        if (color == "white") {
            int x = WhiteKingPos.getX();
            int y = WhiteKingPos.getY();
            return (2 < x && x < 5) && (2 < y && y < 5);
        } else {
            int x = BlackKingPos.getX();
            int y = BlackKingPos.getY();
            return (2 < x && x < 5) && (2 < y && y < 5);
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in isKingActive: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Evaluates control of the center of the board based on possible moves.
 *
 * For every possible move by white that lands in the center (squares 3-4 for both x and y),
 * one point is added; for black, one point is subtracted.
 *
 * @return int The center control score.
 */
int Board::centerControl() {
    int score = 0;
    try {
        for (const auto &pair : getAllPossibleWhiteMoves()) {
            for (const auto &point : pair.second) {
                int x = point.getX();
                int y = point.getY();
                if (x > 2 && x < 5 && y > 2 && y < 5) {
                    score += 1;
                }
            }
        }
        for (const auto &pair : getAllPossibleBlackMoves()) {
            for (const auto &point : pair.second) {
                int x = point.getX();
                int y = point.getY();
                if (x > 2 && x < 5 && y > 2 && y < 5) {
                    score -= 1;
                }
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in centerControl: " << e.what() << std::endl;
        throw;
    }
    return score;
}

/**
 * @brief Computes an overall evaluation of the game state.
 *
 * Combines material, king safety, piece coordination, control of key squares, and endgame features.
 * The weights change gradually with the game phase.
 *
 * @return int The total evaluation score.
 */
int Board::evaluateGameinternal() {
    int totalScore = 0;
    try {
        int materialScore = evaluateBoard();
        int centerScore = centerControl();
        // Pawn structure evaluation could be added here.
        int kingSafetyScore = 0;
        int pieceCoordinationScore = 0;
        int controlScore = evaluateControlOfKeySquares();
        int endGameScore = evaluateEndGameFeatures();  // Assumes this function is defined elsewhere.

        float phase = getGamePhase();
        // Opening weight decreases as phase increases; endgame weight increases.
        float openingWeight = 1 - phase;
        float endGameWeight = phase;
        totalScore = static_cast<int>(materialScore * 1 +
                                      kingSafetyScore * 1.0 +
                                      pieceCoordinationScore * 0.6 +
                                      controlScore * (0.6 * openingWeight + 0.3 * endGameWeight) +
                                      endGameScore * endGameWeight);
    }
    catch (const std::exception& e) {
        std::cerr << "Error in evaluateGameinternal: " << e.what() << std::endl;
        throw;
    }
    return totalScore;
}

/**
 * @brief Prompts a human player to choose a piece for pawn promotion.
 *
 * When a pawn reaches the back rank, the player is asked to choose a promotion:
 * 0: Queen, 1: Rook, 2: Bishop, 3: Knight.
 *
 * @param point The board position of the pawn.
 */
void Board::choosePawnHuman(Point point) {
    try {
        if ((getPiece(point)->getName() == "Pawn") && (point.getY() == 0 || point.getY() == 7)) {
            int idx_piece_chosen;
            cout << "Choose a piece to change your pawn into:" << endl;
            cout << "0: Queen    1: Rook    2: Bishop    3: Knight" << endl;
            while (true) {
                cin >> idx_piece_chosen;
                if (idx_piece_chosen >= 0 && idx_piece_chosen < 4) {
                    break;
                }
                cout << "Choose a valid index between 0 and 3" << endl;
            }
            if (getTurn() == "white") {
                switch (idx_piece_chosen) {
                case 0:
                    setPiece(point, &WhiteQueen);
                    break;
                case 1:
                    setPiece(point, &WhiteRook);
                    break;
                case 2:
                    setPiece(point, &WhiteBishop);
                    break;
                case 3:
                    setPiece(point, &WhiteKnight);
                    break;
                }
            }
            else if (getTurn() == "black") {
                switch (idx_piece_chosen) {
                case 0:
                    setPiece(point, &BlackQueen);
                    break;
                case 1:
                    setPiece(point, &BlackRook);
                    break;
                case 2:
                    setPiece(point, &BlackBishop);
                    break;
                case 3:
                    setPiece(point, &BlackKnight);
                    break;
                }
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in choosePawnHuman: " << e.what() << std::endl;
        throw;
    }
}

/**
 * @brief Automatically promotes a pawn for the AI.
 *
 * When a pawn reaches the back rank, it is automatically promoted to a queen.
 *
 * @param point The board position of the pawn.
 */
void Board::choosePawnAi(Point point) {
    try {
        if ((getPiece(point)->getName() == "Pawn") && (point.getY() == 0 || point.getY() == 7)) {
            if (getTurn() == "white") {
                setPiece(point, &WhiteQueen);
            } else {
                setPiece(point, &BlackQueen);
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error in choosePawnAi: " << e.what() << std::endl;
        throw;
    }
}

// --- Initialization of the board ---

/**
 * @brief Initial board configuration.
 *
 * The board is initialized using standard chess starting positions.
 * (For example, White's first rank contains Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook.)
 */
Piece* initialBoard[8][8] = {
    {&WhiteRook,   &WhiteKnight, &WhiteBishop, &WhiteQueen,  &WhiteKing,   &WhiteBishop, &WhiteKnight, &WhiteRook},
    {&WhitePawn,   &WhitePawn,   &WhitePawn,   &WhitePawn,   &WhitePawn,   &WhitePawn,   &WhitePawn,   &WhitePawn},
    {&Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty},
    {&Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty},
    {&Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty},
    {&Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty,       &Empty},
    {&BlackPawn,   &BlackPawn,   &BlackPawn,   &BlackPawn,   &BlackPawn,   &BlackPawn,   &BlackPawn,   &BlackPawn},
    {&BlackRook,   &BlackKnight, &BlackBishop, &BlackQueen,  &BlackKing,   &BlackBishop, &BlackKnight, &BlackRook}
};

/**
 * @brief Global board instance.
 *
 * This Board object is created using the initial configuration with White to move first.
 */
Board initial_board(initialBoard, "white");
