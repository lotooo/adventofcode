#!/usr/bin/env python3
import re
from collections import defaultdict

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        #data = list(map(prepare_data, f.readlines()))
        raw_data = f.read()
    data = re.split(r'\n\n', raw_data)
    return (
        list(map(prepare_data, data[0].split('\n'))),
        list(map(prepare_fold, data[1].split('\n')[:-1])),
    )


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    coord = x.split(',')
    return (int(coord[0]), int(coord[1]))

def prepare_fold(x):
    """ transform the data the way we want it for the puzzle """
    data = x.split(' ')
    if len(data) > 1:
        return data[2].split('=')

class Paper:
    def __init__(self, points):
        x,y = zip(*points)
        self.x_size = max(x)+1
        self.y_size = max(y)+1

        self.paper = []
        for y in range(self.y_size):
            self.paper.append(self.x_size*'.')

        for x,y in points:
            old_version = list(self.paper[y])
            old_version[x] = '#'
            self.paper[y] = ''.join(old_version)

    def __str__(self):
        return '\n'.join(self.paper) + '\n'

    @property
    def count(self):
        count = 0
        for y in self.paper:
            for x in y:
                if x == '#':
                    count += 1
        return count

    def fold(self, fold):
        side, pos = fold
        if side == 'y':
            pos = int(pos)
            post_fold = pos * [self.x_size*'.']
            for y in range(0, pos):
                for x in range(0, self.x_size):
                    if self.paper[y][x] == "#" or self.paper[-(y+1)][x] == "#":
                        old_version = list(post_fold[y])
                        old_version[x] = '#'
                        post_fold[y] = ''.join(old_version)
            self.y_size = pos
        if side == 'x':
            pos = int(pos)
            post_fold = self.y_size * [pos*'.']
            for y in range(0, self.y_size):
                for x in range(0, pos):
                    if self.paper[y][x] == "#" or self.paper[y][-(x+1)] == "#":
                        old_version = list(post_fold[y])
                        old_version[x] = '#'
                        post_fold[y] = ''.join(old_version)
            self.x_size = pos
        self.paper = post_fold


def solve(data):
    """ Solve the puzzle and return the solution """
    points, folds = data
    p = Paper(points)
    print(p)

    #for fold in folds:
    #    p.fold(fold)
    #    print(p)
    p.fold(folds[0])

    print(p.count)
    return p.count


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 17

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
