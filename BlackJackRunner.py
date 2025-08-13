
import random as rnd
import time

import numpy as np

# initialize bankroll and table minimum
bankroll = 250
table_min_bet = 15

# sim designation
num_decks = 1
num_players = 2


# create shoe of designated number of decks
def create_deck(number_decks):
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    current_deck = ranks * 4   # change number it is multiplied by to alter number of decks in play
    current_deck *= number_decks
    return current_deck


def deal_card(current_deck):
    return current_deck.pop()


# value of a card
def card_value(card):
    if card in ['T', 'J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11  # handle Ace adjustment later
    else:
        return int(card)


def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    aces = hand.count('A')

    # return logic if any aces
    if aces > 0:
        # soft total by default
        hard_flag = 0

        # if total is over 21, subtract aces
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        # if no aces remain, total is hard
        if aces == 0:
            hard_flag = 1

    else:
        hard_flag = 1

    return value, hard_flag


# main play
def play_hand(deck, betting_strategy, player_strategy, round_bankroll, card_counter):

    # reset loop variables
    ace_set = num_players*[False]
    player_set = num_players*[False]
    dealer_set = False
    win_check = 0

    # reset dealer and player cards
    # deck = create_deck(num_decks)
    # rnd.shuffle(deck)

    # deal and players
    dealer_cards = []
    players = [[] for i in np.arange(num_players)]
    for r in range(2):  # deal two rounds
        for p in np.arange(num_players):
            players[p].append(deal_card(deck))
        dealer_cards.append(deal_card(deck))

    # if dealer has an ace up, ask if players want insurance
    if hand_value(dealer_cards[1])[1] == 0:

        # initialize insurance holders
        player_insurance = num_players*[0]

        # loop through all players
        for p in np.arange(num_players):
            player_cards = players[p]

            while not ace_set[p]:
                print("\nPlayer " + str(p+1) + ", Insurance or No? (I/N):")
                player_action = input()
                if str.lower(player_action) == 'i':
                    player_insurance[p] = 1
                    ace_set[p] = True
                elif str.lower(player_action) == 'n':
                    player_insurance[p] = 0
                    ace_set[p] = True

        # if dealer has blackjack, end game and deal with loss condition
        if hand_value(dealer_cards) == 21:
            player_set = num_players * [True]
            dealer_set = True

        else:
            print("Safe.")

    # loop through all players
    for p in np.arange(num_players):
        player_cards = players[p]

        # player hitting loop, goes until hand is set
        while not player_set[p]:

            # set player if they have 21 already
            if hand_value(player_cards)[0] == 21:
                player_set[p] = True
            else:
                # ask for action
                player_action = input()

                # if standing, table is set
                if str.lower(player_action) == 's':
                    player_set[p] = True
                # if hitting, update table display and counts
                elif str.lower(player_action) == 'h':

                    # give player new card and update deck
                    player_cards.append(deal_card(deck))

            # check if player has busted
            if hand_value(player_cards)[0] > 21:
                win_check = -1
                player_set[p] = True

    # dealer hits until 17
    while not dealer_set:

        # stand on 17 and up
        if hand_value(dealer_cards)[0] > 21:
            dealer_set = True
        elif 16 < hand_value(dealer_cards)[0] < 22:
            dealer_set = True
        else:
            # give dealer new card
            dealer_cards.append(deal_card(deck))

    # loop through players again to determine winnings
    for p in np.arange(num_players):
        player_cards = players[p]

        # recalculate dealer and player hand
        player_hand_value = hand_value(player_cards)[0]
        dealer_hand_value = hand_value(dealer_cards)[0]

        # win conditions
        if player_hand_value == 21 and len(player_cards) == 2:  # player blackjack
            win_check = 1.5
        elif dealer_hand_value == 21 and len(dealer_cards) == 2:  # dealer blackjack
            if str.lower(player_action) == 'i':
                win_check = 0
            elif str.lower(player_action) == 'n':
                win_check = -1
        elif player_hand_value > 21:  # player bust
            win_check = -1
        elif dealer_hand_value > 21:  # dealer bust
            win_check = 1
        elif dealer_hand_value > player_hand_value:  # dealer win with higher number
            win_check = -1
        elif dealer_hand_value == player_hand_value:  # push
            win_check = 0
        else:  # player wins everything else
            win_check = 1

        # adjust bankroll
        round_bankroll = round_bankroll+table_min_bet*win_check

    return deck, round_bankroll
