#include "pieces.h"

class Board{
    private:
       // standard chess board
       Piece board[8][8];
       // a string that can either be white or black
       string turn;
    public:
       void changeTurn();
       /* position will be given in chess notations*/
       Point* getPossibleMoves(Point position);
       
       

};