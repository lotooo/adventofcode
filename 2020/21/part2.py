import re
from collections import Counter

test_input = [
    'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
    'trh fvjkl sbzzf mxmxvkd (contains dairy)',
    'sqjhc fvjkl (contains soy)',
    'sqjhc mxmxvkd sbzzf (contains fish)'
]

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

def parse_food(foods):
    """
    parse the food list
    extract the list of ingredients and count them
    extract also the list of allergen
    """
    allergens = {}
    ingredients_counter = Counter()
    for food in foods:
        m = re.match(r"([a-zA-Z ]+)(\(contains (.*)\))?", food)
        if m:
            food_ingredients = m.group(1).split()
            food_allergens = m.group(3).split(',')
        ingredients_counter.update(food_ingredients)

        for food_allergen in [ f.strip() for f in food_allergens]: 
            if food_allergen in allergens:
                allergens[food_allergen] &= set(food_ingredients)  
            else:
                allergens[food_allergen] = set(food_ingredients)
    return (allergens, ingredients_counter)

def filter_allergens(allergens):
    """ 
    Filter alergens by ingredients 
    if an alergien has onluy one ingredient contening it
    removing that ingredient from the other possible allergen containers list
    until we have a 1 ingredient -> 1 allergen match
    """
    all_good = False
    ingredient_to_remove = ""
    while not all_good:
        for allergen, ingredients in allergens.items():
            if len(ingredients) == 1:
                all_good = True
                ingredient_to_remove = list(ingredients)[0]
                for allergen_v2, ingredients_v2 in allergens.items():
                    if allergen_v2 == allergen:
                        continue
                    else:
                        ingredients_v2.discard(ingredient_to_remove)
            if len(ingredients) > 1:
                all_good = False
    return allergens

def get_ingredients_with_allergens(allergens):
    """ Get a list of ingredients with allergen """
    ing = []
    for allergen, ingredients in allergens.items():
        ing.extend(ingredients)
    return set(ing)
        
def get_canonical_dangerous_ingredient_list(foods):
    allergens, ingredients_counter = parse_food(foods)
    filter_allergens(allergens)
    ingredients = set(ingredients_counter.keys())
    ingredients_with_allergens = get_ingredients_with_allergens(allergens)
    ingredients_wo_allergens = ingredients - ingredients_with_allergens
    
    print(allergens)
    canonical_dangerous_ingredient_list = []
    for allergen in sorted(allergens.keys()):
        canonical_dangerous_ingredient_list.append(list(allergens[allergen])[0])
    return ','.join(canonical_dangerous_ingredient_list)

print("--> Test input <--")
assert get_canonical_dangerous_ingredient_list(test_input) == 'mxmxvkd,sqjhc,fvjkl'
print()
print("--> Real input <--")
print(get_canonical_dangerous_ingredient_list(my_input))
