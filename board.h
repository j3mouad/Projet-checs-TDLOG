#pragma once
#include "pieces.h"
#include <vector>

#include <random>
#include <chrono>



class Board{
    private:
        // standard chess board
        Piece board[8][8];
        // a string that can either be white or black
        string turn;

        Point WhiteKingPos = Point(4,0);
        Point BlackKingPos = Point(4,7);

        bool LeftCastleWhite = true;
        bool RightCastleWhite = true;
        bool LeftCastleBlack = true;
        bool RightCastleBlack = true;

        bool isBoardDataCalculated = false;

        int boardEvaluation = 0;
        bool isMinimaxCalculated = false;
        int Minimaxscore = 0;


        map<string,Board>* Hashmap = nullptr;
        
        bool inCheck;
        map<string,int> scores = initialScores;
        map<Point,vector<Point>> moves = STDMAP;

        Point enPassant = Point(-1,-1);

        bool isInCheckinternal();

        int evaluateBoard();
        int evaluatePiece(int x, int y);
        int evaluateGameinternal(); // a little more advanced than evaluate Board

        bool movePiece(Point Position1, Point Position2, bool changeCastling = false);

        void updatecastling(Piece piece, Point Position, Point Position2);
        void updateEnPassant(Piece piece, Point Position, Point Position2);

        

        vector<Point> getPossibleAttacks(Point position);
        vector<Point> getPossibleMoves(Point position);
        vector<Point> getPossibleMovesComp(Point position); // checks for special moves
        map<Point,vector<Point>> getAllPossibleMoves();
        map<Point,vector<Point>> getAllPossibleWhiteMoves();
        map<Point,vector<Point>> getAllPossibleBlackMoves();
    public:
        Board(Piece* board,string turn);
        Board() = default;
        // copy constructor, very important for ai;
        Board(const Board &other);

        void updateBoard();
        bool isBoardCalculated() const{return isBoardDataCalculated;}

        bool isMinimaxCalc() const{return isMinimaxCalculated;}
        int  ScoreMinimax() const{return Minimaxscore;}
        void setMinimaxScore(int score){
            isMinimaxCalculated = true;
            Minimaxscore = score;
        }

        void setGameMap(map<string,Board>* Hash){Hashmap = Hash;}

        string hashBoard();

        void transformToFisher();

        int evaluateGame();

        // getter functions
        Piece getPiece(Point point);
        void setPiece(Point point, Piece piece);
        string getTurn() const {return turn;}
        void changeTurn();

        string gameOver();

        map<Point,vector<Point>> getMoves(){return moves;}

        float getGamePhase();
        bool isInEndGame(){return getGamePhase()>0.7;}
        int evaluateControlOfKeySquares();
        bool isKingActive(string color);
        int evaluateEndGameFeatures(){return 50*isKingActive("white") - 50*isKingActive("Black");}
        int centerControl();


        
        bool movePieceoff(Point Position1, Point Position2);
        void show(); /* temporary */


        bool isInCheck(); // potential ability for improvement by calculating it only once at the beginning of the sentence
        
        void addPawnMoves(vector<Point> &moves, Point position);
        void addCastleMoves(vector<Point> &moves, Point position);


};




extern Board initial_board;

