// AOC C++ helper functions

#pragma once

#include <algorithm>
#include <cassert>
#include <deque>
#include <fstream>
#include <iostream>
#include <memory>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>

std::unique_ptr<std::istream> input(int day) {
    std::string filename = std::to_string(day) + ".txt";
    auto ptr = std::make_unique<std::ifstream>(filename);
    if (!*ptr) {
        throw std::runtime_error("Unable to read " + filename);
    }
    return ptr;
}
