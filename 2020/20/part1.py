import re
from itertools import permutations,chain

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

def find_corners(tiles):
    corners = set()
    for t in tiles:
        if not t.bottom and not t.left and t.right and t.top:
            corners.add(t.id)
        if not t.top and not t.left and t.bottom and t.right:
            corners.add(t.id)
        if not t.bottom and not t.right and t.top and t.left:
            corners.add(t.id)
        if not t.top and not t.right and t.bottom and t.left:
            corners.add(t.id)
    return corners


def solve(unplaced_tiles):
    #tiles = {}
    tiles = []
    i = 0
    while len(unplaced_tiles) > 0:
        print(f"Remaining tiles: {len(unplaced_tiles)}")
        try:
            tile = unplaced_tiles[i]
        except IndexError:
            i = 0
            tile = unplaced_tiles[i]
        
        t = Tile(tile)

        if len(tiles) == 0:
            # This is the first tile
            # there is not reason to find a neighbor
            print(f"Taking tile {t.id} as starter")

            # The code is ready if we need to rotate/flip 
            # the starter tile, but as we only need the corners
            # for step 1, it is not needed to move/rotate it
            # (as the other tiles will just rotate around the started tile)
            moves = t.possible_moves_combinations
            for m in moves[0]:
                t.moves[m]()
            print(t)

            tiles.append(t)
            unplaced_tiles.remove(tile)
            i+=1
            continue

        # Let's try to find where we can put that tile
        print(f"Placing tile {t.id}")

        for placed_tile in tiles:
            t.reset()
            #print(f"Searching next to {placed_tile.id}")

            # Test without modification
            if placed_tile.find_place(t):
                #print("Done")
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
        
    corners = find_corners(tiles) 
    result = 1
    for i in corners:
        result *= int(i)
    return result


test_input = load_data_from_file('test_input')
assert solve(test_input) == 20899048083289

my_input = load_data_from_file('input')
print(solve(my_input))
