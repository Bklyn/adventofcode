#include "aoc.hpp"
#include <unordered_map>
int move(int p, int roll) {
    return (p + roll - 1) % 10 + 1;
}


std::unordered_map<uint32_t, std::pair<size_t, size_t>> cache;

std::pair<size_t, size_t>
dirac_dice(int p1, int p2, int s1=0, int s2=0, bool player1=true, int roll=0, int sum=0) {
    uint32_t key = ((p1 << 21) | (p2 << 17) | (s1 << 12) | (s2 << 7) | ((player1 ? 1 : 0) << 6) |
                    (roll << 4) | sum);
    auto citer = cache.find(key);
    if (citer != cache.end()) {
        return citer->second;
    }
    size_t w1 = 0, w2 = 0, z1 = 0, z2 = 0;
    for (int die : {1, 2, 3}) {
        if (roll + 1 == 3) {
            if (player1) {
                int q1 = move(p1, sum + die);
                if (s1 + q1 >= 21) {
                    ++w1;
                    continue;
                }
                std::tie(z1, z2) = dirac_dice(q1, p2, s1 + q1, s2, false);
            } else {
                int q2 = move(p2, sum + die);
                if (s2 + q2 >= 21) {
                    ++w2;
                    continue;
                }
                std::tie(z1, z2) = dirac_dice(p1, q2, s1, s2 + q2, true);
            }
            w1 += z1;
            w2 += z2;
            continue;
        }
        std::tie(z1, z2) = dirac_dice(p1, p2, s1, s2, player1, roll + 1, sum + die);
        w1 += z1;
        w2 += z2;
    }
    cache[key] = {w1, w2};
    return {w1, w2};
}

int main()
{
    auto [w1, w2] = dirac_dice(10, 2);
    std::cout << std::max(w1, w2) << std::endl;
}
