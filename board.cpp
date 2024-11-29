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
const Point KingAndQueenMoveSet[] = {
    Point(1,0), Point(1,1), Point(0,1), Point(-1,1),
    Point(-1,0), Point(-1,-1), Point(0,-1), Point(1,-1)
};

const Point RookMoveSet[] = {
    Point(1,0), Point(0,1), Point(-1,0), Point(0,-1)
};

const Point BishopMoveSet[] = {
    Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)
};

const Point KnightMoveSet[] = {
    Point(2,1), Point(1,2), Point(-1,2), Point(-2,1),
    Point(-2,-1), Point(-1,-2), Point(1,-2), Point(2,-1)
};

const Point WhitePawnMoveSet[] = {
    Point(0,1)
};

const Point WhitePawnAttackMoveSet[] = {
    Point(1,1), Point(-1,1)
};

const Point BlackPawnMoveSet[] = {
    Point(0,-1)
};

const Point BlackPawnAttackMoveSet[] = {
    Point(1,-1), Point(-1,-1)
};
// Create piece instances
Piece WhiteKing("King", "white", false, KingAndQueenMoveSet,8);
Piece WhiteQueen("Queen", "white", true, KingAndQueenMoveSet,8);
Piece WhiteBishop("Bishop", "white", true, BishopMoveSet,4);
Piece WhiteRook("Rook", "white", true, RookMoveSet,4);
Piece WhiteKnight("Knight", "white", false, KnightMoveSet,8);
Piece WhitePawn("Pawn", "white", false, WhitePawnMoveSet, WhitePawnAttackMoveSet,1,2);
Piece Empty("EmptyPlace","none", false, emptyMoveSet,0);
Piece BlackKing("King", "black", false, KingAndQueenMoveSet,8);
Piece BlackQueen("Queen", "black", true, KingAndQueenMoveSet,8);
Piece BlackBishop("Bishop", "black" ,true, BishopMoveSet,4);
Piece BlackRook("Rook", "black", true, RookMoveSet,4);
Piece BlackKnight("Knight", "black", false, KnightMoveSet,8);
Piece BlackPawn("Pawn", "black", false, BlackPawnMoveSet, BlackPawnAttackMoveSet,1,2);


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



const Point emptyMoveSet[] = {};

Board initial_board(initialBoard,"white");