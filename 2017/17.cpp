#include <vector>
#include <algorithm>
#include <iostream>
#include <iomanip>

using namespace std;

int
spinlock (vector<int>& v, int steps, int rounds=2017)
{
  v.reserve (rounds);
  v.clear ();
  v.push_back (0);
  int pos = 0;
  for (int i = 0; i < rounds; ++i) {
    pos = (pos + steps) % v.size () + 1;
    v.emplace (v.begin () + pos, i + 1);
  }
  return pos;
}

int
spinlock_zero (int steps, int rounds)
{
  int pos = 0;
  int size = 1;
  int val = -1;
  for (int i = 0; i < rounds; ++i) {
    pos = (pos + steps) % size + 1;
    if (pos == 1) {
      val = i + 1;
    }
    ++size;
  }
  return val;
}

#define CATCH_CONFIG_MAIN

#include "catch.hpp"

TEST_CASE( "Examples", "[None]" ) {
  vector<int> v;
  int pos = spinlock (v, 3, 2017);
  REQUIRE (v[(pos + 1) % v.size()] == 638);
}

TEST_CASE ("Part 1", "[None]") {
  vector<int> v;
  int pos = spinlock (v, 329, 2017);
  cout << v[(pos + 1) % v.size ()] << endl;
}

TEST_CASE ("Part 2", "[None]") {
  cout << spinlock_zero (329, 50000000) << endl;
}

