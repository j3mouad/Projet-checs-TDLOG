//
// Created by hassenekallala on 29/11/24.
//

#include "AI.h"
#include<Python.h>
#include <pybind11/pybind11.h>
#include <iostream>
#include<random>
using namespace std ;
// Simple add function to be exposed to Python
pair<int,int> generator() {
    std::random_device rd;
    std::mt19937 gen(rd());
    return make_pair(gen(), gen());
}


// Create the AI Python module using pybind11
PYBIND11_MODULE(libAI, m) {
    m.doc() = "AI Engine Python bindings";  // Optional: module documentation
    m.def("generator", &generator, "A function that will be used to generate AI,moves");
}
