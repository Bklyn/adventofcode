#include <algorithm>
#include <bitset>
#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <utility>
#include <vector>

template <size_t N>
std::bitset<N> filter(std::vector<std::bitset<N>> bitvec, bool oxygen) {
    // Instructions process bits from high to low
    for (int i = N - 1; i >= 0; --i) {
        auto iter = std::partition(bitvec.begin(), bitvec.end(),
            [i](const auto& bits) { return bits.test(i); });
        size_t num_ones = std::distance(bitvec.begin(), iter);
        size_t num_zeroes = bitvec.size() - num_ones;
        const bool keep_ones = (oxygen && num_ones >= num_zeroes) ||
                               (!oxygen && num_ones < num_zeroes);
        if (keep_ones) {
            bitvec.erase(iter, bitvec.end());
        } else {
            bitvec.erase(bitvec.begin(), iter);
        }
        if (bitvec.size() == 1)
            return bitvec.front();
    }
    assert(false);
}

template <size_t N>
std::pair<size_t, size_t> day3(std::istream& in) {
    std::string line;
    std::vector<std::bitset<N>> bitvec;
    while (std::getline(in, line)) {
        bitvec.emplace_back(line);
    }
    std::bitset<N> gamma;
    for (size_t i = 0; i < N; ++i) {
        const auto ones = std::count_if(bitvec.begin(), bitvec.end(),
            [i](const auto& bits) { return bits.test(i); });
        gamma[i] = (ones >= bitvec.size() / 2);
    }
    const auto epsilon = ~gamma;
    return {gamma.to_ulong() * epsilon.to_ulong(),
        filter(bitvec, true).to_ulong() * filter(bitvec, false).to_ulong()};
}

int main() {
    std::stringstream is{
        "00100\n"
        "11110\n"
        "10110\n"
        "10111\n"
        "10101\n"
        "01111\n"
        "00111\n"
        "11100\n"
        "10000\n"
        "11001\n"
        "00010\n"
        "01010"};
    assert((day3<5>(is) == std::pair{198ul, 230ul}));
    std::ifstream in{"3.txt"};
    const auto ans = day3<12>(in);
    std::cout << ans.first << '\n' << ans.second << '\n';
}
