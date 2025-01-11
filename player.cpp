#include "player.h"

void choosePieceHuman(int &x1, int &y1){

}
void chooseMoveHuman(int &x2, int &y2){

}
void choosePawnHuman(Board &gameBoard,Point point){
    int idx_piece_chosen;
    if ((gameBoard.getPiece(point).getName() == "Pawn") && (point.getY()==0 || point.getY()==7)){
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
                        gameBoard.setPiece(point,WhiteQueen);
                        break;
                    case 1:
                        gameBoard.setPiece(point,WhiteRook);
                        break;
                    case 2:
                        gameBoard.setPiece(point,WhiteBishop);
                        break;
                    case 3:
                        gameBoard.setPiece(point,WhiteKnight);
                        break;
                }
            }
            if (gameBoard.getTurn() == "black"){
                switch(idx_piece_chosen){
                    case 0:
                        gameBoard.setPiece(point,BlackQueen);
                        break;
                    case 1:
                        gameBoard.setPiece(point,BlackRook);
                        break;
                    case 2:
                        gameBoard.setPiece(point,BlackBishop);
                        break;
                    case 3:
                        gameBoard.setPiece(point,BlackKnight);
                        break;
                }
            }
        }
}

