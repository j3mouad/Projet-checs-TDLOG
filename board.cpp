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

Piece Board::getPiece(Point point){
    return board[point.getY()][point.getX()];
}

void Board::setPiece(Point point, Piece piece){
    board[point.getY()][point.getX()] = piece;
}

vector<Point> Board::getPossibleMoves(Point position){
    int movex,movey;
    int piecePositionX,piecePositionY;
    int currPosX,currPosY;
    int multiplier;
    vector<Point> VectOfMoves;
    piecePositionX = position.getX();
    piecePositionY = position.getY();
    Piece piece = board[piecePositionY][piecePositionX];
    if(piece.getColor() != turn){
        return VectOfMoves;
    }
    const Point* elemMoves = piece.getElemMoveSet();
    if(piece.isMoveSetAttackMoveSet()){
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
                if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosY][currPosX].getColor()!= turn){
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX,currPosY));
                    if(board[currPosY][currPosX].getName() != "EmptyPlace"){
                        break;
                    }
                }
                else{
                    break;
                }
            }
        }
    }
    else{
        const Point* attackMoves = piece.getAttackMoveSet();
        for(int idx=0; idx<piece.numberOfElemMoves(); idx++){
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while(true){
                if (multiplier == 2 && piece.hasInfiniteMoves() == false){
                    break;
                }
                currPosX = piecePositionX + multiplier*movex;
                currPosY = piecePositionY + multiplier*movey;
                if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosY][currPosX].getName()== "EmptyPlace"){
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX,currPosY));
                }
                else{
                    break;
                }
            }
        }
        for(int idx=0; idx<piece.numberOfAttackMoves(); idx++){
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
                currPosY = piecePositionY + movey;
            if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosY][currPosX].getColor() != turn && board[currPosY][currPosX].getColor() != "none"){
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX,currPosY));
                }
            
        }

    }
    return VectOfMoves;
}

vector<Point> Board::getPossibleAttacks(Point position){
    int movex,movey;
    int piecePositionX,piecePositionY;
    int currPosX,currPosY;
    int multiplier;
    vector<Point> VectOfMoves;
    piecePositionX = position.getX();
    piecePositionY = position.getY();
    Piece piece = board[piecePositionY][piecePositionX];
    if(piece.getColor() != turn){
        return VectOfMoves;
    }
    const Point* elemMoves = piece.getElemMoveSet();
    if(piece.isMoveSetAttackMoveSet()){
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
                if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosY][currPosX].getColor()!= turn){
                    multiplier++;
                    if(board[currPosY][currPosX].getName() != "EmptyPlace"){
                        VectOfMoves.push_back(Point(currPosX,currPosY));
                        break;
                    }
                }
                else{
                    break;
                }
            }
        }
    }
    else{
        const Point* attackMoves = piece.getAttackMoveSet();
        for(int idx=0; idx<piece.numberOfAttackMoves(); idx++){
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
                currPosY = piecePositionY + movey;
            if (currPosX>=0 && currPosX<8 && currPosY>=0 && currPosY<8 && board[currPosY][currPosX].getColor() != turn && board[currPosY][currPosX].getColor() != "none"){
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX,currPosY));
                }
            
        }

    }
    return VectOfMoves;
}

bool Board::movePiece(Point Position1, Point Position2){
    bool winningTheGame = false;
    Piece piece = getPiece(Position1);
    setPiece(Position1,Empty);
    if (getPiece(Position1).getName()== "King"){
        if (getPiece(Position1).getColor() == "white"){
            WhiteKingPos = Position2;
        } else {
            BlackKingPos = Position2;
        }
    }
    if (getPiece(Position2).getName()== "King"){
        winningTheGame = true;
    }
    setPiece(Position2,piece);
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