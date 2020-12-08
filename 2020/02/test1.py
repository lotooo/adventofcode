from collections import Counter
with open('input', 'r') as f:
    lines = f.readlines()

valid_passwords = 0

for line in lines:
    repeat_range,raw_repeated_char, password = tuple(line.rstrip().split(' '))

    inspected_char = raw_repeated_char[0]

    counts = Counter(password)

    min_occurences, max_occurences = tuple(repeat_range.split('-'))

    print("Password %s contains %d %s" % (password, counts[inspected_char], inspected_char))

    if counts[inspected_char] <= int(max_occurences) and counts[inspected_char] >= int(min_occurences):
        valid_passwords += 1

print("Found %d valid passwords" % valid_passwords)
