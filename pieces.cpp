#include "pieces.h"

// Constructors
Piece::Piece(string names, string colors, bool infiniteMovess, const Point* elemMoveSets, int numOfMovess, const char* path){
    int width,height;
    loadGreyImage(path,image,width,height);
    if(height != 60 || width != 60) cout << "something's not right" << endl;
    name = names;
    color = colors;
    infiniteMoves = infiniteMovess;
    elemMoveSet = elemMoveSets;
    numOfMoves = numOfMovess;
}

Piece::Piece(string names, string colors, bool infiniteMovess, const Point* elemMoveSets, const Point* attackMoveSets, int numOfMovess, int numOfAttackMovess, const char* path){
    int width,height;
    loadGreyImage(path,image,width,height);
    if(height != 60 || width != 60) cout << "something's not right" << endl;
    name = names;
    color = colors;
    infiniteMoves = infiniteMovess;
    elemMoveSet = elemMoveSets;
    moveSetisAttackMoveSet = false;
    attackMoveSet = attackMoveSets;
    numOfMoves = numOfMovess; 
    numOfAttackMoves = numOfAttackMovess;
}

// Define the paths 
const char* pathPawnWhite = srcPath("Python/white_pawn.png");
const char* pathPawnBlack = srcPath("Python/black_pawn.png");
const char* pathKingWhite = srcPath("Python/white_king.png");
const char* pathKingBlack = srcPath("Python/black_king.png");
const char* pathKnightWhite = srcPath("Python/white_knight.png");
const char* pathKnightBlack = srcPath("Python/black_knight.png");
const char* pathRookWhite = srcPath("Python/white_rook.png");
const char* pathRookBlack = srcPath("Python/black_rook.png");
const char* pathBishopWhite = srcPath("Python/white_bishop.png");
const char* pathBishopBlack = srcPath("Python/black_bishop.png");
const char* pathQueenWhite = srcPath("Python/white_queen.png");
const char* pathQueenBlack = srcPath("Python/black_queen.png");
const char* pathEmpty = srcPath("");

// Define move sets as const arrays
const Point KingAndQueenMoveSet[] = {Point(1,0), Point(1,1), Point(0,1), Point(-1,1), Point(-1,0), Point(-1,-1), Point(0,-1), Point(1,-1)};
const Point RookMoveSet[] = {Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)};
const Point BishopMoveSet[] = {Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)};
const Point KnightMoveSet[] = {Point(2,1), Point(1,2), Point(-1,2), Point(-2,1), Point(-2,-1), Point(-1,-2), Point(1,-2) ,Point(2,-1)};
const Point WhitePawnMoveSet[] = {Point(0,1)};
const Point WhitePawnAttackMoveSet[] = {Point(1,1),Point(-1,1)};
const Point BlackPawnMoveSet[] = {Point(0,-1)};
const Point BlackPawnAttackMoveSet[] = {Point(1,-1),Point(-1,-1)};
const Point emptyMoveSet[] = {};

// Create piece instances
Piece WhiteKing("King", "white", false, KingAndQueenMoveSet,8,pathKingWhite);
Piece WhiteQueen("Queen", "white", true, KingAndQueenMoveSet,8,pathQueenWhite);
Piece WhiteBishop("Bishop", "white", true, BishopMoveSet,4,pathBishopWhite);
Piece WhiteRook("Rook", "white", true, RookMoveSet,4,pathRookWhite);
Piece WhiteKnight("Knight", "white", false, KnightMoveSet,8,pathKnightWhite);
Piece WhitePawn("Pawn", "white", false, WhitePawnMoveSet, WhitePawnAttackMoveSet,1,2,pathPawnWhite);
Piece Empty("EmptyPlace","none", false, emptyMoveSet,0,pathEmpty);
Piece BlackKing("King", "black", false, KingAndQueenMoveSet,8,pathKingBlack);
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet,8,pathQueenBlack);
Piece BlackBishop("Bishop", "black" ,true, BishopMoveSet,4,pathBishopBlack);
Piece BlackRook("Rook", "black", true, RookMoveSet,4,pathRookBlack);
Piece BlackKnight("Knight", "black", false, KnightMoveSet,8,pathKnightBlack);
Piece BlackPawn("Pawn", "black", false, BlackPawnMoveSet, BlackPawnAttackMoveSet,1,2,pathPawnBlack);
