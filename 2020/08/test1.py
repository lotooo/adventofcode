with open('input', 'r') as f:
    codes = f.readlines()

# Let's start by reading first line
line = 0

# Initialize the accumulator
accumulator = 0

already_executed_lines = []

while line not in already_executed_lines:
    # Mark this line as already read
    already_executed_lines.append(line)

    # let's read the line
    print("Reading line %d" % line)
    instruction = codes[line].strip().split(' ')
    operation = instruction[0]
    value = instruction[1]

    if operation == "nop":
        line += 1
    if operation == "jmp":
        line += int(value)
    if operation == "acc":
        accumulator += int(value)
        line += 1
    continue
        
print("Instruction %d has already been executed" % line)
print("Accumulator value: %d" % accumulator)

