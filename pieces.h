#include <iostream>
#include <string>
using namespace std;

class Piece {
private:
    string name;
    bool canJump;
    bool infiniteMoves;
    const string* elemMoveSet;  // Make elemMoveSet a const pointer

public:
    // Constructor with initializer list
    Piece(string name, bool canJump, bool infiniteMoves, const string* elemMoveSet)
        : name(name), canJump(canJump), infiniteMoves(infiniteMoves), elemMoveSet(elemMoveSet) {}
    Piece() = default;
    // Getter functions
    bool canJump() const { return canJump; }
    bool infiniteMoves() const { return infiniteMoves; }
    const string* getElemMoveSet() const { return elemMoveSet; }
};

// Define move sets as const arrays
const string KingAndQueenMoveSet[] = {"us", "ur", "sr", "dr", "ds", "dl", "sl", "ul"};
const string RookMoveSet[] = {"us", "sr", "ds", "sl"};
const string BishopMoveSet[] = {"ur", "dr", "dl", "ul"};
const string KnightMoveSet[] = {"Ur", "uR", "dR", "Dr", "Dl", "dL" ,"uL" ,"Ul"};
const string PawnMoveSet[] = {"us"};

// Create piece instances
Piece King("King", false, false, KingAndQueenMoveSet);
Piece Queen("Queen", false, true, KingAndQueenMoveSet);
Piece Bishop("Bishop", false, true, BishopMoveSet);
Piece Rook("Rook", false, true, RookMoveSet);
Piece Knight("Knight", true, false, KnightMoveSet);
Piece Pawn("Pawn", false, false, PawnMoveSet);



