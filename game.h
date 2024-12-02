
#include "board.h"
#include "player.h"
#include <map>

extern Point* initialHeatMap;

class Game{
    private:
        Board gameBoard = initial_board;
        Player player1,player2;
    public:
        vector<Point> getPossibleMoves(Point position, Point enPassant); // checks for special moves
        map<Point,vector<Point>> getAllPossibleMoves(Point enPassant);
        map<Point,vector<Point>> getAllPossibleWhiteMoves(Point enPassant);
        map<Point,vector<Point>> getAllPossibleBlackMoves(Point enPassant);
        void play();
        bool isInCheck();
};

