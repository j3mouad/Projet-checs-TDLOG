#include <iostream> 
using namespace std;
#include "game.h"

int main(){
    openWindow(480,580);
    Game game;
    game.play_against_ai();
    endGraphics();
    return 0;
}