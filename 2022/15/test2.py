#!/usr/bin/env python3
import re

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """

    temp_data = re.findall(r'(-?\d+)', x.strip())
    data = list(map(lambda x: int(x), temp_data))
    return ((data[0], data[1]), (data[2], data[3]))

class Sensor:
    def __init__(self, pos, closest_beacon):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

        self.closest_beacon = closest_beacon

        self.distance = abs(closest_beacon[0]-self.x)+abs(closest_beacon[1]-self.y) 
        self.vertical_edges = [ self.y - self.distance , self.y + self.distance ] 
        self.horiz_edges = [ self.x - self.distance , self.x + self.distance ] 

    def is_in_safe_zone(self,x,y):
        return abs(self.x-x)+abs(self.y-y) <= self.distance

    def get_next(self,x,y):
        return self.x + self.distance - abs(y-self.y) + 1

    def __repr__(self):
        return f"({self.x},{self.y})"


def solve(data, maxsize):
    """ Solve the puzzle and return the solution """
    zone = []
    for sensor, closest_beacon in data:
        s = Sensor(sensor,closest_beacon)
        zone.append(s)

    for row in range(0,maxsize+1):
        old=None
        x=0
        while x < maxsize+1:
            if old==(x,row):
                print(f"({x},{row})")
                return x*4000000+row
            old=(x,row)
            for sensor in zone:
                if sensor.is_in_safe_zone(x, row):
                    x = sensor.get_next(x,row)

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input, maxsize=20) == 56000011

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input, maxsize=4000000)}")
