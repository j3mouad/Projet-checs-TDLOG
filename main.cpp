
#include <iostream> 
using namespace std;
#include "game.h"
#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#define PORT 8080


int main() {
    WSADATA wsaData;
    SOCKET sock = INVALID_SOCKET;
    struct sockaddr_in server_addr;
    char buffer[1024] = {0};

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed\n";
        return 1;
    }

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        std::cerr << "Socket creation failed: " << WSAGetLastError() << "\n";
        WSACleanup();
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Connect to the Python server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        std::cerr << "Connection failed: " << WSAGetLastError() << "\n";
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    std::cout << "Connected to the server.\n";

    while (true) {
        // Send data to the Python server
        std::string message = "Hello from C++ client!";
        send(sock, message.c_str(), message.size(), 0);
        std::cout << "Message sent: " << message << std::endl;

        // Receive response from the server
        int valread = recv(sock, buffer, 1024, 0);
        if (valread > 0) {
            std::cout << "Received from server: " << buffer << std::endl;
            memset(buffer, 0, sizeof(buffer));
        }

        Sleep(1000);  // Wait for a second before sending the next message
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}