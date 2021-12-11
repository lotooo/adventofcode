#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return list(map(int,x.strip()))


class Octopuses:
    def __init__(self, octopuses):
        self.octopuses = octopuses
        self.flash = 0
        self.last_flash = 0
        self.flashed_octopuses = set()

    def cleanup(self):
        self.flashed_octopuses = set()
        for line_id, octopuses_line in enumerate(self.tmp_octopuses.copy()):
            for col_id, octopus in enumerate(octopuses_line):
                if octopus > 9:
                    self.tmp_octopuses[line_id][col_id] = 0
        self.octopuses = self.tmp_octopuses.copy()


    def __str__(self):
        """ print the state of our cavern """
        return '\n'.join(
                [''.join(list(map(str,octopus_line))) for octopus_line in self.octopuses ]
        )

    def gain_energy(self):
        self.tmp_octopuses = self.octopuses.copy()
        for line_id, octopuses_line in enumerate(self.tmp_octopuses):
            for col_id, octopus in enumerate(octopuses_line):
                self.tmp_octopuses[line_id][col_id] = octopus+1

    def bankai(self):
        # Let's scroll over the octopuses
        # Increase the light everywhere
        last_flash = None
        while len(self.flashed_octopuses) != last_flash:
            last_flash = len(self.flashed_octopuses)
            for line_id, octopuses_line in enumerate(self.tmp_octopuses.copy()):
                for col_id, octopus in enumerate(octopuses_line):
                    # Add our octopus to the list if it should flash but hasn't yet
                    if octopus > 9 and not (col_id,line_id) in self.flashed_octopuses:
                        self.flashed_octopuses.add((col_id,line_id))
                        # Add energy to the neighbors
                        if col_id != 0 and line_id != 0:
                            self.tmp_octopuses[line_id-1][col_id-1] += 1 
                        if line_id != 0:
                            self.tmp_octopuses[line_id-1][col_id] += 1 
                        if col_id != len(octopuses_line)-1 and line_id != 0:
                            self.tmp_octopuses[line_id-1][col_id+1] += 1 
                        if col_id != 0:
                            self.tmp_octopuses[line_id][col_id-1] += 1 
                        if col_id != len(octopuses_line)-1:
                            self.tmp_octopuses[line_id][col_id+1] += 1 
                        if col_id != 0 and line_id != len(self.tmp_octopuses)-1:
                            self.tmp_octopuses[line_id+1][col_id-1] += 1 
                        if line_id != len(self.tmp_octopuses)-1:
                            self.tmp_octopuses[line_id+1][col_id] += 1 
                        if col_id != len(octopuses_line)-1 and line_id != len(self.tmp_octopuses)-1:
                            self.tmp_octopuses[line_id+1][col_id+1] += 1 
        self.flash += len(self.flashed_octopuses)
        self.last_flash = len(self.flashed_octopuses)

def solve(data, iteration):
    """ Solve the puzzle and return the solution """
    o = Octopuses(data)
    i = 0
    print("before")
    print(o)
    print("")
    while o.last_flash != 100:
        o.gain_energy()
        o.bankai()
        o.cleanup()
        print(f"step {i}")
        print(o)
        print(f"-> {o.flash}")
        print("")
        i+=1
    print(i)
    return i


print("--> test data <--")
test_input = load_data_from_file('test_input')
#assert solve(test_input, 10) == 204
assert solve(test_input, 100) == 195

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input, 100)}")
