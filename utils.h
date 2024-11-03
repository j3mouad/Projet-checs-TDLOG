class Point
{
private:
    // Coords
    int x,y;
public:
    Point(int x, int y) : x(x), y(y){}
    Point() = default;
    int getX () const {return x;}
    int getY () const {return y;}
};
