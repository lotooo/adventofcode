#!/usr/bin/env python3
import sys

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


class Zone:
    def __init__(self, value):
        self.value = value
        self.cells = []

    def add(self, cell):
        if cell not in self.cells:
            self.cells.append(cell)

    @property
    def area(self):
        return len(self.cells)

    @property
    def perimeter(self):
        perimeters = []
        for cell in self.cells:
            cell_perimeter = 4
            x, y = cell
            for neighboor in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if neighboor in self.cells:
                    cell_perimeter -= 1
            perimeters.append(cell_perimeter)
        return sum(perimeters)

    def __repr__(self):
        return f"{self.value}/area:{self.area}/perimeter:{self.perimeter}"


class MyGrid2D(Grid2D):
    def __init__(self, grid):
        super().__init__(grid)

    def get_zone(self, cell):
        x, y = cell
        zone = Zone(self.value(x, y))
        zone.add(cell)
        to_process = (
            self.get_horizontal_neighboors(x, y, 1)
            + self.get_horizontal_neighboors(x, y, -1)
            + self.get_vertical_neighboors(x, y, 1)
            + self.get_vertical_neighboors(x, y, -1)
        )
        while len(to_process) > 0:
            tested_cell = to_process.pop()
            tx, ty = tested_cell
            if self.value(tx, ty) == zone.value:
                zone.add(tested_cell)
                for n in (
                    self.get_horizontal_neighboors(tx, ty, 1)
                    + self.get_horizontal_neighboors(tx, ty, -1)
                    + self.get_vertical_neighboors(tx, ty, 1)
                    + self.get_vertical_neighboors(tx, ty, -1)
                ):
                    if n not in zone.cells:
                        to_process.append(n)
        return zone


def solve(data):
    """Solve the puzzle and return the solution"""
    g = MyGrid2D(data)
    to_process = g.cells
    zones = []
    while len(to_process) > 0:
        cell = to_process.pop()
        z = g.get_zone(cell)
        for c in [tc for tc in z.cells if tc != cell and tc in to_process]:
            to_process.remove(c)
        zones.append(z)
    costs = [z.perimeter * z.area for z in zones]
    return sum(costs)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 140
test_input2 = load_data_from_file("test_input2")
assert solve(test_input2) == 772
test_input3 = load_data_from_file("test_input3")
assert solve(test_input3) == 1930

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
