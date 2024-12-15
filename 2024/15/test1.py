#!/usr/bin/env python3
import sys
from itertools import takewhile, dropwhile

sys.path.append("../../")
from utils import Grid2D


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip()


class Warehouse(Grid2D):
    def __init__(self, data):
        super().__init__(data)

    @property
    def robot(self):
        return self.search("@")[0]

    def move(self, direction):
        x, y = self.robot
        if direction == "<":
            nexts = list(
                map(lambda c: self.value(c[0], c[1]), self.get_nexts(x, y, "L"))
            )
        if direction == ">":
            nexts = list(
                map(lambda c: self.value(c[0], c[1]), self.get_nexts(x, y, "R"))
            )
        if direction == "^":
            nexts = list(
                map(lambda c: self.value(c[0], c[1]), self.get_nexts(x, y, "U"))
            )
        if direction == "v":
            nexts = list(
                map(lambda c: self.value(c[0], c[1]), self.get_nexts(x, y, "D"))
            )
        filtered = list(takewhile(lambda x: x != "#", nexts))
        after_move = filtered.copy()
        has_moved = False
        if "." in filtered:
            after_move.remove(".")
            has_moved = True
        after_move.insert(0, "@")

        if direction == "<":
            new_line = []
            for i in range(x - len(filtered)):
                new_line.append(self.value(i, y))
            new_line.extend(reversed(after_move))
            if has_moved:
                new_line.append(".")
            for i in range(x, self.max_x):
                if i == x:
                    # It's where the robot were. Skip it
                    continue
                else:
                    new_line.append(self.value(i, y))
            self.grid[y] = "".join(new_line)
        if direction == "^":
            new_col = []
            for j in range(y - len(filtered)):
                new_col.append(self.value(x, j))
            new_col.extend(reversed(after_move))
            if has_moved:
                new_col.append(".")
            for j in range(y, self.max_y):
                if j == y:
                    # It's where the robot were. Skip it
                    continue
                else:
                    new_col.append(self.value(x, j))
            for y, value in enumerate(new_col):
                self.set_value(x, y, value)
        if direction == ">":
            new_line = []
            for i in range(x):
                new_line.append(self.value(i, y))
            if has_moved:
                new_line.append(".")
            new_line.extend(after_move)
            for i in range(len(new_line), self.max_x):
                new_line.append(self.value(i, y))
            self.grid[y] = "".join(new_line)
        if direction == "v":
            new_col = []
            for j in range(y):
                new_col.append(self.value(x, j))
            if has_moved:
                new_col.append(".")
            new_col.extend(after_move)
            for j in range(len(new_col), self.max_y):
                new_col.append(self.value(x, j))
            for y, value in enumerate(new_col):
                self.set_value(x, y, value)


def solve(data):
    """Solve the puzzle and return the solution"""
    wh_data = list(takewhile(lambda x: x.startswith("#"), data))
    warehouse = Warehouse(wh_data)
    moves = "".join(dropwhile(lambda x: x.startswith("#") or len(x) == 0, data))
    for move in list(moves):
        warehouse.move(move)
    return sum([b[0] + 100 * b[1] for b in warehouse.search("O")])


print("--> test small data <--")
test_input2 = load_data_from_file("test_input2")
assert solve(test_input2) == 2028

print("--> test larger data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 10092

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
