
#include "board.h"
#include "player.h"
#include <utility>
#include <map>


extern Point* initialHeatMap;

class Game{
    private:
        Board gameBoard = initial_board;
        Player player1,player2;
    public:
        vector<Point> getPossibleMoves(Point position, Point enPassant); // checks for special moves
        map<pair<int, int>,vector<Point>> getAllPossibleMoves(Point enPassant);
        map<pair<int, int>,vector<Point>> getAllPossibleWhiteMoves(Point enPassant);
        map<pair<int, int>,vector<Point>> getAllPossibleBlackMoves(Point enPassant);
        void play();
        bool isInCheck();
};

