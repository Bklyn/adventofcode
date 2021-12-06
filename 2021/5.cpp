#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
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
    std::map<point_t, size_t> graph;
    for (auto [p0, p1] : lines) {
        const auto [x0, y0] = p0;
        const auto [x1, y1] = p1;
        int dx = x0 == x1 ? 0 : x0 < x1 ? 1 : -1;
        int dy = y0 == y1 ? 0 : y0 < y1 ? 1 : -1;
        if (not diagonals and dx and dy)
            continue;
        while (true) {
            graph[p0]++;
            if (p0 == p1)
                break;
            p0 = std::pair{p0.first + dx, p0.second + dy};
        }
    }
    return std::count_if(graph.begin(), graph.end(),
        [](const auto& iter) { return iter.second > 1; });
}

int main() {
    std::ifstream in{"5.txt"};
    auto lines = parse_input(in);
    assert(lines.size() == 500);
    std::cout << covered(lines, false) << "\n" << covered(lines, true) << "\n";
}
