#!/usr/bin/env python3
from queue import PriorityQueue, Queue
#import sys
#sys.setrecursionlimit(50000)

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
            #return 123 # the one after 'z'
            return ord('z') # the one after 'z'
        else:
            return ord(self.elevation)

    @property
    def neighboors(self):
        return [ e for e in [self.up, self.down, self.left, self.right] if e is not None and e.value <= self.value+1 ]

    def __str__(self):
        return f"{self.elevation}"

    def __repr__(self):
        return f"{self.elevation}"

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

    def search(self, start):
        paths = []
        #nodes_to_analyse = PriorityQueue() # Let's use a priority queue to try to analyse the shortest path first
        nodes_to_analyse = Queue() # Let's use a queue to finish some path
        nodes_to_analyse.put((0,[start]))
        visited = {}
        while not nodes_to_analyse.empty():
            mypath = nodes_to_analyse.get()[1]
            if len(paths) > 0:
                min_path_length = min(list(map(lambda x: len(x), paths)))
#                if len(mypath) > min_path_length:
#                    print("This path is longer than the one we already discovered")
#                    continue
            node = mypath[-1]
            if node.pos in visited and visited[node.pos] <= len(mypath):
                #print(f"Alreayd visited {node.pos} but distance ({len(mypath)}) is too high (current shortest: {visited[node.pos]}")
                continue
            else:
                visited[node.pos] = len(mypath)

            if node.elevation == "E":
                #print(f"Found 1 working path. Length: {len(mypath)}")
                paths.append(mypath)
            #for neighboor in [ node for node in node.neighboors if node.pos not in [m.pos for m in mypath]]:
            for neighboor in node.neighboors:
#                if neighboor.pos in visited and visited[neighboor.pos] < distance:
#                    continue
                tmp_path = mypath.copy()
                tmp_path.append(neighboor)
                #if tmp_path not in nodes_to_analyse:
                nodes_to_analyse.put((len(tmp_path), tmp_path))
                    #nodes_to_analyse.append(tmp_path)
        return paths

    def search_distance(self, start):
        paths = []
        nodes_to_analyse = PriorityQueue() # Let's use a priority queue to try to analyse the shortest path first
        nodes_to_analyse = Queue() # Let's use a Queue to try to finish some path first
        nodes_to_analyse.put((0,start))
        visited = {}
        min_distance = None
        while not nodes_to_analyse.empty():
            item = nodes_to_analyse.get()
            distance = item[0]
            node = item[1]
            if node.pos in visited and visited[node.pos] <= distance:
                continue
            else:
                visited[node.pos] = distance

            if node.elevation == "E":
                #print(f"Found 1 working path. Length: {distance}")
                if min_distance:
                    min_distance = min(min_distance, distance)
                else:
                    min_distance = distance
                paths.append(distance)
                continue
            else:
                for neighboor in node.neighboors:
                    if neighboor.pos in visited and visited[neighboor.pos] < distance:
                        continue
                    if min_distance:
                        if distance+1 < min_distance:
                            nodes_to_analyse.put((distance+1, neighboor))
                    else:
                        nodes_to_analyse.put((distance+1, neighboor))
        return paths


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
        for neighboor in sorted(element.neighboors, key=lambda x: x.value, reverse=True):
            if not visited[neighboor.pos]:
                visited[neighboor.pos] = True
                tmp_path = list(path) # Make a copy
                tmp_path.append(neighboor)
                pq.put(tmp_path)
    #print(''.join(list(map(lambda x: str(x), path))))
    #print(len(path))
    return len(path)



def solve(data):
    """ Solve the puzzle and return the solution """
    grid = Grid(data)
    print(f"Grid loaded")
    paths_distances = grid.search_distance(start=grid.start)
    solution1 = min(paths_distances) 
    print(f"{solution1=}")


    paths = grid.search(start=grid.start)
    paths_distances = list(map(lambda x: len(x), paths))
    solution2 = min(paths_distances)-1 # Remove S
    print(f"{solution2=}")

    solution3 = best_first_search(grid)-1 # Remove S
    print(f"{solution3=}")

    return solution1


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 31

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
