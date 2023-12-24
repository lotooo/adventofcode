#!/usr/bin/env python3
import sys
from itertools import combinations

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return Line(x.strip())


class Line:
  def __init__(self, hailstone_data) -> None:
    self.hailsone, self.velocity = hailstone_data.split(" @ ")
    self.x, self.y, self.z = list(map(int, self.velocity.split(",")))
    self.hx, self.hy, self.hyz = list(map(int, self.hailsone.split(",")))
    self.m = self.y / self.x
    self.b = self.hy - (self.m * self.hx)

  def __str__(self):
    return f"y={self.m}*x+{self.b}"

  def is_parallel_with(self, line):
    return self.x * line.y - self.y * line.x == 0

  def intersection(self, line):
    ix = (self.b - line.b) / (line.m - self.m)
    iy = self.m * ix + self.b
    return (ix, iy)


def solve(data, test_min, test_max):
  """Solve the puzzle and return the solution"""
  working = 0
  for l1, l2 in combinations(data, 2):
    if not l1.is_parallel_with(l2):
      ix, iy = l1.intersection(l2)
      if ix < test_min or ix > test_max or iy < test_min or iy > test_max:
        # Intersection is NOT in the test field
        # Let's make sure intersection happens in the future though
        continue
      # Intersection is IN the test field
      # But let's make sure it didn't happen in the PAST
      if l1.x < 0 and ix > l1.hx:
        continue
      if l2.x < 0 and ix > l2.hx:
        continue
      if l1.x > 0 and ix < l1.hx:
        continue
      if l2.x > 0 and ix < l2.hx:
        continue
      if l1.y < 0 and iy > l1.hy:
        continue
      if l2.y < 0 and iy > l2.hy:
        continue
      if l1.y > 0 and iy < l1.hy:
        continue
      if l2.y > 0 and iy < l2.hy:
        continue
      working += 1
    else:
      continue
  return working


print("--> test data <--")

test_input = load_data_from_file("test_input")
assert solve(test_input, 7, 27) == 2

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input,200000000000000,400000000000000)}")
