/**
 * @file game.h
 * @brief Declaration of the Game class and its associated methods.
 */

 #include "player.h"
 #include "board.h"
 #include <utility>
 
 extern Point* initialHeatMap;
 
 /**
  * @brief The Game class encapsulates the logic for managing a chess game.
  *
  * This class handles the game board state, move history, and interactions between players.
  * It supports various gameplay modes such as human vs. human, human vs. random, human vs. AI,
  * and Fischer Random (Chess960) variants.
  */
 class Game {
 private:
     /**
      * @brief A hash map for caching board states.
      */
     std::map<std::string, Board> Hashmap;
 
     /**
      * @brief The current game board.
      */
     Board gameBoard = initial_board;
 
     /**
      * @brief Array of board states representing the game history.
      */
     Board* gameBoards;
 
     /**
      * @brief The current move number.
      */
     int moveNumber = 0;
 
     /**
      * @brief The first player.
      */
     Player player1;
 
     /**
      * @brief The second player.
      */
     Player player2;
 
 public:
     /**
      * @brief Undoes the last move.
      *
      * This function checks if there is a previous move available. If so, it decrements the move counter
      * and resets the game board to the previous state.
      *
      * @return True if a move was undone; false otherwise.
      */
     bool undo() { // true if it did undo, false otherwise
         if (moveNumber > 0) {
             moveNumber--;
             gameBoard = gameBoards[moveNumber];
             return true;
         }
         return false;
     }
 
     /**
      * @brief Starts the game loop for human vs. human gameplay.
      */
     void play();
 
     /**
      * @brief Starts the game loop for playing against a random move generator.
      */
     void play_against_random();
 
     /**
      * @brief Starts the game loop for human vs. AI gameplay.
      */
     void play_against_ai();
 
     /**
      * @brief Starts the game loop for Fischer Random (Chess960) gameplay.
      *
      * @param onevone Optional parameter. If true, plays human vs. human; if false, plays against an AI.
      */
     void play_fisher(bool onevone = true);
 
     /**
      * @brief Computes the minimax evaluation of the current game state.
      *
      * This function performs a minimax search with alpha-beta pruning.
      *
      * @param depth The search depth.
      * @param alpha The current alpha value (default: -INT_MAX).
      * @param beta The current beta value (default: INT_MAX).
      * @return The minimax evaluation score.
      */
     int minimax(int depth, int alpha = -INT_MAX, int beta = INT_MAX);
 
     /**
      * @brief Determines the best move for the current game state using the minimax algorithm.
      *
      * @param depth The search depth for the minimax algorithm.
      * @return A pair of Points representing the source and destination of the best move.
      */
     std::pair<Point, Point> getMinimaxMove(int depth);
 };
 