#!/usr/bin/python
'''
Advent of Code[About][AoC++][Events][Settings][Log Out]Bklyn 38*
   sub y{2016}[Calendar][Leaderboard][Stats][Sponsors]
Our sponsors help make AoC possible:
Infi - Fvzcry gbpu? Xbz arkg-yriry glcra va Hgerpug bc baf areqxjnegvre!

--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later. However, the corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written as plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7
The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed. Then, the only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that is not blocked?

To begin, get your puzzle input.
'''

with open('20.txt') as f:
    segments = []
    for line in f:
        line = line.strip()
        low, hi = map (int, line.split ('-'))
        segments.append ((low, hi))
    reduced = []
    prevlow, prevhi = -1, -1
    allowed = 0
    for low, hi in sorted (segments):
        if not reduced or low > prevhi + 1:
            reduced.append ((low, hi))
            allowed += low - prevhi - 1
            print (prevlow, prevhi), (low, hi), low - prevhi - 1, allowed
            prevlow, prevhi = low, hi
        else:
            reduced[-1] = (prevlow, max (hi, prevhi))
            prevhi = max (hi, prevhi)
    first = reduced[0]
    allowed += 0xffffffff - reduced[-1][1]
    if first[0] > 0:
        print 0
    else:
        print first[1] + 1
    print allowed
