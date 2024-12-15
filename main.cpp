#include <iostream> 
using namespace std;
#include "game.h"

int main(){
    openWindow(480,480);
    Game game;
    game.play_fisher();
    endGraphics();
    return 0;
}