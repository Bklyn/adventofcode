#include <cassert>
#include <iostream>
#include <fstream>
#include <map>
#include <numeric>

std::map<int, size_t>
parse_input(std::istream& in) {
    std::map<int, size_t> fish;
    std::string str;
    while (std::getline(in, str, ',')) {
        fish[std::stol(str)]++;
    }
    return fish;
}

size_t
lanternfish(std::map<int, size_t> fish, int days) {
    for (int i = 0; i < days; ++i) {
        std::map<int, size_t> new_fish;
        for (auto [t, count] : fish) {
            auto timer = t;
            if (timer == 0) {
                timer = 6;
                new_fish.emplace(8, count);
            } else {
                --timer;
            }
            new_fish[timer] += count;
        }
        fish.swap(new_fish);
    }
    return std::accumulate(
        fish.begin(), fish.end(), 0ul,
        [](size_t val, const auto& iter) {
            return val + iter.second;
        });
}

int main() {
    // 3,4,3,1,2
    const std::map<int, size_t> example{{3, 2}, {4, 1}, {1, 1}, {2, 1}};
    assert (lanternfish(example, 80) == 5934);
    assert (lanternfish(example, 256) == 26984457539);
    std::ifstream in{"6.txt"};
    const auto fish = parse_input(in);
    std::cout << lanternfish(fish, 80) << "\n"
              << lanternfish(fish, 256) << "\n";
}
