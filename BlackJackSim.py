import random as rnd
import numpy as np

# initialize bankroll and table minimum
bankroll = 250
table_min_bet = 15

# shoe designation
num_decks = 1


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
    ace_set = False
    table_set = False
    dealer_set = False
    win_check = 0

    # reset dealer and player cards
    deck = create_deck(num_decks)
    rnd.shuffle(deck)

    # deal player and dealer
    player_cards, dealer_cards = [], []
    for _ in range(2):  # deal two rounds
        player_cards.append(deal_card(deck))
        dealer_cards.append(deal_card(deck))

    # display dealer hand
    print("Dealer: " + str(hand_value(dealer_cards[1])[0]) +
          "\n\t\t___\t\t___\n\t\t| |\t\t|" + dealer_cards[1] + "|\n\t\t---\t\t---")

    # display player hand
    if hand_value(player_cards)[1] == 0:
        print("Player: " + str(hand_value(player_cards)[0]), end="")
        print("\\" + str(hand_value(player_cards)[0]-10) + "\n")
    else:
        print("\nPlayer: " + str(hand_value(player_cards)[0]) + "\n")

    # print player cards
    print_cards(player_cards)

    # check for insurance
    while not ace_set:

        # if dealer has an ace up, ask if player wants insurance
        if hand_value(dealer_cards[1])[1] == 11:
            print("\nInsurance or No? (I/N):")
            player_action = input()

            # if dealer has blackjack, end game and deal with loss condition
            if hand_value(dealer_cards) == 21:
                ace_set = True
                table_set = True
                dealer_set = True

            else:
                print("Safe.")
                ace_set = True
        else:
            ace_set = True

    # player hitting loop, goes until hand is set
    while not table_set:

        # set table if player has 21 already
        if hand_value(player_cards)[0] == 21:
            table_set = True
            dealer_set = True
        else:
            # ask for action
            print("\nHit or Stand? (H/S):")
            player_action = input()

            # if standing, table is set
            if str.lower(player_action) == 's':
                table_set = True
            # if hitting, update table display and counts
            elif str.lower(player_action) == 'h':

                # give player new card and update deck
                player_cards.append(deal_card(deck))

                # display dealer hand

                print("\n\n\n\n\n")
                print("Dealer: " + str(hand_value(dealer_cards[1])[0]) +
                      "\n\t\t___\t\t___\n\t\t| |\t\t|" + dealer_cards[1] + "|\n\t\t---\t\t---")

                # display player hand
                if hand_value(player_cards)[1] == 0:
                    print("Player: " + str(hand_value(player_cards)[0]), end="")
                    print("\\" + str(hand_value(player_cards)[0] - 10) + "\n")
                else:
                    print("\nPlayer: " + str(hand_value(player_cards)[0]) + "\n")

                # print player cards
                print_cards(player_cards)

        # check if player has busted
        if hand_value(player_cards)[0] > 21:
            win_check = -1
            table_set = True
            dealer_set = True

    # display hands after dealer show
    print("\n\n\n\n\n")

    # display dealer hand value
    if hand_value(dealer_cards)[1] == 0:
        print("Dealer: " + str(hand_value(dealer_cards)[0]), end="")
        print("\\" + str(hand_value(dealer_cards)[0] - 10) + "\n")
    else:
        print("\nDealer: " + str(hand_value(dealer_cards)[0]) + "\n")

    # print dealer cards
    print_cards(dealer_cards)

    # print player cards
    print("\nPlayer: " + str(hand_value(player_cards)[0]) + "\n")
    print_cards(player_cards)

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

            print("\n\n\n\n\n")

            # display dealer hand value
            if hand_value(dealer_cards)[1] == 0:
                print("Dealer: " + str(hand_value(dealer_cards)[0]), end="")
                print("\\" + str(hand_value(dealer_cards)[0] - 10) + "\n")
            else:
                print("\nDealer: " + str(hand_value(dealer_cards)[0]) + "\n")

            # print dealer cards
            print_cards(dealer_cards)

            # print player cards
            print("\nPlayer: " + str(hand_value(player_cards)[0]) + "\n")
            print_cards(player_cards)

    # recalculate dealer and player hand
    player_hand_value = hand_value(player_cards)[0]
    dealer_hand_value = hand_value(dealer_cards)[0]

    # win conditions
    if player_hand_value == 21 and len(player_cards) == 2:  # player blackjack
        print("\nBlackJack!")
        print("You Won!")
        win_check = 1.5
    elif dealer_hand_value == 21 and len(dealer_cards) == 2:  # dealer blackjack
        print("\nDealer BlackJack!")
        if str.lower(player_action) == 'i':
            print("Insurance Push.")
            win_check = 0
        elif str.lower(player_action) == 'n':
            print("You Lost.")
            win_check = -1
    elif player_hand_value > 21:  # player bust
        print("\nBusted!")
        print("You Lost.")
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

    # adjust and print bankroll
    bankroll = bankroll+table_min_bet*win_check
    print("Bankroll: " + str(bankroll))

    # ask to keep playing
    print("Press any key to go again, or Q to exit.")
    player_action = input()

    if str.lower(player_action) == "q":
        play_hand = False
    else:
        print("\n")

