#!/usr/bin/env python3
from itertools import takewhile

def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip()


def extract_content(folder, content):
    data = []
    for element in content:
        if element.startswith('dir'):
            if folder == '/':
                data.append('/' + element.split()[1])
            else:
                data.append(folder + '/' + element.split()[1])
        else:
            data.append(int(element.split()[0]))
    return data


def is_still_analysing(myfs):
    for elements in myfs.values():
        if any(map(lambda x: type(x) == str, elements)):
            return True
    return False


def flatten(L):
    '''Flattens nested lists or tuples with non-string items'''
    for item in L:
        try:
            for i in flatten(item):
                yield i
        except TypeError:
            yield item


def analyse_fs(myfs):
    while is_still_analysing(myfs):
        temp_fs = myfs.copy()
        for folder, content in temp_fs.items():
            new_content = []
            for id, element in enumerate(content):
                if type(element) == str:
                    new_content.extend(myfs[element])
                else:
                    new_content.append(element)
            myfs[folder] = new_content
    filtered_folders = filter(lambda x: sum(x) < 100000, myfs.values())
    return sum(flatten(filtered_folders))


def solve(data):
    """ Solve the puzzle and return the solution """
    myfs = {}
    folder = ""
    for i, line in enumerate(data):
        if line.startswith('$ cd'):
            if line.split()[-1] == '..':
                folder = '/'.join(folder.split('/')[:-1])
                if folder == '':
                    # We can't go back more than /
                    folder = '/'
            else:
                if folder == "":
                    #folder = line.split()[-1]
                    folder = "/"
                elif folder == "/":
                    folder = '/' + line.split()[-1]
                else:
                    folder = folder + '/' + line.split()[-1]
        if line.startswith('$ ls'):
            content = takewhile(lambda x: not x.startswith("$"), data[i+1:])
            if folder not in myfs:
                myfs[folder] = extract_content(folder, content)
    return analyse_fs(myfs)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 95437

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
