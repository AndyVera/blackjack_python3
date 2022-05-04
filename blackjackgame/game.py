#! /usr/bin/env python3
# Andy Vera
# CPSC 386-01
# 2022-03-23
# andy.vera13@csu.fullerton.edu
# @AndyVera
#
# Lab 03-01
#
# I implemented BlackJack in Python
#

"""This is the file that has the logic for the game"""

import time
import pickle
from blackjackgame.cards import Deck
from blackjackgame.player import Player
from blackjackgame.cards import hand_sum


class BlackJackGame:
    """Represents the a game of blackjack"""

    def __init__(self):
        pass

    @classmethod
    def run(cls):

        print_typing("==========================\n===WELCOME TO BLACKJACK===\n==========================\n")
        """Method that runs the game logic"""

        game_deck = create_deck()
        ai_ = Player("Pakkun")
        ai_first_card = 0
        ai_total_hand = 0

        num_of_players = int(typing_input("\nHow many Players? [1-4] "))

        

        try:
            player_list = from_file('players.pckl')
            #print("\nFile found")
            players = player_initalize(num_of_players, player_list)
        except FileNotFoundError:
            print_typing("The file doesn't exist\n")

        amount_of_players = len(players)

        print_typing("\nThis is the order of the players in the game: {}".format(players))

        while True:
            new_player_hand(players, ai_, amount_of_players)
            setting_player_bets(players, amount_of_players)

            first_draw(players, ai_, game_deck, amount_of_players)
            ai_first_card = hand_sum(ai_.hand)
            second_draw(players, ai_, game_deck, amount_of_players)
            ai_total_hand = hand_sum(ai_.hand)

            for _ in range(amount_of_players):
                current_player = players[_]

                print_typing("\n=={}'s turn!==".format(current_player.name))
                performing_side_bet(current_player, ai_first_card)
                current_total = hand_sum(current_player.hand)

                print_typing(
                    "\n\n{}'s total: {}".format(
                        current_player.name, current_total
                    )
                )

                current_total = player_draw_cards(
                    current_player, current_total, game_deck
                )

            #print_typing("\n{}'s hand: {}".format(ai_.name, ai_.hand))
            print_typing("\n{}'s hand:\n".format(ai_.name))
            ai_.print_hand()
            checking_side_bet(players, ai_total_hand, amount_of_players)

            ai_turn(ai_, game_deck)

            ai_total_hand = hand_sum(ai_.hand)

            outcome_events(players, ai_total_hand, amount_of_players)

            play_again = typing_input(
                "\n\nDoes Anyone Want to Stop Playing? [y/n] "
            )
            if play_again == "y":
                #to_file('players.pckl', player_list)
                updated_list = save_players(players, player_list)
                to_file("players.pckl", updated_list)
                print_typing("\n=== Thanks for playing! ===\n")
                break

    @classmethod
    def temp2(cls):
        """This is just a function to comply with pylint"""
        print("temp2")


def create_deck():
    """Creates the shoe"""
    main_deck = Deck()
    extra_deck = Deck()
    for _ in range(1, 7, 1):
        main_deck.merge(extra_deck)
    main_deck.shuffle()
    main_deck.cut()
    return main_deck


def player_initalize(num_of_players, player_list):
    """Initalzies the players"""
    new_players = []
    index_num = 0
    for _ in range(num_of_players):
        player_found = False
        name = typing_input("\nWhat is your name? ")

        for index_num in range(len(player_list)):
            if name == player_list[index_num].name:
                new_players.append(player_list[index_num])
                print_typing("\nPlayer found!")
                print_typing("\n{}'s balance: ${}".format(player_list[index_num].name, player_list[index_num].balance))
                player_found = True

        if index_num + 1 == len(player_list) and player_found == False:

            new_players.append(Player(name))
            print_typing("\nNew Player!")
            index_num = 0

    return new_players


def setting_player_bets(players, num):
    """Initializes the players main bets"""
    for _ in range(num):
        current_player = players[_]
        bet = int(
            typing_input("\n\n{} place your bet: $".format(current_player.name))
        )
        while bet < 0 or bet > 10000:
            print_typing(
                "\nBet has to be between $0 and ${}".format(
                    current_player.balance
                )
            )
            bet = int(
                typing_input(
                    "\n{} place your bet: ".format(current_player.name)
                )
            )
        current_player.place_bet(bet)


def new_player_hand(players, computer, num):
    """Clears each player's hand for a new game"""
    for _ in range(num):
        current_player = players[_]
        current_player.clear_hand()

    computer.clear_hand()


def first_draw(players, computer, deck, num):
    """Gives all players including the computer a card"""
    print_typing("\nFirst card dealt!")
    for _ in range(num):
        current_player = players[_]
        card_draw = deck.deal()
        current_player.add_to_hand(card_draw)
        print_typing(
            #"\n\n{}'s hand: {}".format(current_player.name, current_player.hand)
            "\n\n==={}'s hand===\n\n".format(current_player.name)
        )
        current_player.print_hand()

    card_draw = deck.deal()
    computer.add_to_hand(card_draw)

    print_typing("\n==={}'s hand===\n\n".format(computer.name))
    computer.print_hand()


def second_draw(players, computer, deck, num):
    """Gives all players including the computer a second card"""
    print_typing("\nSecond card dealt!")
    for _ in range(num):
        current_player = players[_]
        card_draw = deck.deal()
        current_player.add_to_hand(card_draw)
        print_typing(
            #"\n\n{}'s hand: {}".format(current_player.name, current_player.hand)
            "\n\n==={}'s hand:===\n\n".format(current_player.name)
        )
        current_player.print_hand()
        print_typing(
            "\nThis hand has the value of: {}\n".format(
                hand_sum(current_player.hand)
            )
        )

    card_draw = deck.deal()
    computer.add_to_hand(card_draw)
    print_typing(
        "\n==={}'s hand===\n\n".format(computer.name)
    )
    computer.show_first_card()
    print("??? of ???")


def performing_side_bet(player, computer_total):
    """Initializes all player's except computer insurance"""
    if computer_total in (10, 11):
        print_typing("\n\nThe house may have blackjack")
        choice = typing_input("\n\nDo you want to place insurace? [y/n] ")

        if choice == "y":
            insurace_bet = int(typing_input("\n\nHow much? "))
            player.place_side_bet(insurace_bet)


def player_draw_cards(player, current_total, card_deck):
    """Distributes cards to only non-computer players"""
    double_down = typing_input("\n\nDo you want to double down? [y/n] ")

    if double_down == "y":
        double_value = player.double_bet
        player.place_double_bet(double_value)
        new_card = card_deck.deal()
        player.add_to_hand(new_card)
        print_typing("\n\n{}".format(player.hand))
        current_total = hand_sum(player.hand)
        print_typing("\n\nThis hand has the value of: {}".format(current_total))

    elif double_down == "n":
        while current_total < 21:
            drawcard = typing_input(
                ("\nDo you want to draw another card? [y/n] ")
            )

            if drawcard == "y":
                new_card = card_deck.deal()
                player.add_to_hand(new_card)
                #print_typing("\n\n{}".format(player.hand))

                print_typing("\nCurrent Hand: \n")
                player.print_hand()
                current_total = hand_sum(player.hand)
                print_typing(
                    "\nThis hand has the value of: {}\n".format(current_total)
                )

            if drawcard == "n":
                break

    return current_total


def checking_side_bet(players, computer_total, num):
    """Check if house has 21 and takes care of insurance"""
    for _ in range(num):
        current_player = players[_]

        if current_player.side_bet != 0:
            if computer_total == 21:
                print_typing("\n\nThe house does have blackjack")
                print_typing("\n\nYou won the side bet")
                current_player.affect_balance(current_player.side_bet)
                print_typing(
                    "\n\nYour balance is: ${}".format(current_player.balance)
                )

            if computer_total != 21:
                print_typing("\n\nThe house does not have blackjack")
                print_typing("\n\nYou lost the side bet")
                negative_money = -1 * current_player.side_bet
                current_player.affect_balance(negative_money)
                print_typing(
                    "\n\nYour balance is: ${}".format(current_player.balance)
                )


def ai_turn(computer, card_deck):
    """The computer's turn to get cards"""
    while hand_sum(computer.hand) < 17:
        new_card = card_deck.deal()
        computer.add_to_hand(new_card)
        print_typing("\n\n{}".format(hand_sum(computer.hand)))


def outcome_events(players, computer_total, num):
    """All the possible outcomes of the game"""
    for _ in range(num):
        current_player = players[_]
        current_total = hand_sum(current_player.hand)

        if current_total > 21:
            print_typing("\n\n{} busted!".format(current_player.name))
            negative_money = -1 * current_player.bet
            negative_double = -1 * current_player.double_bet
            current_player.affect_balance(negative_money)
            current_player.affect_balance(negative_double)
            current_player.place_double_bet(0)
            print_typing(
                "\n\nYour balance is: ${}".format(current_player.balance)
            )

        elif computer_total < current_total <= 21:
            print_typing("\n\n{} won".format(current_player.name))
            current_player.affect_balance(current_player.bet)
            current_player.affect_balance(current_player.double_bet)
            current_player.place_double_bet(0)
            print_typing(
                "\n\nYour balance is: ${}".format(current_player.balance)
            )

        elif current_total == computer_total:
            print_typing(
                "\n\n{} tied against the house".format(current_player.name)
            )
            print_typing("\n\n{} keeps their money".format(current_player.name))
            current_player.place_double_bet(0)
            print_typing(
                "\n\nYour balance is: ${}".format(current_player.balance)
            )

        elif current_total < computer_total <= 21:
            print_typing(
                "\n\n{} lost against the house".format(current_player.name)
            )
            current_player.affect_balance(-1 * current_player.bet)
            negative_double = -1 * current_player.double_bet
            current_player.affect_balance(negative_double)
            current_player.place_double_bet(0)
            print_typing(
                "\n\nYour balance is: ${}".format(current_player.balance)
            )

        elif current_total <= 21 < computer_total:
            print_typing("\n\n{} won".format(current_player.name))
            current_player.affect_balance(current_player.bet)
            current_player.affect_balance(current_player.double_bet)
            current_player.place_double_bet(0)
            print("\nYour balance is: ${}".format(current_player.balance))


def print_typing(text):
    """This function gives a typewritter effect"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.1)


def typing_input(text):
    """This function gives a typewritter effect"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.1)
    value = input()
    return value

def from_file(pickle_file):
    """Read the contents of pickle_file, decode it, and return it as players."""
    with open(pickle_file, 'rb') as file_handle:
        players = pickle.load(file_handle)
    return players

def to_file(pickle_file, players):
    """Write the list players to the file pickle_file."""
    with open(pickle_file, 'wb') as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)

def save_players(players, player_list):

    index_num = 0

    for _ in range(len(players)):
        current_player = players[_]

        for index_num in range(len(player_list)):

            if current_player.name == player_list[index_num].name:
                player_list[index_num] = current_player
                print_typing("\nUpdating player")

        if index_num + 1 == len(player_list):
            player_list.append(current_player)
            print_typing("\nUploading new player")

    return player_list

            