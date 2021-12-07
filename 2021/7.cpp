#include <cassert>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>
#include <algorithm>

size_t triangle(size_t n) {
    // memoize previous results
    static std::vector<size_t> sums{0, 1, 3};
    for (size_t i = sums.size(); i <= n; ++i) {
        sums.push_back(sums.back() + i);
    }
    return sums.at(n);
}

size_t crab_fuel(std::vector<int> crabs, bool part2) {
    size_t best = std::numeric_limits<size_t>::max();
    // Sort crabs from high position to low so we need only a single
    // expensive call to "triangle".  After that, all other results
    // should be cached.
    std::sort(crabs.begin(), crabs.end(), std::greater<int>());
    for (int i = 0; i <= crabs.front(); ++i) {
        size_t diff = std::accumulate(
            crabs.begin(), crabs.end(), 0,
            [part2, i](size_t sum, int x) {
                size_t move = std::abs(x - i);
                size_t cost = part2 ? triangle(move) : move;
                return sum + cost;
            });
        best = std::min(best, diff);
    }
    return best;
}

int main() {
    std::vector<int> ex7{16,1,2,0,4,2,7,1,2,14};
    assert(crab_fuel(ex7, false) == 37);
    assert(crab_fuel(ex7, true) == 168);
    std::ifstream in{"7.txt"};
    std::vector<int> in7;
    std::string line;
    while (std::getline(in, line, ',')) {
        in7.push_back(std::stoi(line));
    }
    std::cout << crab_fuel(in7, false) << '\n'
              << crab_fuel(in7, true) << '\n';
}
