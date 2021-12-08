#! usr/bin/env python3

from typing import List
from Card import Card

from itertools import combinations as C
from functools import reduce
from collections import defaultdict


class Hand(object):
    def __init__(self, cards: List[Card], draw: Card):
        self.cards: List[Card] = cards
        assert len(self.cards) == 4, f"Must be 4 cards, was {len(self.cards)}"
        self.draw = draw
        self.all_cards = self.cards + [self.draw]

    def __str__(self) -> str:
        return "Cards: " + ", ".join(map(str, self.cards)) + f"\nDraw: {str(self.draw)}"

    def str_short(self):
        return " ".join(map(str, self.all_cards))

    @staticmethod
    def hand_from_str(s):
        cards_str = s.split()
        cards = [Card(card[:-1], card[-1]) for card in cards_str[:4]]
        draw = Card(cards_str[-1][:-1], cards_str[-1][-1])
        return Hand(cards, draw)

    def points_nobs(self):
        for card in self.cards:
            if card.number == "J":
                if card.suit == self.draw.suit:
                    return 1
        return 0

    def points_flush(self):
        suit = self.cards[0].suit
        if any(card.suit != suit for card in self.cards):
            return 0
        return 5 if self.draw.suit == suit else 4

    def points_fifteen(self):
        total = 0
        for num_cards in [2, 3, 4, 5]:
            for indices in C(range(5), num_cards):
                if sum(self.all_cards[i].value for i in indices) == 15:
                    total += 2
        return total

    def points_pair(self):
        total = 0
        for i in [0, 1, 2, 3]:
            for j in range(i + 1, 5):
                if self.all_cards[i].number == self.all_cards[j].number:
                    total += 2
        return total

    def points_run(self):
        frequencies = defaultdict(lambda: 0)
        for index in map(lambda x: x.index, self.all_cards):
            frequencies[index] += 1

        sorted_indices = sorted(frequencies.keys())

        in_run = []
        curr_in_run = []

        max_run_length = 1
        curr_run_length = 1

        for i in range(len(sorted_indices) - 1):
            if len(curr_in_run) == 0:
                curr_in_run.append(sorted_indices[i])
            if sorted_indices[i] + 1 == sorted_indices[i + 1]:
                curr_in_run.append(sorted_indices[i + 1])
                curr_run_length += 1
                max_run_length = max(curr_run_length, max_run_length)
            else:
                if len(curr_in_run) >= 3:
                    in_run = curr_in_run
                    break
                curr_in_run = []
                curr_run_length = 1
        if len(curr_in_run) >= 3 and in_run == []:
            in_run = curr_in_run

        frequencies_in_run = [frequencies[f] for f in frequencies if f in in_run]
        if len(frequencies_in_run) == 0:
            return 0
        return len(in_run) * reduce(lambda a, b: a * b, frequencies_in_run)

    def get_score_report(self):
        score = {}
        score["nobs"] = self.points_nobs()
        score["flush"] = self.points_flush()
        score["fifteen"] = self.points_fifteen()
        score["pair"] = self.points_pair()
        score["run"] = self.points_run()
        return score

    def get_score(self):
        score = self.points_nobs()
        score += self.points_flush()
        score += self.points_fifteen()
        score += self.points_pair()
        score += self.points_run()
        return score
