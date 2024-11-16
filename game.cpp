#include "game.h"

void Game::play(){
    bool game_over = false;
    int x,y,z;
    while (game_over == false){
        gameBoard.show();
        cout << "choose a piece to find the relevant moves" << endl;
        cin >> x >> y ;
        cout << "x : " << x << " ; y : " << y << endl; 
        vector<Point> vect = gameBoard.getPossibleMoves(Point(x,y));
        cout << "the piece is : " << gameBoard.getPiece(x,y).getName() <<" and its color is :" << gameBoard.getPiece(x,y).getColor()<< endl;
        if(vect.size() == 0){
            continue;
        }
        for(int idx = 0; idx < vect.size(); idx++){
            cout<< vect[idx].getX() << ":" << vect[idx].getY() << endl;
        }
        cout << "choose the piece to move" << endl;
        cin >> z;
        if (z>=vect.size()){
            continue;
        }
        if (gameBoard.movePiece(Point(x,y),vect[z])){
            cout << "game over" << endl;
            game_over = true;
        }
        cout << "move made" << endl;
        gameBoard.changeTurn();
        cout << gameBoard.getTurn() << endl;
    }
}