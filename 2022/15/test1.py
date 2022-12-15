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

    def get_safe_zone(self, row):
        no_beacon_range = set(range(self.x - (self.distance - abs(row - self.y)), self.x + (self.distance - abs(row - self.y))+1))
        if self.closest_beacon[1] == row:
            no_beacon_range.remove(self.closest_beacon[0])
        return no_beacon_range

    def __repr__(self):
        return f"({self.x},{self.y})"


def solve(data, row):
    """ Solve the puzzle and return the solution """
    zone = []
    for sensor, closest_beacon in data:
        s = Sensor(sensor,closest_beacon)
        if row > s.vertical_edges[0] and row < s.vertical_edges[1]:
            zone.append(s)
    safe_zone = set()
    for sensor in zone:
        local_safezone = sensor.get_safe_zone(row)
        if len(local_safezone) > 0:
            safe_zone = safe_zone.union(local_safezone)
    return len(safe_zone)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input, row=10) == 26

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input, row=2000000)}")
