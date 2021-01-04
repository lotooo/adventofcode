from collections import Counter

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = [l.strip() for l in f.readlines() ]
    return data

E=1
W=-1
NE=1
SW=-1
SE=1
NW=-1

class Tile:
    def __init__(self, tile_path):
        self.WE = 0
        self.NWSE = 0
        self.SWNE = 0
        self.is_black = False
        i = 0

        while i < len(tile_path):
            read_direction = tile_path[i]
            if read_direction in ['n','s']:
                read_direction += tile_path[i+1]
                i+=2
            else:
                i+=1

            if read_direction == "e":
                self.WE += E
            elif read_direction == "w":
                self.WE += W
            elif read_direction == "se":
                self.NWSE += SE
            elif read_direction == "nw":
                self.NWSE += NW
            elif read_direction == "ne":
                self.SWNE += NE
            elif read_direction == "sw":
                self.SWNE += SW
            #self.tile_coord.update([read_direction])

        # Cleanup coord

        # e + nw => ne
        while self.WE >= E and self.NWSE <= NW:
            self.WE += W
            self.NWSE += SE

            self.SWNE += NE

        # e + sw => se
        while self.WE >= E and self.SWNE <= SW:
            self.WE += W
            self.SWNE += NE

            self.NWSE += SE

        # w + ne => nw
        while self.WE <= W and self.SWNE >= NE:
            self.WE += E
            self.NWSE += SW
            self.SWNE += NW

        # w + se => sw
        while self.WE <= W and self.NWSE >= SE:
            self.WE += E
            self.NWSE += NW

            self.SWNE += SW
        
        # ne + se => e
        while self.SWNE >= NE  and self.NWSE >= SE:
            self.SWNE += SW
            self.NWSE += NW

            self.WE += E

        # nw + sw => w
        while self.SWNE <= SW  and self.NWSE <= NW:
            self.NWSE += SE
            self.SWNE += NE

            self.WE += W

    def __str__(self):
        return "black" if self.is_black else "white"

    def __repr__(self):
        return "black" if self.is_black else "white"

    @property
    def coord(self):
         return (self.WE, self.NWSE, self.SWNE)
    
    def flip(self):
        if self.is_black:
            self.is_black = False
        else:
            self.is_black = True

def solve(data):
    tiles = {}
    print(f"Found {len(data)} tiles to flip")
    for tile in data:
        t = Tile(tile)
        if t.coord not in tiles:
            tiles[t.coord] = t
        tiles[t.coord].flip() 
    black_tiles = [t for t in tiles.values() if t.is_black]
    print(tiles)
    print(black_tiles)
    print(f"Found {len(black_tiles)} black tiles")
    return len(black_tiles)

print("--> test data <--")
test_input = load_data_from_file('2020/24/test_input')
assert solve(test_input) == 10

print()
print("--> real data <--")
my_input = load_data_from_file('2020/24/input')
print(solve(my_input))
