#pragma once
#include "board.h"
#include "player.h"
#include "pieces.h"
extern Point* initialHeatMap;

class Game{
    private:
        Board gameBoard = initial_board;
        Player player1,player2;
    public:
        vector<Point> getPossibleMoves(Point position, Point enPassant); // checks for special moves
        void play();
        bool isInCheck();
};

