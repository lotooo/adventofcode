from collections import Counter

with open('input', 'r') as f:
    my_input = [ line.strip() for line in f.readlines() ]

test_input = [
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL'
]

class Boat:
    def __init__(self, layout):
        self.layout = layout
        self.next_layout = list(layout)

    def __str__(self):
        string_layout = ""
        for line in self.layout:
            string_layout += f"{line}\n"
        return string_layout

    def get_seat_state(self, seat, line):
        if line < 0 or seat < 0 or line >= len(self.layout) or seat >= len(self.layout[line]):
            return None
        else:
            return self.layout[line][seat]

    def set_next_layout_seat_state(self, seat, line, state):
        row = list(self.next_layout[line])
        row[seat] = state
        self.next_layout[line] = ''.join(row)

    def get_seats_around(self, seat, line):
        around = Counter([
            self.get_seat_state(seat-1,line-1),
            self.get_seat_state(seat,line-1),
            self.get_seat_state(seat+1,line-1),
            self.get_seat_state(seat-1,line),
            self.get_seat_state(seat+1,line),
            self.get_seat_state(seat-1,line+1),
            self.get_seat_state(seat,line+1),
            self.get_seat_state(seat+1,line+1)
        ])
        return around
        
    def get_next_layout(self):
        for line in range(0,len(self.layout)):
            for seat in range(0,len(self.layout[line])):
                seat_state = self.get_seat_state(seat,line)
                counts = self.get_seats_around(seat,line)
                if seat_state == "L" and counts["#"] == 0:
                    self.set_next_layout_seat_state(seat, line, "#")
                if seat_state == "#" and counts["#"] >= 4:
                    self.set_next_layout_seat_state(seat, line, "L")
        return self.next_layout

    def get_seats(self):
        c = Counter()
        for line in self.layout:
            c.update(line)
        return c

class BoatV2:
    def __init__(self, layout):
        self.layout = layout
        self.next_layout = list(layout)

    def __str__(self):
        string_layout = ""
        for line in self.layout:
            string_layout += f"{line}\n"
        return string_layout

    def get_seat_state(self, seat, line):
        if line < 0 or seat < 0 or line >= len(self.layout) or seat >= len(self.layout[line]):
            return None
        else:
            return self.layout[line][seat]

    def set_next_layout_seat_state(self, seat, line, state):
        row = list(self.next_layout[line])
        row[seat] = state
        self.next_layout[line] = ''.join(row)

    def get_visible_seats(self, seat, line):
        visible_seats = []

        original_seat = seat
        original_line = line
        

        # Get state of the 1st visible seat on the left
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and seat >= 0:
            seat_state =  self.get_seat_state(seat-1,line)
            seat -= 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat on the right
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and seat < len(self.layout[line]):
            seat_state =  self.get_seat_state(seat+1,line)
            #print(f"reading {seat+1}:{line}: {seat_state}")
            seat += 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat in front
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and line >= 0:
            seat_state = self.get_seat_state(seat,line-1)
            line -= 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat behind
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and line < len(self.layout):
            seat_state = self.get_seat_state(seat,line+1)
            line += 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat in diag top left
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and line >= 0 and seat >= 0:
            seat_state = self.get_seat_state(seat-1,line-1)
            line -= 1
            seat -= 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat in diag top right
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and line >= 0 and seat < len(self.layout[line]):
            seat_state = self.get_seat_state(seat+1,line-1)
            line -= 1
            seat += 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat in diag bottom left
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and line < len(self.layout) and seat >= 0:
            seat_state = self.get_seat_state(seat-1,line+1)
            line += 1
            seat -= 1
        visible_seats.append(seat_state)

        # Get state of the 1st visible seat in diag bottom right
        seat_state = None
        seat = original_seat
        line = original_line
        while seat_state not in [ '#', 'L'] and line < len(self.layout) and seat < len(self.layout[line]):
            seat_state = self.get_seat_state(seat+1,line+1)
            line += 1
            seat += 1
        visible_seats.append(seat_state)
        return Counter(visible_seats)

    def get_seats_around(self, seat, line):
        around = Counter([
            self.get_seat_state(seat-1,line-1),
            self.get_seat_state(seat,line-1),
            self.get_seat_state(seat+1,line-1),
            self.get_seat_state(seat-1,line),
            self.get_seat_state(seat+1,line),
            self.get_seat_state(seat-1,line+1),
            self.get_seat_state(seat,line+1),
            self.get_seat_state(seat+1,line+1)
        ])
        return around
        
    def get_next_layout(self):
        for line in range(0,len(self.layout)):
            for seat in range(0,len(self.layout[line])):
                seat_state = self.get_seat_state(seat,line)
                #counts = self.get_seats_around(seat,line)
                counts = self.get_visible_seats(seat,line)
                if seat_state == "L" and counts["#"] == 0:
                    self.set_next_layout_seat_state(seat, line, "#")
                if seat_state == "#" and counts["#"] >= 5:
                    self.set_next_layout_seat_state(seat, line, "L")
        return self.next_layout

    def get_seats(self):
        c = Counter()
        for line in self.layout:
            c.update(line)
        return c

def test1(boat_layout):        

    boat = Boat(boat_layout)
    while boat.layout != boat.get_next_layout():
        print(boat)
        boat = Boat(boat.get_next_layout())

    print(boat.get_seats())

def test2(boat_layout):        

    boat = BoatV2(boat_layout)
    while boat.layout != boat.get_next_layout():
        print(boat)
        boat = BoatV2(boat.get_next_layout())

    print(boat.get_seats())

test1(test_input)
test1(my_input)
test2(test_input)
test2(my_input)
