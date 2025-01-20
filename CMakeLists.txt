cmake_minimum_required(VERSION 3.4)
project(Projet-echecs-TDLOG)

find_package(Imagine REQUIRED COMPONENTS Graphics)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)

# Add the executable
add_executable(Projet-echecs-TDLOG 
    main.cpp
    utils.h
    game.h 
    game.cpp
    board.h
    board.cpp 
    player.h
    player.cpp
    pieces.h
    pieces.cpp
)

target_link_libraries(Projet-echecs-TDLOG Imagine::Graphics)
