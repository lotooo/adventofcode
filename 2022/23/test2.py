#!/usr/bin/env python3
from itertools import product
from collections import defaultdict

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()

class Map:
    def __init__(self,data):
        self.map = data
        self.next = None
        self.move_proposal = None
        self.tests = [ self.test_north_proposal, self.test_south_proposal, self.test_west_proposal, self.test_east_proposal ]

    def __str__(self):
        return '\n'.join(self.map) + '\n'

    def save(self):
        if self.next:
            self.map = self.next.copy()
        self.next = None
        self.move_proposal = None
        # re-arrange tests order
        first_test = self.tests.pop(0)
        self.tests.append(first_test)

    def solve(self):
        # Let's resolv moves now
        for proposal, elves in self.move_proposal.items():
            if len(elves) > 1:
                continue
            source = elves.pop()
            self.next[source[1]] = self.next[source[1]][:source[0]] + '.' + self.next[source[1]][source[0]+1:]
            self.next[proposal[1]] = self.next[proposal[1]][:proposal[0]] + '#' + self.next[proposal[1]][proposal[0]+1:]

    @property
    def left_column(self):
        col = []
        for line in self.map:
            col.append(line[0])
        return col

    @property
    def right_column(self):
        col = []
        for line in self.map:
            col.append(line[-1])
        return col

    def test_north_proposal(self,x,y):
        # Test if we want to go north
        neighboors_values = [ self.next[y-1][x-1], self.next[y-1][x], self.next[y-1][x+1] ]
        if all(map(lambda x: x == '.', neighboors_values)):
            proposal = (x,y-1)
            return proposal
        return None

    def test_south_proposal(self,x,y):
        # Test if we want to go south
        neighboors_values = [ self.next[y+1][x-1], self.next[y+1][x], self.next[y+1][x+1] ]
        if all(map(lambda x: x == '.', neighboors_values)):
            proposal = (x,y+1)
            return proposal
        return None

    def test_west_proposal(self,x,y):
        # Test if we want to go west
        neighboors_values = [ self.next[y-1][x-1], self.next[y][x-1], self.next[y+1][x-1] ]
        if all(map(lambda x: x == '.', neighboors_values)):
            proposal = (x-1,y)
            return proposal
        return None

    def test_east_proposal(self,x,y):
        # Test if we want to go east
        neighboors_values = [ self.next[y-1][x+1], self.next[y][x+1], self.next[y+1][x+1] ]
        if all(map(lambda x: x == '.', neighboors_values)):
            proposal = (x+1,y)
            return proposal
        return None

    def prepare(self):
        self.next = self.map.copy()
        self.move_proposal = defaultdict(list)
        if "#" in self.left_column:
            for y, line in enumerate(self.next):
                self.next[y] = f".{line}"
        if "#" in self.right_column:
            for y, line in enumerate(self.next):
                self.next[y] = f"{line}."
        if "#" in self.map[0]:
            # Add a new line on North
            self.next.insert(0, '.' * len(self.next[0]))
        if "#" in self.map[-1]:
            # Add a new line on North
            self.next.append('.' * len(self.next[0]))
        self.map = self.next.copy()
        #print('\n'.join(self.next) + '\n')

        for y,line in enumerate(self.map):
            for x, point in enumerate(line):
                if point == "#":
                    #print(f"Found an Elf in ({x},{y})")

                    neighboors_coord = [ pos for pos in map(lambda n: (n[0]+x,n[1]+y), product((-1,0,1),repeat=2)) if pos != (x,y) ]
                    neighboors_values = map(lambda x: self.next[x[1]][x[0]], neighboors_coord)
                    if all(map(lambda x: x == '.', neighboors_values)):
                        # No elves around
                        # Don't move
                        #print("Nobody around. Not moving")
                        continue

                    for test in self.tests:
                        proposal = test(x,y)
                        if proposal:
                            self.move_proposal[proposal].append((x,y))
                            break

    def get_points(self):
        self.next = self.map.copy()
        if not "#" in self.left_column:
            for y, line in enumerate(self.map):
                self.next[y] = line[1:]
        if not "#" in self.right_column:
            for y, line in enumerate(self.next):
                self.next[y] = line[:-1]
        if not "#" in self.map[0]:
            self.next.pop(0)
        if not "#" in self.map[-1]:
            self.next.pop(-1)
        count = 0
        for line in self.next:
            for p in line:
                if p == '.':
                    count+=1
        return count

def solve(data):
    """ Solve the puzzle and return the solution """
    m = Map(data)
    last = None
    i = 1
    while last != m.map:
        last = m.map
        m.prepare()
        m.solve()
        m.save()
        if last == m.map:
            print(f"Nothing changed. Round {i}")
            break
        i+=1
    print(i)
    return i

#print("--> test data2 <--")
#test_input2 = load_data_from_file('test_input2')
#assert solve(test_input2) == 20

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
