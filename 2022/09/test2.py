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

def distance(k1,k2):
    return max(abs(k1.x - k2.x), abs(k1.y - k2.y))

def get_neighboors(k):
    n = []
    for x in range(k.x-1,k.x+1+1):
        for y in range(k.y-1,k.y+1+1):
            n.append((x,y))
    return set(n)

class Rope:
    def __init__(self, x,y, size=10):
        self.knocks = [ Knock(x,y) for i in range(size) ]
        self.head = self.knocks[0]
        self.tail = self.knocks[-1]

    def move(self, direction):
        """ Move the head """
        movement = {
          "R": self.head.right,
          "L": self.head.left,
          "U": self.head.up,
          "D": self.head.down
        }
        movement[direction]()

        next_movement = direction
        for i,knock in enumerate(self.knocks[:-1]):
            last_movement = next_movement
            if distance(self.knocks[i], self.knocks[i+1]) <= 1:
                # nothing to do
                continue
            n1 = get_neighboors(self.knocks[i])
            n2 = get_neighboors(self.knocks[i+1])
            candidates = n1 & n2
            if len(candidates) == 1:
                candidate = candidates.pop()
            else:
                for candidate in candidates:
                    x,y = candidate
                    if x == self.knocks[i].x or y == self.knocks[i].y:
                        break
            x,y = candidate
            self.knocks[i+1].x = x
            self.knocks[i+1].y = y

    def __str__(self):
        xs = [ k.x for k in self.knocks ]
        ys = [ k.y for k in self.knocks ]
        out = []
        for y in range(max(ys)+1):
            line = ""
            for x in range(max(xs)+1):
                found = False
                for i,k in enumerate(self.knocks):
                    if found:
                        continue
                    if k.pos == (x,y):
                        line += str(i)
                        found=True
                if not found:
                    line += "."
            out.append(line)
        out.reverse()
        out.append('==================================================================')
        return '\n'.join(out)

def solve(data):
    """ Solve the puzzle and return the solution """
    rope = Rope(0,0,10)
    tail_history = set()
    tail_history.add(rope.tail.pos)
    print(rope)
    for direction, step in data:
        for i in range(int(step)):
            rope.move(direction)
            print(rope)
            tail_history.add(rope.tail.pos)
    return len(tail_history)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 1
test_input2 = load_data_from_file('test_input2')
assert solve(test_input2) == 36

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
