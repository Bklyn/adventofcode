#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

using point_t = std::pair<int, int>;
using line_t = std::pair<point_t, point_t>;

std::vector<line_t> parse_input(std::istream& in) {
    std::string line;
    std::vector<line_t> result;
    while (std::getline(in, line)) {
        int x0, y0, x1, y1;
        if (sscanf(line.c_str(), "%d,%d -> %d,%d", &x0, &y0, &x1, &y1) != 4) {
            continue;
        }
        result.emplace_back(std::pair{x0, y0}, std::pair{x1, y1});
    }
    return result;
}

int covered(const std::vector<line_t>& lines, bool diagonals) {
    // The bounding box of my input data is 989x989, but 1000x1000 is
    // a bit neater
    std::vector<int8_t> graph;
    graph.resize(1000 * 1000, 0);
    for (auto [p0, p1] : lines) {
        const auto [x0, y0] = p0;
        const auto [x1, y1] = p1;
        int dx = x0 == x1 ? 0 : x0 < x1 ? 1 : -1;
        int dy = y0 == y1 ? 0 : y0 < y1 ? 1 : -1;
        if (not diagonals and dx and dy)
            continue;
        // Note: malformed input would cause us to loop forever; using
        // vector.at should raise an exception in this case
        while (true) {
            const size_t idx = 1000 * p0.second + p0.first;
            graph.at(idx)++;
            if (p0 == p1)
                break;
            p0 = std::pair{p0.first + dx, p0.second + dy};
        }
    }
    return std::count_if(graph.begin(), graph.end(),
        [](const auto& x) { return x > 1; });
}

int main() {
    std::ifstream in{"5.txt"};
    auto lines = parse_input(in);
    std::cout << covered(lines, false) << "\n" << covered(lines, true) << "\n";
}
