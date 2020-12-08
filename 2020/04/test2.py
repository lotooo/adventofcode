import json
import re

debug = True

with open('input', 'r') as f:
    myinput = f.read()

valid_passports = 0

passports = myinput.split('\n\n')

def byr_validation(value):
    if re.fullmatch("\d\d\d\d", str(value)) and int(value) >= 1920 and int(value) <= 2002:
        return True
    else:
        return False

def iyr_validation(value):
    if re.fullmatch("\d\d\d\d", str(value)) and int(value) >= 2010 and int(value) <= 2020:
        return True
    else:
        return False

def eyr_validation(value):
    if re.fullmatch("\d\d\d\d", str(value)) and int(value) >= 2020 and int(value) <= 2030:
        return True
    else:
        return False

def hgt_validation(value):
    m = re.fullmatch("(\d+)cm", value)
    if m:
        size = int(m.group(1))
        if size >= 150 and size <= 193:
            return True
        else:
            return False

    m = re.fullmatch("(\d+)in", value)
    if m:
        size = int(m.group(1))
        if size >= 59 and size <= 76:
            return True
        else:
            return False
    return False

def hcl_validation(value):
    if re.fullmatch("#[0-9a-z]{6}", value):
        return True
    else:
        return False

def ecl_validation(value):
    return value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def pid_validation(value):
    if re.fullmatch("[0-9]{9}", value):
        return True
    else:
        return False


if debug:
    print(pid_validation("zfefz"))
    print(pid_validation("12234"))
    print(pid_validation("#123456"))
    print(pid_validation("#123azr"))
    print(pid_validation("192023in"))
    print(pid_validation("2in"))
    print(pid_validation("60in"))
    print(pid_validation("1234567890"))
    print(pid_validation("123456789"))



is_field_validated = {
    'byr': byr_validation,
    'iyr': iyr_validation,
    'eyr': eyr_validation, 
    'hgt': hgt_validation,
    'hcl': hcl_validation,
    'ecl': ecl_validation,
    'pid': pid_validation
}
    

for passport in passports:
    mandatory_fields =  { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' }
    pp_elements = re.split("\n| ", passport)
    for pp_element in pp_elements:
        if pp_element == "":
            continue
        data = pp_element.split(':')
        field = data[0]
        value = data[1]
        if field not in ["cid", ""]:
            if is_field_validated[field](value): 
                mandatory_fields.remove(field)
            else:
                print("Field %s is not validated : %s" % (field,value))

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
