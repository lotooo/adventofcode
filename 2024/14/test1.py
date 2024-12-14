#!/usr/bin/env python3
import sys
import re

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


class Robot:
    def __init__(self, line):
        x, y, dx, dy = re.findall(r"-?\d+", line)
        self.x = int(x)
        self.y = int(y)
        self.dx = int(dx)
        self.dy = int(dy)

    @property
    def p(self):
        return (self.x, self.y)

    @property
    def v(self):
        return (self.dx, self.dy)

    def __repr__(self):
        return f"{self.p=} {self.v=}"

    def move(self):
        self.x += self.dx
        self.y += self.dy


class BathRoom(Grid2D):
    def __init__(self, robots, size_x=None, size_y=None):
        self.robots = robots
        if size_x is None and size_y is None:
            grid_max_x = 0
            grid_max_y = 0
            for r in robots:
                grid_max_x = max(grid_max_x, r.x)
                grid_max_y = max(grid_max_y, r.y)
        else:
            grid_max_x = size_x - 1
            grid_max_y = size_y - 1

        super().__init__(["." * (grid_max_x + 1)] * (grid_max_y + 1))

    def print(self):
        super().print([robot.p for robot in self.robots])

    def teleport(self):
        for r in self.robots:
            if r.x < 0:
                r.x = self.max_x + r.x
            if r.y < 0:
                r.y = self.max_y + r.y
            if r.x > self.max_x - 1:
                r.x = 0 + (r.x - self.max_x)
            if r.y > self.max_y - 1:
                r.y = 0 + (r.y - self.max_y)

    def wait(self):
        for r in self.robots:
            r.move()


def solve(data, move=100, bx=None, by=None):
    """Solve the puzzle and return the solution"""
    robots = []
    grid_max_x = 0
    grid_max_y = 0
    for robot in data:
        r = Robot(robot)
        grid_max_x = max(grid_max_x, r.x)
        grid_max_y = max(grid_max_y, r.y)
        robots.append(r)
    bathroom = BathRoom(robots, bx, by)
    for i in range(move):
        bathroom.wait()
        bathroom.teleport()
    if bathroom.max_x % 2 == 1:
        middle_x_index = bathroom.max_x // 2
    else:
        raise "Horiz length is odd"
    if bathroom.max_y % 2 == 1:
        middle_y_index = bathroom.max_y // 2
    else:
        raise "Horiz length is odd"

    q1 = [r for r in robots if r.x < middle_x_index and r.y < middle_y_index]
    q2 = [r for r in robots if r.x > middle_x_index and r.y < middle_y_index]
    q3 = [r for r in robots if r.x < middle_x_index and r.y > middle_y_index]
    q4 = [r for r in robots if r.x > middle_x_index and r.y > middle_y_index]

    return len(q1) * len(q2) * len(q3) * len(q4)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 12

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
