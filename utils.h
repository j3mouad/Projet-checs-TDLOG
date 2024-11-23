#pragma once
class Point
{
private:
    // Coords
    int x,y;
public:
    Point(int x, int y) : x(x), y(y){}
    Point() = default;
    // Copy constructor 
    Point(const Point &A) : x(A.x), y(A.y){}
    bool operator==(Point &A) const{return (x==A.x && y==A.y);}
    int getX () const {return x;}
    int getY () const {return y;}
    void setX (int chosenX){x = chosenX;}
    void setY (int chosenY){y = chosenY;}
};
