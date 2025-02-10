
#include <iostream> 
using namespace std;
#include "game.h"
#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#define PORT 8080


int main() {
    Imagine::openWindow(480,480);
    Game game;
    game.play();
    return 0;
}

