#!/usr/bin/env python3
def load_data_from_file(filename):
    """ Load the input from a file and return the transformed version """
    with open(filename, 'r') as f:
        data = list(map(prepare_data, f.readlines()))
    return data


def prepare_data(x):
    """ transform the data the way we want it for the puzzle """
    return int(x.strip())

class Number:
    def __init__(self,n):
        self.value = n
        self.prev = None
        self.next = None
        self.start = False
        self.moved = False

class File:
    def __init__(self,data):
        self.start = Number(data[0])
        self.start.start = True
        self.length = len(data)
        prev = self.start
        for n in data[1:]:
            number = Number(n)
            number.prev = prev
            prev.next = number
            prev = number
        self.start.prev = number
        number.next = self.start
        return None

    def __str__(self):
        out = []
        pointer = self.start
        for i in range(self.length):
            out.append(str(pointer.value))
            pointer = pointer.next
        return ', '.join(out)

    def find_me(self, move, already_moved):
        found = False
        pointer = self.start
        while found == False:
            if pointer.value == move and pointer.moved == already_moved:
                found = True
                target = pointer
                target.moved = True
            else:
                pointer = pointer.next
        return pointer

    def move(self,move):
        target = self.find_me(move,already_moved=False)
        target.moved = True
        #print(move)
        #print(target.start)
        if move > 0:
            for i in range(move):
                current_next = target.next
                current_prev = target.prev
                #print(f"{current_prev.value=}")
                #print(f"{current_next.value=}")
                if target.start:
                    target.start = False
                    current_next.start = True
                    self.start = current_next

                current_next.next.prev = target

                current_prev.next = current_next
                target.next = current_next.next
                current_next.next = target

                target.prev = current_next
                #print(target.prev.value)
                #print(target.next.value)
                #print(current_next.value)
                current_next.prev = current_prev
                #print(self)
        if move < 0:
            for i in range(move,0):
                current_next = target.next
                current_prev = target.prev
                if target.start:
                    target.start = False
                    current_next.start = True
                    self.start = current_next
                if current_prev.start:
                    target.start = True
                    current_prev.start = False
                    self.start = current_prev

                current_prev.prev.next = target
                target.next =  current_prev
                current_prev.next = current_next

                target.prev =  current_prev.prev
                current_prev.prev = target
                current_next.prev = current_prev
        return True

    def get_solution(self,element):
        n = self.start
        while n.value != 0:
            n = n.next
        for i in range(element):
            n = n.next
        return n.value


def solve(data):
    """ Solve the puzzle and return the solution """
    f = File(data)
    for move in data:
        f.move(move)
    return f.get_solution(1000) + f.get_solution(2000) + f.get_solution(3000)


print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 3

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(f"\nanswer: {solve(my_input)}")
