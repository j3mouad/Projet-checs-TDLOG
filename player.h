#pragma once
#include "board.h"

class Player{
    private:
        /*white or black*/
        string color;
        /*human or a type of ai*/
        string type;
    public:
        Player(string color, string type) : color(color), type(type){}
        Player() = default;
        string getColor() const {return color;}
        string getType() const {return type;}      
};


