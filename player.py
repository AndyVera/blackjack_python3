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

"""This is the Player class with its necessary functions"""


class Player:
    """Represents a Player in Blackjack"""

    def __init__(self, name, bankroll=10000):
        self._name = name
        self._balance = bankroll
        self._bet = 0
        self._side_bet = 0
        self._double_bet = 0
        self._hand = []

    @property
    def name(self):
        """Function to access private variable"""
        return self._name

    @property
    def balance(self):
        """Function to access private variable"""
        return self._balance

    @property
    def bet(self):
        """Function to access private variable"""
        return self._bet

    @property
    def side_bet(self):
        """Function to access private variable"""
        return self._side_bet

    @property
    def double_bet(self):
        """Function to access private variale"""
        return self._double_bet

    @property
    def hand(self):
        """Property function that makes it easier to call"""
        return self._hand

    def __repr__(self):
        """Function to make it easier to call"""
        return self._name

    def __str__(self):
        """Function to make it easier to call"""
        return self._name

    def place_bet(self, main_bet):
        """Function that adjusts a player's bet"""
        self._bet = main_bet

    def place_side_bet(self, other_bet):
        """Function that adjusts a player's side bet"""
        self._side_bet = other_bet

    def place_double_bet(self, d_bet):
        """Function that sets double down"""
        self._double_bet = d_bet

    def add_to_hand(self, cards):
        """Function that adjusts a player's hand"""
        self._hand += cards

    def clear_hand(self):
        """Function that clears a player's hand"""
        self._hand = []

    def show_first_card(self):
        """Function that shows a player's first card"""
        first_card = []
        first_card.append(self._hand[0])
        print("{}".format(first_card[0]))

    def affect_balance(self, other_bet):
        """Function that adjusts a player's balance"""
        self._balance += other_bet
        return self._balance

    def print_hand(self):
        for _ in range(len(self._hand)):
            print("{}".format(self._hand[_]))
