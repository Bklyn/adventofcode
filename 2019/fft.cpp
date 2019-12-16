#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// There must be a way to do this w/o the brute force inner loop...
std::string fft(std::string input, int rounds = 1) {
    std::vector<size_t> incsum(input.size() + 1);
    std::string output;
    output.reserve(input.size());
    for (; rounds > 0; --rounds) {
        size_t sum = 0;
        output.clear();
        incsum.resize(1, 0);
        for (auto c : input) {
            sum += c - '0';
            incsum.push_back(sum);
        }
        for (auto i = 0u; i < input.size(); ++i) {
            long digit = 0;
            size_t window = i + 1;
            const auto maxidx = incsum.size() - 1;
            for (auto idx = i; idx < input.size(); idx += 4 * window) {
                digit += incsum.at(std::min(idx + window, maxidx)) -
                         incsum.at(idx) -
                         (incsum.at(std::min(idx + 3 * window, maxidx)) -
                          incsum.at(std::min(idx + 2 * window, maxidx)));
            }
            output.append(1, '0' + std::abs(digit) % 10);
        }
        std::swap(input, output);
    }
    return input;
}

int
main()
{
    assert (fft("12345678") == "48226158");
    assert (fft("80871224585914546619083218645595", 100).substr(0, 8) == "24176176");

    std::ifstream in("16.txt");
    std::string input;
    std::getline(in, input);
    std::cout << fft(input, 100).substr(0, 8) << std::endl;

    // 10,000 times longer...
    std::string longer;
    longer.reserve(input.size() * 10000);
    for (size_t i = 0; i < 10000; ++i) {
        longer.append(input);
    }
    size_t offset = std::stol(input.substr(0, 7));
    assert (offset + 8 < longer.size());
    auto part2 = fft(longer, 100);
    std::cout << part2.substr(offset, 8) << std::endl;
}
