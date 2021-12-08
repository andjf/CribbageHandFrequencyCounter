#! usr/bin/env python3

import colorama
from Deck import Deck
from Card import Card
from Hand import Hand
from itertools import combinations as C
from time import time
from colorama import Fore


def pos(x, y):
    # Sets the position of the cursor in the terminal
    return f"\x1b[{y};{x}H"


def list_without(i):
    # Generates the list [0, 1, 2, ..., i-1, i+1, ..., 49, 50, 51]
    # [0-51] without the number i
    return list(range(0, i)) + list(range(i + 1, 52))


def get_frequencies(verbose=True):

    # Clear the screen and move to (0, 0)
    if verbose:
        print("\033[2J")
        print(Fore.GREEN + f"{pos(0, 0)}Counting All Possible Cribbage Hands:" + Fore.RESET)

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
            print(Fore.YELLOW + f"{pos(0, 2)}Currently Calculating: {draw} ({draw_index + 1}/52)" + Fore.RESET)

        # Loop through each possible combination of the deck
        # such that the hand comes from the deck that doesn't
        # contain the current draw card (choose 4 cards) (C(51, 4) = 249,900)
        for hand_index, indices in enumerate(C(list_without(draw_index), 4)):

            # Inform user about progress of current scoring with loading bar
            if verbose and hand_index % (249900 // bar_width) == 0:
                curr_bar_width = int((hand_index / 249900) * bar_width)
                print(Fore.LIGHTYELLOW_EX + f"{pos(0, 3)}|{'#'*curr_bar_width}{' '*(bar_width-curr_bar_width - 1)}|" + Fore.RESET)

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
    true_frequencies = [1009008, 99792, 2813796, 505008, 2855676, 697508, 1800268, 751324, 1137236, 361224, 388740, 51680, 317340, 19656, 90100, 9168, 58248, 11196, 2708, 0, 8068, 2496, 444, 356, 3680, 0, 0, 0, 76, 4]
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
