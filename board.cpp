#include "board.h"

Board::Board(Piece* initial__board,string Turn){
    turn = Turn;
    for (int idxY= 0; idxY<8; idxY++){
        for (int idxX=0; idxX<8; idxX++){
            board[idxY][idxX] = initial__board[idxX + 8*idxY];
        }
    }
}


void Board::changeTurn(){
    if (turn == "white"){ turn = "black";}
    else {turn = "white";}
}

vector<Point> Board::getPossibleMoves(Point position){
    int movex,movey;
    int piecePositionX,piecePositionY;
    int currPosX,currPosY;
    int multiplier;
    vector<Point> VectOfMoves;
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
            if (multiplier == 2 && piece.hasInfiniteMoves() == false){
                break;
            }
            currPosX = piecePositionX + multiplier*movex;
            currPosY = piecePositionY + multiplier*movey;
            if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosX][currPosY].getColor()!= turn){
                multiplier++;
                VectOfMoves.push_back(Point(currPosX,currPosY));
                if(board[currPosX][currPosY].getName() != "EmptyPlace"){
                    break;
                }
            }
            else{
                break;
            }
        }
    }
    return VectOfMoves;
}

bool Board::movePiece(Point Position1, Point Position2){
    bool winningTheGame = false;
    Piece piece = board[Position1.getX()][Position1.getY()];
    board[Position1.getX()][Position1.getY()] = Empty;
    if (board[Position2.getX()][Position2.getY()].getName()== "King"){
        winningTheGame = true;
    }
    board[Position2.getX()][Position2.getY()] = piece;
    return winningTheGame;
}

void Board::show(){
    for (int idxY = 7; idxY >= 0; idxY-- ){
        for (int idxX = 0; idxX < 8; idxX++ ){
            cout << board[idxY][idxX].getName() << ":" << board[idxY][idxX].getColor()[0] << "    ";
        }
        cout << endl;
    }
}


// lengthwise 
Piece initialBoard[64] = {
    WhiteRook,WhiteKnight,WhiteBishop,WhiteQueen,WhiteKing,WhiteBishop,WhiteKnight,WhiteRook,
    WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,WhitePawn,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    Empty,Empty,Empty,Empty,Empty,Empty,Empty,Empty,
    BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,BlackPawn,
    BlackRook,BlackKnight,BlackBishop,BlackQueen,BlackKing,BlackBishop,BlackKnight,BlackRook
};

Board initial_board(initialBoard,"white");
