#include "game.h"
#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#define PORT 8080
#include <iostream>
using namespace std;


void Game::play(){
    gameBoards = new Board[10000];
    cout << 1 << endl;
    gameBoard.setGameMap(&Hashmap);
    gameBoards[0] = gameBoard;
    cout << 2 << endl;
    bool game_over = false;
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    int x_chosen_2, y_chosen_2;
    map<Point,vector<Point>> MapOfMoves;
    while (!game_over){
        cout << "size of the hashmap is : "<< Hashmap.size() << endl;
        Imagine::clearWindow();
        Imagine::fillRect(0,480,480,100,Imagine::RED);
        if (!gameBoard.isBoardCalculated()){
            gameBoard.updateBoard();
        }
        MapOfMoves = gameBoard.getMoves();
        gameBoard.show();
        
        if(gameBoard.gameOver() != "NONE"){
            gameBoard.changeTurn();
            cout << gameBoard.gameOver() << endl;
            break;
        };
        //if (test == 0) break;
        Imagine::getMouse(x_chosen,y_chosen);
        if(y_chosen >= 480){
            undo();
            continue;
        }
        x_chosen = x_chosen/60;
        y_chosen = (480-y_chosen-1)/60;
        vector<Point> vect = MapOfMoves[Point(x_chosen,y_chosen)];
        cout << "the piece is : " << (gameBoard.getPiece(Point(x_chosen,y_chosen)))->getName() <<" and its color is :" << (gameBoard.getPiece(Point(x_chosen,y_chosen)))->getColor()<< endl;
        if(vect.size() == 0){
            continue;
        }
        map<Point,int> graphicalMoves;
        for (int idx = 0; idx < vect.size(); idx++){
            Point point = vect[idx];
            graphicalMoves[point] = idx;
        }
        for(int idx = 0; idx < vect.size(); idx++){
            Imagine::fillRect(vect[idx].getX()*60,480-(vect[idx].getY()+1)*60,60,60,Imagine::Color(120,120,120));
        }
        Imagine::getMouse(x_chosen_2,y_chosen_2);
        x_chosen_2 = x_chosen_2/60;
        y_chosen_2 = (480-y_chosen_2-1)/60;
        if (graphicalMoves.find(Point(x_chosen_2, y_chosen_2)) == graphicalMoves.end()) {
            continue;
        }
        idx_chosen = graphicalMoves[Point(x_chosen_2, y_chosen_2)];
        if (gameBoard.movePieceoff(Point(x_chosen,y_chosen),vect[idx_chosen])){
            cout << "game over" << endl;
            game_over = true;
        }
        cout << "move made" << endl;
        moveNumber++;
        gameBoards[moveNumber] = gameBoard;
        cout << gameBoard.getTurn() << endl;
    }
}
/*
void Game::play_against_random(){
    srand(static_cast<unsigned int>(std::time(nullptr)));
    bool game_over = false;
    Point enPassant = Point(-1,-1); // no enPassant can be done
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    int x_chosen_2, y_chosen_2;
    map<Point,vector<Point>> MapOfMoves;
    vector<Point> vectorOfChoice;
    vector<Point> chosenVector;
    int sizeOfMap;
    int sizeOfVector;
    Point ChosenStart, ChosenDestination;
    while (!game_over){
        clearWindow();
        MapOfMoves = getAllPossibleMoves(enPassant);
        gameBoard.show();
        cout << "choose a piece to find the relevant moves" << endl;
        //int test;
        //cin >> test;
        if(MapOfMoves.size()==0){
            if (isInCheck()){
                gameBoard.changeTurn();
                cout << "the winner is" << gameBoard.getTurn() << endl;
                break;
            };
            cout << "Stalemate" << endl;
            break;
        };
        //if (test == 0) break;
        getMouse(x_chosen,y_chosen);
        x_chosen = x_chosen/60;
        y_chosen = (480-y_chosen-1)/60;
        cout << "x : " << x_chosen << " ; y : " << y_chosen << endl; 
        vector<Point> vect = MapOfMoves[Point(x_chosen,y_chosen)];
        cout << "the piece is : " << gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() <<" and its color is :" << gameBoard.getPiece(Point(x_chosen,y_chosen)).getColor()<< endl;
        if(vect.size() == 0){
            continue;
        }
        map<Point,int> graphicalMoves;
        for (int idx = 0; idx < vect.size(); idx++){
            Point point = vect[idx];
            graphicalMoves[point] = idx;
        }
        for(int idx = 0; idx < vect.size(); idx++){
            cout<< vect[idx].getX() << ":" << vect[idx].getY() << endl;
            fillRect(vect[idx].getX()*60,480-(vect[idx].getY()+1)*60,60,60,Color(120,120,120));
        }
        cout << "choose the piece to move" << endl;
        getMouse(x_chosen_2,y_chosen_2);
        x_chosen_2 = x_chosen_2/60;
        y_chosen_2 = (480-y_chosen_2-1)/60;
        if (graphicalMoves.find(Point(x_chosen_2, y_chosen_2)) == graphicalMoves.end()) {
            continue;
        }
        idx_chosen = graphicalMoves[Point(x_chosen_2, y_chosen_2)];
        if (gameBoard.movePieceoff(Point(x_chosen,y_chosen),vect[idx_chosen])){
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
        MapOfMoves = getAllPossibleMoves(enPassant);
        if(MapOfMoves.size()==0){
            if (isInCheck()){
                gameBoard.changeTurn();
                cout << "the winner is" << gameBoard.getTurn() << endl;
                break;
            };
            cout << "Stalemate" << endl;
            break;
        };
        vectorOfChoice.clear();
        for (const auto element : MapOfMoves){
            vectorOfChoice.push_back(element.first);
        }
        sizeOfMap = MapOfMoves.size();
        if (sizeOfMap == 1){
            chosenVector = MapOfMoves[vectorOfChoice[0]];
            ChosenStart = Point(vectorOfChoice[0]);
        } else {
            ChosenStart = Point(vectorOfChoice[rand()%(sizeOfMap)]);
            chosenVector = MapOfMoves[make_pair(ChosenStart.getX(),ChosenStart.getY())];
        }
        sizeOfVector = chosenVector.size();       
        cout << ChosenStart.getX() << ":" << ChosenStart.getY() << endl;
        if (sizeOfVector == 1){
            ChosenDestination = chosenVector[0];
        } else {
            ChosenDestination = chosenVector[rand()%(sizeOfVector)];
        }            
        cout << ChosenDestination.getX() << ":" << ChosenDestination.getY() << endl;
        if (gameBoard.movePieceoff(ChosenStart,ChosenDestination)){
            cout << "game over" << endl;
            game_over = true;
        }
        cout << "move made" << endl;
        if ((gameBoard.getPiece(ChosenDestination).getName() == "Pawn") && (ChosenDestination.getY()==0 || ChosenDestination.getY()==7)){
            idx_piece_chosen = rand()%4;
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

void Game::play_fisher(bool onevone){
    gameBoard.transformToFisher();
    if(onevone){
        play();
    } else {
        play_against_random();
    }
}
*/

void Game::play_against_ai(){
    WSADATA wsaData;
    SOCKET sock = INVALID_SOCKET;
    struct sockaddr_in server_addr;
    char buffer[1024] = {0};

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed\n";
    }

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        std::cerr << "Socket creation failed: " << WSAGetLastError() << "\n";
        WSACleanup();
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // Connect to the Python server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        std::cerr << "Connection failed: " << WSAGetLastError() << "\n";
        closesocket(sock);
        WSACleanup();
    }

    gameBoards = new Board[10000];
    gameBoard.setGameMap(&Hashmap);
    gameBoards[0] = gameBoard;
    bool game_over = false;
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    int x_chosen_2, y_chosen_2;
    map<Point,vector<Point>> MapOfMoves;
    string message = "Hello from C++ client!";
    send(sock, message.c_str(), message.size(), 0);
    cout << "Message sent: " << message << std::endl;

    // Receive response from the server
    int valread = recv(sock, buffer, 1024, 0);
    if (valread > 0) {
        cout << "Received from server: " << buffer << std::endl;
        memset(buffer, 0, sizeof(buffer));
    }
    while (!game_over){
        int valread = recv(sock, buffer, 1024, 0);
        while(valread <= 0){
            valread = recv(sock,buffer,1024,0);
            Imagine::milliSleep(200);
        }
        memset(buffer, 0, sizeof(buffer));

        Point iniMove = Point(stoi(string(1,buffer[1])),stoi(string(1,buffer[3])));
        Point finMove = Point(stoi(string(1,buffer[7])),stoi(string(1,buffer[9])));

        if (!gameBoard.isBoardCalculated()){
            gameBoard.updateBoard();
        }
        MapOfMoves = gameBoard.getMoves();
        if(gameBoard.gameOver() != "NONE"){
            cout << gameBoard.gameOver() << endl;
            break;
        };
        gameBoard.movePieceoff(iniMove,finMove);
        moveNumber++;
        gameBoards[moveNumber] = gameBoard;
        if(gameBoard.gameOver() != "NONE"){
            cout << gameBoard.gameOver() << endl;
            break;
        };
        pair<Point,Point> bestMove = getMinimaxMove(2);
        gameBoard.movePieceoff(bestMove.first,bestMove.second,false);
        moveNumber++;
        gameBoards[moveNumber] = gameBoard;
        string message = "("+to_string(bestMove.first.getX())+","+to_string(bestMove.first.getY())+"),("+to_string(bestMove.second.getX()) +","+to_string(bestMove.second.getY())+")";
        send(sock, message.c_str(), message.size(), 0);
        
    }
}

int Game::minimax(int depth, int alpha, int beta) {
    if (!gameBoard.isBoardCalculated()) {
        gameBoard.updateBoard();
    }
    // Terminal condition: reached maximum search depth.
    if (depth == 0) {
        return gameBoard.evaluateGame();
    }
    // Check for game over.
    if (gameBoard.gameOver() != "NONE") {
        if (gameBoard.gameOver() == "white won") {
            return INT_MAX;
        } else if (gameBoard.gameOver() == "black won") {
            return -INT_MAX;
        } else {
            return 0;
        }
    }
    // (Optional) Look up cached minimax results if you have implemented that.
    if (gameBoard.isMinimaxDepthStored(depth)) {
        return gameBoard.getMinimaxDepth(depth);
    }

    // Get all legal moves.
    auto moves = gameBoard.getMoves();

    // Save the current turn.
    string currentTurn = gameBoard.getTurn();
    
    if (currentTurn == "white") {
        int maxEval = -INT_MAX;
        for (const auto& movePair : moves) {
            for (const auto& dest : movePair.second) {
                // Make the move.
                gameBoard.movePieceoff(movePair.first, dest, false);
                moveNumber++;
                gameBoards[moveNumber] = gameBoard;
                // Recursively evaluate.
                int eval = minimax(depth - 1, alpha, beta);
                Hashmap[gameBoard.hashBoard()].setMinimaxDepth(depth-1,eval);
                // Undo the move.
                undo();
                maxEval = max(maxEval, eval);
                alpha = max(alpha, eval);
                if (beta <= alpha) {
                    break; // Beta cutoff.
                }
            }
            if (beta <= alpha) {
                break; // Beta cutoff.
            }
        }
        // (Optional) Cache the computed minimax score here.
        gameBoard.setMinimaxScore(maxEval);
        gameBoards[moveNumber].setMinimaxScore(maxEval);
        return maxEval;
    } else { // currentTurn == "black"
        int minEval = INT_MAX;
        for (const auto& movePair : moves) {
            for (const auto& dest : movePair.second) {
                gameBoard.movePieceoff(movePair.first, dest, false);
                moveNumber++;
                gameBoards[moveNumber] = gameBoard;
                int eval = minimax(depth - 1, alpha, beta);
                undo();
                minEval = min(minEval, eval);
                beta = min(beta, eval);
                if (beta <= alpha) {
                    break; // Alpha cutoff.
                }
            }
            if (beta <= alpha) {
                break; // Alpha cutoff.
            }
        }
        gameBoard.setMinimaxScore(minEval);
        gameBoards[moveNumber].setMinimaxScore(minEval);
        return minEval;
    }
}

pair<Point, Point> Game::getMinimaxMove(int depth) {
    if (!gameBoard.isBoardCalculated()) {
        gameBoard.updateBoard();
    }
    // Retrieve all legal moves.
    auto moves = gameBoard.getMoves();
    if (moves.empty()) {
        // No legal moves—return an invalid move.
        return make_pair(Point(-1, -1), Point(-1, -1));
    }
    // Save the AI's color (the player whose turn it is before making any move).
    string aiColor = gameBoard.getTurn();
    
    pair<Point, Point> bestMove;
    int bestScore = 0;
    bool firstMove = true;
    
    // Loop through every legal move.
    for (const auto& movePair : moves) {
        for (const auto& dest : movePair.second) {
            pair<Point, Point> move = make_pair(movePair.first, dest);
            // Make the move (without changing castling, etc.).
            gameBoard.movePieceoff(move.first, move.second, false);
            moveNumber++;
            gameBoards[moveNumber] = gameBoard;
            // Use alpha-beta with the full window.
            int score = minimax(depth - 1, -INT_MAX, INT_MAX);
            // Undo the move to restore the board.
            undo();
            // For the very first move, initialize bestScore.
            if (firstMove) {
                bestScore = score;
                bestMove = move;
                firstMove = false;
            } else {
                // For white, we want to maximize; for black, minimize.
                if (aiColor == "white" && score > bestScore) {
                    bestScore = score;
                    bestMove = move;
                } else if (aiColor == "black" && score < bestScore) {
                    bestScore = score;
                    bestMove = move;
                }
            }
        }
    }
    return bestMove;
}

/*





def hash_game(game):
    """
    Hash the current game state. This should return a unique identifier
    for the current board position and turn.
    """
    # For simplicity, you can hash the chessboard and current player
    board_state = ''.join([str(piece) for row in game.chess_board for piece in row])
    turn = game.turn  # Assuming 'white' or 'black' for the turn
    return hash(board_state + turn)
def minimax(game, depth, transposition_table, alpha=float('-inf'), beta=float('inf')):

    # Get the hash of the current game state
    game_hash = hash_game(game)

    # Check if the current game state has already been evaluated
    if game_hash in transposition_table:
        return transposition_table[game_hash]

    if not game.running:
        if game.winner == 'Stalemate':
            return 0
        return 1e9 if game.winner == 'white' else -1e9

    if depth == 0:
        eval_score = evaluate(game,transposition_table)
        transposition_table[game_hash] = eval_score  # Store evaluation result
        return eval_score

    if game.turn == 'white':  # Maximizing for white
        max_eval = float('-inf')
        for start_pos, possible_moves in game.white_moves.items():
            for end_pos in possible_moves:
                copy_game = game.copy_game()
                x, y = end_pos
                copy_game.move_piece(start_pos, x, y)
                copy_game.change_player()
                copy_game.all_moves()
                eval_score = minimax(copy_game, depth - 1, transposition_table, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune outer loop
            if beta <= alpha:
                break  # Prune outer loop
        # Store the evaluation result in the transposition table
        transposition_table[game_hash] = max_eval
        return max_eval

    else:  # Minimizing for black
        min_eval = float('inf')
        for start_pos, possible_moves in game.black_moves.items():
            for end_pos in possible_moves:
                copy_game = game.copy_game()
                x, y = end_pos
                copy_game.move_piece(start_pos, x, y)
                copy_game.change_player()
                copy_game.all_moves()
                eval_score = minimax(copy_game, depth - 1, transposition_table, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune outer loop
            if beta <= alpha:
                break  # Prune outer loop
        # Store the evaluation result in the transposition table
        transposition_table[game_hash] = min_eval
        return min_eval

transposition_table = {}
def AI(game, depth=2):
    """
    AI for determining the best move using minimax evaluation.
    Returns the best move as a tuple (start_pos, end_pos).
    depth must be pair so that it works
    """
    moves_scores = []
    moves = game.white_moves if game.turn == 'white' else game.black_moves
    total_time = 0
    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            start_time = time.time()  # Record the start time
            # Create a copy of the game to simulate the move
            copy_game = game.copy_game()
            copy_game.all_moves()
            x, y = end_pos
            copy_game.move_piece(start_pos, x, y)
            copy_game.change_player()
            score = minimax(copy_game, depth - 1,transposition_table)
            moves_scores.append((score, (start_pos, end_pos)))
          #  print(f"Move: {start_pos} -> {end_pos}, Score: {score}")
            end_time = time.time()
           # print(end_time-start_time)
            total_time += end_time - start_time
    # Sort moves by score (higher is better for white, lower for black)
    moves_scores.sort(reverse=(game.turn == 'white'), key=lambda x: x[0])

    # Return the move with the best score
    if moves_scores:
       # print(f"Best move: {moves_scores[0][1]} with score {moves_scores[0][0]}")
       # print(total_time)
        return moves_scores[0][1]
    #print("No valid moves found")
    return None
*/