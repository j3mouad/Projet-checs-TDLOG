#ifndef GAME_H
#define GAME_H

#include "player.h"
#include "board.h"
#include <utility>

/// @brief External variable for initial heat map.
extern Point* initialHeatMap;

/**
 * @brief The Game class manages the game logic, players, and board state.
 */
class Game {
private:
    /// @brief Stores hashed board states for AI decision-making.
    map<string, Board> Hashmap;

    /// @brief The current game board.
    Board gameBoard = initial_board;

    /// @brief Stores all board states for undo functionality.
    Board* gameBoards;

    /// @brief Tracks the number of moves made.
    int moveNumber = 0;

    /// @brief Represents the two players.
    Player player1, player2;

public:
    /**
     * @brief Undoes the last move if possible.
     * @return True if the undo was successful, false otherwise.
     */
    bool undo() {
        if (moveNumber > 0) {
            moveNumber--;
            gameBoard = gameBoards[moveNumber];
            return true;
        }
        return false;
    }

    /// @brief Starts a standard game where two players take turns.
    void play();

    /// @brief Starts a game against a random AI opponent.
    void play_against_random();

    /// @brief Starts a game against an AI opponent using network communication.
    void play_against_ai();

    /**
     * @brief Starts a Fischer Random Chess game.
     * @param onevone If true, the game is player vs. player; otherwise, it's against AI.
     */
    void play_fisher(bool onevone = true);

    /**
     * @brief Implements the Minimax algorithm with Alpha-Beta pruning.
     * @param depth The depth to search in the game tree.
     * @param alpha The alpha value for pruning.
     * @param beta The beta value for pruning.
     * @return The evaluated score of the board position.
     */
    int minimax(int depth, int alpha = -INT_MAX, int beta = INT_MAX);

    /**
     * @brief Determines the best move for the AI using Minimax.
     * @param depth The depth to search in the game tree.
     * @return A pair of Points representing the best move (start position, end position).
     */
    pair<Point, Point> getMinimaxMove(int depth);
};

#endif // GAME_H

