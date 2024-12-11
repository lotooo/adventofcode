#!/usr/bin/env python3
import sys

sys.path.append("../../")


def load_data_from_file(filename):
    """Load the input from a file and return the transformed version"""
    with open(filename, "r") as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """transform the data the way we want it for the puzzle"""
    return x.strip()


class FS:
    def __init__(self, string):
        """Extract file from compressed string"""
        out = []
        i = 0
        while i < len(string):
            if i % 2 == 0:
                out.append((str(int(i / 2)), int(string[i])))
            else:
                if int(string[i]) != 0:
                    out.append((".", int(string[i])))
            i += 1
        self.fs = out

    def __str__(self):
        out = ""
        for block in self.fs:
            out += block[0] * block[1]
        return out

    @property
    def files(self):
        return [block for block in self.fs if block[0] != "."]

    @property
    def spaces(self):
        return [block for block in self.fs if block[0] == "."]

    def move(self, file_block):
        processing = self.fs.copy()
        moved = False
        # I guess I could use an index instead
        # of a loop from the end
        # but I'm not sure the files are really unique
        # I think they are
        # but it's too late to think and be smart about it
        for i in range(len(self.fs) - 1, 0, -1):
            block_candidate = self.fs[i]
            if block_candidate != file_block:
                continue
            if moved:
                break
            needed_space = file_block[1]
            for j in range(i):
                space_block = self.fs[j]
                if space_block[0] != ".":
                    continue
                if needed_space <= space_block[1]:
                    # Move the file block where the space is
                    processing[j] = file_block
                    # Replace the file block with a space
                    processing[i] = (".", needed_space)
                    # Add any missing spaces next to the new position of the file
                    # Needed if we move a file with 2 (or X) char to a 3 (or Y spaces)
                    # We need to add the extra space
                    if space_block[1] - needed_space != 0:
                        processing.insert(j + 1, ((".", space_block[1] - needed_space)))
                    moved = True
                    break
        out = []

        # Let's merge two blocks of spaces if they are next to each other
        i = 0
        while i < len(processing):
            block = processing[i]
            if (
                i < (len(processing) - 1)
                and block[0] == "."
                and processing[i + 1][0] == "."
            ):
                out.append((".", processing[i][1] + processing[i + 1][1]))
                i += 2
            else:
                out.append(block)
                i += 1
        self.fs = out

    def get_checksum(self):
        checksum = []
        i = 0
        for block in self.fs:
            for _ in range(block[1]):
                if block[0] == ".":
                    i += 1
                    continue
                checksum.append(i * int(block[0]))
                i += 1
        return checksum


def solve(data):
    """Solve the puzzle and return the solution"""
    fs = FS(data[0])
    file_blocks = reversed(fs.files)
    for file_block in file_blocks:
        fs.move(file_block)
    return sum(fs.get_checksum())


print("--> unit test <--")
assert solve(["123456789123456789123456789123456789"]) == 38529
assert solve(["21132"]) == 20
assert solve(["111"]) == 1
assert solve(["112"]) == 5
assert solve(["122"]) == 3

print("--> test data <--")
test_input = load_data_from_file("test_input")
assert solve(test_input) == 2858

print()
print("--> real data <--")
my_input = load_data_from_file("input")
print(f"\nanswer: {solve(my_input)}")
