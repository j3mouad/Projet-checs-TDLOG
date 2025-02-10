#include "pieces.h"

/**
 * @brief Constructs a Piece object using a single move set.
 *
 * This constructor initializes a Piece with the specified name, color, basic move set, and other properties.
 * It also loads the piece's image from the given path. The image is expected to have dimensions 60x60 pixels.
 *
 * @param names The name of the piece.
 * @param colors The color of the piece.
 * @param infiniteMovess Flag indicating whether the piece has infinite moves (e.g., Rook, Bishop, Queen).
 * @param elemMoveSets Pointer to an array of Points representing the basic move set.
 * @param numOfMovess The number of moves in the basic move set.
 * @param path The file path to the image of the piece.
 * @param Scores Pointer to an array of integers used for positional scoring.
 */
Piece::Piece(string names, string colors, bool infiniteMovess, const Point* elemMoveSets, int numOfMovess, const char* path, const int* Scores) {
    int width, height;
    loadGreyImage(path, image, width, height);
    if (height != 60 || width != 60)
        cout << "something's not right" << endl;
    name = names;
    color = colors;
    infiniteMoves = infiniteMovess;
    elemMoveSet = elemMoveSets;
    numOfMoves = numOfMovess;
    scores = Scores;
}

/**
 * @brief Constructs a Piece object with separate basic and attack move sets.
 *
 * This constructor initializes a Piece with distinct move sets for general movement and for attacks.
 * It loads the piece's image from the specified path, which is expected to be 60x60 pixels.
 *
 * @param names The name of the piece.
 * @param colors The color of the piece.
 * @param infiniteMovess Flag indicating whether the piece can move infinitely.
 * @param elemMoveSets Pointer to an array of Points representing the basic move set.
 * @param attackMoveSets Pointer to an array of Points representing the attack move set.
 * @param numOfMovess The number of moves in the basic move set.
 * @param numOfAttackMovess The number of moves in the attack move set.
 * @param path The file path to the image of the piece.
 * @param Scores Pointer to an array of integers used for positional scoring.
 */
Piece::Piece(string names, string colors, bool infiniteMovess, const Point* elemMoveSets, const Point* attackMoveSets, int numOfMovess, int numOfAttackMovess, const char* path, const int* Scores) {
    int width, height;
    loadGreyImage(path, image, width, height);
    if (height != 60 || width != 60)
        cout << "something's not right" << endl;
    name = names;
    color = colors;
    infiniteMoves = infiniteMovess;
    elemMoveSet = elemMoveSets;
    moveSetisAttackMoveSet = false;
    attackMoveSet = attackMoveSets;
    numOfMoves = numOfMovess;
    numOfAttackMoves = numOfAttackMovess;
    scores = Scores;
}

/**
 * @brief Generates a hash string representation of the piece.
 *
 * This function returns a one-character string that represents the piece for board hashing purposes.
 * For example, an empty square returns "E", while a white pawn returns "p" and a black pawn returns "P".
 *
 * @return A string hash representing the piece.
 */
string Piece::hashPiece() const {
    if (name == "EmptyPlace") {
        return "E";
    }
    if (name == "Pawn") {
        if (color == "white") {
            return "p";
        } else {
            return "P";
        }
    }
    if (name == "King") {
        if (color == "white") {
            return "k";
        } else {
            return "K";
        }
    }
    if (name == "Queen") {
        if (color == "white") {
            return "q";
        } else {
            return "Q";
        }
    }
    if (name == "Bishop") {
        if (color == "white") {
            return "b";
        } else {
            return "B";
        }
    }
    if (name == "Knight") {
        if (color == "white") {
            return "n";
        } else {
            return "N";
        }
    }
    if (name == "Rook") {
        if (color == "white") {
            return "r";
        } else {
            return "R";
        }
    }
    return "";
}

//============================================================================
// Global definitions: Image paths
//============================================================================

/**
 * @brief Path to the white pawn image.
 */
const char* pathPawnWhite = srcPath("python/images/white_pawn.png");

/**
 * @brief Path to the black pawn image.
 */
const char* pathPawnBlack = srcPath("python/images/black_pawn.png");

/**
 * @brief Path to the white king image.
 */
const char* pathKingWhite = srcPath("python/images/white_king.png");

/**
 * @brief Path to the black king image.
 */
const char* pathKingBlack = srcPath("python/images/black_king.png");

/**
 * @brief Path to the white knight image.
 */
const char* pathKnightWhite = srcPath("python/images/white_knight.png");

/**
 * @brief Path to the black knight image.
 */
const char* pathKnightBlack = srcPath("python/images/black_knight.png");

/**
 * @brief Path to the white rook image.
 */
const char* pathRookWhite = srcPath("python/images/white_rook.png");

/**
 * @brief Path to the black rook image.
 */
const char* pathRookBlack = srcPath("python/images/black_rook.png");

/**
 * @brief Path to the white bishop image.
 */
const char* pathBishopWhite = srcPath("python/images/white_bishop.png");

/**
 * @brief Path to the black bishop image.
 */
const char* pathBishopBlack = srcPath("python/images/black_bishop.png");

/**
 * @brief Path to the white queen image.
 */
const char* pathQueenWhite = srcPath("python/images/white_queen.png");

/**
 * @brief Path to the black queen image.
 */
const char* pathQueenBlack = srcPath("python/images/black_queen.png");

/**
 * @brief An empty image path (used for empty board squares).
 */
const char* pathEmpty = srcPath("");

//============================================================================
// Global definitions: Move sets as constant arrays
//============================================================================

/**
 * @brief Move set for both king and queen.
 */
const Point KingAndQueenMoveSet[] = {Point(1,0), Point(1,1), Point(0,1), Point(-1,1), Point(-1,0), Point(-1,-1), Point(0,-1), Point(1,-1)};

/**
 * @brief Move set for rooks.
 */
const Point RookMoveSet[] = {Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)};

/**
 * @brief Move set for bishops.
 */
const Point BishopMoveSet[] = {Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)};

/**
 * @brief Move set for knights.
 */
const Point KnightMoveSet[] = {Point(2,1), Point(1,2), Point(-1,2), Point(-2,1), Point(-2,-1), Point(-1,-2), Point(1,-2), Point(2,-1)};

/**
 * @brief Standard move set for white pawns.
 */
const Point WhitePawnMoveSet[] = {Point(0,1)};

/**
 * @brief Attack move set for white pawns.
 */
const Point WhitePawnAttackMoveSet[] = {Point(1,1), Point(-1,1)};

/**
 * @brief Standard move set for black pawns.
 */
const Point BlackPawnMoveSet[] = {Point(0,-1)};

/**
 * @brief Attack move set for black pawns.
 */
const Point BlackPawnAttackMoveSet[] = {Point(1,-1), Point(-1,-1)};

/**
 * @brief An empty move set.
 */
const Point emptyMoveSet[] = {};

//============================================================================
// Global definitions: Positional evaluation tables
//============================================================================

/**
 * @brief Positional evaluation table for pawns.
 */
const int PawnTable[8][8] = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {10, 10, 10, 10, 10, 10, 10, 10},
    {5, 5, 10, 20, 20, 10, 5, 5},
    {0, 0, 10, 30, 30, 10, 0, 0},
    {5, 5, 20, 40, 40, 20, 5, 5},
    {10, 10, 20, 50, 50, 20, 10, 10},
    {20, 20, 30, 20, 20, 30, 20, 20},
    {0, 0, 0, 0, 0, 0, 0, 0}
};

/**
 * @brief Positional evaluation table for knights.
 */
const int KnightTable[8][8] = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {10, 20, 0, 5, 5, 0, 20, 10},
    {-30, 5, 30, 30, 30, 30, 5, -30},
    {10, 10, 30, 30, 30, 30, 10, 10},
    {10, 10, 30, 30, 40, 30, 10, 10},
    {-30, 5, 30, 30, 30, 30, 5, -30},
    {10, 20, 0, 5, 5, 0, 20, 10},
    {0, 0, 0, 0, 0, 0, 0, 0}
};

/**
 * @brief Positional evaluation table for bishops.
 */
const int BishopTable[8][8] = {
    {20, 10, 10, 10, 10, 10, 10, 20},
    {10, 30, 0, 0, 0, 0, 30, 10},
    {10, 0, 5, 10, 10, 5, 0, 10},
    {10, 5, 10, 15, 15, 10, 5, 10},
    {10, 5, 10, 15, 15, 10, 5, 10},
    {10, 0, 5, 10, 10, 5, 0, 10},
    {10, 30, 0, 0, 0, 0, 30, 10},
    {20, 10, 10, 10, 10, 10, 10, 20}
};

/**
 * @brief Positional evaluation table for rooks.
 */
const int RookTable[8][8] = {
    {0, -50, 10, 15, 15, 10, -50, 0},    
    {5, 10, 15, 20, 20, 15, 10, 5},    
    {10, 15, 20, 25, 25, 20, 15, 10},   
    {15, 20, 25, 30, 30, 25, 20, 15},   
    {20, 25, 30, 35, 35, 30, 25, 20},
    {15, 20, 25, 30, 30, 25, 20, 15},
    {10, 15, 20, 25, 25, 20, 15, 10},
    {0, -50, 10, 15, 15, 10, -50, 0}
};

/**
 * @brief Positional evaluation table for queens.
 */
const int QueenTable[8][8] = {
    {20, 10, 10, 5, 5, 10, 10, 20},
    {10, 0, 0, 0, 0, 0, 0, 10},
    {10, 0, 50, 50, 50, 50, 0, 10},
    {5, 0, 50, 100, 100, 50, 0, 5},
    {0, 50, 50, 100, 100, 50, 50, 0},
    {10, 50, 50, 50, 50, 50, 0, 10},
    {10, 0, 50, 0, 0, 0, 0, 10},
    {20, 10, 10, 5, 5, 10, 10, 20}
};

/**
 * @brief Positional evaluation table for kings.
 */
const int KingTable[8][8] = {
    {30, 40, 40, 50, 50, 40, 40, 30},
    {30, 40, 40, 50, 50, 40, 40, 30},
    {30, 40, 40, 50, 50, 40, 40, 30},
    {30, 40, 40, 50, 50, 40, 40, 30},
    {20, 30, 30, 40, 40, 30, 30, 20},
    {10, 20, 20, 20, 20, 20, 20, 10},
    {20, 20, 0, 0, 0, 0, 20, 20},
    {20, 30, 100, -40, 0, -40, 100, 20}
};

//============================================================================
// Global definitions: Initial scores and standard maps
//============================================================================

/**
 * @brief Initial material scores for each piece type.
 */
map<string,int> initialScores = {
    {"King", 100000},
    {"Queen", 900},
    {"Rook", 500},
    {"Knight", 300},
    {"Bishop", 300},
    {"Pawn", 100}
};

/**
 * @brief A standard vector containing a single Point.
 */
vector<Point> STDVECTOR = {Point(10,10)};

/**
 * @brief A standard map of Points to vectors of Points.
 */
map<Point,vector<Point>> STDMAP {
    {Point(10,10), STDVECTOR}
};

//============================================================================
// Global definitions: Piece instances
//============================================================================

/**
 * @brief Global instance of the white king.
 */
Piece WhiteKing("King", "white", false, KingAndQueenMoveSet, 8, pathKingWhite, (const int*)KingTable);

/**
 * @brief Global instance of the white queen.
 */
Piece WhiteQueen("Queen", "white", true, KingAndQueenMoveSet, 8, pathQueenWhite, (const int*)QueenTable);

/**
 * @brief Global instance of the white bishop.
 */
Piece WhiteBishop("Bishop", "white", true, BishopMoveSet, 4, pathBishopWhite, (const int*)BishopTable);

/**
 * @brief Global instance of the white rook.
 */
Piece WhiteRook("Rook", "white", true, RookMoveSet, 4, pathRookWhite, (const int*)RookTable);

/**
 * @brief Global instance of the white knight.
 */
Piece WhiteKnight("Knight", "white", false, KnightMoveSet, 8, pathKnightWhite, (const int*)KnightTable);

/**
 * @brief Global instance of the white pawn.
 */
Piece WhitePawn("Pawn", "white", false, WhitePawnMoveSet, WhitePawnAttackMoveSet, 1, 2, pathPawnWhite, (const int*)PawnTable);

/**
 * @brief Global instance representing an empty square.
 */
Piece Empty("EmptyPlace", "none", false, emptyMoveSet, 0, pathEmpty, nullptr);

/**
 * @brief Global instance of the black king.
 */
Piece BlackKing("King", "black", false, KingAndQueenMoveSet, 8, pathKingBlack, (const int*)KingTable);

/**
 * @brief Global instance of the black queen.
 */
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet, 8, pathQueenBlack, (const int*)QueenTable);

/**
 * @brief Global instance of the black bishop.
 */
Piece BlackBishop("Bishop", "black", true, BishopMoveSet, 4, pathBishopBlack, (const int*)BishopTable);

/**
 * @brief Global instance of the black rook.
 */
Piece BlackRook("Rook", "black", true, RookMoveSet, 4, pathRookBlack, (const int*)RookTable);

/**
 * @brief Global instance of the black knight.
 */
Piece BlackKnight("Knight", "black", false, KnightMoveSet, 8, pathKnightBlack, (const int*)KnightTable);

/**
 * @brief Global instance of the black pawn.
 */
Piece BlackPawn("Pawn", "black", false, BlackPawnMoveSet, BlackPawnAttackMoveSet, 1, 2, pathPawnBlack, (const int*)PawnTable);
