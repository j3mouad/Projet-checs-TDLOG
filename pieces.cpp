#include "pieces.h"

#include "pieces.h"

// Define move sets as const arrays
const Point KingAndQueenMoveSet[] = {Point(1,0), Point(1,1), Point(0,1), Point(-1,1), Point(-1,0), Point(-1,-1), Point(0,-1), Point(1,-1)};
const Point RookMoveSet[] = {Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)};
const Point BishopMoveSet[] = {Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)};
const Point KnightMoveSet[] = {Point(2,1), Point(1,2), Point(-1,2), Point(-2,1), Point(-2,-1), Point(-1,-2), Point(1,-2) ,Point(2,-1)};
const Point PawnMoveSet[] = {Point(1,0)};
const Point PawnAttackMoveSet[] = {Point(1,1),Point(1,-1)};
const Point emptyMoveSet[] = {};

// Create piece instances
Piece WhiteKing("King", "white", false, KingAndQueenMoveSet,8);
Piece WhiteQueen("Queen", "white", true, KingAndQueenMoveSet,8);
Piece WhiteBishop("Bishop", "white", true, BishopMoveSet,4);
Piece WhiteRook("Rook", "white", true, RookMoveSet,4);
Piece WhiteKnight("Knight", "white", false, KnightMoveSet,8);
Piece WhitePawn("Pawn", "white", false, PawnMoveSet,PawnAttackMoveSet,1);
Piece Empty("EmptyPlace","none", false, emptyMoveSet,0);
Piece BlackKing("King", "black", false, KingAndQueenMoveSet,8);
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet,8);
Piece BlackBishop("Bishop", "black" ,true, BishopMoveSet,4);
Piece BlackRook("Rook", "black", true, RookMoveSet,4);
Piece BlackKnight("Knight", "black", false, KnightMoveSet,8);
Piece BlackPawn("Pawn", "black", false, PawnMoveSet,PawnAttackMoveSet,1);
