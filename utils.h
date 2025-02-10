#pragma once

/**
 * @brief Represents a point in a 2D coordinate system.
 *
 * The Point class encapsulates an x and y coordinate, providing constructors,
 * getter and setter methods, and overloaded operators for equality, ordering, and
 * stream output.
 */
class Point
{
private:
    /**
     * @brief The x-coordinate of the point.
     */
    int x;
    
    /**
     * @brief The y-coordinate of the point.
     */
    int y;
    
public:
    /**
     * @brief Constructs a Point with given x and y coordinates.
     *
     * @param x The x-coordinate.
     * @param y The y-coordinate.
     */
    Point(int x, int y) : x(x), y(y) {}

    /**
     * @brief Constructs a Point from a std::pair of integers.
     *
     * @param p A pair where the first element is the x-coordinate and the second is the y-coordinate.
     */
    Point(pair<int,int> p) : x(p.first), y(p.second) {}

    /**
     * @brief Default constructor.
     */
    Point() = default;

    /**
     * @brief Copy constructor.
     *
     * @param A The Point object to copy.
     */
    Point(const Point &A) : x(A.x), y(A.y) {}

    /**
     * @brief Equality operator.
     *
     * Compares two Point objects for equality.
     *
     * @param A The Point to compare with.
     * @return True if both x and y coordinates are equal, false otherwise.
     */
    bool operator==(const Point &A) const { return (x == A.x && y == A.y); }

    /**
     * @brief Less-than operator.
     *
     * Provides a lexicographical ordering for Point objects. The ordering is based on the x-coordinate first,
     * and then the y-coordinate if the x-coordinates are equal.
     *
     * @param A The Point to compare with.
     * @return True if this point is less than A, false otherwise.
     */
    bool operator<(const Point &A) const { return (x < A.x) || (x == A.x && y < A.y); }

    /**
     * @brief Output stream operator.
     *
     * Outputs the point in the format "(x:y)".
     *
     * @param os The output stream.
     * @param point The Point object to output.
     * @return A reference to the output stream.
     */
    friend ostream& operator<<(ostream& os, const Point& point) {
        os << "(" << point.x << ":" << point.y << ")";
        return os;
    }

    /**
     * @brief Retrieves the x-coordinate.
     *
     * @return The x-coordinate of the point.
     */
    int getX() const { return x; }

    /**
     * @brief Retrieves the y-coordinate.
     *
     * @return The y-coordinate of the point.
     */
    int getY() const { return y; }

    /**
     * @brief Sets the x-coordinate.
     *
     * @param chosenX The new x-coordinate.
     */
    void setX(int chosenX) { x = chosenX; }

    /**
     * @brief Sets the y-coordinate.
     *
     * @param chosenY The new y-coordinate.
     */
    void setY(int chosenY) { y = chosenY; }
};
