#include <iostream> 
using namespace std;
#include "game.h"

int main(){
    openWindow(480,480);
    Game game;
    game.play_against_random();
    endGraphics();
    return 0;
}