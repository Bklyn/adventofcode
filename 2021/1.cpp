#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

int sonar(const std::vector<int>& v, size_t window = 1) {
    if (v.size() < window + 1)
        return 0;
    auto prev_begin = std::begin(v);
    auto prev_end = prev_begin + window;
    auto curr_begin = prev_begin + 1;
    auto curr_end = curr_begin + window;
    auto prev_sum = std::accumulate(prev_begin, prev_end, 0);
    auto curr_sum = std::accumulate(curr_begin, curr_end, 0);
    int increasing = curr_sum > prev_sum;
    while (curr_end != v.end()) {
        prev_sum -= *prev_begin++;
        prev_sum += *prev_end++;
        curr_sum -= *curr_begin++;
        curr_sum += *curr_end++;
        increasing += curr_sum > prev_sum;
    }
    return increasing;
}

int main() {
    std::ifstream in{"1.txt"};
    int i;
    std::vector<int> v;
    while (in >> i) {
        v.push_back(i);
    }
    std::cout << sonar(v, 1) << "\n" << sonar(v, 3) << "\n";
    return 0;
}