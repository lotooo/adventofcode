test_input1 = [ 0,3,6 ]
test_input2 = [ 1,3,2 ]
test_input3 = [ 2,1,3 ]
test_input4 = [ 1,2,3 ]
test_input5 = [ 2,3,1 ]
test_input6 = [ 3,2,1 ]
test_input7 = [ 3,1,2 ]
my_input = [9,3,1,0,8,4]

class StupidElvesGame:
    def __init__(self):
        self.history = []
        pass

    def add(self, spoken_number):
        self.history.append(spoken_number)
    
    @property
    def last_spoken_number(self):
        return self.history[-1]

    def num_history(self, number):
        return [ i for i,v in enumerate(self.history) if v == number ]

    def num_count(self, number):
        return len(self.num_history(number))

def stupid_elves_memory(data):
    g = StupidElvesGame()

    for i in range(0,2020):
        if i < len(data):
            spoken_number = data[i]
        else:
            # we are not in the starting numbers list anymore
            if g.num_count(g.last_spoken_number)-1 == 0:
                spoken_number = 0
            else:
                last_spoken = g.num_history(g.last_spoken_number)
                spoken_number = last_spoken[-1] - last_spoken[-2]

        g.add(spoken_number)
            
    return g.last_spoken_number


assert stupid_elves_memory(test_input1) == 436
assert stupid_elves_memory(test_input2) == 1
assert stupid_elves_memory(test_input3) == 10
assert stupid_elves_memory(test_input4) == 27
assert stupid_elves_memory(test_input5) == 78
assert stupid_elves_memory(test_input6) == 438
assert stupid_elves_memory(test_input7) == 1836
print(stupid_elves_memory(my_input))
