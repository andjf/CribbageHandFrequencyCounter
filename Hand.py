#! usr/bin/env python3

from typing import DefaultDict, List
from Card import Card

from itertools import combinations as C
from functools import reduce
from collections import defaultdict


class Hand(object):
    """The representation of a "hand" in cribbage
    that contains the cards that the player has in
    their hand as well as a common draw card
    """

    def __init__(self, cards: List[Card], draw: Card) -> None:
        """Constructor for the Hand class

        Parameters
        ---------------------
        `cards` : `List[Card]`
            The cards that are a part of the player's hand
        `draw` : `Card`
            The common draw card for the hand
        """
        self.cards: List[Card] = cards
        assert len(self.cards) == 4, f"Must be 4 cards, was {len(self.cards)}"
        self.draw: Card = draw
        self.all_cards: List[Card] = self.cards + [self.draw]

    def __str__(self) -> str:
        """String casting method for the Hand class in the format:

        ```
        Cards: AD 3C TS 6S
        Draw: 8C
        ```

        Returns
        ---------------------
        `to_str` : `str`
            The string representation of the hand
        """
        return "Cards: " + ", ".join(map(str, self.cards)) + f"\nDraw: {str(self.draw)}"

    @staticmethod
    def hand_from_str(hand_str: str):
        """Creates a hand based on a string of the format:

        `"AD 3C TS JC QD"`

        Where the last card is considered to be the draw card

        Parameters
        ---------------------
        `hand_str` : `str`
            The space-seperated representation of the hand

        Returns
        ---------------------
        `hand` : `Hand`
            The hand created from the given `hand_str`
        """
        cards_str: List[str] = hand_str.split()
        cards: List[Card] = [Card(number, suit) for number, suit in cards_str[:4]]
        draw: Card = Card(cards_str[-1][0], cards_str[-1][1])
        return Hand(cards, draw)

    def points_nobs(self) -> int:
        """Calculates and returns the points earned from nobs

        Returns
        ---------------------
        `score` : `int`
            The number of points earned from nobs
        """
        # Loops through all the card
        for card in self.cards:
            # Checks if the current card is a Jack
            if card.number == "J":
                # If it is, check if the suit is
                # the same as the draw card
                if card.suit == self.draw.suit:
                    # If the suits are the same, return 1
                    return 1
        # Otherwise return 0
        return 0

    def points_flush(self) -> int:
        """Calculates and returns the points earned from flush

        Returns
        ---------------------
        `score` : `int`
            The number of points earned from flush
        """
        # Gets the suit of the first card to compare against
        suit: str = self.cards[0].suit
        # If any of the cards have a different suit from the first card,
        if any(card.suit != suit for card in self.cards):
            # There is no flush and return 0
            return 0
        # If all 4 card in the hand have the same suit,
        # check if the draw card also has the same suit.
        # If it does, return 5 (full flush), otherwise,
        # return 4 (partial flush)
        return 5 if self.draw.suit == suit else 4

    def points_fifteen(self) -> int:
        """Calculates and returns the points earned from fifteens

        Returns
        ---------------------
        `score` : `int`
            The number of points earned from fifteens
        """
        # Initialize a total
        total: int = 0
        # Loop through how many cards should be used in the combination
        for num_cards in [2, 3, 4, 5]:
            # Loop through every possible combination of cards
            for indices in C(range(5), num_cards):
                # Check if the sum of the chosen cards is 15
                if sum(self.all_cards[i].value for i in indices) == 15:
                    # If so, add 2 to the total points for fifteens
                    total += 2
        # Return the total
        return total

    def points_pair(self) -> int:
        """Calculates and returns the points earned from pairs

        Returns
        ---------------------
        `score` : `int`
            The number of points earned from pairs
        """
        # Initialize a total
        total: int = 0
        # Loop through indices of the first card
        for i in range(len(self.all_cards) - 1):
            # Loop through indices of the second card
            for j in range(i + 1, len(self.all_cards)):
                # If the numbers are the same,
                if self.all_cards[i].number == self.all_cards[j].number:
                    # Add 2 to the point total
                    total += 2
        # Return the total
        return total

    def points_run(self) -> int:
        """Calculates and returns the points earned from runs

        Returns
        ---------------------
        `score` : `int`
            The number of points earned from runs
        """
        # Store the frequencies of each of the numbers in the hand
        # DefaultDict[number_index, frequency]
        frequencies: DefaultDict[int, int] = defaultdict(lambda: 0)
        for index in map(lambda x: x.index, self.all_cards):
            frequencies[index] += 1

        # Sort the unique cards to make it easier to check for runs
        sorted_indices: List[int] = sorted(frequencies.keys())

        # Helper Lists for checking for runs
        in_run: List[int] = []
        curr_in_run: List[int] = []

        # Variables to keep track of run lengths
        max_run_length: int = 1
        curr_run_length: int = 1

        # Look at each card (minus the last card)
        for i in range(len(sorted_indices) - 1):
            # If a current run doesn't exist,
            if len(curr_in_run) == 0:
                # this is the start of a one
                curr_in_run.append(sorted_indices[i])
            # If the next card is 1 more than the current card
            if sorted_indices[i] + 1 == sorted_indices[i + 1]:
                # The run continues
                curr_in_run.append(sorted_indices[i + 1])
                curr_run_length += 1
                max_run_length = max(curr_run_length, max_run_length)
            else:
                # Otherwise, the run is broken
                # If the previous run was 3 or more cards,
                if len(curr_in_run) >= 3:
                    # The current run is the only run in the hand
                    in_run = curr_in_run
                    # If the hand is 5 cards it is impossible
                    # to have multiple runs that exceed length 3
                    # after you have taken out repeated cards
                    break
                # If the previous run wasn't of length 3,
                # erase the current run
                curr_in_run = []
                curr_run_length = 1
        # If the run occured at the end of the list it
        # would go unaccounted for unless we had this check
        if len(curr_in_run) >= 3 and in_run == []:
            in_run = curr_in_run

        # Get the frequencies of the numbers that exist in the run
        frequencies_in_run: List[int] = [frequencies[f] for f in frequencies if f in in_run]
        # If the run doesn't exist, return 0
        if len(frequencies_in_run) == 0:
            return 0
        # Otherwise calculate the points earned by the run
        # by multiplying all of the frequencies of the cards
        # that were in the run together and multiplying that
        # product by the length of the run that was found.
        return len(in_run) * reduce(lambda a, b: a * b, frequencies_in_run)

    def get_score_report(self):
        """Returns the score report for this hand

        Returns
        ---------------------
        `report` : `Dict[str, int]`
            The report of points earned from different scoring methods
        """
        report = {}
        report["nobs"] = self.points_nobs()
        report["flush"] = self.points_flush()
        report["fifteen"] = self.points_fifteen()
        report["pair"] = self.points_pair()
        report["run"] = self.points_run()
        return report

    def get_score(self):
        """Returns the score of the hand

        Returns
        ---------------------
        `score` : `int`
            The score of this hand based on the various scoring methods
        """
        score = self.points_nobs()
        score += self.points_flush()
        score += self.points_fifteen()
        score += self.points_pair()
        score += self.points_run()
        return score
