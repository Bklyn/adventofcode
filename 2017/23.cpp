#include <iostream>
#include <cstdio>
#include <cassert>

using namespace std;

#define DUMP printf ("LINE=%d a=%ld b=%ld c=%ld d=%ld e=%ld f=%ld g=%ld h=%ld " \
                     "jumps1=%lu jumps2=%lu\n",                         \
                     __LINE__, a,b,c,d,e,f,g,h, jumps1, jumps2);

/*
 1 set b 65
 2 set c b
 3 jnz a 2
 4 jnz 1 5
 5 mul b 100
 6 sub b -100000
 7 set c b
 8 sub c -17000
 9 set f 1
10 set d 2
11 set e 2
12 set g d
13 mul g e
14 sub g b
15 jnz g 2
16 set f 0
17 sub e -1
18 set g e
19 sub g b
20 jnz g -8
21 sub d -1
22 set g d
23 sub g b
24 jnz g -13
25 jnz f 2
26 sub h -1
27 set g b
28 sub g c
29 jnz g 2
30 jnz 1 3
31 sub b -17
32 32 jnz 1 -23
*/
int
prog (long a=1)
{
    long b=0, c=0, d=0, e=0, f=0, g=0, h=0;
    b = 65;
    c = b;
    if (a != 0) {
        b *= 100;
        b += 100000;
        c = b + 17000;
    }
    size_t jumps1 = 0, jumps2 = 0;
    while (true) {
        f = 1;
        d = 2;
      line11:
        e = 2;
      line12:
        if (d * e == b) {
            DUMP;
            f = 0;
            d = e = b;
            goto done;
        }
        // 17: e++
        // 18-19: g = e-b
        // 20: if (g != 0) goto 12
        if (++e != b) {
            ++jumps1;
            goto line12;
        }
        // ASSERT: e == b
        if (++d != b) {
            ++jumps2;
            goto line11;
        }
        // ASSERT: d == e == b
      done:
        if (f == 0) {
            ++h;
            DUMP;
        } else {
            DUMP;
        }
        if (b == c) {
            break;
        }
        b += 17;
        DUMP;
    }
    return h;
}

int
main ()
{
    cout << prog (1) << endl;
}
