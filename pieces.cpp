#include "pieces.h"


// Constructors
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



// Define the paths 
const char* pathPawnWhite = srcPath("python/images/white_pawn.png");
const char* pathPawnBlack = srcPath("python/images/black_pawn.png");
const char* pathKingWhite = srcPath("python/images/white_king.png");
const char* pathKingBlack = srcPath("python/images/black_king.png");
const char* pathKnightWhite = srcPath("python/images/white_knight.png");
const char* pathKnightBlack = srcPath("python/images/black_knight.png");
const char* pathRookWhite = srcPath("python/images/white_rook.png");
const char* pathRookBlack = srcPath("python/images/black_rook.png");
const char* pathBishopWhite = srcPath("python/images/white_bishop.png");
const char* pathBishopBlack = srcPath("python/images/black_bishop.png");
const char* pathQueenWhite = srcPath("python/images/white_queen.png");
const char* pathQueenBlack = srcPath("python/images/black_queen.png");
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

// Define scores per square of a given piece;
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

map<string,int> initialScores = {
    {"King", 100000},
    {"Queen", 900},
    {"Rook", 500},
    {"Knight", 300},
    {"Bishop", 300},
    {"Pawn", 100}
};

vector<Point> STDVECTOR = {Point(10,10)};

map<Point,vector<Point>> STDMAP {
    {Point(10,10), STDVECTOR}
};



Piece WhiteKing("King", "white", false, KingAndQueenMoveSet, 8, pathKingWhite,(const int*)KingTable);
Piece WhiteQueen("Queen", "white", true, KingAndQueenMoveSet, 8, pathQueenWhite, (const int*)QueenTable);
Piece WhiteBishop("Bishop", "white", true, BishopMoveSet, 4, pathBishopWhite, (const int*)BishopTable);
Piece WhiteRook("Rook", "white", true, RookMoveSet, 4, pathRookWhite, (const int*)RookTable);
Piece WhiteKnight("Knight", "white", false, KnightMoveSet, 8, pathKnightWhite, (const int*)KnightTable);
Piece WhitePawn("Pawn", "white", false, WhitePawnMoveSet, WhitePawnAttackMoveSet, 1, 2, pathPawnWhite, (const int*)PawnTable);
Piece Empty("EmptyPlace","none", false, emptyMoveSet, 0, pathEmpty, nullptr);
Piece BlackKing("King", "black", false, KingAndQueenMoveSet, 8, pathKingBlack, (const int*)KingTable);
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet, 8, pathQueenBlack, (const int*)QueenTable);
Piece BlackBishop("Bishop", "black" ,true, BishopMoveSet, 4, pathBishopBlack, (const int*)BishopTable);
Piece BlackRook("Rook", "black", true, RookMoveSet, 4, pathRookBlack, (const int*)RookTable);
Piece BlackKnight("Knight", "black", false, KnightMoveSet, 8, pathKnightBlack, (const int*)KnightTable);
Piece BlackPawn("Pawn", "black", false, BlackPawnMoveSet, BlackPawnAttackMoveSet, 1, 2, pathPawnBlack, (const int*)PawnTable);
