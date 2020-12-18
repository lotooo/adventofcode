from collections import defaultdict
from itertools import product
import re

test_input = [
    '.#.',
    '..#',
    '###'
]

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

class Cube:
    def __init__(self,x,y,z,state="."):
        self.x = x
        self.y = y
        self.z = z
        self.state = state
        self.future_state = state

    def __str__(self):
        return self.state

    def __repr__(self):
        return f"z{self.z}_x{self.x}_y{self.y}_{self.state}"

    @property
    def is_active(self):
        return self.state == "#"

    def get_neighbors(self):
        neighbors = list(map(lambda prout: (prout[0]+self.x,prout[1]+self.y,prout[2]+self.z), product([0,1,-1],repeat=3)))
        neighbors.remove((self.x,self.y,self.z))
        return neighbors

class PocketDimension:
    def __init__(self,initial_state):
        self.initial_state = initial_state
        self.cubes = {}
        self.dimension = len(initial_state)
        for y,line in enumerate(initial_state):
            for x,state in enumerate(line):
                self.cubes[f"0_{x}_{y}"] = Cube(x,y,0,state)

    def get_cube(self,x,y,z):
        #if not f"{z}_{x}_{y}" in self.cubes:
        #    self.cubes[f"{z}_{x}_{y}"] = Cube(x,y,z)
        #return self.cubes[f"{z}_{x}_{y}"]
        if f"{z}_{x}_{y}" in self.cubes:
            return self.cubes[f"{z}_{x}_{y}"]
        else:
            return Cube(x,y,z)

    def __str__(self):
        prev_z = None
        prev_y = None
        for cube_key in sorted(self.cubes):
            m = re.match("(-?\d+)_(-?\d+)_(-?\d+)", cube_key)
            z = m.group(1)
            y = m.group(2)
            x = m.group(3)
            if z != prev_z:
                print("\n")
                print(f"z={z}")
                prev_z = z
            if y != prev_y:
                print("\n", end="")
                prev_y = y
            print(self.get_cube(x,y,z), end="")
        return "\n"

    @property
    def nb_active_cubes(self):
        return len([cube for cube in self.cubes.values() if cube.is_active ]) 

    def enlarge_my_dimension(self):
        for cube in [c for c in self.cubes.values()]:
            neighbors = cube.get_neighbors()
            for x,y,z in neighbors:
                if f"{z}_{x}_{y}" not in self.cubes: 
                    self.cubes[f"{z}_{x}_{y}"] = Cube(x,y,z)

    def apply(self):
        for cube in [c for c in self.cubes.values()]:
            cube.state = cube.future_state
            
    def cycle(self):
        self.enlarge_my_dimension()

        # Now let's check every cubes we have
        # And chec the state of their neighbors
        for cube in [c for c in self.cubes.values()]:
            active_neighbors = [ self.get_cube(x,y,z) for x,y,z in cube.get_neighbors() if self.get_cube(x,y,z).is_active ]
            if cube.is_active and not len(active_neighbors) in [2,3]:
                cube.future_state = "."
            if not cube.is_active and len(active_neighbors) == 3:
                cube.future_state = "#"

        self.apply()

pd = PocketDimension(my_input)
for i in range(0,6):
    pd.cycle()
print(pd.nb_active_cubes)

