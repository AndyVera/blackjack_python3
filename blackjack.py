#! /usr/bin/env python3
# Andy Vera
# CPSC 386-01
# 2022-03-23
# andy.vera13@csu.fullerton.edu
# @AndyVera
#
# Lab 03-01
#
# I implemented Blackjack in Python
#

"""Main file that Executes Blackjack"""

from blackjackgame import game

if __name__ == "__main__":
    GAME = game.BlackJackGame()
    GAME.run()
