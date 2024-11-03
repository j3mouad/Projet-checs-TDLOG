#include "board.h"

Board::Board(Piece* initial_board,string Turn){
    turn = Turn;
    for (int idxX= 0; idxX<8; idxX++){
        for (int idxY=0; idxY<8; idxY++){
            board[idxX][idxY] = initial_board[idxX + 8*idxY];
        }
    }
    delete initial_board;
}

// lengthwise 
Piece initialBoard[64] = {
    WhiteRook,WhiteKnight,WhiteBishop,WhiteQueen,WhiteKing,WhiteBishop,WhiteKnight,WhiteRook,
    WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    BlackRook,BlackKnight,BlackBishop,BlackQueen,BlackKing,BlackBishop,BlackKnight,BlackRook,
    BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn
};

Board initial_board(initialBoard,"white");

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
            if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 ){
                multiplier++;
                ListOfPoints[idx_list] = Point(currPosX,currPosY);
                idx_list ++;
                if(board[currPosX][currPosY].getName() != "EmptyPlace"){
                    break;
                }
            }
            else{
                break;
            }
        }
    }
    ListOfPoints[idx_list] = Point(-1,-1); // to know the last element;
    return ListOfPoints;
}

void Board::movePiece(Point Position1, Point Position2){
    Piece piece = board[Position1.getX()][Position2.getY()];
    board[Position1.getX()][Position1.getY()] = Empty;
    board[Position2.getX()][Position2.getY()] = piece;
}