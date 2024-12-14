#include "game.h"

vector<Point> Game::getPossibleMoves(Point position, Point enPassant){
    vector<Point> moves = gameBoard.getPossibleMoves(position);
    int x = position.getX();
    int y = position.getY();
    if(gameBoard.getPiece(position).getName() == "Pawn"){
        if (gameBoard.getPiece(position).getColor() == "white" && gameBoard.getTurn() == "white"){
            if(y == 1){
                if(gameBoard.getPiece(Point(x,y+2)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x,y+1)).getName() == "EmptyPlace"){
                    moves.push_back(Point(x,y+2));
                }
            } else if(((Point(x+1,y+1) == enPassant) || (Point(x-1,y+1) == enPassant))){
                    moves.push_back(enPassant);
                }
        } else if (gameBoard.getPiece(position).getColor() == "black" && gameBoard.getTurn() == "black"){
            if(y==6){
                if(gameBoard.getPiece(Point(x,y-2)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x,y-1)).getName() == "EmptyPlace"){
                    moves.push_back(Point(x,y-2));
                }
            } else if(((Point(x+1,y-1) == enPassant) || (Point(x-1,y-1) == enPassant))){
                moves.push_back(enPassant);
                }
            }
    }
        
        
    
    vector<Point> trueMoves;
    for (int idx = 0; idx < moves.size(); idx++){
        Point destination = moves[idx];
        Piece piece = gameBoard.getPiece(destination);
        gameBoard.movePiece(position,destination);
        if (not isInCheck()){
            trueMoves.push_back(destination);
        }
        gameBoard.movePiece(destination,position);
        gameBoard.setPiece(destination,piece);
    }
    if (gameBoard.getPiece(position).getName() == "King" && !(isInCheck())){
        int x_castle = position.getX();
        int y_castle = position.getY();
        if(gameBoard.getPiece(position).getColor() == "white" && gameBoard.getTurn() == "white"){
            if (gameBoard.getRCW()){
                if(gameBoard.getPiece(Point(x_castle+1,y_castle)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x_castle+2,y_castle)).getName() == "EmptyPlace" ){
                    gameBoard.movePiece(position,Point(x_castle+1,y_castle));
                    if (!(isInCheck())){
                        gameBoard.movePiece(Point(x_castle+1,y_castle),Point(x_castle+2,y_castle));
                        if(!(isInCheck())){
                            trueMoves.push_back(Point(x_castle+2,y_castle));
                        }
                        gameBoard.movePiece(Point(x_castle+2,y_castle),position);
                    } else {
                        gameBoard.movePiece(Point(x_castle+1,y_castle),position);
                    }
                }
            } if (gameBoard.getLCW()){
                if(gameBoard.getPiece(Point(x_castle-1,y_castle)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x_castle-2,y_castle)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x_castle-3,y_castle)).getName() == "EmptyPlace" ){
                    gameBoard.movePiece(position,Point(x_castle-1,y_castle));
                    if (!(isInCheck())){
                        gameBoard.movePiece(Point(x_castle-1,y_castle),Point(x_castle-2,y_castle));
                        if(!(isInCheck())){
                            trueMoves.push_back(Point(x_castle-2,y_castle));
                        }
                        gameBoard.movePiece(Point(x_castle-2,y_castle),position);
                    } else {
                        gameBoard.movePiece(Point(x_castle-1,y_castle),position);
                    }
                }
            }
        } else if (gameBoard.getPiece(position).getColor() == "black" && gameBoard.getTurn() == "black"){
            if(gameBoard.getRCB()){
                if(gameBoard.getPiece(Point(x_castle+1,y_castle)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x_castle+2,y_castle)).getName() == "EmptyPlace" ){
                    gameBoard.movePiece(position,Point(x_castle+1,y_castle));
                    if (!(isInCheck())){
                        gameBoard.movePiece(Point(x_castle+1,y_castle),Point(x_castle+2,y_castle));
                        if(!(isInCheck())){
                            trueMoves.push_back(Point(x_castle+2,y_castle));
                        }
                        gameBoard.movePiece(Point(x_castle+2,y_castle),position);
                    } else {
                        gameBoard.movePiece(Point(x_castle+1,y_castle),position);
                    }
                }
            }if (gameBoard.getLCB()){
                if(gameBoard.getPiece(Point(x_castle-1,y_castle)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x_castle-2,y_castle)).getName() == "EmptyPlace" && gameBoard.getPiece(Point(x_castle-3,y_castle)).getName() == "EmptyPlace" ){
                    gameBoard.movePiece(position,Point(x_castle-1,y_castle));
                    if (not isInCheck()){
                        gameBoard.movePiece(Point(x_castle-1,y_castle),Point(x_castle-2,y_castle));
                        if(not isInCheck()){
                            trueMoves.push_back(Point(x_castle-2,y_castle));
                        }
                        gameBoard.movePiece(Point(x_castle-2,y_castle),position);
                    } else {
                        gameBoard.movePiece(Point(x_castle-1,y_castle),position);
                    }
                }            
            }
        }
    }
    return trueMoves;
}

map<pair<int, int>,vector<Point>> Game::getAllPossibleMoves(Point enPassant){
    map<pair<int, int>,vector<Point>> possibleMoves;
    for(int x=0; x<8; x++){
        for(int y=0; y<8; y++){
            pair<int, int> pair(x,y);
            Point point(x,y);
            vector<Point> moves = getPossibleMoves(point,enPassant);
            if (moves.size() != 0) possibleMoves[pair] = getPossibleMoves(point,enPassant);
        }
    }
    return possibleMoves;
}

map<pair<int, int>,vector<Point>> Game::getAllPossibleWhiteMoves(Point enPassant){
    if(gameBoard.getTurn() == "white"){
        return getAllPossibleMoves(enPassant);
    } else {
        gameBoard.changeTurn();
        map<pair<int, int>,vector<Point>> possibleMoves = getAllPossibleMoves(enPassant);
        gameBoard.changeTurn();
        return possibleMoves;
    }
}

map<pair<int, int>,vector<Point>> Game::getAllPossibleBlackMoves(Point enPassant){
    if(gameBoard.getTurn() == "black"){
        return getAllPossibleMoves(enPassant);
    } else {
        gameBoard.changeTurn();
        map<pair<int, int>,vector<Point>> possibleMoves = getAllPossibleMoves(enPassant);
        gameBoard.changeTurn();
        return possibleMoves;
    }
}

void Game::play(){
    bool game_over = false;
    Point enPassant = Point(-1,-1); // no enPassant can be done
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    int x_chosen_2, y_chosen_2;
    map<pair<int, int>,vector<Point>> MapOfMoves;
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
        vector<Point> vect = MapOfMoves[pair(x_chosen,y_chosen)];
        cout << "the piece is : " << gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() <<" and its color is :" << gameBoard.getPiece(Point(x_chosen,y_chosen)).getColor()<< endl;
        if(vect.size() == 0){
            continue;
        }
        map<pair<int,int>,int> graphicalMoves;
        for (int idx = 0; idx < vect.size(); idx++){
            Point point = vect[idx];
            graphicalMoves[make_pair(point.getX(),point.getY())] = idx;
        }
        for(int idx = 0; idx < vect.size(); idx++){
            cout<< vect[idx].getX() << ":" << vect[idx].getY() << endl;
            fillRect(vect[idx].getX()*60,480-(vect[idx].getY()+1)*60,60,60,Color(120,120,120));
        }
        cout << "choose the piece to move" << endl;
        getMouse(x_chosen_2,y_chosen_2);
        x_chosen_2 = x_chosen_2/60;
        y_chosen_2 = (480-y_chosen_2-1)/60;
        if (graphicalMoves.find(make_pair(x_chosen_2, y_chosen_2)) == graphicalMoves.end()) {
            continue;
        }
        idx_chosen = graphicalMoves[pair(x_chosen_2, y_chosen_2)];
        if(vect[idx_chosen] == enPassant){
            if(gameBoard.getTurn() == "white"){
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()-1),Empty);
            }
            else{
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()+1),Empty);
            }
        }
        enPassant = Point(-1,-1);
        if(gameBoard.getPiece(Point(x_chosen,y_chosen)).getName()=="Pawn" && ((vect[idx_chosen].getY() - y_chosen) == 2 || (vect[idx_chosen].getY() - y_chosen) == -2 )){
            y_enPassant = (vect[idx_chosen].getY() + y_chosen)/2;
            x_enPassant = x_chosen;
            enPassant = Point(x_enPassant,y_enPassant);
        }
        if (gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() == "King"){
            if (vect[idx_chosen].getX() - x_chosen == 2){
                gameBoard.movePiece(Point(7,y_chosen),Point(x_chosen+1,y_chosen),true);
            } else if (vect[idx_chosen].getX() - x_chosen == -2) {
                gameBoard.movePiece(Point(0,y_chosen),Point(x_chosen-1,y_chosen),true);
            }
        }
        if (gameBoard.movePiece(Point(x_chosen,y_chosen),vect[idx_chosen],true)){
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
    }
}

void Game::play_against_random(){
    srand(static_cast<unsigned int>(std::time(nullptr)));
    bool game_over = false;
    Point enPassant = Point(-1,-1); // no enPassant can be done
    int y_enPassant, x_enPassant;
    int x_chosen, y_chosen, idx_chosen, idx_piece_chosen;
    int x_chosen_2, y_chosen_2;
    map<pair<int, int>,vector<Point>> MapOfMoves;
    vector<pair<int,int>> vectorOfChoice;
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
        vector<Point> vect = MapOfMoves[pair(x_chosen,y_chosen)];
        cout << "the piece is : " << gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() <<" and its color is :" << gameBoard.getPiece(Point(x_chosen,y_chosen)).getColor()<< endl;
        if(vect.size() == 0){
            continue;
        }
        map<pair<int,int>,int> graphicalMoves;
        for (int idx = 0; idx < vect.size(); idx++){
            Point point = vect[idx];
            graphicalMoves[make_pair(point.getX(),point.getY())] = idx;
        }
        for(int idx = 0; idx < vect.size(); idx++){
            cout<< vect[idx].getX() << ":" << vect[idx].getY() << endl;
            fillRect(vect[idx].getX()*60,480-(vect[idx].getY()+1)*60,60,60,Color(120,120,120));
        }
        cout << "choose the piece to move" << endl;
        getMouse(x_chosen_2,y_chosen_2);
        x_chosen_2 = x_chosen_2/60;
        y_chosen_2 = (480-y_chosen_2-1)/60;
        if (graphicalMoves.find(make_pair(x_chosen_2, y_chosen_2)) == graphicalMoves.end()) {
            continue;
        }
        idx_chosen = graphicalMoves[pair(x_chosen_2, y_chosen_2)];
        if(vect[idx_chosen] == enPassant){
            if(gameBoard.getTurn() == "white"){
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()-1),Empty);
            }
            else{
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()+1),Empty);
            }
        }
        enPassant = Point(-1,-1);
        if(gameBoard.getPiece(Point(x_chosen,y_chosen)).getName()=="Pawn" && ((vect[idx_chosen].getY() - y_chosen) == 2 || (vect[idx_chosen].getY() - y_chosen) == -2 )){
            y_enPassant = (vect[idx_chosen].getY() + y_chosen)/2;
            x_enPassant = x_chosen;
            enPassant = Point(x_enPassant,y_enPassant);
        }
        if (gameBoard.getPiece(Point(x_chosen,y_chosen)).getName() == "King"){
            if (vect[idx_chosen].getX() - x_chosen == 2){
                gameBoard.movePiece(Point(7,y_chosen),Point(x_chosen+1,y_chosen),true);
            } else if (vect[idx_chosen].getX() - x_chosen == -2) {
                gameBoard.movePiece(Point(0,y_chosen),Point(x_chosen-1,y_chosen),true);
            }
        }
        if (gameBoard.movePiece(Point(x_chosen,y_chosen),vect[idx_chosen],true)){
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
        if(ChosenDestination == enPassant){
            if(gameBoard.getTurn() == "white"){
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()-1),Empty);
            }
            else{
                gameBoard.setPiece(Point(enPassant.getX(),enPassant.getY()+1),Empty);
            }
        }
        enPassant = Point(-1,-1);
        cout << "random point selected" << endl;
        if(gameBoard.getPiece(ChosenStart).getName()=="Pawn" && ((ChosenDestination.getY() - y_chosen) == 2 || (ChosenDestination.getY() - y_chosen) == -2 )){
            y_enPassant = (ChosenDestination.getY() + ChosenStart.getY())/2;
            x_enPassant = ChosenStart.getX();
            enPassant = Point(x_enPassant,y_enPassant);
        }
        if (gameBoard.getPiece(ChosenStart).getName() == "King"){
            if (ChosenDestination.getX() - ChosenStart.getX() == 2){
                gameBoard.movePiece(Point(7,ChosenStart.getY()),Point(ChosenStart.getX()+1,ChosenStart.getY()),true);
            } else if (ChosenDestination.getX() - ChosenStart.getX() == -2) {
                gameBoard.movePiece(Point(0,ChosenStart.getY()),Point(ChosenStart.getX()-1,ChosenStart.getY()),true);
            }
        }
        if (gameBoard.movePiece(ChosenStart,ChosenDestination,true)){
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

bool Game::isInCheck(){
    vector<Point> test;
    int x,y;
    if (gameBoard.getTurn() == "white"){
        Point kingpos = gameBoard.getWhiteKingPos();
        x = kingpos.getX();
        y = kingpos.getY();
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "King"){
                return true; 
            }
        }
        if (gameBoard.getPiece(Point(x+1,y+1)).getName() == "Pawn" && gameBoard.getPiece(Point(x+1,y+1)).getColor() == "black"){
            return true;
        }
        if (gameBoard.getPiece(Point(x-1,y+1)).getName() == "Pawn" && gameBoard.getPiece(Point(x-1,y+1)).getColor() == "black"){
            return true;
        }
        gameBoard.setPiece(kingpos,WhiteBishop);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Bishop"){
                gameBoard.setPiece(kingpos,WhiteKing);
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,WhiteRook);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Rook"){
                gameBoard.setPiece(kingpos,WhiteKing);
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,WhiteKnight);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Knight"){
                gameBoard.setPiece(kingpos,WhiteKing);
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,WhiteKing);
    } else {
        Point kingpos = gameBoard.getBlackKingPos();
        x = kingpos.getX();
        y = kingpos.getY();
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "King"){
                return true; 
            }
        }
        if (gameBoard.getPiece(Point(x+1,y-1)).getName() == "Pawn" && gameBoard.getPiece(Point(x+1,y-1)).getColor() == "white"){
            return true;
        }
        if (gameBoard.getPiece(Point(x-1,y-1)).getName() == "Pawn" && gameBoard.getPiece(Point(x-1,y-1)).getColor() == "white"){
            return true;
        }
        gameBoard.setPiece(kingpos,BlackBishop);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Bishop"){
                gameBoard.setPiece(kingpos,BlackKing);
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,BlackRook);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Queen" ||gameBoard.getPiece(test[idx]).getName() == "Rook"){
                gameBoard.setPiece(kingpos,BlackKing);
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,BlackKnight);
        test = gameBoard.getPossibleAttacks(kingpos);
        for(int idx = 0; idx < test.size(); idx++){
            if(gameBoard.getPiece(test[idx]).getName() == "Knight"){
                gameBoard.setPiece(kingpos,BlackKing);
                return true; 
            }
        }
        gameBoard.setPiece(kingpos,BlackKing);
    }
    return false;
}