#include "aoc.hpp"

#include <functional>
#include <string>
#include <variant>
#include <cctype>
#include <list>

std::string to_bits(const std::string& input)
{
    std::ostringstream os;
    for (char c : input) {
        unsigned i = std::isdigit(c) ? c - '0' : std::toupper(c) - 'A' + 10;
        os << std::bitset<4>{i}.to_string();
    }
    return os.str();
}

struct packet {
    uint8_t version;
    uint8_t type_id;
    std::variant<uint64_t, std::list<packet>> contents;
    std::string_view tail;

    friend std::ostream& operator<<(std::ostream& os, const packet& p) {
        os << int(p.version) << '/' << int(p.type_id) << '/';
        if (const auto* pi = std::get_if<uint64_t>(&p.contents)) {
            return os << *pi;
        }
        const auto& l = std::get<1>(p.contents);
        os << '[';
        for (const auto& q : l) {
            os << q << ' ';
        }
        return os << ']';
    }
};

packet
parse_bits(std::string_view bits) {
    assert (bits.size() > 6);
    uint8_t version = std::bitset<3>{bits.data(), 3}.to_ulong();
    uint8_t type_id = std::bitset<3>{bits.data() + 3, 3}.to_ulong();
    bits = bits.substr(6);
    if (type_id == 4) {
        uint64_t value = 0;
        while (!bits.empty()) {
            char cont = bits[0];
            std::bitset<4> word{bits.data() + 1, 4};
            bits = bits.substr(5);
            value = (value << 4) + word.to_ulong();
            if (cont == '0')
                break;
        }
        return {version, type_id, value, bits};
    }
    auto ltid = bits[0];
    bits = bits.substr(1);
    if (ltid == '0') {
        auto len = std::bitset<15>{bits.data(), 15}.to_ulong();
        bits = bits.substr(15);
        const auto end = bits.substr(len);
        std::list<packet> pkts;
        while (bits != end) {
            pkts.push_back(parse_bits(bits));
            bits = pkts.back().tail;
        }
        return {version, type_id, pkts, bits};
    }
    auto num_pkts = std::bitset<11>{bits.data(), 11}.to_ulong();
    bits = bits.substr(11);
    std::list<packet> pkts;
    for (size_t i = 0; i < num_pkts; ++i) {
        pkts.push_back(parse_bits(bits));
        bits = pkts.back().tail;
    }
    return {version, type_id, pkts, bits};
}

uint64_t version_sum(const packet& p) {
    uint64_t ver = p.version;
    if (const auto* pl = std::get_if<std::list<packet>>(&p.contents)) {
        ver += std::accumulate(
            pl->begin(), pl->end(), 0,
            [](auto x, const auto& p) { return x + version_sum(p); });
    }
    return ver;
}

uint64_t eval(const packet& p) {
    if (p.type_id == 4) {
        return std::get<0>(p.contents);
    }
    std::vector<uint64_t> args;
    std::ranges::transform(
        std::get<1>(p.contents),
        std::back_inserter(args),
        &eval);
    switch (p.type_id) {
        case 0: return std::accumulate(args.begin(), args.end(), 0ul);
        case 1: return std::accumulate(args.begin(), args.end(), 1ul, std::multiplies<uint64_t>{});
        case 2: return std::ranges::min(args);
        case 3: return std::ranges::max(args);
        case 5: assert(args.size() == 2); return args[0] > args[1];
        case 6: assert(args.size() == 2); return args[0] < args[1];
        case 7: assert(args.size() == 2); return args[0] == args[1];
        default: assert(false); break;
    }
    return 0;
}

int main()
{
    std::string line;
    *input(16) >> line;
    const auto pkt = parse_bits(to_bits(line));
    std::cout << version_sum(pkt) << "\n" << eval(pkt) << std::endl;
}
