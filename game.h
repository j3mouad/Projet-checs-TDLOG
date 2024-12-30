<<<<<<< HEAD

#include "board.h"
#include "player.h"
#include <utility>


=======
#pragma once
#include "board.h"
#include "player.h"
#include "pieces.h"
>>>>>>> Hassen_C++_work
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
        void play_against_random();
        void play_fisher(bool onevone = true);
        bool isInCheck();
};

