#include "aoc.hpp"

std::pair<int, int> octopus(std::istream& in) {
    size_t maxx = 0, maxy = 0;
    std::vector<int> board;
    std::string line;
    while (std::getline(in, line)) {
        maxy++;
        for (auto c : line) {
            assert(std::isdigit(c));
            board.push_back(c - '0');
        }
        maxx = line.size();
    }
    assert(board.size() == maxx * maxy);
    std::vector<std::set<int>> neighbors;
    neighbors.resize(board.size());
    for (size_t i = 0; i < board.size(); ++i) {
        size_t x = i % maxx;
        size_t y = i / maxx;
        auto& n = neighbors[i];
        for (auto [dx, dy] : std::vector<std::tuple<int, int>>{{-1, -1},
                 {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}}) {
            if ((x > 0 || dx >= 0) && x + dx < maxx && (y > 0 || dy >= 0) &&
                y + dy < maxy)
                n.insert((y + dy) * maxx + x + dx);
        }
    }
    int round = 0;
    size_t flashes = 0;
    while (true) {
        // Check for flashes
        std::unordered_set<size_t> flashed;
        for (size_t i = 0; i < board.size(); ++i) {
            if (++board[i] > 9) {
                flashed.insert(i);
            }
        }
        // Recursive flashing
        std::deque<size_t> flashq{flashed.begin(), flashed.end()};
        while (!flashq.empty()) {
            auto i = flashq.front();
            for (auto n : neighbors[i]) {
                if (++board[n] > 9 && !flashed.contains(n)) {
                    flashed.insert(n);
                    flashq.push_back(n);
                }
            }
            flashq.pop_front();
        }
        if (++round <= 100)
            flashes += flashed.size();
        if (flashed.size() == board.size())
            break;
        for (auto i : flashed) {
            board[i] = 0;
        }
    }
    return {flashes, round};
}

int main() {
    auto res = octopus(*input(11));
    std::cout << res.first << "\n" << res.second << "\n";
    return 0;
}
