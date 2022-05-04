# Andy Vera
# CPSC 386-01
# 2022-03-23
# andy.vera13@csu.fullerton.edu
# @AndyVera
#
# Lab 03-01
#
# This is the player class for Blackjack
#

"""This is the Card class"""

from collections import namedtuple
from random import shuffle, randrange
from math import floor

Card = namedtuple("Card", ["rank", "suit"])


def stringify_card(d_card):
    """Function that prints cards in a nice way"""
    return "{} of {}".format(d_card.rank, d_card.suit)


Card.__str__ = stringify_card


class Deck:
    """Deck class which is composed of Card objects"""

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "Clubs hearts Spades Diamonds".split()
    values = list(range(1, 11)) + [10, 10, 10]
    values_dict = dict(zip(ranks, values))

    def __init__(self):
        self._cut_card_position = randrange(60, 80)
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    @property
    def cards(self):
        """Function for access to privates"""
        return self._cards

    def needs_shuffling(self):
        """If it requires shuffling"""
        return len(self._cards) <= self._cut_card_position

    def __getitem__(self, position):
        """Gets a card in a specific position"""
        return self._cards[position]

    def __len__(self):
        """Returns number of cards"""
        return len(self._cards)

    def shuffle(self, index=1):
        """shuffles deck"""
        for _ in range(index):
            shuffle(self._cards)

    def cut(self):
        """It cuts the deck; used after shuffling"""
        temp = floor(len(self._cards) * 0.2)
        half = len(self._cards) // 2 + randrange(-temp, temp)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def deal(self, index=1):
        """Deals one card"""
        return [self._cards.pop() for _ in range(index)]

    def merge(self, other_deck):
        """Used to create a shoe"""
        self._cards += other_deck.cards

    def __str__(self):
        """Used to show entire deck"""
        return "\n".join(map(str, self._cards))


def card_value(current_card):
    """Return the numeric value of a card"""
    return Deck.values_dict[current_card.rank]


Card.__int__ = card_value


def hand_sum(hand):
    """Gives sum of hand"""
    total = sum(map(int, hand))
    if sum(map(lambda c: c.rank == "Ace", hand)) and total + 10 <= 21:
        total += 10
    return total
