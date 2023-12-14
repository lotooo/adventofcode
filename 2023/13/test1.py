#!/usr/bin/env python3
import sys


def load_data_from_file(filename):
  """Load the input from a file and return the transformed version"""
  with open(filename, "r") as f:
    data = f.read()
  return list(map(prepare_data, data.split("\n\n")))


def prepare_data(x):
  """transform the data the way we want it for the puzzle"""
  return x.strip()


def get_mirror(puzzle):
  working = []
  offset = None
  for mirror_line in range(1, len(puzzle)):
    if puzzle[mirror_line - 1] == puzzle[mirror_line]:
      offset = 0
      while mirror_line - offset - 1 >= 0 and mirror_line + offset < len(puzzle):
        if puzzle[mirror_line - offset - 1] == puzzle[mirror_line + offset]:
          offset += 1
        else:
          offset = None
          break
    if offset and mirror_line != len(puzzle) - 1:
      working.append((mirror_line, offset))
  if len(working) > 0:
    return working[0]
  else:
    return (mirror_line, offset)


def rotate(puzzle):
  new_puzzle = []
  for x in range(len(puzzle[0])):
    new_line = ""
    for y in range(len(puzzle)):
      new_line += puzzle[y][x]
    new_puzzle.append(new_line)
  return new_puzzle


def solve(data):
  """Solve the puzzle and return the solution"""
  result = 0
  for puzzle in data:
    clean_puzzle = list(map(lambda x: x.strip(), puzzle.strip().split("\n")))
    rotated_puzzle = rotate(clean_puzzle)

    vertical_mirror = get_mirror(clean_puzzle)
    if vertical_mirror[1]:
      result += 100 * (vertical_mirror[0])

    horizontal_mirror = get_mirror(rotated_puzzle)
    if horizontal_mirror[1]:
      result += horizontal_mirror[0]

    if not horizontal_mirror[1] and not vertical_mirror[1]:
      raise "No mirror found"
  return result


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 405

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
