#include "board.h"
vector<pair<int,string>> generateRandomBackRank() { //written by chatgpt
        unsigned seed = chrono::system_clock::now().time_since_epoch().count();
        mt19937 rng(seed);
        vector<pair<int, string>> pieces = {
            make_pair(0, "Rook"), make_pair(1, "Knight"), make_pair(2, "Bishop"),
            make_pair(3, "Queen"), make_pair(4, "King"), make_pair(5, "Bishop"),
            make_pair(6, "Knight"), make_pair(7, "Rook")
        };

        while (true) {
            shuffle(pieces.begin(), pieces.end(), rng);

            int bishop1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string>& p) { return p.second == "Bishop"; }) - pieces.begin();
            int bishop2Pos = find_if(pieces.begin() + bishop1Pos + 1, pieces.end(), [](const pair<int, string>& p) { return p.second == "Bishop"; }) - pieces.begin();

            if ((bishop1Pos % 2 == bishop2Pos % 2)) {
                continue; 
            }


            int kingPos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string>& p) { return p.second == "King"; }) - pieces.begin();
            int rook1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string>& p) { return p.second == "Rook"; }) - pieces.begin();
            int rook2Pos = find_if(pieces.begin() + rook1Pos + 1, pieces.end(), [](const pair<int, string>& p) { return p.second == "Rook"; }) - pieces.begin();

            if (rook1Pos < kingPos && kingPos < rook2Pos) {
                break; // Valid configuration
            }
        }

        return pieces;
}

void Board::transformToFisher(){
    cout << 1 << endl;
    vector<pair<int,string>> backRank = generateRandomBackRank();
    for (pair<int,string> couple : backRank){
        cout << couple.second << " : " << couple.first << endl;
    }
    cout << 2 << endl;
    for (int i = 0; i < 8; ++i) {
        movePiece(Point(i, 0), Point(i, 2)); 
        movePiece(Point(i, 7), Point(i, 5));
    }
    for (int i = 0; i < 8; ++i) {
        movePiece(Point(backRank[i].first, 2), Point(i, 0)); 
        movePiece(Point(backRank[i].first, 5), Point(i, 7));
    }
}

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

bool Board::movePiece(Point Position1, Point Position2, bool changeCastling){
    bool winningTheGame = false;
    Piece piece = getPiece(Position1);
    if (piece.getName()== "King"){
        if (piece.getColor() == "white"){
            if (changeCastling){
                LeftCastleWhite = false;
                RightCastleWhite = false;
            }
            WhiteKingPos = Position2;
        } else {
            if (changeCastling){
                LeftCastleBlack = false;
                RightCastleBlack = false;
            }
            BlackKingPos = Position2;
        }
    }
    if (piece.getName()== "Rook" && changeCastling){
        if(Position1.getX() == 7 && Position1.getY() == 0){
            RightCastleWhite = false;
        }else if(Position1.getX() == 0 && Position1.getY() == 0){
            LeftCastleWhite = false;
        }else if(Position1.getX() == 0 && Position1.getY() == 7){
            LeftCastleBlack = false;
        }else if(Position1.getX() == 7 && Position1.getY() == 7){
            RightCastleBlack = false;
        }
    }
    if (changeCastling){
        if(Position2.getX() == 7 && Position2.getY() == 0){
            RightCastleWhite = false;
        }else if(Position2.getX() == 0 && Position2.getY() == 0){
            LeftCastleWhite = false;
        }else if(Position2.getX() == 0 && Position2.getY() == 7){
            LeftCastleBlack = false;
        }else if(Position2.getX() == 7 && Position2.getY() == 7){
            RightCastleBlack = false;
        }
    }
    setPiece(Position1,Empty);
    if (getPiece(Position2).getName()== "King"){
        winningTheGame = true;
    }
    setPiece(Position2,piece);
    return winningTheGame;
}

void Board::show(){
    for (int idxY = 7; idxY >= 0; idxY-- ){
        for (int idxX = 0; idxX < 8; idxX++ ){
            putGreyImage(60*idxX,480 - (60*(idxY+1)),getPiece(Point(idxX,idxY)).getImage(),60,60);
        }
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