import re
from itertools import permutations,chain
from collections import Counter

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        raw_data = f.read()
    data = re.split(r'\n\n', raw_data)
    return data

class Tile:
    def __init__(self,init_data):
        data = init_data.split('\n')
        m = re.match(r"Tile (\d+):", data[0])
        if m:
            self.id = m.group(1)
        self.data = data[1:]

        if self.data[-1] == "":
            self.data.remove("")

        self.init_data = self.data

        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.moves = {
            "fliph": self.fliph,
            "flipv": self.flipv,
            "rotate": self.rotate
        }
    
    @property
    def possible_moves_combinations(self):
        possible_movements_combinations = list(
            chain(
                permutations(self.moves.keys(),1),
                permutations(self.moves.keys(),2),
                permutations(self.moves.keys(),3)
            )
        )
        return possible_movements_combinations

    def reset(self):
        self.data = self.init_data

    @property
    def sharps(self):
        sharps = Counter()
        for line in self.data:
            sharps.update(line)
        return sharps['#']

    @property
    def topline(self):
        return self.data[0]

    @property
    def bottomline(self):
        return self.data[-1]

    @property
    def leftcol(self):
        return ''.join(list(map(lambda x: x[0], self.data)))

    @property
    def rightcol(self):
        return ''.join(list(map(lambda x: x[-1], self.data)))

    def find_missing_neighbors(self,tiles):
        """ Find missing neighbors from the list of tiles with the good shape """
        for t in tiles:
            self.find_place(t)

    def __str__(self):
        for line in self.data:
            print(line)
        return ""

    def fliph(self):
        reverse_data = list(map(lambda x: x[::-1], self.data))
        self.data = reverse_data

    def flipv(self):
        tmp_data = list(self.data)
        tmp_data.reverse()
        self.data = tmp_data

    def rotate(self):
        tmp_data = [ ''.join(list(r)) for r in zip(*self.data[::-1]) ]
        self.data = tmp_data

    def curate(self):
        self.data.pop(0)
        self.data.pop()
        self.data = list(
            map(lambda x: x[1:len(x)-1],self.data)
        )

    def find_place(self,tile):
        found_neighbor = False
        if tile.leftcol == self.rightcol:
            self.right = tile
            tile.left = self
            found_neighbor = True
        if tile.rightcol == self.leftcol:
            self.left = tile
            tile.right = self
            found_neighbor = True
        if tile.topline == self.bottomline:
            self.bottom = tile
            tile.top = self
            found_neighbor = True
        if tile.bottomline == self.topline:
            self.top = tile
            tile.bottom = self
            found_neighbor = True
        return found_neighbor

class SatelliteImage:
    def __init__(self, tiles):
        self.tiles = tiles 
        self.data = self.get_full_picture()
        self.init_data = self.data
        self.moves = {
            "fliph": self.fliph,
            "flipv": self.flipv,
            "rotate": self.rotate
        }
    
    @property
    def possible_moves_combinations(self):
        possible_movements_combinations = list(
            chain(
                permutations(self.moves.keys(),1),
                permutations(self.moves.keys(),2),
                permutations(self.moves.keys(),3)
            )
        )
        return possible_movements_combinations

    def __str__(self):
        for line in self.data:
            print(line)
        return ""

    @property
    def first_col_tiles(self):
        col = []
        next_tile = self.top_left_corner_tile
        while next_tile:
            col.append(next_tile)
            next_tile = next_tile.bottom
        return col

    @property
    def top_left_corner_tile(self):
        return [ t for t in self.tiles if not t.top and not t.left and t.bottom and t.right ][0]

    @property
    def sharps_count(self):
        sharps = 0
        for tile in self.tiles:
            sharps += tile.sharps
        return sharps

    @property
    def corners(self):
        corners = set()
        for t in self.tiles:
            if not t.bottom and not t.left and t.right and t.top:
                corners.add(t.id)
            if not t.top and not t.left and t.bottom and t.right:
                corners.add(t.id)
            if not t.bottom and not t.right and t.top and t.left:
                corners.add(t.id)
            if not t.top and not t.right and t.bottom and t.left:
                corners.add(t.id)
        return corners

    def get_line(self, starting_tile):
        line = []
        next_tile = starting_tile
        while next_tile:
            line.append(next_tile)
            next_tile = next_tile.right
        return line

    def reset(self):
        self.data = self.init_data

    def rotate(self):
        tmp_data = [ ''.join(list(r)) for r in zip(*self.data[::-1]) ]
        self.data = tmp_data

    def fliph(self):
        reverse_data = list(map(lambda x: x[::-1], self.data))
        self.data = reverse_data

    def flipv(self):
        tmp_data = list(self.data)
        tmp_data.reverse()
        self.data = tmp_data

    def get_full_picture(self):
        """ 
        Convert an array of tiles in 1 array of string 
        to get the full picture and easily extract sea monsters pattern
        """
        full_picture = []
        for line in [self.get_line(l) for l in self.first_col_tiles]:
            for index in range(0,len(line[0].data)):
                my_line = ''.join(
                    list(
                        map(lambda x: x.data[index], line)
                    )
                 )
                full_picture.append(my_line)
        return full_picture

    def get_sea_monsters(self):
        sea_monster = [
          "xxxxxxxxxxxxxxxxxx#x",
          "#xxxx##xxxx##xxxx###",
          "x#xx#xx#xx#xx#xx#xxx"
        ]
        nb_sea_monsters = 0
        # The pattern seems be to be harder to find 
        # on line 1
        # Let's scan for that pattern and see if line 0 and line 2 
        # works too
        index_line = 1 
        while index_line < len(self.data)-1:
            index_col = 0
            while index_col < len(self.data[0])-len(sea_monster[0]):
                sub_str = self.data[index_line][index_col:index_col+len(sea_monster[0])]
                #sharps_pos = set([pos for pos, char in enumerate(sub_str) if char == '#'])
                #sea_monster_sharps_pos = set([pos for pos, char in enumerate(sea_monster[1]) if char == '#'])
                #if sea_monster_sharps_pos.issubset(sharps_pos):
                if compare_line_pattern(sub_str, sea_monster[1]):
                    # We found a matching pattern
                    # let's test the previous and next line
                    # to make sure it's a real
                    prev_sub_str = self.data[index_line-1][index_col:index_col+len(sea_monster[0])]
                    next_sub_str = self.data[index_line+1][index_col:index_col+len(sea_monster[2])]
                    if compare_line_pattern(prev_sub_str, sea_monster[0]) and compare_line_pattern(next_sub_str, sea_monster[2]):
                        nb_sea_monsters += 1
                index_col += 1
            index_line += 1
        return nb_sea_monsters
            
def compare_line_pattern(substr_satellite, substr_sea_monster):
    sat_sharps_pos = set([pos for pos, char in enumerate(substr_satellite) if char == '#'])
    monster_sharps_pos = set([pos for pos, char in enumerate(substr_sea_monster) if char == '#'])
    return monster_sharps_pos.issubset(sat_sharps_pos)

def place_tiles(unplaced_tiles):
    tiles = []
    i = 0
    while len(unplaced_tiles) > 0:
        try:
            tile = unplaced_tiles[i]
        except IndexError:
            i = 0
            tile = unplaced_tiles[i]
        
        t = Tile(tile)

        if len(tiles) == 0:
            # This is the first tile
            # there is not reason to find a neighbor

            # The code is ready if we need to rotate/flip 
            # the starter tile, but as we only need the corners
            # for step 1, it is not needed to move/rotate it
            # (as the other tiles will just rotate around the started tile)
            moves = t.possible_moves_combinations
            for m in moves[0]:
                t.moves[m]()

            tiles.append(t)
            unplaced_tiles.remove(tile)
            i+=1
            continue

        for placed_tile in tiles:
            t.reset()

            # Test without modification
            if placed_tile.find_place(t):
                tiles.append(t)
                unplaced_tiles.remove(tile)
                break

            found = False
            for moves in t.possible_moves_combinations:
                t.reset()
                for m in moves:
                    t.moves[m]()
                    if placed_tile.find_place(t):
                        tiles.append(t)
                        unplaced_tiles.remove(tile)
                        found = True
                        break
                if found:
                    break
            if found:
                break
        i+=1

    # We now have the perfect shape for every tile
    # And at least one link between each tiles
    # Let's fill up the blank now
    for tile in tiles:
        tile.find_missing_neighbors(tiles)
        
    return tiles

def get_sea_roughness(mydata):
    placed_tiles = place_tiles(mydata)
    for tile in placed_tiles:
        # Remove the borders of the tiles
        tile.curate()

    sat_image = SatelliteImage(placed_tiles)
    sea_monsters = sat_image.get_sea_monsters()

    if sea_monsters == 0:
        print(f"No sea monsters found. Moving the picture")
        for moves in sat_image.possible_moves_combinations:
            sat_image.reset()
            for m in moves:
                sat_image.moves[m]()
                sea_monsters = sat_image.get_sea_monsters()
                if sea_monsters > 0:
                    break
            if sea_monsters > 0:
                break
    print(f"Found {sat_image.sharps_count} sharps") 
    print(f"Found {sea_monsters} sea monsters") 
    return sat_image.sharps_count - sea_monsters * 15

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert get_sea_roughness(test_input) == 273
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"sea roughness: {get_sea_roughness(my_input)}")
