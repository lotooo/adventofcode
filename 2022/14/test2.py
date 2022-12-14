#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return list(map(lambda y: y.split(','), x.strip().split(' -> ')))

def get_rocks(line):
    rocks = []
    for i in range(len(line)-1):
        startx = int(line[i][0])
        starty = int(line[i][1])
        endx = int(line[i+1][0])
        endy = int(line[i+1][1])

        stepx = -1 if startx > endx else 1
        stepy = -1 if starty > endy else 1

        for x in range(startx, endx+stepx,stepx):
            for y in range(starty, endy+stepy,stepy):
                rocks.append((x,y))
    return rocks

SANDSOURCE = (500,0)

class Cavemap:
    def __init__(self, data):
        self.cavemap = {}
        self.cavemap[SANDSOURCE] = '+'
        for line in data:
            for r in get_rocks(line):
                self.cavemap[r] = '#'

        self.infinite_sandfall = False

        keys = self.cavemap.keys()
        keysx = [ point[0] for point in keys ]
        keysy = [ point[1] for point in keys ]
        self.maxx = max(keysx)
        self.maxy = max(keysy)
        self.minx = min(keysx)
        self.miny = min(keysy)

        # Add a bottom line
        for x in range(SANDSOURCE[0]-2*self.maxy,SANDSOURCE[0]+2*self.maxy):
            self.cavemap[(x,self.maxy+2)] = "#"

        keys = self.cavemap.keys()
        keysx = [ point[0] for point in keys ]
        keysy = [ point[1] for point in keys ]
        self.maxx = max(keysx)
        self.maxy = max(keysy)
        self.minx = min(keysx)
        self.miny = min(keysy)

        self.sand = 0

    def __str__(self):
        out = ""
        for y in range(self.miny, self.maxy+1):
            #out += f"{y=} "
            for x in range(self.minx,self.maxx+1):
                try:
                    out += self.cavemap[(x,y)]
                except KeyError:
                    out += '.'
            out+='\n'
        return out

    def find_candidate(self, x,y):
        for y in range(y, self.maxy+1):
            if (x, y) in self.cavemap:
                if self.cavemap[(x,y)] in ["#", "o"]:
                    if (x-1, y) in self.cavemap and (x+1, y) in self.cavemap:
                        return (x,y-1)
                    elif not (x-1, y) in self.cavemap:
                        return self.find_candidate(x-1, y)
                    elif not (x+1, y) in self.cavemap: 
                        return self.find_candidate(x+1, y)
        return None

    def add_sand(self, sandsource):
        candidate = self.find_candidate(sandsource[0], sandsource[1])
        if candidate:
            self.cavemap[(candidate[0],candidate[1])] = "o"
            self.sand += 1
            self.infinite_sandfall = False
            return True
        self.infinite_sandfall = True
        return False

def solve(data):
    """ Solve the puzzle and return the solution """
    cavemap = Cavemap(data)
    #print(cavemap)
    while cavemap.cavemap[(SANDSOURCE[0],SANDSOURCE[1])] == '+':
        cavemap.add_sand(SANDSOURCE)
        #print(cavemap)
    return cavemap.sand


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 93

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
