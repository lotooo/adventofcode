from collections import Counter
with open('input', 'r') as f:
    lines = f.readlines()

valid_passwords = 0

for line in lines:
    repeat_range,raw_repeated_char, password = tuple(line.rstrip().split(' '))

    inspected_char = raw_repeated_char[0]
    pos1, pos2 = tuple(repeat_range.split('-'))

    pos1_matches = password[int(pos1)-1] == inspected_char 
    pos2_matches = password[int(pos2)-1] == inspected_char 

    if pos1_matches and pos2_matches:
        continue

    if pos1_matches or pos2_matches:
        print(line.rstrip())
        valid_passwords += 1

print("Found %d valid passwords" % valid_passwords)
