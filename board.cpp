#include "board.h"
vector<pair<int, string>> generateRandomBackRank()
{ // written by chatgpt
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    mt19937 rng(seed);
    vector<pair<int, string>> pieces = {
        make_pair(0, "Rook"), make_pair(1, "Knight"), make_pair(2, "Bishop"),
        make_pair(3, "Queen"), make_pair(4, "King"), make_pair(5, "Bishop"),
        make_pair(6, "Knight"), make_pair(7, "Rook")};

    while (true)
    {
        shuffle(pieces.begin(), pieces.end(), rng);

        int bishop1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string> &p)
                                 { return p.second == "Bishop"; }) -
                         pieces.begin();
        int bishop2Pos = find_if(pieces.begin() + bishop1Pos + 1, pieces.end(), [](const pair<int, string> &p)
                                 { return p.second == "Bishop"; }) -
                         pieces.begin();

        if ((bishop1Pos % 2 == bishop2Pos % 2))
        {
            continue;
        }

        int kingPos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string> &p)
                              { return p.second == "King"; }) -
                      pieces.begin();
        int rook1Pos = find_if(pieces.begin(), pieces.end(), [](const pair<int, string> &p)
                               { return p.second == "Rook"; }) -
                       pieces.begin();
        int rook2Pos = find_if(pieces.begin() + rook1Pos + 1, pieces.end(), [](const pair<int, string> &p)
                               { return p.second == "Rook"; }) -
                       pieces.begin();

        if (rook1Pos < kingPos && kingPos < rook2Pos)
        {
            break; // Valid configuration
        }
    }

    return pieces;
}

void Board::transformToFisher()
{
    cout << 1 << endl;
    vector<pair<int, string>> backRank = generateRandomBackRank();

    for (pair<int, string> couple : backRank)
    {
        cout << couple.second << " : " << couple.first << endl;
    }
    cout << 2 << endl;

    for (int i = 0; i < 8; ++i)
    {
        movePiece(Point(i, 0), Point(i, 2));
        movePiece(Point(i, 7), Point(i, 5));
    }

    for (int i = 0; i < 8; ++i)
    {
        movePiece(Point(backRank[i].first, 2), Point(i, 0));
        movePiece(Point(backRank[i].first, 5), Point(i, 7));
    }
}

int Board::evaluatePiece(int x, int y)
{
    Piece piece = getPiece(Point(x, y));
    if (piece.getName() == "EmptyPlace")
    {
        return 0;
    }
    int factor = -1 + 2*(piece.getColor() == "white");
    int value = scores[piece.getName()];
    //value += piece.getScore(x, (8 - 2 * y) * (piece.getColor() == "white") + y);
    value *= factor;
    return value;
}

int Board::evaluateBoard()
{
    int value = 0;

    for (int x = 0; x < 8; x++)
    {
        for (int y = 0; y < 8; y++)
        {
            value += evaluatePiece(x, y);
        }
    }

    return value;
}

Board::Board(Piece *initial__board, string Turn)
{
    turn = Turn;

    for (int idxY = 0; idxY < 8; idxY++)
    {
        for (int idxX = 0; idxX < 8; idxX++)
        {
            board[idxY][idxX] = initial__board[idxX + 8 * idxY];
        }
    }
}

Board::Board(const Board &other)
{

    turn = other.turn;
    WhiteKingPos = other.WhiteKingPos;
    BlackKingPos = other.BlackKingPos;
    LeftCastleBlack = other.LeftCastleBlack;
    RightCastleBlack = other.RightCastleBlack;
    LeftCastleWhite = other.LeftCastleWhite;
    RightCastleWhite = other.RightCastleWhite;
    enPassant = other.enPassant;
    Hashmap = other.Hashmap;
    isMinimaxCalculated = other.isMinimaxCalculated;
    Minimaxscore = other.Minimaxscore;
    depthMap = other.depthMap;

    for (int idx1 = 0; idx1 < 8; idx1++)
    {
        for (int idx2 = 0; idx2 < 8; idx2++)
        {
            board[idx1][idx2] = other.board[idx1][idx2];
        }
    }

    moves = other.moves;
}
/*
bool testCopyConstructor()
{
    Board secondBoard = initial_board;
    secondBoard.movePiece(Point(0, 1), Point(0, 3));
    return initial_board.getPiece(Point(0, 3)).getName() == "EmptyPlace";
}
this function was already tested;
*/



void Board::changeTurn()
{
    if (turn == "white")
    {
        turn = "black";
    }
    else
    {
        turn = "white";
    }
}

Piece Board::getPiece(Point point)
{
    return board[point.getY()][point.getX()];
}

void Board::setPiece(Point point, Piece piece)
{
    board[point.getY()][point.getX()] = piece;
}

vector<Point> Board::getPossibleMoves(Point position)
{
    int movex, movey;
    int piecePositionX, piecePositionY;
    int currPosX, currPosY;
    int multiplier;
    vector<Point> VectOfMoves;
    piecePositionX = position.getX();
    piecePositionY = position.getY();
    Piece piece = board[piecePositionY][piecePositionX];
    if (piece.getColor() != turn)
    {
        return VectOfMoves;
    }
    const Point *elemMoves = piece.getElemMoveSet();
    if (piece.isMoveSetAttackMoveSet())
    {
        for (int idx = 0; idx < piece.numberOfElemMoves(); idx++)
        {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true)
            {
                if (multiplier == 2 && piece.hasInfiniteMoves() == false)
                {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 && currPosY >= 0 && currPosY < 8 && board[currPosY][currPosX].getColor() != turn)
                {
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX, currPosY));
                    if (board[currPosY][currPosX].getName() != "EmptyPlace")
                    {
                        break;
                    }
                }
                else
                {
                    break;
                }
            }
        }
    }
    else
    {
        const Point *attackMoves = piece.getAttackMoveSet();
        for (int idx = 0; idx < piece.numberOfElemMoves(); idx++)
        {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true)
            {
                if (multiplier == 2 && piece.hasInfiniteMoves() == false)
                {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 && currPosY >= 0 && currPosY < 8 && board[currPosY][currPosX].getName() == "EmptyPlace")
                {
                    multiplier++;
                    VectOfMoves.push_back(Point(currPosX, currPosY));
                }
                else
                {
                    break;
                }
            }
        }
        for (int idx = 0; idx < piece.numberOfAttackMoves(); idx++)
        {
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
            currPosY = piecePositionY + movey;
            if (currPosX >= 0 && currPosX < 8 && currPosY >= 0 && currPosY < 8 && board[currPosY][currPosX].getColor() != turn && board[currPosY][currPosX].getColor() != "none")
            {
                multiplier++;
                VectOfMoves.push_back(Point(currPosX, currPosY));
            }
        }
    }
    return VectOfMoves;
}

vector<Point> Board::getPossibleAttacks(Point position)
{
    int movex, movey;
    int piecePositionX, piecePositionY;
    int currPosX, currPosY;
    int multiplier;
    vector<Point> VectOfMoves;
    piecePositionX = position.getX();
    piecePositionY = position.getY();
    Piece piece = board[piecePositionY][piecePositionX];
    if (piece.getColor() != turn)
    {
        return VectOfMoves;
    }
    const Point *elemMoves = piece.getElemMoveSet();
    if (piece.isMoveSetAttackMoveSet())
    {
        for (int idx = 0; idx < piece.numberOfElemMoves(); idx++)
        {
            movex = elemMoves[idx].getX();
            movey = elemMoves[idx].getY();
            multiplier = 1;
            while (true)
            {
                if (multiplier == 2 && piece.hasInfiniteMoves() == false)
                {
                    break;
                }
                currPosX = piecePositionX + multiplier * movex;
                currPosY = piecePositionY + multiplier * movey;
                if (currPosX >= 0 && currPosX < 8 && currPosY >= 0 && currPosY < 8 && board[currPosY][currPosX].getColor() != turn)
                {
                    multiplier++;
                    if (board[currPosY][currPosX].getName() != "EmptyPlace")
                    {
                        VectOfMoves.push_back(Point(currPosX, currPosY));
                        break;
                    }
                }
                else
                {
                    break;
                }
            }
        }
    }
    else
    {
        const Point *attackMoves = piece.getAttackMoveSet();
        for (int idx = 0; idx < piece.numberOfAttackMoves(); idx++)
        {
            movex = attackMoves[idx].getX();
            movey = attackMoves[idx].getY();
            currPosX = piecePositionX + movex;
            currPosY = piecePositionY + movey;
            if (currPosX >= 0 && currPosX < 8 && currPosY >= 0 && currPosY < 8 && board[currPosY][currPosX].getColor() != turn && board[currPosY][currPosX].getColor() != "none")
            {
                multiplier++;
                VectOfMoves.push_back(Point(currPosX, currPosY));
            }
        }
    }
    return VectOfMoves;
}

void Board::updateBoard(){
            string key = hashBoard();
            if ((*Hashmap).find(key) != (*Hashmap).end()){
                *this = (*Hashmap)[key];
            } else {
                isBoardDataCalculated = true;
                //the order of the functions is important
                inCheck = isInCheckinternal();
                moves = getAllPossibleMoves();
                boardEvaluation = evaluateGameinternal();
                isMinimaxCalculated = false;
                Minimaxscore = 0;
                (*Hashmap)[key] = *this;
            }
        }

bool Board::movePiece(Point Position1, Point Position2, bool changeCastling)
{
    bool winningTheGame = false;
    Piece piece = getPiece(Position1);

    if (piece.getName() == "King")
    {

        if (piece.getColor() == "white")
        {
            if (changeCastling)
            {
                LeftCastleWhite = false;
                RightCastleWhite = false;
            }
            WhiteKingPos = Position2;
        }

        else
        {
            if (changeCastling)
            {
                LeftCastleBlack = false;
                RightCastleBlack = false;
            }
            BlackKingPos = Position2;
        }
    }

    if (piece.getName() == "Rook" && changeCastling)
    {

        if (Position1.getX() == 7 && Position1.getY() == 0)
        {
            RightCastleWhite = false;
        }
        else if (Position1.getX() == 0 && Position1.getY() == 0)
        {
            LeftCastleWhite = false;
        }
        else if (Position1.getX() == 0 && Position1.getY() == 7)
        {
            LeftCastleBlack = false;
        }
        else if (Position1.getX() == 7 && Position1.getY() == 7)
        {
            RightCastleBlack = false;
        }
    }
    if (changeCastling)
    {

        if (Position2.getX() == 7 && Position2.getY() == 0)
        {
            RightCastleWhite = false;
        }
        else if (Position2.getX() == 0 && Position2.getY() == 0)
        {
            LeftCastleWhite = false;
        }
        else if (Position2.getX() == 0 && Position2.getY() == 7)
        {
            LeftCastleBlack = false;
        }
        else if (Position2.getX() == 7 && Position2.getY() == 7)
        {
            RightCastleBlack = false;
        }
    }
    setPiece(Position1, Empty);
    if (getPiece(Position2).getName() == "King")
    {
        winningTheGame = true;
    }
    setPiece(Position2, piece);
    return winningTheGame;
}
bool Board::movePieceoff(Point Position1, Point Position2, bool IsPlayer)
{
    bool winningTheGame = false;
    Piece piece = getPiece(Position1);

    updatecastling(piece, Position1, Position2);

    updateEnPassant(piece, Position1, Position2);

    setPiece(Position1, Empty);
    if (getPiece(Position2).getName() == "King")
    {
        winningTheGame = true;
    }
    setPiece(Position2, piece);
    if (IsPlayer){
        choosePawnHuman(Position2);
    } else{
        choosePawnAi(Position2);
    }
    string turn = getTurn();
    changeTurn();
    updateBoard();
    return winningTheGame;
}

void Board::updatecastling(Piece piece, Point Position1, Point Position2)
{
    if (piece.getName() == "King")
    {

        if (piece.getColor() == "white")
        {
            LeftCastleWhite = false;
            RightCastleWhite = false;
            WhiteKingPos = Position2;
        }

        else
        {
            LeftCastleBlack = false;
            RightCastleBlack = false;
            BlackKingPos = Position2;
        }
    }

    if (piece.getName() == "Rook")
    {

        if (Position1.getX() == 7 && Position1.getY() == 0)
        {
            RightCastleWhite = false;
        }
        else if (Position1.getX() == 0 && Position1.getY() == 0)
        {
            LeftCastleWhite = false;
        }
        else if (Position1.getX() == 0 && Position1.getY() == 7)
        {
            LeftCastleBlack = false;
        }
        else if (Position1.getX() == 7 && Position1.getY() == 7)
        {
            RightCastleBlack = false;
        }
    }

    if(getPiece(Position2).getName() == "Rook"){
        if (Position2.getX() == 7 && Position2.getY() == 0)
        {
            RightCastleWhite = false;
        }
        else if (Position2.getX() == 0 && Position2.getY() == 0)
        {
            LeftCastleWhite = false;
        }
        else if (Position2.getX() == 0 && Position2.getY() == 7)
        {
            LeftCastleBlack = false;
        }
        else if (Position2.getX() == 7 && Position2.getY() == 7)
        {
            RightCastleBlack = false;
        }
    }

    if (getPiece(Position1).getName() == "King")
    {
        if (Position2.getX() - Position1.getX() == 2)
        {
            Piece rook = getPiece(Point(7, Position1.getY()));
            setPiece(Point(7, Position1.getY()), Empty);
            setPiece(Point(Position1.getX() + 1, Position1.getY()), rook);
        }
        else if (Position2.getX() - Position1.getX() == -2)
        {
            Piece rook = getPiece(Point(0, Position1.getY()));
            setPiece(Point(0, Position1.getY()), Empty);
            setPiece(Point(Position1.getX() - 1, Position1.getY()), rook);
        }
    }
}

void Board::updateEnPassant(Piece piece, Point Position1, Point Position2)
{
    if (Position2 == enPassant)
    {
        if (getTurn() == "white")
        {
            setPiece(Point(enPassant.getX(), enPassant.getY() - 1), Empty);
        }
        else
        {
            setPiece(Point(enPassant.getX(), enPassant.getY() + 1), Empty);
        }
    }
    enPassant = Point(-1, -1);

    if (getPiece(Position1).getName() == "Pawn" && ((Position2.getY() - Position1.getY()) == 2 || (Position2.getY() - Position1.getY()) == -2))
    {
        enPassant = Point(Position1.getX(), (Position2.getY() + Position1.getY()) / 2);
    }
}

void Board::show()
{

    for (int idxY = 7; idxY >= 0; idxY--)
    {
        for (int idxX = 0; idxX < 8; idxX++)
        {
            putGreyImage(60 * idxX, 480 - (60 * (idxY + 1)), getPiece(Point(idxX, idxY)).getImage(), 60, 60);
        }
    }
}

void Board::print()
{

    for (int idxY = 7; idxY >= 0; idxY--)
    {
        for (int idxX = 0; idxX < 8; idxX++)
        {
            cout << getPiece(Point(idxX,idxY)).getName();
        }
        cout << endl;
    }
}

vector<Point> Board::getPossibleMovesComp(Point position)
{
    vector<Point> moves = getPossibleMoves(position);
    addPawnMoves(moves, position);
    int x = position.getX();
    int y = position.getY();
    vector<Point> trueMoves;
    for (int idx = 0; idx < moves.size(); idx++)
    {
        Point destination = moves[idx];
        Piece piece = getPiece(destination);
        movePiece(position, destination);
        if (!isInCheckinternal())
        {
            trueMoves.push_back(destination);
        }
        movePiece(destination, position);
        setPiece(destination, piece);
    }
    addCastleMoves(trueMoves, position);
    return trueMoves;
}

void Board::addCastleMoves(vector<Point> &trueMoves, Point position)
{
    if (getPiece(position).getName() == "King" && !(isInCheck()))
    {
        int x_castle = position.getX();
        int y_castle = position.getY();
        if (getPiece(position).getColor() == "white" && getTurn() == "white")
        {
            if (RightCastleWhite)
            {
                if (getPiece(Point(x_castle + 1, y_castle)).getName() == "EmptyPlace" && getPiece(Point(x_castle + 2, y_castle)).getName() == "EmptyPlace")
                {
                    movePiece(position, Point(x_castle + 1, y_castle));
                    if (!(isInCheckinternal()))
                    {
                        movePiece(Point(x_castle + 1, y_castle), Point(x_castle + 2, y_castle));
                        if (!(isInCheckinternal()))
                        {
                            trueMoves.push_back(Point(x_castle + 2, y_castle));
                        }
                        movePiece(Point(x_castle + 2, y_castle), position);
                    }
                    else
                    {
                        movePiece(Point(x_castle + 1, y_castle), position);
                    }
                }
            }
            if (LeftCastleWhite)
            {
                if (getPiece(Point(x_castle - 1, y_castle)).getName() == "EmptyPlace" && getPiece(Point(x_castle - 2, y_castle)).getName() == "EmptyPlace" && getPiece(Point(x_castle - 3, y_castle)).getName() == "EmptyPlace")
                {
                    movePiece(position, Point(x_castle - 1, y_castle));
                    if (!(isInCheckinternal()))
                    {
                        movePiece(Point(x_castle - 1, y_castle), Point(x_castle - 2, y_castle));
                        if (!(isInCheckinternal()))
                        {
                            trueMoves.push_back(Point(x_castle - 2, y_castle));
                        }
                        movePiece(Point(x_castle - 2, y_castle), position);
                    }
                    else
                    {
                        movePiece(Point(x_castle - 1, y_castle), position);
                    }
                }
            }
        }
        else if (getPiece(position).getColor() == "black" && getTurn() == "black")
        {
            if (RightCastleBlack)
            {
                if (getPiece(Point(x_castle + 1, y_castle)).getName() == "EmptyPlace" && getPiece(Point(x_castle + 2, y_castle)).getName() == "EmptyPlace")
                {
                    movePiece(position, Point(x_castle + 1, y_castle));
                    if (!(isInCheckinternal()))
                    {
                        movePiece(Point(x_castle + 1, y_castle), Point(x_castle + 2, y_castle));
                        if (!(isInCheckinternal()))
                        {
                            trueMoves.push_back(Point(x_castle + 2, y_castle));
                        }
                        movePiece(Point(x_castle + 2, y_castle), position);
                    }
                    else
                    {
                        movePiece(Point(x_castle + 1, y_castle), position);
                    }
                }
            }
            if (LeftCastleBlack)
            {
                if (getPiece(Point(x_castle - 1, y_castle)).getName() == "EmptyPlace" && getPiece(Point(x_castle - 2, y_castle)).getName() == "EmptyPlace" && getPiece(Point(x_castle - 3, y_castle)).getName() == "EmptyPlace")
                {
                    movePiece(position, Point(x_castle - 1, y_castle));
                    if (!isInCheckinternal())
                    {
                        movePiece(Point(x_castle - 1, y_castle), Point(x_castle - 2, y_castle));
                        if (!isInCheckinternal())
                        {
                            trueMoves.push_back(Point(x_castle - 2, y_castle));
                        }
                        movePiece(Point(x_castle - 2, y_castle), position);
                    }
                    else
                    {
                        movePiece(Point(x_castle - 1, y_castle), position);
                    }
                }
            }
        }
    }
}

void Board::addPawnMoves(vector<Point> &moves, Point position)
{
    int x = position.getX();
    int y = position.getY();
    if (getPiece(position).getName() == "Pawn")
    {
        if (getPiece(position).getColor() == "white" && getTurn() == "white")
        {
            if (y == 1)
            {
                if (getPiece(Point(x, y + 2)).getName() == "EmptyPlace" && getPiece(Point(x, y + 1)).getName() == "EmptyPlace")
                {
                    moves.push_back(Point(x, y + 2));
                }
            }
            else if (((Point(x + 1, y + 1) == enPassant) || (Point(x - 1, y + 1) == enPassant)))
            {
                moves.push_back(enPassant);
            }
        }
        else if (getPiece(position).getColor() == "black" && getTurn() == "black")
        {
            if (y == 6)
            {
                if (getPiece(Point(x, y - 2)).getName() == "EmptyPlace" && getPiece(Point(x, y - 1)).getName() == "EmptyPlace")
                {
                    moves.push_back(Point(x, y - 2));
                }
            }
            else if (((Point(x + 1, y - 1) == enPassant) || (Point(x - 1, y - 1) == enPassant)))
            {
                moves.push_back(enPassant);
            }
        }
    }
}

map<Point, vector<Point>> Board::getAllPossibleMoves()
{
    map<Point, vector<Point>> possibleMoves;
    for (int x = 0; x < 8; x++)
    {
        for (int y = 0; y < 8; y++)
        {
            Point point(x, y);
            vector<Point> movees = getPossibleMovesComp(point);
            if (movees.size() != 0)
                possibleMoves[point] = movees;
        }
    }
    return possibleMoves;
}
map<Point, vector<Point>> Board::getAllPossibleWhiteMoves()
{
    if (getTurn() == "white")
    {
        return getAllPossibleMoves();
    }
    else
    {
        changeTurn();
        map<Point, vector<Point>> possibleMoves = getAllPossibleMoves();
        changeTurn();
        return possibleMoves;
    }
}
map<Point, vector<Point>> Board::getAllPossibleBlackMoves()
{
    if (getTurn() == "black")
    {
        return getAllPossibleMoves();
    }
    else
    {
        changeTurn();
        map<Point, vector<Point>> possibleMoves = getAllPossibleMoves();
        changeTurn();
        return possibleMoves;
    }
}


string Board::hashBoard(){
    string hashedBoard = "";
    for (int x = 0; x < 8; x++){
        for(int y =0; y < 8; y++){
            hashedBoard += board[x][y].hashPiece();
        }
    }
    if(LeftCastleBlack){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    if(RightCastleBlack){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    if(LeftCastleWhite){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    if(RightCastleWhite){
        hashedBoard += "T";
    } else {
        hashedBoard += "F";
    }
    hashedBoard += to_string(turn == "white");
    hashedBoard += to_string(enPassant.getX());
    hashedBoard += to_string(enPassant.getY());
    return hashedBoard;
}

bool Board::isInCheckinternal()
{
    vector<Point> test;
    int x, y;
    if (getTurn() == "white")
    {
        x = WhiteKingPos.getX();
        y = WhiteKingPos.getY();
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "King")
            {
                return true;
            }
        }
        if (getPiece(Point(x + 1, y + 1)).getName() == "Pawn" && getPiece(Point(x + 1, y + 1)).getColor() == "black")
        {
            return true;
        }
        if (getPiece(Point(x - 1, y + 1)).getName() == "Pawn" && getPiece(Point(x - 1, y + 1)).getColor() == "black")
        {
            return true;
        }
        setPiece(WhiteKingPos, WhiteBishop);
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" || getPiece(test[idx]).getName() == "Bishop")
            {
                setPiece(WhiteKingPos, WhiteKing);
                return true;
            }
        }
        setPiece(WhiteKingPos, WhiteRook);
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" || getPiece(test[idx]).getName() == "Rook")
            {
                setPiece(WhiteKingPos, WhiteKing);
                return true;
            }
        }
        setPiece(WhiteKingPos, WhiteKnight);
        test = getPossibleAttacks(WhiteKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Knight")
            {
                setPiece(WhiteKingPos, WhiteKing);
                return true;
            }
        }
        setPiece(WhiteKingPos, WhiteKing);
    }
    else
    {
        x = BlackKingPos.getX();
        y = BlackKingPos.getY();
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "King")
            {
                return true;
            }
        }
        if (getPiece(Point(x + 1, y - 1)).getName() == "Pawn" && getPiece(Point(x + 1, y - 1)).getColor() == "white")
        {
            return true;
        }
        if (getPiece(Point(x - 1, y - 1)).getName() == "Pawn" && getPiece(Point(x - 1, y - 1)).getColor() == "white")
        {
            return true;
        }
        setPiece(BlackKingPos, BlackBishop);
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" || getPiece(test[idx]).getName() == "Bishop")
            {
                setPiece(BlackKingPos, BlackKing);
                return true;
            }
        }
        setPiece(BlackKingPos, BlackRook);
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Queen" || getPiece(test[idx]).getName() == "Rook")
            {
                setPiece(BlackKingPos, BlackKing);
                return true;
            }
        }
        setPiece(BlackKingPos, BlackKnight);
        test = getPossibleAttacks(BlackKingPos);
        for (int idx = 0; idx < test.size(); idx++)
        {
            if (getPiece(test[idx]).getName() == "Knight")
            {
                setPiece(BlackKingPos, BlackKing);
                return true;
            }
        }
        setPiece(BlackKingPos, BlackKing);
    }
    return false;
}

bool Board::isInCheck(){
    if (!isBoardDataCalculated){
        updateBoard();
    }
    return inCheck;
}

int Board::evaluateGame(){
    if (!isBoardDataCalculated){
        updateBoard();
    }
    return boardEvaluation;
}

string Board::gameOver()
{
    if (!isBoardDataCalculated)
    {
        updateBoard();
    }
    if (moves.size() == 0)
    {
        if (isInCheck())
        {
            return getTurn() + " won";
        }
        else
        {
            return "stalemate";
        }
    }
    else
    {
        return "NONE";
    }
}

float Board::getGamePhase()
{
    int whitePieces = 0;
    int blackPieces = 0;
    int val;
    float total, phase;
    for (int y = 0; y < 8; y++)
    {
        for (int x = 0; x < 8; x++)
        {
            Piece piece = getPiece(Point(x, y));
            if (piece.getName() != "EmptyPlace")
            {
                int val = initialScores[piece.getName()];
                if (piece.getColor() == "white")
                {
                    whitePieces += val;
                }
                else
                {
                    blackPieces += val;
                }
            }
        }
    }
    total = whitePieces + blackPieces;
    phase = max(0.0, min(1.0, (5600.0 - total) / 3600.0));
    return phase;
}

int Board::evaluateControlOfKeySquares()
{
    Point centerSquares[4] = {Point(3, 3), Point(3, 4), Point(4, 3), Point(4, 4)};
    int score = 0;
    for (int idx = 0; idx < 4; idx++)
    {
        Piece piece = getPiece(centerSquares[idx]);
        if (piece.getColor() == "white")
        {
            score += 20;
        }
        else if (piece.getColor() == "black")
        {
            score -= 20;
        }
    }
    return score;
}

bool Board::isKingActive(string color)
{
    if (color == "white")
    {
        int x = WhiteKingPos.getX();
        int y = WhiteKingPos.getY();
        return (2 < x && x < 5) && (2 < y && y < 5);
    }
    else
    {
        int x = BlackKingPos.getX();
        int y = BlackKingPos.getY();
        return (2 < x && x < 5) && (2 < y && y < 5);
    }
}

int Board::centerControl()
{
    int score = 0;
    for (const auto &pair : getAllPossibleWhiteMoves())
    {
        for (const auto &point : pair.second)
        {
            int x = point.getX();
            int y = point.getY();
            if (x > 2 && x < 5 && y > 2 && y < 5)
            {
                score += 1;
            }
        }
    }
    for (const auto &pair : getAllPossibleBlackMoves())
    {
        for (const auto &point : pair.second)
        {
            int x = point.getX();
            int y = point.getY();
            if (x > 2 && x < 5 && y > 2 && y < 5)
            {
                score -= 1;
            }
        }
    }
    return score;
}

int Board::evaluateGameinternal()
{
    int materialScore = evaluateBoard();
    /*
    int centerScore = centerControl();
    // Pawn structure

    int kingSafetyScore = 0;
    int pieceCoordinationScore = 0;
    int controlScore = evaluateControlOfKeySquares();
    int endGameScore = evaluateEndGameFeatures();

    int phase = getGamePhase();
    // opening_weight ~ (1 - phase)
    // endgame_weight ~ phase
    int openingWeight = 1 - phase;
    int endGameWeight = phase;
    int totalScore = (materialScore * 1 +
                      kingSafetyScore * 1.0 +
                      pieceCoordinationScore * 0.6 +
                      controlScore * (0.6 * openingWeight + 0.3 * endGameWeight) +
                      endGameScore * endGameWeight);
    */
    return materialScore;
}

void Board::choosePawnHuman(Point point){
    int idx_piece_chosen;
    if ((getPiece(point).getName() == "Pawn") && (point.getY()==0 || point.getY()==7)){
            cout << "choose a piece to change your pawn into" << endl;
            cout << "0: Queen    1: Rook    2: Bishop    3: Knight" << endl;
            while(true){
                cin >> idx_piece_chosen;
                if (idx_piece_chosen>=0 && idx_piece_chosen<4){
                    break;
                }
                cout << "choose a valid index between 0 and 3" << endl;
            }
            if (getTurn() == "white"){
                switch(idx_piece_chosen){
                    case 0:
                        setPiece(point,WhiteQueen);
                        break;
                    case 1:
                        setPiece(point,WhiteRook);
                        break;
                    case 2:
                        setPiece(point,WhiteBishop);
                        break;
                    case 3:
                        setPiece(point,WhiteKnight);
                        break;
                }
            }
            if (getTurn() == "black"){
                switch(idx_piece_chosen){
                    case 0:
                        setPiece(point,BlackQueen);
                        break;
                    case 1:
                        setPiece(point,BlackRook);
                        break;
                    case 2:
                        setPiece(point,BlackBishop);
                        break;
                    case 3:
                        setPiece(point,BlackKnight);
                        break;
                }
            }
        }
}

void Board::choosePawnAi(Point point){
    if ((getPiece(point).getName() == "Pawn") && (point.getY()==0 || point.getY()==7)){
        if (getTurn() == "white"){
                setPiece(point,WhiteQueen);
        } else{
                setPiece(point,BlackQueen);
        }
    }
}

// lengthwise
Piece initialBoard[64] = {
    WhiteRook, WhiteKnight, WhiteBishop, WhiteQueen, WhiteKing, WhiteBishop, WhiteKnight, WhiteRook,
    WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty,
    BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn,
    BlackRook, BlackKnight, BlackBishop, BlackQueen, BlackKing, BlackBishop, BlackKnight, BlackRook};

Board initial_board(initialBoard, "white");