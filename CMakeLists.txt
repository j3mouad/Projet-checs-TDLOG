cmake_minimum_required(VERSION 3.15)
project(Projet-echecs-TDLOG)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Ensure position-independent code (needed for shared libraries)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find required packages
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

# Add library for Python module (pybind11-based)
add_library(AI MODULE AI.cpp)
target_link_libraries(AI PRIVATE Python3::Python pybind11::module)

# Add the main executable for the chess project
add_executable(Projet-echecs-TDLOG
        main.cpp
        utils.h
        game.h
        game.cpp
        board.h
        board.cpp
        player.h
        pieces.h
        pieces.cpp
)

# Link additional libraries if needed
target_link_libraries(Projet-echecs-TDLOG PRIVATE Python3::Python pybind11::module)
