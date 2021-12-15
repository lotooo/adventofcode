#!/usr/bin/env python3
import re

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
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

def empty_array(x,y):
    my_array = []
    line_tmp = []
    for i in range(0, x):
        line_tmp.append('.')
    for j in range(0, y):
        my_array.append(line_tmp.copy())
    return my_array

class Paper:
    def __init__(self, points):
        x,y = zip(*points)
        self.x_size = max(x)+1
        self.y_size = max(y)+1

        self.paper = empty_array(self.x_size, self.y_size)

        for x,y in points:
            self.paper[y][x] = '#'

    @property
    def count(self):
        count = 0
        for line in self.paper:
            for value in line:
                if value == '#':
                    count += 1
        return count


    def __str__(self):
        return '\n'.join(
                list(
                    map(lambda x: ''.join(x), self.paper)
                )
        )


    def fold(self, fold):
        side, pos = fold
        if side == 'y':
            post_fold = empty_array(self.x_size, int(pos))
            if self.y_size % 2 == 1:
                startup = 0
                offset=1
            else:
                startup = 1
                offset=0
            for y in range(startup, int(pos)):
                for x in range(self.x_size):
                    if self.paper[y][x] == "#" or self.paper[-(y+offset)][x] == "#":
                        post_fold[y][x] = '#'
            self.y_size = int(pos)
        if side == 'x':
            post_fold = empty_array(int(pos), self.y_size)
            if self.x_size % 2 == 1:
                startup = 0
                offset=1
            else:
                startup = 1
                offset=0
            for y in range(self.y_size):
                for x in range(startup,int(pos)):
                    if self.paper[y][x] == "#" or self.paper[y][-(x+offset)] == "#":
                        post_fold[y][x] = '#'
            self.x_size = int(pos)
        self.paper = post_fold


def solve(data):
    """ Solve the puzzle and return the solution """
    points, folds = data
    p = Paper(points)
    #print(f"Startup: {p.x_size} * {p.y_size}")
    #print(p)
    for fid, fold in enumerate(folds):
        #print(f"Size: {p.x_size} * {p.y_size}")
        #print(f"will fold at  {fold[0]} : {fold[1]}")
        p.fold(fold)
    print(p)
    return True


my_input = load_data_from_file('input')
solve(my_input)
