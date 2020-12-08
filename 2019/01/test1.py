from math import trunc

with open('input', 'r') as f:
    masses = f.readlines()

def get_fuel_volume(m):
    needed_fuel_volume = trunc(int(m)/3)-2
    if needed_fuel_volume < 0:
        return 0
    else:
        return needed_fuel_volume + get_fuel_volume(needed_fuel_volume)

total = 0
for mass in [ module_mass.rstrip() for module_mass in masses ]:
    if mass not in ['', '\n']:
        fuel_needed_for_module = trunc(int(mass)/3)-2
        fuel_needed_for_fuel = get_fuel_volume(fuel_needed_for_module)
        fuel_needed = fuel_needed_for_module + fuel_needed_for_fuel
        print(mass)
        print(fuel_needed_for_module)
        print(fuel_needed_for_fuel)
        print(fuel_needed)
        print()
        total += fuel_needed
print(total)
