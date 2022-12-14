#!/usr/bin/env python3
from queue import PriorityQueue, Queue

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data

def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()

class Element:
    def __init__(self,elevation,x,y):
        self.elevation = elevation
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    @property
    def value(self):
        if self.elevation == 'S':
            return ord('a')
        elif self.elevation == 'E':
            return 123
        else:
            return ord(self.elevation)

    @property
    def neighboors(self):
        n = []
        return [ e for e in [self.up, self.down, self.left, self.right] if e is not None and e.value <= self.value+1 ]

    def __str__(self):
        return f"{self.elevation}"

    def __repr__(self):
        return f"{self.elevation}"

    def __lt__(self, other):
        return self.value >= other.value

class Grid:
    def __init__(self,grid):
        self.grid = {}
        self.max_y = len(grid)
        self.max_x = len(grid[0])
        for y, line in enumerate(grid):
            for x, elevation in enumerate(line):
                self.grid[(x,y)] = Element(elevation, x, y)
                if elevation == 'S':
                    self.start = self.grid[(x,y)]
        for y, line in enumerate(grid):
            for x, elevation in enumerate(line):
                if x == 0:
                    self.grid[(x,y)].left = None
                else:
                    self.grid[(x,y)].left = self.grid[(x-1),y]
                if x == self.max_x-1:
                    self.grid[(x,y)].right = None
                else:
                    self.grid[(x,y)].right = self.grid[(x+1),y]
                if y == 0:
                    self.grid[(x,y)].up = None
                else:
                    self.grid[(x,y)].up = self.grid[(x),y-1] 
                if y == self.max_y-1:
                    self.grid[(x,y)].down = None
                else:
                    self.grid[(x,y)].down = self.grid[(x),y+1]
        self.me = self.start

def best_first_search(grid):
    start = grid.start
    visited = { k: False for k,v in grid.grid.items() }
    pq = Queue()
    visited[start.pos] = True
    pq.put([start])

    while not pq.empty(): 
        path = pq.get()
        element = path[-1]
        if element.elevation == 'E':
            break
        for neighboor in element.neighboors:
            if not visited[neighboor.pos]:
                visited[neighboor.pos] = True
                tmp_path = list(path) # Make a copy
                tmp_path.append(neighboor)
                pq.put(tmp_path)
    print(len(path))
    return len(path)

def solve(data):
    """ Solve the puzzle and return the solution """
    grid = Grid(data)
    return best_first_search(grid)-1 # Remove S


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 31

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")