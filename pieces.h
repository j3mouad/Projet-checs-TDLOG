#include <iostream>
#include <string>
using namespace std;
#include "utils.h"

class Piece {
private:
    /* the name of the piece */
    string name;
    /*white or black*/
    string color;
    /* the ability of a piece to reach the other side of the arena*/
    bool infiniteMoves;
    bool moveSetisAttackMoveSet = true ;
    /* the MoveSet of a given piece given as a two letter string
       the left one is the movement on the y axis and the right 
       one is on the x axis */
    const Point* attackMoveSet;
    const Point* elemMoveSet; 
    int numOfMoves;

public:
    // Constructors
    Piece(string name, string color, bool infiniteMoves, const Point* elemMoveSet, int numOfMoves)
        : name(name),color(color), infiniteMoves(infiniteMoves), elemMoveSet(elemMoveSet), numOfMoves(numOfMoves) {}
    Piece(string name, string(color), bool infiniteMoves, const Point* elemMoveSet, const Point* attackMoveSet, int numOfMoves)
        : name(name), color(color), infiniteMoves(infiniteMoves), elemMoveSet(elemMoveSet),moveSetisAttackMoveSet(false), attackMoveSet(attackMoveSet), numOfMoves(numOfMoves)  {}
    // Copy Constructor;
    Piece(const Piece &other) : name(name), color(other.color), infiniteMoves(infiniteMoves), elemMoveSet(elemMoveSet), numOfMoves(numOfMoves), attackMoveSet(attackMoveSet), moveSetisAttackMoveSet(other.moveSetisAttackMoveSet) {}
    // Default Constructor;
    Piece() = default;
    // Getter functions
    string getName() const { return name; }
    string getColor() const {return color; }
    bool hasInfiniteMoves() const { return infiniteMoves; }
    int numberOfElemMoves() const {return numOfMoves;}
    const Point* getElemMoveSet() const { return elemMoveSet; }
    const Point* getAttackMoveSet() const { return attackMoveSet; }
};

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
Piece Empty("EmptyPlace","white", false, emptyMoveSet,0);
Piece BlackKing("King", "black", false, KingAndQueenMoveSet,8);
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet,8);
Piece BlackBishop("Bishop", "black" ,true, BishopMoveSet,4);
Piece BlackRook("Rook", "black", true, RookMoveSet,4);
Piece BlackKnight("Knight", "black", false, KnightMoveSet,8);
Piece BlackPawn("Pawn", "black", false, PawnMoveSet,PawnAttackMoveSet,1);