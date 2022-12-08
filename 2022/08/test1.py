#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def am_i_visible(x,y,trees):
    tree_height = int(trees[x][y])
    print(f"{tree_height=}")

    tree_line = list(trees[x])
    print(f"{tree_line=}")
    tree_column = [ line[y] for line in trees ]
    print(f"{tree_column=}")

    visible_from_left = not any(map(lambda h: int(h) >= tree_height, tree_line[0:y]))
    visible_from_right = not any(map(lambda h: int(h) >= tree_height, tree_line[y+1:]))
    visible_from_top = not any(map(lambda h: int(h) >= tree_height, tree_column[0:x]))
    visible_from_bottom = not any(map(lambda h: int(h) >= tree_height, tree_column[x+1:]))

    return visible_from_left or visible_from_right or visible_from_top or visible_from_bottom

def solve(data):
    """ Solve the puzzle and return the solution """
    # Count Edge trees as they are always visible
    edge_trees = len(data[0]) + len(data[-1]) + 2 * (len(data)-2)
    print(f"{edge_trees=}")

    visible_interior_tree = 0
    for x in range(1,len(data[0])-1):
        for y in range(1, len(data)-1):
            print(f"{x=},{y=}")
            if am_i_visible(x,y,data):
                visible_interior_tree+=1
    print(f"{visible_interior_tree=}")
    return visible_interior_tree + edge_trees


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 21

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
