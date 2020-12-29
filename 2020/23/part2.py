from collections import deque

test_input = "389125467"
my_input = "326519478"

class Cup(int):
    def __init__(self,value):
        self.prev = None
        self.next = None

class Cups:
    def __init__(self, init_data, extra_cups=None):
        prev = None
        self.data = {}
        for i,c in enumerate(map(int,init_data)):
            cup = Cup(c) 
            if i == 0:
                self.current_cup = cup
            self.data[c] = cup
            cup.prev = prev
            if prev:
                prev.next = cup
            prev = cup

        if extra_cups:
            highest_label = int(max(map(int,init_data)))
            for v in range(highest_label+1, extra_cups+1):
                cup = Cup(v)
                self.data[v] = cup
                cup.prev = prev
                if prev:
                    prev.next = cup
                prev = cup
        cup.next = self.current_cup
        self.max = max(self.data.keys())
    
    def __str__(self):
        cup_str = ''
        c = self.current_cup
        while len(cup_str) < len(self.data):
            cup_str += str(c)
            c = c.next
        return cup_str
    

    def index(self,label):
        return self.data.index(label)

    def label(self, index):
        return self.data[index]

    def move(self):
        picked_up_cups = []
        next_cup = self.current_cup.next
        while len(picked_up_cups) < 3:
            selected_cup = next_cup
            picked_up_cups.append(selected_cup)
            next_cup = selected_cup.next
        self.current_cup.next = next_cup 
        possible_destination = self.current_cup-1

        found_destination = False
        while not found_destination:
            if possible_destination in picked_up_cups:
                possible_destination -= 1
            else:
                if possible_destination < 1:
                    possible_destination = self.max
                else:
                    destination = self.data[possible_destination]
                    found_destination = True
        
        picked_up_cups[-1].next = self.data[destination].next
        self.data[destination].next = picked_up_cups[0]
        self.data[picked_up_cups[0]].prev = self.data[destination] 
        self.current_cup = self.current_cup.next

def solve(cups_input):
    is_test = False
    if is_test:
        extra_cups = None
        nb_iteration = 10
    else:
        extra_cups = 1000000
        nb_iteration = 10000000
    cups = Cups(cups_input,extra_cups=extra_cups)
    for i in range(1,nb_iteration+1):
        if is_test:
            print(f"Move {i}")
            print(cups)
        else:
            if i % 100000 == 1:
                print(f"Move {i}")
        cups.move()
    print("done")
    if is_test:
        print(cups)
    ref_cup = cups.data[1]
    return ref_cup.next * ref_cup.next.next

print("--> test data <--")
assert solve(test_input) == 149245887792

print()
print("--> real data <--")
print(solve(my_input))
