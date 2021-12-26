#include "aoc.hpp"
#include "monad.hpp"
// #include "q.hpp"

int main()
{
    for (auto i : {
            94992992796199,
            11931881141161,
        }) {
        std::cout << i << ' ' << monad(i) << std::endl;
    }
    return 0;
    for (int64_t i = 99999999999999L; i >= 11111111111111; --i) {
        auto z = monad(i);
        if (z == -1) continue;
        std::cout << i << ' ' << z << '\n';
        if (z == 0) break;
    }
}
