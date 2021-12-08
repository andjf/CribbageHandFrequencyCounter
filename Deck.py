#! usr/bin/env python3

from random import randrange
from typing import List
from Hand import Hand
from Card import Card


class Deck(object):
    def __init__(self):
        self.cards = self.create_card_list()

    @staticmethod
    def create_card_list():
        build = []
        for suit in "SHCD":
            for number in "A23456789TJQK":
                build.append(Card(number, suit))
        return build

    def __str__(self) -> str:
        return " ".join(map(str, self.cards))

    @staticmethod
    def generate_hand(indices: List[int], draw_index: int):
        cards = Deck.create_card_list()
        hand = []
        for i in indices:
            hand.append(cards[i])
        return Hand(hand, cards[draw_index])

    def random_card(self):
        return self.cards.pop(randrange(0, len(self.cards)))

    def random_hand(self):
        hand = [self.random_card() for i in range(4)]
        draw = self.random_card()
        return Hand(hand, draw)
