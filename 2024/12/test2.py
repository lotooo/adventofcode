#!/usr/bin/env python3
import sys
from itertools import combinations

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

    @property
    def edges(self):
        edges = set()
        for cell in self.cells:
            x, y = cell
            # is it a top edge ?
            if (x, y - 1) not in self.cells:
                edges.add((x, y - 1, "U"))
            # is it a bottom edge ?
            if (x, y + 1) not in self.cells:
                edges.add((x, y + 1, "D"))
            # is it a left edge ?
            if (x - 1, y) not in self.cells:
                edges.add((x - 1, y, "L"))
            # is it a right edge ?
            if (x + 1, y) not in self.cells:
                edges.add((x + 1, y, "R"))
        return sorted(list(edges), key=lambda x: (x[2], x[0], x[1]))

    @property
    def sides(self):
        # Let's find connected edges (facing same direction)
        visited = set()
        sides = 0

        def find_sides(edge_node):
            x, y, orientation = edge_node
            current = edge_node
            visited.add(current)
            this_side = [current]
            for direction in [-1, 1]:
                while True:
                    if orientation in ["U", "D"]:
                        nx = x + direction
                        ny = y
                        next = (nx, ny, orientation)
                    else:  # "L" or "R"
                        nx = x
                        ny = y + direction
                        next = (nx, ny, orientation)
                    if next in self.edges and next not in visited:
                        current = next
                        x, y, orientation = current
                        visited.add(current)
                        this_side.append(current)
                    else:
                        break

        for edge in self.edges:
            if edge not in visited:
                find_sides(edge)
                sides += 1

        return sides

    def __repr__(self):
        return f"{self.value}/area:{self.area}/sides:{self.sides}"


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
    costs = [z.sides * z.area for z in zones]
    return sum(costs)


print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 80
test_input2 = load_data_from_file("test_input2")
assert solve(test_input2) == 436
test_input4 = load_data_from_file("test_input4")
assert solve(test_input4) == 236
test_input5 = load_data_from_file("test_input5")
assert solve(test_input5) == 368
test_input3 = load_data_from_file("test_input3")
assert solve(test_input3) == 1206

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
