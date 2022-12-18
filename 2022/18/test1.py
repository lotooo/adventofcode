#!/usr/bin/env python3
from itertools import product
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    p = list(map(lambda y:int(y), x.strip().split(',')))
    return (p[0], p[1], p[2])

def get_points(cube_start):
    x,y,z = cube_start[0], cube_start[1], cube_start[2]
    points = set()
    for px,py,pz in product((0,1), repeat=3):
        points.add((px+x,py+y,pz+z))
    return points

def solve(data):
    """ Solve the puzzle and return the solution """
    cubes = {}
    exposed_sides = {}
    for cube in data:
        points = get_points(cube)
        cubes[cube] = points
        exposed_sides[cube] = 6
    for cube, points in cubes.items():
        for tcube,tpoints in cubes.items():
            if cube == tcube:
                continue
            if len(cubes[cube] & cubes[tcube]) == 4:
                exposed_sides[cube] -= 1
    return sum(exposed_sides.values())

print("--> test data 1 <--")
assert solve([(1,1,1), (2,1,1)]) == 10

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 64

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
