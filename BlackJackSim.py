
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


# print cards
def print_cards(current_cards):
    for i in current_cards:
        print("\t\t___", end="")
    print("")
    for i in np.arange(len(current_cards)):
        print("\t\t|" + str(current_cards[i]) + "|", end="")
    print("")
    for i in current_cards:
        print("\t\t___", end="")


# initialize playing loop
play_hand = True
while play_hand:

    # bet and print bankroll
    print("Bankroll: " + str(bankroll))

    # reset loop variables
    ace_set = num_players*[False]
    player_set = num_players*[False]
    dealer_set = False
    win_check = 0

    # reset dealer and player cards
    deck = create_deck(num_decks)
    rnd.shuffle(deck)

    # deal and players
    dealer_cards = []
    players = [[] for i in np.arange(num_players)]
    for r in range(2):  # deal two rounds
        for p in np.arange(num_players):
            players[p].append(deal_card(deck))
        dealer_cards.append(deal_card(deck))

    # display dealer hand
    print("Dealer: " + str(hand_value(dealer_cards[1])[0]) +
          "\n\t\t___\t\t___\n\t\t| |\t\t|" + dealer_cards[1] + "|\n\t\t---\t\t---")

    # if dealer has an ace up, ask if players want insurance
    if hand_value(dealer_cards[1])[1] == 0:

        # initialize insurance holders
        player_insurance = num_players*[0]

        # loop through all players
        for p in np.arange(num_players):
            player_cards = players[p]

            # display player hand
            if hand_value(player_cards)[1] == 0:
                print("Player " + str(p + 1) + ": " + str(hand_value(player_cards)[0]), end="")
                print("\\" + str(hand_value(player_cards)[0] - 10) + "\n")
            else:
                print("\nPlayer " + str(p + 1) + ": " + str(hand_value(player_cards)[0]) + "\n")

            # print player cards
            print_cards(player_cards)

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

        # display player hand
        if hand_value(player_cards)[1] == 0:
            print("Player " + str(p + 1) + ": " + str(hand_value(player_cards)[0]), end="")
            print("\\" + str(hand_value(player_cards)[0] - 10) + "\n")
        else:
            print("\nPlayer " + str(p + 1) + ": " + str(hand_value(player_cards)[0]) + "\n")

        # player hitting loop, goes until hand is set
        while not player_set[p]:

            # print player cards
            print_cards(player_cards)

            # set player if they have 21 already
            if hand_value(player_cards)[0] == 21:
                print("\nBlackJack!")
                player_set[p] = True
            else:
                # ask for action
                print("\nHit or Stand? (H/S):")
                player_action = input()

                # if standing, table is set
                if str.lower(player_action) == 's':
                    player_set[p] = True
                # if hitting, update table display and counts
                elif str.lower(player_action) == 'h':

                    # give player new card and update deck
                    player_cards.append(deal_card(deck))

                    # display dealer hand
                    print("Dealer: " + str(hand_value(dealer_cards[1])[0]) +
                          "\n\t\t___\t\t___\n\t\t| |\t\t|" + dealer_cards[1] + "|\n\t\t---\t\t---")

                    # display player hand
                    if hand_value(player_cards)[1] == 0:
                        print("Player " + str(p+1) + ": " + str(hand_value(player_cards)[0]), end="")
                        print("\\" + str(hand_value(player_cards)[0] - 10) + "\n")
                    else:
                        print("\nPlayer " + str(p+1) + ": " + str(hand_value(player_cards)[0]) + "\n")

                    # print player cards
                    print_cards(player_cards)

            # check if player has busted
            if hand_value(player_cards)[0] > 21:
                win_check = -1
                player_set[p] = True
        time.sleep(1.5)

    # display hands after dealer show
    print("\n\n\n\n\n\n\n")

    # display dealer hand value
    if hand_value(dealer_cards)[1] == 0:
        print("Dealer: " + str(hand_value(dealer_cards)[0]), end="")
        print("\\" + str(hand_value(dealer_cards)[0] - 10) + "\n")
    else:
        print("\nDealer: " + str(hand_value(dealer_cards)[0]) + "\n")

    # print dealer cards
    print_cards(dealer_cards)

    # # print player cards
    # for p in np.arange(num_players):
    #     player_cards = players[p]
    #     print("\nPlayer " + str(p+1) + ": " + str(hand_value(player_cards)[0]) + "\n")
    #     print_cards(player_cards)

    time.sleep(1.5)

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

            print("\n\n\n\n\n\n\n")

            # display dealer hand value
            if hand_value(dealer_cards)[1] == 0:
                print("Dealer: " + str(hand_value(dealer_cards)[0]), end="")
                print("\\" + str(hand_value(dealer_cards)[0] - 10) + "\n")
            else:
                print("\nDealer: " + str(hand_value(dealer_cards)[0]) + "\n")

            # print dealer cards
            print_cards(dealer_cards)

            # print player cards
            # for p in np.arange(num_players):
            #     player_cards = players[p]
            #     print("\nPlayer " + str(p+1) + ": " + str(hand_value(player_cards)[0]) + "\n")
            #     print_cards(player_cards)
            time.sleep(1.5)

    # loop through players again to determine winnings
    for p in np.arange(num_players):
        player_cards = players[p]

        # display player hand
        if hand_value(player_cards)[1] == 0:
            print("Player " + str(p + 1) + ": " + str(hand_value(player_cards)[0]), end="")
            print("\\" + str(hand_value(player_cards)[0] - 10) + "\n")
        else:
            print("\nPlayer " + str(p + 1) + ": " + str(hand_value(player_cards)[0]) + "\n")

        # print player cards
        print_cards(player_cards)

        # recalculate dealer and player hand
        player_hand_value = hand_value(player_cards)[0]
        dealer_hand_value = hand_value(dealer_cards)[0]

        # win conditions
        if player_hand_value == 21 and len(player_cards) == 2:  # player blackjack
            print("BlackJack! You Won!")
            win_check = 1.5
        elif dealer_hand_value == 21 and len(dealer_cards) == 2:  # dealer blackjack
            print("Dealer BlackJack!", end="")
            if str.lower(player_action) == 'i':
                print("Insurance Push.")
                win_check = 0
            elif str.lower(player_action) == 'n':
                print("You Lost.")
                win_check = -1
        elif player_hand_value > 21:  # player bust
            print("Busted! You Lost.")
            win_check = -1
        elif dealer_hand_value > 21:  # dealer bust
            print("\nYou Won!")
            win_check = 1
        elif dealer_hand_value > player_hand_value:  # dealer win with higher number
            print("\nYou Lost.")
            win_check = -1
        elif dealer_hand_value == player_hand_value:  # push
            print("\nCards Pushed.")
            win_check = 0
        else:  # player wins everything else
            print("\nYou Won!")
            win_check = 1

        # adjust bankroll
        bankroll = bankroll+table_min_bet*win_check

    # ask to keep playing
    print("Bankroll: " + str(bankroll))
    print("Press any key to go again, or Q to exit.")
    player_action = input()

    if str.lower(player_action) == "q":
        play_hand = False
    else:
        print("\n\n")
