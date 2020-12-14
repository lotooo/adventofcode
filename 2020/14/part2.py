import re
from itertools import product

test_input = [
    'mask = 000000000000000000000000000000X1001X',
    'mem[42] = 100',
    'mask = 00000000000000000000000000000000X0XX',
    'mem[26] = 1'
]

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def bitmask_that(bitmask, value):
    if bitmask == "X":
        return "X"
    return str(int(bitmask) | int(value))

def get_targets(bitmask, bin_target):
    targets = []
    bitmasked_target = list(map(bitmask_that, bitmask, bin_target))
    floating_bits = [ i for i,v in enumerate(bitmasked_target) if v == 'X' ]    
    
    bitmasked_target_str = ''.join(bitmasked_target).replace("X", "%s")

    for poss in product(["0", "1"], repeat=len(floating_bits)):
        possible_target_bin = bitmasked_target_str % poss
        possible_target_decimal = int(possible_target_bin,2)
        targets.append(possible_target_decimal)
    return targets

def dock_ferry(lines):
    memory = {}
    for instruction in lines:
        mask_extraction = re.match(r"mask = (.*)", instruction)
        if mask_extraction:
            mask = mask_extraction.group(1)
            continue
        extract = re.match(r"mem\[(\d+)\] = (\d+)", instruction)
        if extract:
            target = int(extract.group(1))
            bin_target = '{0:036b}'.format(target)
            value = int(extract.group(2))
            bin_value = '{0:036b}'.format(value)
        else:
            raise Exception ("WrongInstructionFormat", instruction)
        bin_result = ''.join(map(bitmask_that, mask, bin_value))

        targets = get_targets(mask, bin_target)
        for target in targets:
            memory[target] = value

    return sum(memory.values())
    
assert dock_ferry(test_input) == 208
print(dock_ferry(my_input))
