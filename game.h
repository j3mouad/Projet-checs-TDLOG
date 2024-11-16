#include "board.h"
#include "player.h"

class Game{
    private:
        Board gameBoard = initial_board;
        Player player1,player2;
        vector<Point> getPossibleMoves(Point position); // checks for special moves
    public:
        void play();
};