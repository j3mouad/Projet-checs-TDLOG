#include "board.h"

void Board::changeTurn(){
    if (turn == "white"){ turn = "black";}
    else {turn = "white";}
}

Point* Board::getPossibleMoves(Point position){
    int movex,movey;
    int piecePositionX,piecePositionY;
    int currPosX,currPosY;
    int multiplier;
    int idx_list = 0;
    piecePositionX = position.getX();
    piecePositionY = position.getY();
    Piece piece = board[piecePositionX][piecePositionY];
    Point* ListOfPoints = new Point[30];
    const Point* elemMoves = piece.getElemMoveSet();
    for(int idx=0;idx<piece.numberOfElemMoves(); idx++){
        movex = elemMoves[idx].getX();
        movey = elemMoves[idx].getY();
        multiplier = 1;
        while(true){
            if (multiplier == 2 && piece.hasInfiniteMoves()){
                break;
            }
            currPosX = piecePositionX + multiplier*movex;
            currPosY = piecePositionY + multiplier*movey;
            if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosX][currPosY].getName() == "EmptyPlace"){
                multiplier++;
                ListOfPoints[idx_list] = Point(currPosX,currPosY);
                idx_list ++;
            }
            else{
                break;
            }
        }
    }
    ListOfPoints[idx_list] = Point(-1,-1); // to know the last element;
    return ListOfPoints;
}