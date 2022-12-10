#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def solve(data):
    """ Solve the puzzle and return the solution """
    signal_strength = {}
    register = 1
    cycle = 1
    for op in data:
        if op == "noop":
            signal_strength[cycle] = register
            cycle+=1
            continue
        signal_strength[cycle] = register
        signal_strength[cycle+1] = register
        register += int(op.split()[1])
        signal_strength[cycle+2] = register
        cycle+=2

    out = []
    line = ""
    for index, register in signal_strength.items():
        if index % 40 == 1:
            out.append(line)
            line = ""
        if index % 40 - 1 in [register-1, register, register+1]:
            line += "#"
        else:
            line += "."
    # Add the last line
    out.append(line)
    print('\n'.join(out))
    return True


print("--> test data <--")
test_input = load_data_from_file('test_input')
solve(test_input)

print()
print("--> real data <--")
my_input = load_data_from_file('input')
solve(my_input)
