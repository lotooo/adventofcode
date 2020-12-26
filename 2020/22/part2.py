import re
from collections import deque

def load_data_from_file(filename):
    with open(filename, 'r') as f:
        raw_data = f.read()
    data = re.split(r'\n\n', raw_data)
    return data

def get_result(deck):
    result = 0
    deck.reverse()
    for i,card in enumerate(deck):
        result += card*(i+1)
    return result

def game(player1,player2,game_id=1):
    nb_round = 1
    p1_already_played_deck = list()
    p2_already_played_deck = list()

    while len(player1) > 0 and len(player2) > 0:
        # First, let's see if we already have played that hand
        p1_deck_hash = '_'.join(list(map(str,player1))).strip()
        p2_deck_hash = '_'.join(list(map(str,player2))).strip()
        if p1_deck_hash in p1_already_played_deck or p2_deck_hash in p2_already_played_deck:
            #print(f"g{game_id}: deck already played. p1 wins")
            return "player1"
        else:
            # Save it for later if we haven't
            p1_already_played_deck.append(p1_deck_hash)
            p2_already_played_deck.append(p2_deck_hash)

        # Draw the first card of each player
        p1_card = int(player1.popleft())
        p2_card = int(player2.popleft())

        # Check the size of the current remaining deck
        p1_deck_size = len(player1)
        p2_deck_size = len(player2)

        if p1_deck_size >= p1_card and p2_deck_size >= p2_card:
            # both players have enough cards to recurse
            p1_new_deck = deque(list(player1)[0:p1_card])
            p2_new_deck = deque(list(player2)[0:p2_card])
            winner = game(p1_new_deck, p2_new_deck, game_id=game_id+1)
            if winner == "player1":
                #print(f"Player 1 wins game {game_id+1}")
                player1.append(p1_card)
                player1.append(p2_card)
            else:
                #print(f"Player 2 wins game {game_id+1}")
                player2.append(p2_card)
                player2.append(p1_card)
        else:    
            # Normal game
            if p1_card > p2_card:
                winner = "player1"
            else:
                winner = "player2"
            if winner == "player1":
                player1.append(p1_card)
                player1.append(p2_card)
            else:
                player2.append(p2_card)
                player2.append(p1_card)

        nb_round += 1
    if len(player1) > 0:
        return "player1"
    else:
        return "player2"

def solve(data):
    player1_deck = list(filter(lambda x: re.match(r"^\d+", x), data[0].splitlines()))
    player2_deck = list(filter(lambda x: re.match(r"^\d+", x), data[1].splitlines()))
    player1 = deque(player1_deck)
    player2 = deque(player2_deck)
    winner = game(player1,player2)
    if winner == "player1":
        result = get_result(player1)
    else:
        result = get_result(player2)
    return result

print("--> test data <--")
test_input = load_data_from_file('test_input')
assert solve(test_input) == 291

print()
print("--> real data <--")
my_input = load_data_from_file('input')
print(solve(my_input))
