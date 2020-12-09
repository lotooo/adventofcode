from itertools import combinations

test_input1 = [1,9,10,3,2,3,11,0,99,30,40,50]
test_input2 = [1,0,0,0,99]
test_input3 = [2,3,0,3,99]
test_input4 = [2,4,4,5,99,0]
test_input5 = [1,1,1,4,99,5,6,0,99]

my_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,5,19,23,1,23,5,27,2,27,10,31,1,5,31,35,2,35,6,39,1,6,39,43,2,13,43,47,2,9,47,51,1,6,51,55,1,55,9,59,2,6,59,63,1,5,63,67,2,67,13,71,1,9,71,75,1,75,9,79,2,79,10,83,1,6,83,87,1,5,87,91,1,6,91,95,1,95,13,99,1,10,99,103,2,6,103,107,1,107,5,111,1,111,13,115,1,115,13,119,1,13,119,123,2,123,13,127,1,127,6,131,1,131,9,135,1,5,135,139,2,139,6,143,2,6,143,147,1,5,147,151,1,151,2,155,1,9,155,0,99,2,14,0,0]

def intcode_computer(numbers):
    index = 0
    op = numbers[index]

    while op != 99:
        if op == 1:
            numbers[numbers[index+3]] = numbers[numbers[index+1]] + numbers[numbers[index+2]]
            index += 4
            op = numbers[index]
            continue
        if op == 2:
            numbers[numbers[index+3]] = numbers[numbers[index+1]] * numbers[numbers[index+2]]
            index += 4
            op = numbers[index]
            continue
    return numbers[0]
        

def validate(test_input):
    intcode_computer(test_input)


validate(test_input1)
validate(test_input2)
validate(test_input3)
validate(test_input4)
validate(test_input5)

for noun,verb in [ (a,b) for a in range(0,100) for b in range(0,100)]:
    program = my_input.copy()
    program[1] = noun
    program[2] = verb
    if intcode_computer(program) == 19690720:
        print(f"noun: {noun} verb: {verb} answer: {100*noun+verb}")
