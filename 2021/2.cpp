#include <fstream>
#include <iostream>

int main() {
    std::ifstream in{"2.txt"};
    std::string cmd;
    int arg;
    int position = 0;
    int depth1 = 0;
    int depth2 = 0;
    int aim = 0;
    while (in >> cmd >> arg) {
        if (cmd == "forward") {
            position += arg;
            depth2 += arg * aim;
        } else if (cmd == "up") {
            depth1 -= arg;
            aim -= arg;
        } else if (cmd == "down") {
            depth1 += arg;
            aim += arg;
        }
    }
    std::cout << position * depth1 << "\n" << position * depth2 << "\n";
}
