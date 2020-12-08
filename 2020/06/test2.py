import re
from collections import Counter

with open('input', 'r') as f:
    myinput = f.read()

groups = myinput.split('\n\n')

total_questions_answered_by_yes = 0

for group in groups:
    print("New group !")
    responses = Counter()
    people_in_group = group.split('\n')
    for people_answer in people_in_group:
        print(people_answer)
        for question in people_answer:
            responses[question] += 1
        print(responses)

    for question, number_of_yes in responses.items():
        if number_of_yes == len(people_in_group):
            print(people_in_group)
            print(len(people_in_group))
            print("%s: %d" % (question, number_of_yes))
            total_questions_answered_by_yes += 1
    print("")

print("Total questions answer by yes: %d" % total_questions_answered_by_yes)
        
