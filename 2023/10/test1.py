#!/usr/bin/env python3
import sys


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = list(map(prepare_data, f.readlines()))
  return data


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def get_startup_tiles(sketch, x, y):
  """Find the 2 next tiles of our animal"""
  nexts = []
  if x >= 0 and x < len(sketch[0]):
    if sketch[y][x - 1] not in ["7", "|", "J", "."]:
      nexts.append((x - 1, y))
    if sketch[y][x + 1] not in ["L", "|", "F", "."]:
      nexts.append((x + 1, y))
  if y >= 0 and y < len(sketch):
    if sketch[y - 1][x] not in ["L", "-", "J", "."]:
      nexts.append((x, y - 1))
    if sketch[y + 1][x] not in ["7", "-", "F", "."]:
      nexts.append((x, y + 1))
  return nexts


def get_next_tile(sketch, x, y, previous):
  if sketch[y][x] == "|":
    tiles = [(x, y - 1), (x, y + 1)]
  if sketch[y][x] == "-":
    tiles = [(x - 1, y), (x + 1, y)]
  if sketch[y][x] == "L":
    # connecting north and east
    tiles = [(x, y - 1), (x + 1, y)]
  if sketch[y][x] == "J":
    # connecting north and west
    tiles = [(x, y - 1), (x - 1, y)]
  if sketch[y][x] == "7":
    # connect south and west
    tiles = [(x, y + 1), (x - 1, y)]
  if sketch[y][x] == "F":
    # connect south and east
    tiles = [(x, y + 1), (x + 1, y)]
  if sketch[y][x] == ".":
    # Ground. Problem ?
    print("GROUND. Weird no ?")
  if sketch[y][x] == "S":
    # Starting point. Problem ?
    print("STARTING. Weird no ?")
  valid_tiles = [
    tile for tile in tiles if tile != previous and tile[0] >= 0 and tile[1] >= 0
  ]
  return valid_tiles


def solve(sketch):
  """Solve the puzzle and return the solution"""
  # Find the starting point
  for y, line in enumerate(sketch):
    if "S" in line:
      x = line.index("S")
      break

  nexts = get_startup_tiles(sketch, x, y)
  follow1 = [(x, y), (nexts[0][0], nexts[0][1])]
  follow2 = [(x, y), (nexts[1][0], nexts[1][1])]

  f1_previous = (x, y)
  f1_x = nexts[0][0]
  f1_y = nexts[0][1]
  f2_previous = (x, y)
  f2_x = nexts[1][0]
  f2_y = nexts[1][1]

  done = False

  while not done:
    f1_n = get_next_tile(sketch, f1_x, f1_y, f1_previous)
    follow1.append(f1_n[0])
    f1_x = f1_n[0][0]
    f1_y = f1_n[0][1]
    f1_previous = follow1[-2]

    f2_n = get_next_tile(sketch, f2_x, f2_y, f2_previous)
    follow2.append(f2_n[0])
    f2_x = f2_n[0][0]
    f2_y = f2_n[0][1]
    f2_previous = follow2[-2]

    if (f1_x, f1_y) == (f2_x, f2_y):
      done = True
  return len(follow1) - 1


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 4

print("--> test data2 <--")
test_input = load_data_from_file("test_input2")
assert solve(test_input) == 8

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
