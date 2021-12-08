#! usr/bin/env python3

class Card(object):
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        self.index = "A23456789TJQK".index(self.number)
        self.value = (10 if self.number in "TJQK" else (1 if self.number == "A" else int(self.number)))

    def __str__(self):
        return self.number + self.suit
