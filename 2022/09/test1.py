#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return x.strip().split()

class Knock:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def up(self):
        self.y += 1
    def down(self):
        self.y -= 1
    def left(self):
        self.x -= 1
    def right(self):
        self.x += 1
    @property
    def pos(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"{self.x=},{self.y=}"

class Rope:
    def __init__(self, x,y):
        self.head = Knock(x,y)
        self.tail = Knock(x,y)

    @property
    def xdistance(self):
        return abs(self.head.x - self.tail.x)

    @property
    def ydistance(self):
        return abs(self.head.y - self.tail.y)

    def move(self, direction):
        """ Move the head """
        movement = {
          "R": self.head.right,
          "L": self.head.left,
          "U": self.head.up,
          "D": self.head.down
        }
        movement[direction]()

        if max(self.xdistance,self.ydistance) <= 1:
            # Nothing do to
            return

        if direction == "L":
            self.tail.x = self.head.x + 1
            self.tail.y = self.head.y
        if direction == "R":
            self.tail.x = self.head.x - 1
            self.tail.y = self.head.y
        if direction == "U":
            self.tail.y = self.head.y - 1
            self.tail.x = self.head.x
        if direction == "D":
            self.tail.y = self.head.y + 1
            self.tail.x = self.head.x

def solve(data):
    """ Solve the puzzle and return the solution """
    rope = Rope(0,0)
    tail_history = set()
    tail_history.add(rope.tail.pos)
    for direction, step in data:
        #print(f"Moving {step} times to {direction}")
        for i in range(int(step)):
            rope.move(direction)
            tail_history.add(rope.tail.pos)
    return len(tail_history)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 13

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
