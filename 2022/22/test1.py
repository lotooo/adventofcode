#!/usr/bin/env python3
import re
from time import sleep
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.rstrip()

symbol = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^'
}

class Map:
    def __init__(self, data):
        self.map = data
        self.drawn_map = data.copy()

        # Find start
        self.start = None
        for y,line in enumerate(data):
            for x, tile in enumerate(line):
                if tile == "." and not self.start:
                    self.start = (x,y)
                    break

        self.facing = 0
        self.x = self.start[0]
        self.y = self.start[1]

    @property
    def me(self):
        return (self.x, self.y)

    def turn(self, side):
        if side == 'R':
            self.facing = (self.facing+1)%4
        if side == 'L':
            self.facing = (self.facing-1)%4

    def move(self, distance):
        if self.facing == 0:
            # RIGHT
            for i in range(1, distance+1):
                try:
                    if self.map[self.y][self.x+1] == '#':
                        return
                    self.x+=1
                except IndexError:
                    # End of line
                    ind = self.map[self.y].index('.')
                    if self.map[self.y][ind] == '#':
                        return
                    self.x = ind
                self.drawn_map[self.y] = self.drawn_map[self.y][:self.x] + symbol[self.facing] + self.drawn_map[self.y][self.x+1:]
        if self.facing == 2:
            # LEFT
            for i in range(1, distance+1):
                # No index error on a string with negative indexes
                if self.x-1 >= 0:
                    if self.map[self.y][self.x-1] == '#':
                        return
                    if self.map[self.y][self.x-1] == ' ':
                        ind = len(self.map[self.y])-1
                        if self.map[self.y][ind] == '#':
                            return
                        self.x = ind
                        continue
                    self.x-=1
                else:
                    ind = len(self.map[self.y])-1
                    if self.map[self.y][ind] == '#':
                        return
                    self.x = ind
                self.drawn_map[self.y] = self.drawn_map[self.y][:self.x] + symbol[self.facing] + self.drawn_map[self.y][self.x+1:]
        if self.facing == 1:
            # DOWN
            for i in range(1, distance+1):
                try:
                    if self.map[self.y+1][self.x] == ' ':
                        line_found = False
                        my_y_ind = 0
                        while not line_found:
                            if self.map[my_y_ind][self.x] == ' ':
                                my_y_ind+=1
                            else:
                                line_found = True
                        if self.map[my_y_ind][self.x] == '#':
                            return
                        self.y = my_y_ind
                        continue
                    if self.map[self.y+1][self.x] == '#':
                        return
                    self.y+=1
                except IndexError:
                    line_found = False
                    my_y_ind = 0
                    while not line_found:
                        if self.map[my_y_ind][self.x] == ' ':
                            my_y_ind+=1
                        else:
                            line_found = True
                    if self.map[my_y_ind][self.x] == '#':
                        return
                    self.y = my_y_ind
                self.drawn_map[self.y] = self.drawn_map[self.y][:self.x] + symbol[self.facing] + self.drawn_map[self.y][self.x+1:]
        if self.facing == 3:
            # UP
            for i in range(1, distance+1):
                try:
                    if self.map[self.y-1][self.x] == '#':
                        return
                    self.y-=1
                except IndexError:
                    line_found = False
                    my_y_ind = len(self.map)-1
                    while not line_found:
                        if len(self.map[my_y_ind]) < self.x:
                            my_y_ind-=1
                            continue
                        if self.map[my_y_ind][self.x] == ' ':
                            my_y_ind-=1
                        else:
                            line_found = True
                    if self.map[my_y_ind][self.x] == '#':
                        return
                    self.y = my_y_ind
                self.drawn_map[self.y] = self.drawn_map[self.y][:self.x] + symbol[self.facing] + self.drawn_map[self.y][self.x+1:]

    def __str__(self):
        return '\n'.join(self.drawn_map)
    #return f"{self.me=}/{self.facing=}"

def solve(data):
    """ Solve the puzzle and return the solution """
    path = data.pop()
    # remove empty line
    data.pop() 
    m = Map(data)

    for move in re.split(r'(\d+)',path):
        if move == '':
            continue
        if move in ['L', 'R']:
            m.turn(move)
        else:
            m.move(int(move))
    return 1000 * (m.y+1) + 4 * (m.x+1) + m.facing


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 6032

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
