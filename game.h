#include "player.h"
#include "board.h"
#include <utility>


extern Point* initialHeatMap;

class Game{
    private:
        map<string,Board> Hashmap;
        Board gameBoard = initial_board;
        Board* gameBoards;
        int moveNumber = 0;
        Player player1,player2;
    public:
        bool undo(){// true if it did undo, false otherwise
            if (moveNumber > 0){
                moveNumber--;
                gameBoard = gameBoards[moveNumber] ;
                return true;
            }
            return false;
        }
        void play();
        void play_against_random();
        void play_against_ai();
        void play_fisher(bool onevone = true);
        int minimax(int depth, int alpha = -INT_MAX, int beta = INT_MAX);
        pair<Point,Point> getMinimaxMove(int depth);


};

