//
// Created by hassenekallala on 29/11/24.
//

#include "AI.h"
#include<Python.h>
#include <pybind11/pybind11.h>
#include <iostream>
// Simple add function to be exposed to Python
int add(int a, int b) {
    std::cout << "We are adding " << a << " and " << b << std::endl;
    return a + b;
}

// Create the AI Python module using pybind11
PYBIND11_MODULE(AI, m) {
    m.doc() = "AI Engine Python bindings";  // Optional: module documentation
    m.def("add", &add, "A function that adds two numbers");
}