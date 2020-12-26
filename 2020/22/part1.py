import re
from collections import deque

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        raw_data = f.read()
    data = re.split(r'\n\n', raw_data)
    #with open(filename, 'r') as f:
    #    data = f.readlines()
    return data

def get_result(deck):
    result = 0
    deck.reverse()
    for i,card in enumerate(deck):
        result += card*(i+1)
    return result

def solve(data):
    player1_deck = list(filter(lambda x: re.match(r"^\d+", x), data[0].splitlines()))
    player2_deck = list(filter(lambda x: re.match(r"^\d+", x), data[1].splitlines()))
    player1 = deque(player1_deck)
    player2 = deque(player2_deck)
    nb_round = 1
    while len(player1) > 0 and len(player2) > 0:
        print(f"-- Round {nb_round} --")
        print(f"Player1's deck: {player1}")
        print(f"Player2's deck: {player2}")
        p1_card = int(player1.popleft())
        p2_card = int(player2.popleft())
        print(f"Player1 plays: {p1_card}")
        print(f"Player2 plays: {p2_card}")
        if p1_card > p2_card:
            print(f"Player 1 wins the round")
            player1.append(p1_card)
            player1.append(p2_card)
        else:
            print(f"Player 2 wins the round")
            player2.append(p2_card)
            player2.append(p1_card)
        nb_round += 1
    print(f"p1: {player1}")
    print(f"p2: {player2}")
    if len(player1) > 0:
        result = get_result(player1)
    else:
        result = get_result(player2)
    return result

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 306

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
