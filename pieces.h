#pragma once
#include <iostream>
#include <string>
using namespace std;
#include "utils.h"
#include <map>
#include <Imagine/Graphics.h>
using namespace Imagine;

/**
 * @brief Represents a chess piece.
 *
 * The Piece class encapsulates the properties and behavior of a chess piece, including its
 * name, color, movement abilities, associated image, and positional scoring information.
 */
class Piece {
private:
    /**
     * @brief The name of the piece (e.g., "Pawn", "King").
     */
    string name;
    
    /**
     * @brief The color of the piece ("white" or "black").
     */
    string color;
    
    /**
     * @brief Indicates whether the piece has infinite movement (e.g., Rook, Bishop, Queen).
     */
    bool infiniteMoves;
    
    /**
     * @brief Flag indicating if the basic move set is also used as the attack move set.
     */
    bool moveSetisAttackMoveSet = true;
    
    /**
     * @brief Pointer to an array of Points representing the attack move set.
     *
     * The attack move set defines the directions in which a piece can capture an opponent's piece.
     */
    const Point* attackMoveSet;
    
    /**
     * @brief Pointer to an array of Points representing the basic (elementary) move set.
     *
     * The basic move set defines the directions in which a piece can move.
     */
    const Point* elemMoveSet;
    
    /**
     * @brief The number of moves in the basic move set.
     */
    int numOfMoves;
    
    /**
     * @brief The number of moves in the attack move set.
     */
    int numOfAttackMoves;
    
    /**
     * @brief Pointer to the image data for the piece.
     */
    byte* image;
    
    /**
     * @brief Pointer to an array of integers used for positional scoring.
     */
    const int* scores;

public:
    /**
     * @brief Constructs a Piece object with a single move set.
     *
     * This constructor initializes a piece with the given name, color, basic move set, and positional scores.
     * It loads the image from the specified path. The image is expected to be 60x60 pixels.
     *
     * @param names The name of the piece.
     * @param colors The color of the piece.
     * @param infiniteMoves Flag indicating whether the piece has infinite moves.
     * @param elemMoveSet Pointer to an array of Points representing the basic move set.
     * @param numOfMoves The number of moves in the basic move set.
     * @param path The file path to the piece's image.
     * @param scores Pointer to an array of integers for positional scoring.
     */
    Piece(string names, string colors, bool infiniteMoves, const Point* elemMoveSet, int numOfMoves, const char* path, const int* scores);

    /**
     * @brief Constructs a Piece object with separate basic and attack move sets.
     *
     * This constructor initializes a piece with distinct move sets for movement and for attacking.
     * It loads the piece's image from the specified path (expected to be 60x60 pixels).
     *
     * @param name The name of the piece.
     * @param color The color of the piece.
     * @param infiniteMoves Flag indicating whether the piece can move infinitely.
     * @param elemMoveSet Pointer to an array of Points representing the basic move set.
     * @param attackMoveSet Pointer to an array of Points representing the attack move set.
     * @param numOfMoves The number of moves in the basic move set.
     * @param numOfAttackMoves The number of moves in the attack move set.
     * @param path The file path to the piece's image.
     * @param scores Pointer to an array of integers for positional scoring.
     */
    Piece(string name, string(color), bool infiniteMoves, const Point* elemMoveSet, const Point* attackMoveSet, int numOfMoves, int numOfAttackMoves, const char* path, const int* scores);

    /**
     * @brief Copy constructor.
     *
     * Creates a copy of an existing Piece.
     *
     * @param other The Piece object to copy.
     */
    Piece(const Piece &other) : name(other.name), color(other.color), infiniteMoves(other.infiniteMoves), elemMoveSet(other.elemMoveSet), numOfMoves(other.numOfMoves), attackMoveSet(other.attackMoveSet), moveSetisAttackMoveSet(other.moveSetisAttackMoveSet), numOfAttackMoves(other.numOfAttackMoves), image(other.image), scores(other.scores) {}

    /**
     * @brief Default constructor.
     */
    Piece() = default;

    // Getter functions

    /**
     * @brief Returns a test score from the positional score table.
     *
     * This function returns the score located at position (4,4) of the piece's score table.
     *
     * @return The score at position (4,4).
     */
    int testing_scores() {
        const int (*scoreTable)[8] = reinterpret_cast<const int(*)[8]>(scores);
        return scoreTable[4][4]; 
    }

    /**
     * @brief Retrieves the positional score at the specified coordinates.
     *
     * @param x The x-coordinate.
     * @param y The y-coordinate.
     * @return The score from the score table at position (y, x).
     */
    int getScore(int x, int y) {
        const int (*scoreTable)[8] = reinterpret_cast<const int(*)[8]>(scores);
        return scoreTable[y][x]; 
    }

    /**
     * @brief Generates a hash string representation of the piece.
     *
     * This function returns a one-character string that represents the piece's type and color,
     * used for board state hashing.
     *
     * @return A string hash representing the piece.
     */
    string hashPiece() const;

    /**
     * @brief Gets the name of the piece.
     *
     * @return The piece's name.
     */
    string getName() const { return name; }

    /**
     * @brief Gets the color of the piece.
     *
     * @return The piece's color.
     */
    string getColor() const { return color; }

    /**
     * @brief Gets the image data for the piece.
     *
     * @return A pointer to the image data.
     */
    byte* getImage() const { return image; }

    /**
     * @brief Checks if the piece has infinite movement.
     *
     * @return True if the piece has infinite moves; otherwise, false.
     */
    bool hasInfiniteMoves() const { return infiniteMoves; }

    /**
     * @brief Checks if the basic move set is used as the attack move set.
     *
     * @return True if the basic move set is used as the attack move set; otherwise, false.
     */
    bool isMoveSetAttackMoveSet() const { return moveSetisAttackMoveSet; }

    /**
     * @brief Gets the number of attack moves.
     *
     * @return The number of attack moves.
     */
    int numberOfAttackMoves() const { return numOfAttackMoves; }

    /**
     * @brief Gets the number of basic moves.
     *
     * @return The number of basic moves.
     */
    int numberOfElemMoves() const { return numOfMoves; }

    /**
     * @brief Retrieves the basic move set.
     *
     * @return A pointer to an array of Points representing the basic move set.
     */
    const Point* getElemMoveSet() const { return elemMoveSet; }

    /**
     * @brief Retrieves the attack move set.
     *
     * @return A pointer to an array of Points representing the attack move set.
     */
    const Point* getAttackMoveSet() const { return attackMoveSet; }
};

// Global piece declarations

/**
 * @brief Global instance of the white king.
 */
extern Piece WhiteKing;

/**
 * @brief Global instance of the white queen.
 */
extern Piece WhiteQueen;

/**
 * @brief Global instance of the white bishop.
 */
extern Piece WhiteBishop;

/**
 * @brief Global instance of the white rook.
 */
extern Piece WhiteRook;

/**
 * @brief Global instance of the white knight.
 */
extern Piece WhiteKnight;

/**
 * @brief Global instance of the white pawn.
 */
extern Piece WhitePawn;

/**
 * @brief Global instance representing an empty board square.
 */
extern Piece Empty;

/**
 * @brief Global instance of the black king.
 */
extern Piece BlackKing;

/**
 * @brief Global instance of the black queen.
 */
extern Piece BlackQueen;

/**
 * @brief Global instance of the black bishop.
 */
extern Piece BlackBishop;

/**
 * @brief Global instance of the black rook.
 */
extern Piece BlackRook;

/**
 * @brief Global instance of the black knight.
 */
extern Piece BlackKnight;

/**
 * @brief Global instance of the black pawn.
 */
extern Piece BlackPawn;

/**
 * @brief Global map containing initial material scores for each piece type.
 */
extern map<string,int> initialScores;

/**
 * @brief Global standard map for board moves.
 */
extern map<Point,vector<Point>> STDMAP;
