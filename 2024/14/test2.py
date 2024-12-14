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


def solve(data):
    """Solve the puzzle and return the solution"""
    robots = []
    grid_max_x = 0
    grid_max_y = 0
    for robot in data:
        r = Robot(robot)
        grid_max_x = max(grid_max_x, r.x)
        grid_max_y = max(grid_max_y, r.y)
        robots.append(r)
    bathroom = BathRoom(robots)
    num_seconds = 1
    found = False
    while not found:
        if num_seconds % 500 == 1:
            print(f"{num_seconds=}")
        bathroom.wait()
        bathroom.teleport()

        # We "know" the tree won't be a full line
        # Let's search for 8 robots in a row to see
        # if it works
        robots = [r.p for r in bathroom.robots]
        for r in bathroom.robots:
            if (
                (r.x + 1, r.y) in robots
                and (r.x + 2, r.y) in robots
                and (r.x + 3, r.y) in robots
                and (r.x + 4, r.y) in robots
                and (r.x + 5, r.y) in robots
                and (r.x + 6, r.y) in robots
                and (r.x + 7, r.y) in robots
                and (r.x + 8, r.y) in robots
            ):
                print("<----------------------------->")
                print(f"Found in {num_seconds}")
                bathroom.print()
                print("<----------------------------->")
                found = True
                break
        if not found:
            num_seconds += 1
    bathroom.print()
    return num_seconds


print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
