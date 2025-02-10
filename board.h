#pragma once
#include "pieces.h"
#include <vector>
#include <random>
#include <chrono>

/**
 * @brief The Board class represents a chess board and manages game logic.
 */
class Board {
private:
    /// @brief Standard 8x8 chess board containing Piece pointers.
    Piece* board[8][8];

    /// @brief Indicates the current turn ("white" or "black").
    string turn;

    /// @brief Stores the positions of the White and Black Kings.
    Point WhiteKingPos = Point(4, 0);
    Point BlackKingPos = Point(4, 7);

    /// @brief Castling rights for both players.
    bool LeftCastleWhite = true;
    bool RightCastleWhite = true;
    bool LeftCastleBlack = true;
    bool RightCastleBlack = true;

    /// @brief Flags to track board evaluation state.
    bool isBoardDataCalculated = false;

    /// @brief Stores the board evaluation score.
    int boardEvaluation = 0;

    /// @brief Flags and score for Minimax evaluation.
    bool isMinimaxCalculated = false;
    int Minimaxscore = 0;

    /// @brief Stores depth-based evaluation scores for Minimax.
    map<int, int> depthMap;

    /// @brief Hash map for board states, useful for AI search.
    map<string, Board>* Hashmap = nullptr;

    /// @brief Tracks whether the current player is in check.
    bool inCheck;

    /// @brief Stores predefined piece scores.
    map<string, int> scores = initialScores;

    /// @brief Stores possible legal moves for the current turn.
    map<Point, vector<Point>> moves = STDMAP;

    /// @brief Tracks the en passant square.
    Point enPassant = Point(-1, -1);

    /// @brief Determines if the current player is in check.
    bool isInCheckinternal();

    /// @brief Evaluates the board state.
    int evaluateBoard();

    /// @brief Evaluates a piece based on its position.
    int evaluatePiece(int x, int y);

    /// @brief Advanced board evaluation considering position and game state.
    int evaluateGameinternal();

    /**
     * @brief Moves a piece while considering special moves (castling, en passant).
     * @param Position1 Source position.
     * @param Position2 Destination position.
     * @param changeCastling Whether castling rights should be updated.
     * @return True if the move is successful, false otherwise.
     */
    bool movePiece(Point Position1, Point Position2, bool changeCastling = false);

    /// @brief Updates castling rights based on a move.
    void updatecastling(Piece* piece, Point Position, Point Position2);

    /// @brief Updates the en passant target square after a move.
    void updateEnPassant(Piece* piece, Point Position, Point Position2);

    /// @brief Returns a list of positions where a piece can attack.
    vector<Point> getPossibleAttacks(Point position);

    /// @brief Returns a list of all legal moves for a piece.
    vector<Point> getPossibleMoves(Point position);

    /// @brief Returns possible moves considering special rules like castling.
    vector<Point> getPossibleMovesComp(Point position);

    /// @brief Retrieves all possible legal moves on the board.
    map<Point, vector<Point>> getAllPossibleMoves();

    /// @brief Retrieves all possible legal moves for white pieces.
    map<Point, vector<Point>> getAllPossibleWhiteMoves();

    /// @brief Retrieves all possible legal moves for black pieces.
    map<Point, vector<Point>> getAllPossibleBlackMoves();

public:
    /**
     * @brief Constructor for Board.
     * @param board Initial board setup.
     * @param turn The starting turn ("white" or "black").
     */
    Board(Piece* board[8][8], string turn);

    /// @brief Default constructor.
    Board() = default;

    /**
     * @brief Copy constructor for deep copying a board state.
     * @param other The board to copy.
     */
    Board(const Board& other);

    /// @brief Updates the board state and recalculates possible moves.
    void updateBoard();

    /// @brief Checks if board state calculations are up-to-date.
    bool isBoardCalculated() const { return isBoardDataCalculated; }

    /// @brief Checks if Minimax evaluation has been performed.
    bool isMinimaxCalc() const { return isMinimaxCalculated; }

    /// @brief Retrieves the Minimax evaluation score.
    int ScoreMinimax() const { return Minimaxscore; }

    /// @brief Sets the Minimax evaluation score.
    void setMinimaxScore(int score) {
        isMinimaxCalculated = true;
        Minimaxscore = score;
    }

    /// @brief Assigns a hashmap for board states (used for AI calculations).
    void setGameMap(map<string, Board>* Hash) { Hashmap = Hash; }

    /// @brief Generates a hash string for the current board position.
    string hashBoard();

    /// @brief Transforms the board to a Fischer Random Chess setup.
    void transformToFisher();

    /// @brief Evaluates the game state and returns a score.
    int evaluateGame();

    /// @brief Retrieves a piece at a given position.
    Piece* getPiece(Point point);

    /// @brief Sets a piece at a given position.
    void setPiece(Point point, Piece* piece);

    /// @brief Retrieves the current player's turn.
    string getTurn() const { return turn; }

    /// @brief Changes the current player's turn.
    void changeTurn();

    /**
     * @brief Checks if a Minimax depth evaluation has been stored.
     * @param depth The depth to check.
     * @return True if the evaluation is stored, false otherwise.
     */
    bool isMinimaxDepthStored(int depth) {
        return depthMap.find(depth) != depthMap.end();
    }

    /**
     * @brief Stores a Minimax evaluation score for a given depth.
     * @param depth The depth of the evaluation.
     * @param value The evaluation score.
     */
    void setMinimaxDepth(int depth, int value) {
        depthMap[depth] = value;
    }

    /**
     * @brief Retrieves a stored Minimax evaluation score.
     * @param depth The depth of the evaluation.
     * @return The stored Minimax score.
     */
    int getMinimaxDepth(int depth) {
        return depthMap[depth];
    }

    /// @brief Determines if the game is over and returns the result.
    string gameOver();

    /// @brief Retrieves all possible moves for the current player.
    map<Point, vector<Point>> getMoves() { return moves; }

    /// @brief Calculates the game phase (opening, midgame, endgame).
    float getGamePhase();

    /// @brief Checks if the game is in the endgame phase.
    bool isInEndGame() { return getGamePhase() > 0.7; }

    /// @brief Evaluates control over key board squares.
    int evaluateControlOfKeySquares();

    /// @brief Determines if the king is actively positioned.
    bool isKingActive(string color);

    /// @brief Evaluates endgame characteristics.
    int evaluateEndGameFeatures() { return 50 * isKingActive("white") - 50 * isKingActive("Black"); }

    /// @brief Evaluates control of the board's center squares.
    int centerControl();

    /// @brief Handles pawn promotion for a human player.
    void choosePawnHuman(Point point);

    /// @brief Handles pawn promotion for an AI player.
    void choosePawnAi(Point point);

    /**
     * @brief Moves a piece considering special moves and user input.
     * @param Position1 Source position.
     * @param Position2 Destination position.
     * @param IsPlayer Whether the move is made by a player or AI.
     * @return True if the move results in checkmate.
     */
    bool movePieceoff(Point Position1, Point Position2, bool IsPlayer = true);

    /// @brief Displays the board (temporary function for debugging).
    void show();

    /// @brief Determines if the current player is in check.
    bool isInCheck();

    /// @brief Adds legal pawn moves to the move list.
    void addPawnMoves(vector<Point>& moves, Point position);

    /// @brief Adds castling moves to the move list.
    void addCastleMoves(vector<Point>& moves, Point position);
};

/// @brief Stores the initial board configuration.
extern Board initial_board;

