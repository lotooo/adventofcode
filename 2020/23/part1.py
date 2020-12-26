test_input = "389125467"
my_input = "326519478"

def curate(cups,cup_selector,current_cup_label):
    tmp_cups = [] 
    for nb in cups:
        tmp_cups.extend(list(nb))
    # We must rotate our string properly
    while tmp_cups[cup_selector] != current_cup_label:
        tmp_element = tmp_cups.pop(0)
        tmp_cups.append(tmp_element)
    return "".join(tmp_cups)

def move(cups,cup_selector=0):
    current_cup_label = cups[cup_selector]
    picked_up_labels = cups[cup_selector+1:cup_selector+1+3]
    if len(picked_up_labels) < 3:
        extra_needed = 3-len(picked_up_labels)
        picked_up_labels = "".join(picked_up_labels + cups[0:extra_needed])
    print(f"cups: {cups}")
    print(f"selector: {cup_selector}")
    print(f"curr: {current_cup_label}")
    print(f"pickup: {picked_up_labels}")

    tmp_cups = list(cups)
    for element_to_remove in list(picked_up_labels):
        tmp_cups.remove(element_to_remove)

    possible_destination = int(current_cup_label)-1
    found_destination = False
    while not found_destination:
        if str(possible_destination) in picked_up_labels:
            print(f"{possible_destination} is currently picked up")
            possible_destination -= 1
        else:
            if possible_destination < min([ int(c) for c in tmp_cups ]):
                possible_destination = int(max(tmp_cups))
            else:
                found_destination = True
                print(f"destination: {possible_destination}")
                destination = tmp_cups.index(str(possible_destination))

    print(f"destination_index: {destination}")

    tmp_cups.insert(destination+1, picked_up_labels)
    new_cups = curate(tmp_cups, cup_selector, current_cup_label)
    new_cup_selector = (cup_selector+1)%len(cups)

    return (new_cups, new_cup_selector)
    
def get_result(cups):
    starting_index = cups.index("1")
    for i in range(0,starting_index):
        tmp_element = cups.pop(0)
        cups.append(tmp_element)
    cups.remove('1')
    return int(''.join(cups))

def solve(cups):
    cup_selector = 0
    for i in range(1,101):
        print(f"Move {i}")
        cups,cup_selector = move(cups,cup_selector)
        print("---")
    r = get_result(list(cups))
    return r

print("--> test data <--")
assert solve(test_input) == 67384529

print()
print("--> real data <--")
print(solve(my_input))
