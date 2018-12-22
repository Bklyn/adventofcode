#include <stdio.h>
#include <limits.h>

#include <set>

int a=0, b=0, c=0, d=0, e=0, f=0;
std::set<int> seen;

void machine()
{
    long insns = 0;

#include "machine.c"
    return;
}

int
main ()
{
    a = 0; // 2525738;
    machine ();
    printf ("RESULT: %d\n", b);
    // a = 11316540;
    a = 1; b = c = d = e = f = 0;
    machine();
    printf ("RESULT: %d\n", b);
}

