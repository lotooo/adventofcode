from collections import defaultdict

test_input1 = [ 0,3,6 ]
test_input2 = [ 1,3,2 ]
test_input3 = [ 2,1,3 ]
test_input4 = [ 1,2,3 ]
test_input5 = [ 2,3,1 ]
test_input6 = [ 3,2,1 ]
test_input7 = [ 3,1,2 ]
my_input = [9,3,1,0,8,4]

def stupid_elves_memory(data,elves_are_bored):
    print("Starting !")
    saved_index = defaultdict(list)
    for i in range(0,elves_are_bored):
        if i < len(data):
            spoken_number = data[i]
        else:
            if last_spoken_number in saved_index:
                if len(saved_index[last_spoken_number]) == 1:
                    spoken_number = 0
                else:
                    spoken_number = saved_index[last_spoken_number][-1] - saved_index[last_spoken_number][-2]
            else:
                #print(f"{i}: First time we see {last_spoken_number}. Returnin 0")
                spoken_number = 0
        saved_index[spoken_number].append(i)
        last_spoken_number = spoken_number
    return spoken_number

elves_are_bored = 30000000

assert stupid_elves_memory(test_input1, elves_are_bored) == 175594
assert stupid_elves_memory(test_input2, elves_are_bored) == 2578
assert stupid_elves_memory(test_input3, elves_are_bored) == 3544142
assert stupid_elves_memory(test_input4, elves_are_bored) == 261214
assert stupid_elves_memory(test_input5, elves_are_bored) == 6895259
assert stupid_elves_memory(test_input6, elves_are_bored) == 18
assert stupid_elves_memory(test_input7, elves_are_bored) == 362
print(stupid_elves_memory(my_input, elves_are_bored))
