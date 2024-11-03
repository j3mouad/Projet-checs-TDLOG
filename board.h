#include "pieces.h"

class Board{
    private:
        // standard chess board
        Piece board[8][8];
        // a string that can either be white or black
        string turn;
    public:
        Board(Piece* board,string turn);
        Board() = default;
        void changeTurn();
        /* position will be given in chess notations*/
        Point* getPossibleMoves(Point position);
        // this function does not verify if the move is correct that is verified elsewhere
        void movePiece(Point Position1, Point Position2);
       

};

