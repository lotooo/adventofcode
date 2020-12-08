with open('input', 'r') as f:
    passwords = f.readlines()
i=0
for password in passwords:
    line_array = password.split(" ")
    min_required = int(line_array[0].split("-")[0])
    max_allowed = int(line_array[0].split("-")[1])
    letter = line_array[1].strip(":") 
    pw = line_array[2]
    valid_char = pw.count(letter)
    print(min_required)
    print(max_allowed)
    print(list(range(min_required, max_allowed)))
    print()
    if valid_char in range(min_required, max_allowed+1):
        i += 1
print(i)
