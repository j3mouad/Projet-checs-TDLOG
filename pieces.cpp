/**
 * @file pieces.cpp
 * @brief Implementation of the Piece class and global definitions.
 */

#include "pieces.h"

/**
 * @brief Constructor for a Piece.
 *
 * This constructor initializes a Piece object with the given name, color, movement properties,
 * image path, and score table.
 *
 * @param names The name of the piece.
 * @param colors The color of the piece.
 * @param infiniteMovess Indicates if the piece has infinite moves.
 * @param elemMoveSets Pointer to an array of Points representing the basic move set.
 * @param numOfMovess The number of moves in the basic move set.
 * @param path Path to the image file representing the piece.
 * @param Scores Pointer to an array of scores for the piece.
 */
Piece::Piece(string names, string colors, bool infiniteMovess, const Point* elemMoveSets, int numOfMovess, const char* path, const int* Scores){
    int width,height;
    Imagine::loadGreyImage(path,image,width,height);
    if(height != 60 || width != 60) cout << "something's not right" << endl;
    name = names;
    color = colors;
    infiniteMoves = infiniteMovess;
    elemMoveSet = elemMoveSets;
    numOfMoves = numOfMovess;
    scores = Scores;
}

/**
 * @brief Constructor for a Piece with separate attack move set.
 *
 * This constructor initializes a Piece object with the given name, color, movement properties including
 * a separate attack move set, image path, and score table.
 *
 * @param names The name of the piece.
 * @param colors The color of the piece.
 * @param infiniteMovess Indicates if the piece has infinite moves.
 * @param elemMoveSets Pointer to an array of Points representing the basic move set.
 * @param attackMoveSets Pointer to an array of Points representing the attack move set.
 * @param numOfMovess The number of moves in the basic move set.
 * @param numOfAttackMovess The number of moves in the attack move set.
 * @param path Path to the image file representing the piece.
 * @param Scores Pointer to an array of scores for the piece.
 */
Piece::Piece(string names, string colors, bool infiniteMovess, const Point* elemMoveSets, const Point* attackMoveSets, int numOfMovess, int numOfAttackMovess, const char* path, const int* Scores){
    int width,height;
    Imagine::loadGreyImage(path,image,width,height);
    if(height != 60 || width != 60) cout << "something's not right" << endl;
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
 * @brief Generates a hash representation of the piece.
 *
 * Returns a single character string representing the piece type and color.
 *
 * @return A string hash of the piece.
 */
string Piece::hashPiece() const{
    if (name == "EmptyPlace"){
        return "E";
    }
    if (name == "Pawn"){
        if(color == "white"){
            return "p";
        } else {
            return "P";
        }
    }
    if (name == "King"){
        if(color == "white"){
            return "k";
        } else {
            return "K";
        }
    }
    if (name == "Queen"){
        if(color == "white"){
            return "q";
        } else {
            return "Q";
        }
    }
    if (name == "Bishop"){
        if(color == "white"){
            return "b";
        } else {
            return "B";
        }
    }
    if (name == "Knight"){
        if(color == "white"){
            return "n";
        } else {
            return "N";
        }
    }
    if (name == "Rook"){
        if(color == "white"){
            return "r";
        } else {
            return "R";
        }
    }
}

/**
 * @brief Path for white pawn image.
 */
const char* pathPawnWhite = srcPath("python/images/white_pawn.png");

/**
 * @brief Path for black pawn image.
 */
const char* pathPawnBlack = srcPath("python/images/black_pawn.png");

/**
 * @brief Path for white king image.
 */
const char* pathKingWhite = srcPath("python/images/white_king.png");

/**
 * @brief Path for black king image.
 */
const char* pathKingBlack = srcPath("python/images/black_king.png");

/**
 * @brief Path for white knight image.
 */
const char* pathKnightWhite = srcPath("python/images/white_knight.png");

/**
 * @brief Path for black knight image.
 */
const char* pathKnightBlack = srcPath("python/images/black_knight.png");

/**
 * @brief Path for white rook image.
 */
const char* pathRookWhite = srcPath("python/images/white_rook.png");

/**
 * @brief Path for black rook image.
 */
const char* pathRookBlack = srcPath("python/images/black_rook.png");

/**
 * @brief Path for white bishop image.
 */
const char* pathBishopWhite = srcPath("python/images/white_bishop.png");

/**
 * @brief Path for black bishop image.
 */
const char* pathBishopBlack = srcPath("python/images/black_bishop.png");

/**
 * @brief Path for white queen image.
 */
const char* pathQueenWhite = srcPath("python/images/white_queen.png");

/**
 * @brief Path for black queen image.
 */
const char* pathQueenBlack = srcPath("python/images/black_queen.png");

/**
 * @brief Empty image path.
 */
const char* pathEmpty = srcPath("");

/**
 * @brief Move set for King and Queen.
 */
const Point KingAndQueenMoveSet[] = {Point(1,0), Point(1,1), Point(0,1), Point(-1,1), Point(-1,0), Point(-1,-1), Point(0,-1), Point(1,-1)};

/**
 * @brief Move set for Rook.
 */
const Point RookMoveSet[] = {Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)};

/**
 * @brief Move set for Bishop.
 */
const Point BishopMoveSet[] = {Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)};

/**
 * @brief Move set for Knight.
 */
const Point KnightMoveSet[] = {Point(2,1), Point(1,2), Point(-1,2), Point(-2,1), Point(-2,-1), Point(-1,-2), Point(1,-2) ,Point(2,-1)};

/**
 * @brief Move set for white pawn.
 */
const Point WhitePawnMoveSet[] = {Point(0,1)};

/**
 * @brief Attack move set for white pawn.
 */
const Point WhitePawnAttackMoveSet[] = {Point(1,1),Point(-1,1)};

/**
 * @brief Move set for black pawn.
 */
const Point BlackPawnMoveSet[] = {Point(0,-1)};

/**
 * @brief Attack move set for black pawn.
 */
const Point BlackPawnAttackMoveSet[] = {Point(1,-1),Point(-1,-1)};

/**
 * @brief Empty move set.
 */
const Point emptyMoveSet[] = {};

/**
 * @brief Score table for Pawn.
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
 * @brief Score table for Knight.
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
 * @brief Score table for Bishop.
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
 * @brief Score table for Rook.
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
 * @brief Score table for Queen.
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
 * @brief Score table for King.
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

/**
 * @brief Initial scores mapping for pieces.
 *
 * Maps piece names to their initial score values.
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
 * @brief A standard vector of Points.
 */
vector<Point> STDVECTOR = {Point(10,10)};

/**
 * @brief A standard map mapping Points to vectors of Points.
 */
map<Point,vector<Point>> STDMAP {
    {Point(10,10), STDVECTOR}
};

/**
 * @brief White King piece.
 */
Piece WhiteKing("King", "white", false, KingAndQueenMoveSet, 8, pathKingWhite,(const int*)KingTable);

/**
 * @brief White Queen piece.
 */
Piece WhiteQueen("Queen", "white", true, KingAndQueenMoveSet, 8, pathQueenWhite, (const int*)QueenTable);

/**
 * @brief White Bishop piece.
 */
Piece WhiteBishop("Bishop", "white", true, BishopMoveSet, 4, pathBishopWhite, (const int*)BishopTable);

/**
 * @brief White Rook piece.
 */
Piece WhiteRook("Rook", "white", true, RookMoveSet, 4, pathRookWhite, (const int*)RookTable);

/**
 * @brief White Knight piece.
 */
Piece WhiteKnight("Knight", "white", false, KnightMoveSet, 8, pathKnightWhite, (const int*)KnightTable);

/**
 * @brief White Pawn piece.
 */
Piece WhitePawn("Pawn", "white", false, WhitePawnMoveSet, WhitePawnAttackMoveSet, 1, 2, pathPawnWhite, (const int*)PawnTable);

/**
 * @brief Empty piece representing an empty place.
 */
Piece Empty("EmptyPlace","none", false, emptyMoveSet, 0, pathEmpty, nullptr);

/**
 * @brief Black King piece.
 */
Piece BlackKing("King", "black", false, KingAndQueenMoveSet, 8, pathKingBlack, (const int*)KingTable);

/**
 * @brief Black Queen piece.
 */
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet, 8, pathQueenBlack, (const int*)QueenTable);

/**
 * @brief Black Bishop piece.
 */
Piece BlackBishop("Bishop", "black" ,true, BishopMoveSet, 4, pathBishopBlack, (const int*)BishopTable);

/**
 * @brief Black Rook piece.
 */
Piece BlackRook("Rook", "black", true, RookMoveSet, 4, pathRookBlack, (const int*)RookTable);

/**
 * @brief Black Knight piece.
 */
Piece BlackKnight("Knight", "black", false, KnightMoveSet, 8, pathKnightBlack, (const int*)KnightTable);

/**
 * @brief Black Pawn piece.
 */
Piece BlackPawn("Pawn", "black", false, BlackPawnMoveSet, BlackPawnAttackMoveSet, 1, 2, pathPawnBlack, (const int*)PawnTable);
