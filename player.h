#include "pieces.h"

class player{
    private:
        /*white or black*/
        string color;
        /*human or a type of ai*/
        string type;
    public:
        player(string color, string type) : color(color), type(type){}
        player() = default;
        string getColor() const {return color;}
        string getType() const {return type;}
};