#undef NDEBUG

#include <algorithm>
#include <cassert>
#include <deque>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <unordered_set>
#include <utility>

void smoke_basin(std::istream& input) {
    std::string line;
    std::vector<int8_t> caves;
    size_t maxx = 0, maxy = 0;
    while (std::getline(input, line)) {
        maxx = line.size();
        for (auto c : line) {
            caves.push_back(c - '0');
        }
        ++maxy;
    }
    auto&& index = [maxx](int x, int y) { return x + maxx * y; };
    std::vector<int> low_points;
    std::vector<std::set<int>> neighbors;
    neighbors.resize(caves.size());
    int risk = 0;
    // Populate neighbors for each index, find low-points, and
    // calculate part 1 solution
    for (int i = 0; i < caves.size(); ++i) {
        int y = i / maxx;
        int x = i % maxx;
        auto& n = neighbors[i];
        for (auto& [dx, dy] : {std::pair{0, -1}, std::pair{0, 1},
                 std::pair{-1, 0}, std::pair{1, 0}}) {
            if (x + dx >= 0 && x + dx < maxx && y + dy >= 0 && y + dy < maxy) {
                n.insert(index(x + dx, y + dy));
            }
        }
        if (std::all_of(n.begin(), n.end(), [&, current = caves[i]](int idx) {
                return current < caves[idx];
            })) {
            risk += 1 + caves[i];
            low_points.push_back(i);
        }
    }

    // Part 2: map basins
    std::vector<int> basins;
    for (int lp : low_points) {
        std::unordered_set<int> seen;
        std::deque<int> to_visit{{lp}};
        while (!to_visit.empty()) {
            for (auto n : neighbors[to_visit.front()]) {
                if (caves[n] < 9 && !seen.contains(n)) {
                    seen.insert(n);
                    to_visit.push_back(n);
                }
            }
            to_visit.pop_front();
        }
        basins.push_back(seen.size());
    }
    assert(basins.size() >= 3);
    std::sort(basins.begin(), basins.end(), std::greater<int>());

    std::cout << risk << "\n"
              << std::accumulate(basins.begin(), basins.begin() + 3, 1,
                     [](int i, int j) { return i * j; })
              << "\n";
}

int main() {
    std::ifstream input("9.txt");
    smoke_basin(input);
    return 0;
}
