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
    def __init__(self, tile_path="", coord=None):
        self.WE, self.NWSE, self.SWNE = (0,0,0)
        self.is_black = False
        if coord:
            self.WE, self.NWSE, self.SWNE = coord
        else:
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
    def is_white(self):
        return not self.is_black
    
    @property
    def neighbors(self):
        return [
            (self.WE+W, self.NWSE, self.SWNE),
            (self.WE+E, self.NWSE, self.SWNE),
            (self.WE, self.NWSE+NW, self.SWNE),
            (self.WE, self.NWSE+SE, self.SWNE),
            (self.WE, self.NWSE, self.SWNE+SW),
            (self.WE, self.NWSE, self.SWNE+NE),
        ]

    @property
    def coord(self):
         return (self.WE, self.NWSE, self.SWNE)
    
    def flip(self):
        if self.is_black:
            self.is_black = False
        else:
            self.is_black = True

class Floor:
    def __init__(self, data):
        self.tiles = {}
        for tile in data:
            t = Tile(tile)
            if t.coord not in self.tiles:
                self.tiles[t.coord] = t
            self.tiles[t.coord].flip() 
    
    def get_tile(self,coord):
        if coord in self.tiles:
            tile = self.tiles[coord]
        else:
            # let's test if by any chance
            # The tile doesn't already exist
            # with our simplified coord
            tile = Tile(coord=coord)
            if tile.coord not in self.tiles:
                # This is really a new tile
                # Adding it to the floor for tomorrow
                self.next_day[tile.coord] = tile
            else:
                tile = self.tiles[tile.coord]
                print(f"I am {tile.coord} (from {coord}), I'm new and I'm {tile}")
        return tile
    
    def __str__(self):
        str_floor = ""
        for tile in self.tiles.values():
            str_floor += f"{tile.coord}: {tile}\n"
        return str_floor
            

    @property
    def black_tiles(self):
        return len([t for t in self.tiles.values() if t.is_black])

    def wait_24_hours(self):
        self.next_day = self.tiles.copy()
        for tile in self.tiles.values():
            print(f"I am {tile.coord} and my neighbors are {tile.neighbors}")
            print(f"I am {tile} and my neighbors are {[self.get_tile(t) for t in tile.neighbors]}")
            nb_black_neighbors = len(list(filter(lambda x: self.get_tile(x).is_black, tile.neighbors)))
            if tile.is_black and nb_black_neighbors in [0,3,4,5,6]:
                print(f"=> {tile} + {nb_black_neighbors} black neighbors")
                self.next_day[tile.coord].is_black = False
            if tile.is_white and nb_black_neighbors == 2:
                self.next_day[tile.coord].is_black = True
                print(f"=> {tile} + {nb_black_neighbors} black neighbors")
        self.tiles = self.next_day.copy()

def solve(data):
    floor = Floor(data)
    print(floor)
    print(f"day0: Found {floor.black_tiles} black tiles")
    for d in range(0,2):
        floor.wait_24_hours()
        print(f"day{d+1}: Found {floor.black_tiles} black tiles")
    return floor.black_tiles

print("--> test data <--")
test_input = load_data_from_file('2020/24/test_input')
assert solve(test_input) == 2208

print()
print("--> real data <--")
my_input = load_data_from_file('2020/24/input')
print(solve(my_input))
