#! usr/bin/env python3


class Card(object):
    """The representation of a "card" in cribbage
    that has a certain number and suit
    """

    def __init__(self, number: str, suit: str) -> None:
        """Constructor for the Card class

        Parameters
        ---------------------
        `number` : `str`
            The number of the card (A23456789TJQK)
        `suit` : `str`
            The suit of the card (SHCD)
        """
        self.number: str = number
        self.suit: str = suit
        self.index: int = "A23456789TJQK".index(self.number)
        self.value: int = (10 if self.number in "TJQK" else (1 if self.number == "A" else int(self.number)))

    def __str__(self) -> str:
        """String casting method for the Card class

        Returns
        ---------------------
        `to_str` : `str`
            The string representation of the card like "3C"
        """
        return self.number + self.suit
