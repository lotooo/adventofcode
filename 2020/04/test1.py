import json
import re

with open('input', 'r') as f:
    myinput = f.read()

valid_passports = 0

passports = myinput.split('\n\n')

for passport in passports:
    mandatory_fields =  { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' }
    pp_elements = re.split("\n| ", passport)
    for pp_element in pp_elements:
        field = pp_element.split(':')[0]
        if field not in ["cid", ""]:
            mandatory_fields.remove(field)

    if len(mandatory_fields) == 0:
        valid_passports += 1
        print("This passport is valid !")
        print("")
    else:
        print("This passport is NOT  valid !")
        print("Missing field(s):")
        print(mandatory_fields)
        print("")
        
print("Found %d valid passeports !" % valid_passports)
