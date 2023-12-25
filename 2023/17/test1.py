#!/usr/bin/env python3
import sys
from heapq import heappush, heappop

sys.path.append("../../")
from utils import *


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def get_next(heat, direction, position, grid):
  x, y = position
  if heat is None:
    heat = 0
  else:
    heat += int(grid[y][x])
  if direction[-1] == ">":
    nexts = []
    if y > 0:
      nexts.append((heat, "^", (x, y - 1)))
    if y < len(grid) - 1:
      nexts.append((heat, "v", (x, y + 1)))
    if x < len(grid[0]) - 1 and direction[-3:] != ">>>":
      nexts.append((heat, direction + ">", (x + 1, y)))
    return nexts
  if direction[-1] == "<":
    nexts = []
    if y > 0:
      nexts.append((heat, "^", (x, y - 1)))
    if y < len(grid) - 1:
      nexts.append((heat, "v", (x, y + 1)))
    if x > 0 and direction[-3:] != "<<<":
      nexts.append((heat, direction + ">", (x - 1, y)))
    return nexts
  if direction[-1] == "^":
    nexts = []
    if x > 0:
      nexts.append((heat, "<", (x - 1, y)))
    if x < len(grid[0]) - 1:
      nexts.append((heat, ">", (x + 1, y)))
    if y > 0 and direction[-3:] != "^^^":
      nexts.append((heat, direction + "^", (x, y - 1)))
    return nexts
  if direction[-1] == "v":
    nexts = []
    if x > 0:
      nexts.append((heat, "<", (x - 1, y)))
    if x < len(grid[0]) - 1:
      nexts.append((heat, ">", (x + 1, y)))
    if y < len(grid) - 1 and direction[-3:] != "vvv":
      nexts.append((heat, direction + "v", (x, y + 1)))
    return nexts
  if direction[-1] == "?":
    nexts = []
    if x > 0:
      nexts.append((heat, "<", (x - 1, y)))
    if x < len(grid[0]) - 1:
      nexts.append((heat, ">", (x + 1, y)))
    if y < len(grid) - 1:
      nexts.append((heat, "v", (x, y + 1)))
    if y > 0:
      nexts.append((heat, "^", (x, y - 1)))
    return nexts
  raise "WTF am I supposed to do ?"


def solve(data):
  """Solve the puzzle and return the solution"""
  minimum_heat_loss = 9 * len(data) + 9 * len(data[0]) - 9
  print(f"{minimum_heat_loss=}")
  start = (0, 0)
  final = (len(data[0]) - 1, len(data) - 1)
  processed = {}
  to_be_processed = []
  heappush(to_be_processed, (None, "?", start))
  while len(to_be_processed) > 0:
    # node = to_be_processed.pop()
    node = heappop(to_be_processed)
    sum_heat_loss, direction, position = node
    if (direction, position) in processed:
      if sum_heat_loss >= processed[(direction, position)]:
        continue
    processed[(direction, position)] = sum_heat_loss
    if sum_heat_loss is not None and sum_heat_loss >= minimum_heat_loss:
      # STOP !
      continue
    if position == final:
      print(f"Found path to {position}: {minimum_heat_loss=}/{sum_heat_loss=}")
      minimum_heat_loss = min(sum_heat_loss, minimum_heat_loss)
    else:
      nexts = get_next(*node, data)
      for n in nexts:
        # to_be_processed.append(n)
        heappush(to_be_processed, n)
  final_heat_loss = int(data[-1][-1])
  print(f"{final_heat_loss=}")
  print(f"{minimum_heat_loss=}")
  return minimum_heat_loss + final_heat_loss


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert get_next(None, ">", (0, 0), test_input) == [(0, "v", (0, 1)), (0, ">>", (1, 0))]
assert solve(test_input) == 102

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
