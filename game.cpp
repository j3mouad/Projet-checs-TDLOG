#include "game.h"

/**
 * @brief Main game loop for two human players.
 *
 * This function initializes the game board and enters a loop that:
 * - Updates and displays the board.
 * - Waits for mouse input to select a piece and a destination.
 * - Validates and makes the move.
 * - Checks for game over conditions (e.g., checkmate or stalemate).
 * - Stores each board state in an array for possible undo/analysis.
 *
 * The game loop continues until the game is over.
 */
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
        cout << "size of the hashmap is : " << Hashmap.size() << endl;
        clearWindow();
        fillRect(0,480,480,100,RED);
        
        // Update board state if not already calculated.
        if (!gameBoard.isBoardCalculated()){
            gameBoard.updateBoard();
        }
        
        MapOfMoves = gameBoard.getMoves();
        gameBoard.show();
        
        // Check if the game is over.
        if(gameBoard.gameOver() != "NONE"){
            gameBoard.changeTurn();
            cout << gameBoard.gameOver() << endl;
            break;
        }
        
        // Get the player's selected piece.
        getMouse(x_chosen,y_chosen);
        if(y_chosen >= 480){
            undo();
            continue;
        }
        x_chosen = x_chosen / 60;
        y_chosen = (480 - y_chosen - 1) / 60;
        vector<Point> vect = MapOfMoves[Point(x_chosen,y_chosen)];
        cout << "the piece is : " 
             << gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() 
             << " and its color is : " 
             << gameBoard.getPiece(Point(x_chosen,y_chosen)).getColor() 
             << endl;
        
        // If there are no legal moves for the selected piece, continue.
        if(vect.size() == 0){
            continue;
        }
        
        // Map the move destinations for graphical selection.
        map<Point,int> graphicalMoves;
        for (int idx = 0; idx < vect.size(); idx++){
            Point point = vect[idx];
            graphicalMoves[point] = idx;
        }
        // Highlight possible moves.
        for (int idx = 0; idx < vect.size(); idx++){
            fillRect(vect[idx].getX()*60, 480 - (vect[idx].getY()+1)*60, 60, 60, Color(120,120,120));
        }
        
        // Get the destination from the player's mouse click.
        getMouse(x_chosen_2, y_chosen_2);
        x_chosen_2 = x_chosen_2 / 60;
        y_chosen_2 = (480 - y_chosen_2 - 1) / 60;
        if (graphicalMoves.find(Point(x_chosen_2, y_chosen_2)) == graphicalMoves.end()) {
            continue;
        }
        idx_chosen = graphicalMoves[Point(x_chosen_2, y_chosen_2)];
        
        // Attempt to move the piece. If movePieceoff returns true, the game is over.
        if (gameBoard.movePieceoff(Point(x_chosen,y_chosen), vect[idx_chosen])){
            cout << "game over" << endl;
            game_over = true;
        }
        cout << "move made" << endl;
        moveNumber++;
        gameBoards[moveNumber] = gameBoard;
        cout << gameBoard.getTurn() << endl;
    }
}

/**
 * @brief Main game loop for playing against an AI opponent.
 *
 * This function is similar to @ref play but incorporates an AI opponent.
 * In addition to processing the human player's move, after each turn the function:
 * - Checks for game over conditions.
 * - Computes the best move for the AI using minimax (via @ref getMinimaxMove).
 * - Makes the AI move and updates the board state.
 *
 * The loop continues until the game is over.
 */
void Game::play_against_ai(){
    gameBoards = new Board[10000];
    gameBoard.setGameMap(&Hashmap);
    gameBoards[0] = gameBoard;
    bool game_over = false;
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    int x_chosen_2, y_chosen_2;
    map<Point,vector<Point>> MapOfMoves;
    
    while (!game_over){
        cout << gameBoard.isBoardCalculated() << endl;
        cout << "size of hashmap is : " << Hashmap.size() << endl;
        clearWindow();
        fillRect(0,480,480,100,RED);
        
        // Update board state if necessary.
        if (!gameBoard.isBoardCalculated()){
            gameBoard.updateBoard();
        }
        MapOfMoves = gameBoard.getMoves();
        gameBoard.show();
        cout << "choose a piece to find the relevant moves" << endl;
        
        // Check if the game is over.
        if(gameBoard.gameOver() != "NONE"){
            cout << gameBoard.gameOver() << endl;
            break;
        }
        
        // Get the human player's selected piece.
        getMouse(x_chosen, y_chosen);
        if(y_chosen >= 480){
            undo();
            undo();
            continue;
        }
        x_chosen = x_chosen / 60;
        y_chosen = (480 - y_chosen - 1) / 60;
        cout << "x : " << x_chosen << " ; y : " << y_chosen << endl; 
        vector<Point> vect = MapOfMoves[Point(x_chosen, y_chosen)];
        cout << "the piece is : " 
             << gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() 
             << " and its color is : " 
             << gameBoard.getPiece(Point(x_chosen,y_chosen)).getColor() 
             << endl;
        
        if(vect.size() == 0){
            continue;
        }
        
        // Map the graphical moves for selection.
        map<Point,int> graphicalMoves;
        for (int idx = 0; idx < vect.size(); idx++){
            Point point = vect[idx];
            graphicalMoves[point] = idx;
        }
        // Highlight possible move destinations.
        for (int idx = 0; idx < vect.size(); idx++){
            fillRect(vect[idx].getX()*60, 480 - (vect[idx].getY()+1)*60, 60, 60, Color(120,120,120));
        }
        
        // Get the destination move from the player's mouse input.
        getMouse(x_chosen_2, y_chosen_2);
        x_chosen_2 = x_chosen_2 / 60;
        y_chosen_2 = (480 - y_chosen_2 - 1) / 60;
        if (graphicalMoves.find(Point(x_chosen_2, y_chosen_2)) == graphicalMoves.end()) {
            continue;
        }
        idx_chosen = graphicalMoves[Point(x_chosen_2, y_chosen_2)];
        
        // Make the human player's move.
        if (gameBoard.movePieceoff(Point(x_chosen, y_chosen), vect[idx_chosen])){
            cout << "game over" << endl;
            game_over = true;
        }
        cout << "move made" << endl;
        cout << gameBoard.isBoardCalculated() << endl;
        moveNumber++;
        gameBoards[moveNumber] = gameBoard;
        cout << gameBoard.getTurn() << endl;
        
        // Check again if the game is over.
        if(gameBoard.gameOver() != "NONE"){
            cout << gameBoard.gameOver() << endl;
            break;
        }
        
        // Compute and make the AI move using minimax.
        pair<Point,Point> bestMove = getMinimaxMove(2);
        gameBoard.movePieceoff(bestMove.first, bestMove.second, false);
        moveNumber++;
        gameBoards[moveNumber] = gameBoard;
    }
}



