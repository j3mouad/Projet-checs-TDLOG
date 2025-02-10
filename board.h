#pragma once
#include "pieces.h"
#include <vector>
#include <random>
#include <chrono>
#include <map>
#include <string>

using std::string;
using std::vector;
using std::map;

/**
 * @brief Represents a chess board and manages the game state.
 *
 * The Board class encapsulates the state and logic of a chess game including piece positions,
 * move generation, game evaluation, and special moves (castling, en passant, pawn promotion).
 */
class Board{
    private:
        /**
         * @brief The chess board represented as an 8x8 array of Piece objects.
         */
        Piece board[8][8];

        /**
         * @brief Indicates the current turn ("white" or "black").
         */
        string turn;

        /**
         * @brief The current position of the white king.
         */
        Point WhiteKingPos = Point(4,0);

        /**
         * @brief The current position of the black king.
         */
        Point BlackKingPos = Point(4,7);

        /**
         * @brief Flag for white's left (queen side) castling rights.
         */
        bool LeftCastleWhite = true;

        /**
         * @brief Flag for white's right (king side) castling rights.
         */
        bool RightCastleWhite = true;

        /**
         * @brief Flag for black's left (queen side) castling rights.
         */
        bool LeftCastleBlack = true;

        /**
         * @brief Flag for black's right (king side) castling rights.
         */
        bool RightCastleBlack = true;

        /**
         * @brief Indicates whether board data (moves, evaluation, etc.) has been calculated.
         */
        bool isBoardDataCalculated = false;

        /**
         * @brief The evaluation score of the board.
         */
        int boardEvaluation = 0;

        /**
         * @brief Indicates if the minimax score has been calculated.
         */
        bool isMinimaxCalculated = false;

        /**
         * @brief The minimax evaluation score.
         */
        int Minimaxscore = 0;

        /**
         * @brief Maps depths to minimax scores.
         */
        map<int,int> depthMap;

        /**
         * @brief Pointer to a hash map used to cache board states.
         */
        map<string,Board>* Hashmap = nullptr;
        
        /**
         * @brief Indicates if the current side's king is in check.
         */
        bool inCheck;

        /**
         * @brief Maps piece names to their evaluation scores.
         */
        map<string,int> scores = initialScores;

        /**
         * @brief Maps board positions to legal moves.
         */
        map<Point,vector<Point>> moves = STDMAP;

        /**
         * @brief The en passant target square. (-1,-1) indicates no en passant is available.
         */
        Point enPassant = Point(-1,-1);

        // Private member functions

        /**
         * @brief Internal function to determine if the current side's king is in check.
         *
         * @return True if the king is in check; false otherwise.
         */
        bool isInCheckinternal();

        /**
         * @brief Evaluates the board based solely on material.
         *
         * @return The material evaluation score.
         */
        int evaluateBoard();

        /**
         * @brief Evaluates the board using an advanced algorithm.
         *
         * This function may include additional factors (such as piece positioning) beyond material.
         *
         * @return The evaluation score of the board.
         */
        int evaluateGameinternal();

        /**
         * @brief Moves a piece from one position to another.
         *
         * Updates castling rights if necessary.
         *
         * @param Position1 The starting position.
         * @param Position2 The destination position.
         * @param changeCastling Optional flag to update castling rights (default is false).
         * @return True if the move results in capturing a king (winning move); false otherwise.
         */
        bool movePiece(Point Position1, Point Position2, bool changeCastling = false);

        /**
         * @brief Updates castling rights and moves the rook accordingly.
         *
         * @param piece The piece being moved.
         * @param Position The source position.
         * @param Position2 The destination position.
         */
        void updatecastling(Piece piece, Point Position, Point Position2);

        /**
         * @brief Updates the en passant target square and performs en passant capture if applicable.
         *
         * @param piece The piece being moved.
         * @param Position The source position.
         * @param Position2 The destination position.
         */
        void updateEnPassant(Piece piece, Point Position, Point Position2);

        /**
         * @brief Computes all possible attack moves for the piece at the given position.
         *
         * @param position The current position of the piece.
         * @return A vector of Points representing valid attack destinations.
         */
        vector<Point> getPossibleAttacks(Point position);

        /**
         * @brief Computes all possible moves (ignoring check) for the piece at the given position.
         *
         * @param position The current position of the piece.
         * @return A vector of Points representing possible moves.
         */
        vector<Point> getPossibleMoves(Point position);

        /**
         * @brief Computes all legal moves for the piece at the given position, including special moves.
         *
         * This function simulates moves to check for legality (e.g., not leaving the king in check)
         * and also adds pawn-specific and castling moves.
         *
         * @param position The current position of the piece.
         * @return A vector of Points representing legal moves.
         */
        vector<Point> getPossibleMovesComp(Point position);

        /**
         * @brief Computes all possible moves for the entire board.
         *
         * @return A map where each key is a board position and its value is a vector of legal destination positions.
         */
        map<Point,vector<Point>> getAllPossibleMoves();

        /**
         * @brief Computes all legal moves for white pieces.
         *
         * @return A map of white's legal moves.
         */
        map<Point,vector<Point>> getAllPossibleWhiteMoves();

        /**
         * @brief Computes all legal moves for black pieces.
         *
         * @return A map of black's legal moves.
         */
        map<Point,vector<Point>> getAllPossibleBlackMoves();
        
    public:
        /**
         * @brief Constructs a Board object with an initial configuration.
         *
         * @param board A pointer to an array of Pieces representing the initial board configuration.
         * @param turn A string indicating which side starts ("white" or "black").
         */
        Board(Piece* board, string turn);

        /**
         * @brief Default constructor.
         */
        Board() = default;

        /**
         * @brief Copy constructor.
         *
         * Creates a deep copy of an existing Board object.
         *
         * @param other The Board object to copy.
         */
        Board(const Board &other);

        /**
         * @brief Prints a textual representation of the board.
         */
        void print();

        /**
         * @brief Updates the board state, including legal moves and evaluation.
         */
        void updateBoard();

        /**
         * @brief Checks if board data has been calculated.
         *
         * @return True if board data is calculated; false otherwise.
         */
        bool isBoardCalculated() const { return isBoardDataCalculated; }

        /**
         * @brief Checks if the minimax score has been calculated.
         *
         * @return True if the minimax score is calculated; false otherwise.
         */
        bool isMinimaxCalc() const { return isMinimaxCalculated; }

        /**
         * @brief Retrieves the minimax score.
         *
         * @return The minimax score.
         */
        int ScoreMinimax() const { return Minimaxscore; }

        /**
         * @brief Sets the minimax score and marks it as calculated.
         *
         * @param score The minimax score to set.
         */
        void setMinimaxScore(int score){
            isMinimaxCalculated = true;
            Minimaxscore = score;
        }

        /**
         * @brief Sets the pointer to the hash map for caching board states.
         *
         * @param Hash Pointer to a map that caches board states.
         */
        void setGameMap(map<string,Board>* Hash){ Hashmap = Hash; }

        /**
         * @brief Generates a string hash representing the current board state.
         *
         * @return A string uniquely representing the board state.
         */
        string hashBoard();

        /**
         * @brief Transforms the board into a Fischer-Random (Chess960) configuration.
         */
        void transformToFisher();

        /**
         * @brief Evaluates the current board position.
         *
         * @return The evaluation score of the board.
         */
        int evaluateGame();

        // Getter functions

        /**
         * @brief Retrieves the piece at a specified board position.
         *
         * @param point The board position.
         * @return The Piece at the given position.
         */
        Piece getPiece(Point point);

        /**
         * @brief Sets a piece at a specified board position.
         *
         * @param point The board position.
         * @param piece The Piece to place.
         */
        void setPiece(Point point, Piece piece);

        /**
         * @brief Retrieves the current turn.
         *
         * @return A string indicating the current turn ("white" or "black").
         */
        string getTurn() const { return turn; }

        /**
         * @brief Changes the turn to the other player.
         */
        void changeTurn();

        /**
         * @brief Checks if a minimax evaluation is stored for the given depth.
         *
         * @param depth The search depth.
         * @return True if a score is stored for that depth; false otherwise.
         */
        bool isMinimaxDepthStored(int depth){
            if(depthMap.find(depth) == depthMap.end()){
                return false;
            }
            return true;
        }

        /**
         * @brief Retrieves the stored minimax score for a given depth.
         *
         * @param depth The search depth.
         * @return The stored minimax score.
         */
        int getMinimaxDepth(int depth){
            return depthMap[depth];
        }

        /**
         * @brief Determines if the game is over (checkmate or stalemate).
         *
         * @return A string indicating the game outcome ("white won", "black won", "stalemate", or "NONE").
         */
        string gameOver();

        /**
         * @brief Retrieves the map of legal moves.
         *
         * @return A map where keys are board positions and values are vectors of legal move destinations.
         */
        map<Point,vector<Point>> getMoves(){ return moves; }

        /**
         * @brief Computes the game phase as a float between 0.0 (opening) and 1.0 (endgame).
         *
         * @return The game phase.
         */
        float getGamePhase();

        /**
         * @brief Checks if the game is in the endgame phase.
         *
         * @return True if the game phase is greater than 0.7 (endgame); false otherwise.
         */
        bool isInEndGame(){ return getGamePhase() > 0.7; }

        /**
         * @brief Evaluates control over key central squares.
         *
         * @return A score representing control of the center squares.
         */
        int evaluateControlOfKeySquares();

        /**
         * @brief Determines if the king is active (centralized) based on its color.
         *
         * @param color The color of the king ("white" or "black").
         * @return True if the king is active; false otherwise.
         */
        bool isKingActive(string color);

        /**
         * @brief Evaluates additional endgame features.
         *
         * @return A score representing endgame features.
         */
        int evaluateEndGameFeatures(){ return 50 * isKingActive("white") - 50 * isKingActive("Black"); }

        /**
         * @brief Computes a score representing control over the center of the board.
         *
         * @return The center control score.
         */
        int centerControl();

        /**
         * @brief Prompts a human player to choose a piece for pawn promotion.
         *
         * @param point The board position of the pawn to be promoted.
         */
        void choosePawnHuman(Point point);

        /**
         * @brief Automatically promotes a pawn for an AI move.
         *
         * @param point The board position of the pawn to be promoted.
         */
        void choosePawnAi(Point point);

        /**
         * @brief Moves a piece, handling special moves and pawn promotion.
         *
         * This function updates castling, en passant, changes the turn, and updates the board state.
         *
         * @param Position1 The source position.
         * @param Position2 The destination position.
         * @param IsPlayer Optional flag indicating if the move is by a human player (default is true).
         * @return True if the move results in capturing a king; false otherwise.
         */
        bool movePieceoff(Point Position1, Point Position2, bool IsPlayer = true);

        /**
         * @brief Renders the board graphically (temporary implementation).
         */
        void show();

        /**
         * @brief Checks if the current side is in check.
         *
         * @return True if in check; false otherwise.
         */
        bool isInCheck();

        /**
         * @brief Adds pawn-specific moves (such as the initial two-square move and en passant).
         *
         * @param moves A reference to a vector of move destinations to update.
         * @param position The board position of the pawn.
         */
        void addPawnMoves(vector<Point> &moves, Point position);

        /**
         * @brief Adds castling moves for the king at the given position.
         *
         * @param moves A reference to a vector of move destinations to update.
         * @param position The board position of the king.
         */
        void addCastleMoves(vector<Point> &moves, Point position);
};

/**
 * @brief External declaration of the initial board configuration.
 */
extern Board initial_board;
