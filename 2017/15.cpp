#include <iostream>
#include <limits.h>

int
GenA (unsigned long seed)
{
    return (seed * 16807ul) % INT_MAX;
}

int
GenA2 (unsigned long seed)
{
    do {
        seed = (seed * 16807ul) % INT_MAX;
    } while (seed & 0x3);
    return seed;
}

int
GenB (unsigned long seed)
{
    return (seed * 48271ul) % INT_MAX;
}

int
GenB2 (unsigned long seed)
{
    do {
        seed = (seed * 48271ul) % INT_MAX;
    } while (seed & 0x7);
    return seed;
}

int
main ()
{
    int count = 0;
    int a = 699, b = 124;
    for (int i = 0; i < 40000000; ++i) {
        a = GenA (a);
        b = GenB (b);
        if ((a & USHRT_MAX) == (b & USHRT_MAX)) {
            ++count;
        }
    }
    printf ("%d\n", count);

    count = 0;
    a = 699, b = 124;
    for (int i = 0; i < 5000000; ++i) {
        a = GenA2 (a);
        b = GenB2 (b);
        if ((a & USHRT_MAX) == (b & USHRT_MAX)) {
            ++count;
        }
    }
    printf ("%d\n", count);
}
