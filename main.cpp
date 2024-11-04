#include <iostream> 
using namespace std;
#include "board.h"

int main(){
    Point A1(0,0);
    Point A2(6,6);
    initial_board.movePiece(A1,A2);
    initial_board.show();
    vector<Point> vect = initial_board.getPossibleMoves(A2);
    for(int idx = 0; idx < vect.size(); idx++){
        cout<< vect[idx].getX() << ":" << vect[idx].getY() << endl;
    }
    return 0;
}