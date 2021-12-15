#! usr/bin/env python3
"""
Usage: 
>> python3 ./main.py
   or, for faster run times:
>> pypy3 ./main.py
"""

from Deck import Deck
from Card import Card
from Hand import Hand
from itertools import combinations as C
from time import time


def list_without(i):
    # Generates the list [0, 1, 2, ..., i-1, i+1, ..., 49, 50, 51]
    # [0-51] without the number i
    return list(range(0, i)) + list(range(i + 1, 52))


def get_frequencies(verbose=True):

    # Clear the screen and move to (0, 0)
    if verbose:
        print("Counting All Possible Cribbage Hands:")

    # Get the start time of the loop
    start_time = time()

    # A list where the value at each index is the
    # number of hands that produce that score
    scores = [0] * 30

    # Get deck that cards will be taken from
    deck = Deck()

    # Set the loading bar width
    bar_width = 30

    # Loop through each possible draw card
    # use enumerate to also get the index
    for draw_index, draw in enumerate(deck.cards):

        # Inform the user on the current status of the loop
        if verbose:
            print(f"Currently Calculating: {draw} ({draw_index + 1}/52)")

        # Loop through each possible combination of the deck
        # such that the hand comes from the deck that doesn't
        # contain the current draw card (choose 4 cards) (C(51, 4) = 249,900)
        for indices in C(list_without(draw_index), 4):

            # Get the current cards that should be a part of the hand
            curr_cards = [deck.cards[i] for i in indices]

            # Add one to the scores list at the index of the score of the hand
            scores[Hand(curr_cards, draw).get_score()] += 1

    if verbose:
        # Print the scores frequency list
        print(scores)
        # Print the amount of time that it took to explore
        print(f"Took {time()-start_time:.02f} seconds")

    # return the scores
    return scores


def main():
    with open("./true_scores.txt", "r") as f:
        true_frequencies = [int(line) for line in f.readlines()]
    mismatch = False
    for i, (m, t) in enumerate(zip(get_frequencies(), true_frequencies)):
        if m != t:
            mismatch = True
            print(f"║  Incorrect response for score {i}")
            print(f"╚════╣ Should be {t:<8} -  found {m:<8}\n")
    if not mismatch:
        print("Program accurately reproduces results")


if __name__ == "__main__":
    main()
