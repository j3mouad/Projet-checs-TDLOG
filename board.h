#include "pieces.h"
#include <vector>

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
        vector<Point> getPossibleMoves(Point position);
        /* this function does not verify if the move is correct that is verified elsewhere
           returns true if the king is killed*/
        bool movePiece(Point Position1, Point Position2);
        void show(); /* temporary */
       

};

extern Board initial_board;

