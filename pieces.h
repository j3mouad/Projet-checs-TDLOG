#pragma once
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
    int numOfAttackMoves;

public:
    // Constructors
    Piece(string name, string color, bool infiniteMoves, const Point* elemMoveSet, int numOfMoves)
        : name(name),color(color), infiniteMoves(infiniteMoves), elemMoveSet(elemMoveSet), numOfMoves(numOfMoves) {}
    Piece(string name, string(color), bool infiniteMoves, const Point* elemMoveSet, const Point* attackMoveSet, int numOfMoves, int numOfAttackMoves)
        : name(name), color(color), infiniteMoves(infiniteMoves), elemMoveSet(elemMoveSet),moveSetisAttackMoveSet(false), attackMoveSet(attackMoveSet), numOfMoves(numOfMoves), numOfAttackMoves(numOfAttackMoves) {}
    // Copy Constructor;
    Piece(const Piece &other) : name(other.name), color(other.color), infiniteMoves(other.infiniteMoves), elemMoveSet(other.elemMoveSet), numOfMoves(other.numOfMoves), attackMoveSet(other.attackMoveSet), moveSetisAttackMoveSet(other.moveSetisAttackMoveSet), numOfAttackMoves(other.numOfAttackMoves) {}
    // Default Constructor;
    Piece() = default;
    // Getter functions
    string getName() const {return name;}
    string getColor() const {return color;}
    bool hasInfiniteMoves() const {return infiniteMoves;}
    bool isMoveSetAttackMoveSet() const {return moveSetisAttackMoveSet;}
    int numberOfAttackMoves() const {return numOfAttackMoves;}
    int numberOfElemMoves() const {return numOfMoves;}
    const Point* getElemMoveSet() const {return elemMoveSet;}
    const Point* getAttackMoveSet() const {return attackMoveSet;}
};


extern Piece WhiteKing;
extern Piece WhiteQueen;
extern Piece WhiteBishop;
extern Piece WhiteRook;
extern Piece WhiteKnight;
extern Piece WhitePawn;
extern Piece Empty;
extern Piece BlackKing;
extern Piece BlackQueen;
extern Piece BlackBishop;
extern Piece BlackRook;
extern Piece BlackKnight;
extern Piece BlackPawn;


