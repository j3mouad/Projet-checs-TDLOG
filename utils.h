#pragma once
class Point
{
private:
    // Coords
    int x,y;
public:
    Point(int x, int y) : x(x), y(y){}
    Point(pair<int,int> p) : x(p.first), y(p.second) {}
    Point() = default;
    // Copy constructor 
    Point(const Point &A) : x(A.x), y(A.y){}
    bool operator==(const Point &A) const{return (x==A.x && y==A.y);}
    bool operator<(const Point &A) const{return (x<A.x)||(x==A.x && y<A.y);}
    friend ostream& operator<<(ostream& os, const Point& point){
        os << "(" << point.x << ":" << point.y << ")";
        return os;
    }
    int getX () const {return x;}
    int getY () const {return y;}
    void setX (int chosenX){x = chosenX;}
    void setY (int chosenY){y = chosenY;}
};
