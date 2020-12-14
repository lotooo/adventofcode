import re

test_input = [
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0'
]

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def bitmask_that(bitmask, value):
    if bitmask == "X":
        return value
    else:
        return bitmask

def dock_ferry(lines):
    memory = {}
    for instruction in lines:
        mask_extraction = re.match(r"mask = (.*)", instruction)
        if mask_extraction:
            mask = mask_extraction.group(1)
            continue
        extract = re.match(r"mem\[(\d+)\] = (\d+)", instruction)
        if extract:
            target = extract.group(1)
            value = int(extract.group(2))
            bin_value = '{0:036b}'.format(value)
        else:
            raise Exception ("WrongInstructionFormat", instruction)
        result = int(''.join(map(bitmask_that, mask, bin_value)),2)
        memory[target] = result
    return sum(memory.values())
    
assert dock_ferry(test_input) == 165
print(dock_ferry(my_input))
