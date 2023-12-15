#!/usr/bin/env python3
import sys

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


def get_score(board):
  score = 0
  r = rotate_matrix(board)
  for col in r:
    score += sum([score + 1 for score, c in enumerate(reversed(col)) if c == "O"])
  return score


def solve(data):
  """Solve the puzzle and return the solution"""
  backup = []
  repeater = None
  iteration = 1000000000
  new_board = data
  for j in range(1, iteration + 1):
    for i in range(4):
      board = new_board
      new_board = []
      rotated = rotate_matrix(board)
      score = 0
      for column in rotated:
        new_column = []
        for block in column.split("#")[::-1]:
          # it might be stupid to reverse twice everything to properly count the load
          # Let's use the already reversed column
          new_column.append("".join(sorted(block)))
        new_board.append("#".join(new_column))
      for r in range(i % 4):
        new_board = rotate_matrix(new_board)[::-1]
      for r in range(i % 4):
        new_board = rotate_matrix(new_board)
    if new_board in backup:
      index = backup.index(new_board)
      if repeater == None:
        repeater = j - index - 1
        starter = j
        first_index = index
      break
    else:
      backup.append(new_board)
  myindex = ((iteration - starter) % (repeater)) + first_index
  score = get_score(backup[myindex])
  return score


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 64

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
