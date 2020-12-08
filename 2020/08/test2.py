with open('input', 'r') as f:
    codes = f.readlines()

test_codes = [
    'nop +0',
    'acc +1',
    'jmp +4',
    'acc +3',
    'jmp -3',
    'acc -99',
    'acc +1',
    'jmp -4',
    'acc +6'
]

possible_versions = []

def read_instruction(line):
    instruction = line.strip().split()
    return (instruction[0], instruction[1])

def test_code(instructions):
    line = 0
    already_executed_lines = []
    # Initialize the accumulator
    accumulator = 0

    while line not in already_executed_lines:
        # Mark this line as already read
        already_executed_lines.append(line)

        # let's read the line
        if codes[line].strip() == '':
            return (True, line, accumulator)

        try:
            instruction = instructions[line]
        except IndexError:
            return (True, line, accumulator)

        operation, value  = read_instruction(instruction)

        if operation == "nop":
            line += 1
        if operation == "jmp":
            line += int(value)
        if operation == "acc":
            accumulator += int(value)
            line += 1
        continue
    return (False, line, accumulator)

def code_variants(initial_codes):
    index = 0
    for instruction in initial_codes:
        operation, value  = read_instruction(instruction)
        if operation == "jmp":
            variant = list(initial_codes)
            variant[index] = "nop %s" % value
            yield variant
        if operation == "nop":
            variant = list(initial_codes)
            variant[index] = "jmp %s" % value
            yield variant
        index += 1

for variant in code_variants(codes):
    is_valid, line, accumulator = test_code(variant)
    if is_valid:
        print(":great_success:")
        print("Accumulator value: %d" % accumulator)
        break
