#!/usr/bin/env python3
from collections import Counter

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    p1,p2 = x.strip().split(' -> ')
    return (
            tuple(map(int,p1.split(','))), 
            tuple(map(int,p2.split(',')))
            )


class Vent:
    """ Define a vent line """
    def __init__(self, coords):
        p1, p2 = coords
        self.p1x = p1[0]
        self.p1y = p1[1]
        self.p2x = p2[0]
        self.p2y = p2[1]

    def __str__(self):
        return f"({self.p1x}, {self.p1y}) -> ({self.p2x},{self.p2y})"

    @property
    def is_horizontal(self):
        return self.p1y == self.p2y

    @property
    def is_vertical(self):
        return self.p1x == self.p2x

    @property
    def is_diagonal(self):
        return not self.is_horizontal and not self.is_vertical

    def dangerous_points(self):
        print(self)
        points = []
        if self.is_vertical or self.is_horizontal:
            for x in range(min(self.p1x,self.p2x), max(self.p1x,self.p2x)+1):
                for y in range(min(self.p1y,self.p2y), max(self.p1y,self.p2y)+1):
                    points.append((x,y))
        else:
            if self.p1x < self.p2x:
                x_increment = 1
            else:
                x_increment = -1
            if self.p1y < self.p2y:
                y_increment = 1
            else:
                y_increment = -1
            pos = (self.p1x, self.p1y)
            points.append(pos)
            while pos != (self.p2x, self.p2y):
                pos = (pos[0]+x_increment,pos[1]+y_increment)
                points.append(pos)

        return points

def solve(data):
    """ Solve the puzzle and return the solution """
    dangerous_points = []
    for vent_coord in data:
        v = Vent(vent_coord)
        dangerous_points.extend(v.dangerous_points())
    return len(list(filter(lambda x: x > 1, Counter(dangerous_points).values())))


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 12

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
