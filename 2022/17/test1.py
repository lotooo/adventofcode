#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data

rocks = [
    ["@@@@"],
    ['.@.', '@@@', '.@.'],
    ['..@', '..@', '@@@'],
    ['@', '@', '@', '@'],
    ['@@','@@']
]

class Cave:
    def __init__(self, jets):
        self.jets = jets[0]
        #self.map = [ '-------' ]
        self.map = []
        self.i = 0

    def __str__(self):
        return '\n'.join(reversed([ f"{i:5}: {line}" for i, line in enumerate(self.map)])) + '\n'

    def add_rock(self, rock):
        self.map.append('.......')
        self.map.append('.......')
        self.map.append('.......')

        # Add the rock
        for line in reversed(rock):
            self.map.append(f"..{line}{'.'*(7-len(line)-2)}")

        rest = False
        while rest == False:
            move = self.jets[self.i % len(self.jets)]
            movable =  True
            lines_to_move = {}
            if move == ">":
                for y, line in enumerate(self.map):
                    if "@" in line:
                        first_pos = line.index("@")
                        last_pos = line.rindex("@")
                        if last_pos < len(line)-1 and line[last_pos+1] == '.':
                            lines_to_move[y] = line[:first_pos] + '.' + line[first_pos:last_pos+1] + line[last_pos+2:]
                            movable = movable & True
                        else:
                            movable = False
                if movable:
                    for index, new_line in lines_to_move.items():
                        self.map[index] = new_line
            if move == "<":
                for y, line in enumerate(self.map):
                    if "@" in line:
                        first_pos = line.index("@")
                        last_pos = line.rindex("@")
                        if first_pos > 0 and line[first_pos-1] == '.':
                            lines_to_move[y] = line[:first_pos-1] + line[first_pos:last_pos+1] + '.' + line[last_pos+1:]
                            movable = movable & True
                        else:
                            movable = False
                if movable:
                    for index, new_line in lines_to_move.items():
                        self.map[index] = new_line

            movable = True
            min_pos = 7 # init
            max_pos = 0 # init
            for y, line in enumerate(self.map):
                if "@" in line:
                    first_pos = line.index("@")
                    last_pos = line.rindex("@")
                    min_pos = min(min_pos, first_pos)
                    max_pos = max(max_pos, last_pos)
                    if y > 0 and not '#' in self.map[y-1][first_pos:last_pos+1]:
                        lines_to_move[y-1] = self.map[y-1][:min_pos] + line[min_pos:max_pos+1] + self.map[y-1][max_pos+1:]
                        lines_to_move[y] = self.map[y][:first_pos] + '.'*(last_pos-first_pos+1) + self.map[y][last_pos+1:]
                        movable = movable & True
                    else:
                        movable = False
                        rest = True
            if movable:
                for index, new_line in lines_to_move.items():
                    self.map[index] = new_line
            self.i+=1
        for y, line in enumerate(self.map):
            if "@" in line:
                self.map[y] = line.replace('@', '#')
        # Remove extra empty lines
        for line in self.map.copy():
            if not "#" in line:
                self.map.pop()

def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def solve(data):
    """ Solve the puzzle and return the solution """
    c = Cave(data)
    for i in range(2022):
        c.add_rock(rocks[i%len(rocks)])
    print(c)
    return len(c.map)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 3068

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
