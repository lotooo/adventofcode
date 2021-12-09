#!/usr/bin/env python3
import sys
from functools import reduce

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


class bcolors:
    BLACK = '\u001b[30m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def solve(data):
    """ Solve the puzzle and return the solution """
    bassins = []
    lowpoints = []
    for line_id, line in enumerate(data): 
        for col_id, value in enumerate(line):
            # A 9 is not part of a basin
            if value == '9':
                continue
            # Now let's see if we are a lowpoint
            if line_id != 0:
                if int(data[line_id-1][col_id]) <= int(value):
                    continue
            if line_id != len(data)-1:
                if int(data[line_id+1][col_id]) <= int(value):
                    continue
            if col_id != 0:
                if int(data[line_id][col_id-1]) <= int(value):
                    continue
            if col_id != len(line)-1:
                if int(data[line_id][col_id+1]) <= int(value):
                    continue
            lowpoints.append((col_id,line_id))
     
    # We don't want to list every bassin
    # we want bassin starting from a lowpoint
    for lowpoint in lowpoints:
            cold_id,line_id = lowpoint
            bassin = [lowpoint]

            last_bassin_size = 0
            # Let's navigate every possible path for our bassin
            # until it stops growing
            while len(bassin) != last_bassin_size:
                last_bassin_size = len(bassin)
                for b in bassin:
                    col_id,line_id = b

                    if line_id != 0:
                        # Find bassin on top
                        x,y = col_id, line_id-1
                        end_of_bassin = False
                        while end_of_bassin == False:
                            if y >= 0 and data[y][x] != '9' and (x,y) not in bassin:
                                bassin.append((x,y))
                                y-=1
                            else:
                                end_of_bassin = True
                    if line_id != len(data)-1:
                        # Find bassin on bottom
                        x,y = col_id, line_id+1
                        end_of_bassin = False
                        while end_of_bassin == False:
                            if y < len(data) and data[y][x] != '9' and (x,y) not in bassin:
                                bassin.append((x,y))
                                y+=1
                            else:
                                end_of_bassin = True
                    if col_id != 0:
                        # Find bassin on left
                        x,y = col_id-1, line_id
                        end_of_bassin = False
                        while end_of_bassin == False:
                            if x >= 0 and data[y][x] != '9' and (x,y) not in bassin:
                                bassin.append((x,y))
                                x-=1
                            else:
                                end_of_bassin = True
                    if col_id != len(line)-1:
                        # Find bassin on right
                        x,y = col_id+1, line_id
                        end_of_bassin = False
                        while end_of_bassin == False:
                            if x < len(line) and data[y][x] != '9' and (x,y) not in bassin:
                                bassin.append((x,y))
                                x+=1
                            else:
                                end_of_bassin = True
            bassins.append(set(bassin))

    print(len(bassins))
    biggest_bassins = sorted(list(map(len,bassins)))[-3:]
    print(biggest_bassins)
    return reduce(lambda x,y: x*y, biggest_bassins)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 1134

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
