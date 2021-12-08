#! usr/bin/env python3

from typing import List
from Hand import Hand
from Card import Card


class Deck(object):
    """The representation of a "deck" in cribbage
    that contains 52 unique cards
    """

    def __init__(self) -> None:
        """Constructor for the Deck class. Creates a full deck"""
        self.cards: List[Card] = self.create_card_list()

    @staticmethod
    def create_card_list() -> List[Card]:
        """Generates and returns a standard deck of cards

        Returns
        ---------------------
        `cards` : `List[Card]`
            The list of all 52 Card objects in a standard deck
        """
        build: List[Card] = []
        # Loop through each suit
        for suit in "SHCD":
            # Loop through each number
            for number in "A23456789TJQK":
                # Create a card with the current number and suit
                build.append(Card(number, suit))
        # Return the result
        return build

    def __str__(self) -> str:
        """String casting method for the Deck class

        Returns
        ---------------------
        `to_str` : `str`
            The string representation of the deck as
            a space seperated representation of the cards
        """
        return " ".join(map(str, self.cards))
