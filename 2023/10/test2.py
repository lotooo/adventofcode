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
  nexts2 = [
    (mx, my)
    for (mx, my) in [
      (x, y - 1),
      (x - 1, y),
      (x + 1, y),
      (x, y + 1),
    ]
    if sketch[my][mx] != "."
    and my >= 0
    and my < len(sketch)
    and mx >= 0
    and mx < len(sketch[0])
    and sketch[y][x - 1] not in ["7", "|", "J"]
    and sketch[y][x + 1] not in ["L", "|", "F"]
    and sketch[y - 1][x] not in ["L", "-", "J"]
    and sketch[y + 1][x] not in ["7", "-", "F"]
  ]
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
  valid_tiles = [
    tile for tile in tiles if tile != previous and tile[0] >= 0 and tile[1] >= 0
  ]
  return valid_tiles


def print_sketch(sketch, marked_tiles):
  for y, line in enumerate(sketch):
    for x, c in enumerate(line):
      if (x, y) in marked_tiles:
        print(f"\033[2;31;43m{c}\033[0;0m", end="")
      else:
        print(c, end="")
    print("\n", end="")


def solve(sketch):
  """Solve the puzzle and return the solution"""
  # First, extract the loop

  # Find the starting point
  for y, line in enumerate(sketch):
    if "S" in line:
      x = line.index("S")
      break
  nexts = get_startup_tiles(sketch, x, y)
  ax = nexts[0][0]
  ay = nexts[0][1]
  loop = [(x, y), (ax, ay)]
  previous = (x, y)
  done = False
  while not done:
    n = get_next_tile(sketch, ax, ay, previous)
    loop.append(n[0])
    ax = n[0][0]
    ay = n[0][1]
    previous = loop[-2]
    if sketch[ay][ax] == "S":
      done = True
  print(f"Loop:")
  print_sketch(sketch, loop)

  #  sketch[0].replace('.','O')
  #  sketch[-1].replace('.','O')
  #  for lid,line in enumerate(sketch.copy()):
  #    if line[0] == '.':
  #      sketch[lid] = 'O' + line[1:]
  #    if line[-1] == '.':
  #      sketch[lid] = line[:-1] + "O"

  last_outdoor = -1
  grounds = []
  double_pipes = []
  outdoor = []
  for y, line in enumerate(sketch):
    for x, c in enumerate(line):
      if (x, y) not in loop:
        grounds.append((x, y))
      if (x, y) in loop and c == "|":
        if x > 0 and (x - 1, y) in loop and sketch[y][x - 1] == "|":
          double_pipes.append((x, y))
        if x < len(sketch[0]) - 1 and (x + 1, y) in loop and sketch[y][x + 1] == "|":
          double_pipes.append((x, y))
      if (x, y) in loop and c == "-":
        if y > 0 and (x, y - 1) in loop and sketch[y - 1][x] == "-":
          double_pipes.append((x, y))
        if y < len(sketch[0]) - 1 and (x, y + 1) in loop and sketch[y + 1][x] == "-":
          double_pipes.append((x, y))
  print(f"Double pipes:")
  print_sketch(sketch, double_pipes)

  # Analyse doublepipes
  for x, y in double_pipes.copy():
    if y == 0 or y == len(sketch) - 1:
      outdoor.append((x, y))
      double_pipes.remove((x, y))
      continue
    if x == 0 or x == len(sketch[0]) - 1:
      outdoor.append((x, y))
      double_pipes.remove((x, y))
      continue
    neighboors = [
      (x - 1, y - 1),
      (x, y - 1),
      (x + 1, y - 1),
      (x - 1, y),
      (x + 1, y),
      (x - 1, y + 1),
      (x, y + 1),
      (x + 1, y + 1),
    ]
    for neighboor_x, neighboor_y in neighboors:
      if (neighboor_x, neighboor_y) in outdoor:
        outdoor.append((x, y))
        double_pipes.remove((x, y))
        break
  print(f"Outdoor double pipes:")
  print_sketch(sketch, double_pipes)
  print(f"Grounds:")
  print_sketch(sketch, grounds)

  while last_outdoor != len(outdoor):
    last_outdoor = len(outdoor)
    for x, y in grounds.copy():
      if y == 0 or y == len(sketch) - 1:
        outdoor.append((x, y))
        grounds.remove((x, y))
        continue
      if x == 0 or x == len(sketch[0]) - 1:
        outdoor.append((x, y))
        grounds.remove((x, y))
        continue
      neighboors = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
      ]
      for neighboor_x, neighboor_y in neighboors:
        if (neighboor_x, neighboor_y) in outdoor:
          outdoor.append((x, y))
          grounds.remove((x, y))
          break
  print(f"Result:")
  print_sketch(sketch, grounds)
  return len(grounds)


print("--> test data <--")
test_input = load_data_from_file("test_input_step2_1")
assert solve(test_input) == 4

print("--> test data2 <--")
test_input = load_data_from_file("test_input_step2_2")
assert solve(test_input) == 8

print("--> test data3 <--")
test_input = load_data_from_file("test_input_step2_3")
assert solve(test_input) == 10

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
