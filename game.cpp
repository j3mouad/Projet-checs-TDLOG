#include "game.h"

vector<Point> Game::getPossibleMoves(Point position, Point enPassant){
    vector<Point> moves = gameBoard.getPossibleMoves(position);
    int x = position.getX();
    int y = position.getY();
    if(gameBoard.getPiece(position).getName() == "Pawn"){
        if(gameBoard.getTurn() == "white" && y == 1){
            if(gameBoard.getPiece(Point(x,y+2)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x,y+1)).getName() == "EmptyPlace"){
                moves.push_back(Point(x,y+2));
            }
        }
        if(gameBoard.getTurn() == "black" && y == 6){
            if(gameBoard.getPiece(Point(x,y-2)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x,y-1)).getName() == "EmptyPlace"){
                moves.push_back(Point(x,y-2));
            }
        }
        if((gameBoard.getTurn() == "white") && ((Point(x+1,y+1) == enPassant) || (Point(x-1,y+1) == enPassant))){
            moves.push_back(enPassant);
        }
        if((gameBoard.getTurn() == "black") && ((Point(x+1,y-1) == enPassant) || (Point(x-1,y-1) == enPassant))){
            moves.push_back(enPassant);
        }
    }
    return moves;
}

void Game::play(){
    bool game_over = false;
    Point enPassant = Point(-1,-1); // no enPassant can be done
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    while (!game_over){
        gameBoard.show();
        cout << "choose a piece to find the relevant moves" << endl;
        cin >> x_chosen >> y_chosen ;
        cout << "x : " << x_chosen << " ; y : " << y_chosen << endl; 
        vector<Point> vect = getPossibleMoves(Point(x_chosen,y_chosen), enPassant);
        cout << "the piece is : " << gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() <<" and its color is :" << gameBoard.getPiece(Point(x_chosen,y_chosen)).getColor()<< endl;
        if(vect.size() == 0){
            continue;
        }
        for(int idx = 0; idx < vect.size(); idx++){
            cout<< vect[idx].getX() << ":" << vect[idx].getY() << endl;
        }
        cout << "choose the piece to move" << endl;
        cin >> idx_chosen;
        if (idx_chosen>=vect.size()){
            continue;
        }
        if(vect[idx_chosen] == enPassant){
            if(gameBoard.getTurn() == "white"){
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()-1),Empty);
            }
            else{
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()+1),Empty);
            }
        }
        enPassant = Point(-1,-1);
        if(gameBoard.getPiece(Point(x_chosen,y_chosen)).getName()=="Pawn" && ((vect[idx_chosen].getY() - y_chosen) == 2 || (vect[idx_chosen].getY() - y_chosen) == -2 )){
            y_enPassant = (vect[idx_chosen].getY() + y_chosen)/2;
            x_enPassant = x_chosen;
            enPassant = Point(x_enPassant,y_enPassant);
        }
        if (gameBoard.movePiece(Point(x_chosen,y_chosen),vect[idx_chosen])){
            cout << "game over" << endl;
            game_over = true;
        }
        if ((gameBoard.getPiece(vect[idx_chosen]).getName() == "Pawn") && (vect[idx_chosen].getY()==0 || vect[idx_chosen].getY()==7)){
            cout << "choose a piece to change your pawn into" << endl;
            cout << "0: Queen    1: Rook    2: Bishop    3: Knight" << endl;
            while(true){
                cin >> idx_piece_chosen;
                if (idx_piece_chosen>=0 && idx_piece_chosen<4){
                    break;
                }
                cout << "choose a valid index between 0 and 3" << endl;
            }
            if (gameBoard.getTurn() == "white"){
                switch(idx_piece_chosen){
                    case 0:
                        gameBoard.setPiece(vect[idx_chosen],WhiteQueen);
                        break;
                    case 1:
                        gameBoard.setPiece(vect[idx_chosen],WhiteRook);
                        break;
                    case 2:
                        gameBoard.setPiece(vect[idx_chosen],WhiteBishop);
                        break;
                    case 3:
                        gameBoard.setPiece(vect[idx_chosen],WhiteKnight);
                        break;
                }
            }
            if (gameBoard.getTurn() == "black"){
                switch(idx_piece_chosen){
                    case 0:
                        gameBoard.setPiece(vect[idx_chosen],BlackQueen);
                        break;
                    case 1:
                        gameBoard.setPiece(vect[idx_chosen],BlackRook);
                        break;
                    case 2:
                        gameBoard.setPiece(vect[idx_chosen],BlackBishop);
                        break;
                    case 3:
                        gameBoard.setPiece(vect[idx_chosen],BlackKnight);
                        break;
                }
            }
        }
        cout << "move made" << endl;
        gameBoard.changeTurn();
        cout << gameBoard.getTurn() << endl;
        if (isInCheck()){
            cout << "check" << endl << endl << endl << endl << "check" << endl;
        }
    }
}

bool Game::isInCheck(){
    vector<Point> test;
    int x,y;
    if (gameBoard.getTurn() == "white"){
        Point kingpos = gameBoard.getWhiteKingPos();
        x = kingpos.getX();
        y = kingpos.getY();
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "King"){
                return true; 
            }
        }
        if (gameBoard.getPiece(Point(x+1,y+1)).getName() == "Pawn" && gameBoard.getPiece(Point(x+1,y+1)).getColor() == "black"){
            return true;
        }
        if (gameBoard.getPiece(Point(x-1,y+1)).getName() == "Pawn" && gameBoard.getPiece(Point(x+1,y+1)).getColor() == "black"){
            return true;
        }
        gameBoard.setPiece(kingpos,WhiteBishop);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Bishop"){
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,WhiteRook);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Rook"){
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,WhiteKnight);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Knight"){
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,WhiteKing);
    } else {
        Point kingpos = gameBoard.getBlackKingPos();
        x = kingpos.getX();
        y = kingpos.getY();
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "King"){
                return true; 
            }
        }
        if (gameBoard.getPiece(Point(x+1,y-1)).getName() == "Pawn" && gameBoard.getPiece(Point(x+1,y-1)).getColor() == "white"){
            return true;
        }
        if (gameBoard.getPiece(Point(x-1,y-1)).getName() == "Pawn" && gameBoard.getPiece(Point(x+1,y-1)).getColor() == "white"){
            return true;
        }
        gameBoard.setPiece(kingpos,BlackBishop);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Bishop"){
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,BlackRook);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Rook"){
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,BlackKnight);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Knight"){
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,BlackKing);
    }
    return false;
}