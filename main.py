import random
from collections import defaultdict

def create_deck():
    """Creates and returns a single 52-card deck."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = ranks * 4  #change number it is multiplied by to alter number of decks in play
    return deck

def card_value(card):
    """Returns the blackjack value of a card."""
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11  # handle Ace adjustment later
    else:
        return int(card)

def hand_value(hand):
    """Calculates the best blackjack value for a hand."""
    value = sum(card_value(card) for card in hand)
    aces = hand.count('A')

    # Adjust Aces from 11 to 1 if needed
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value





def deal_card(deck):
    return deck.pop()

def dealer_play(deck, dealer_hand):
    """Dealer hits until hand value is 17 or more."""
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        showDealerHand(dealer_hand,1)
    return dealer_hand

def showDealerHand(dealer_hand,flag):

  if flag == 0:
    handVal = hand_value(dealer_hand[0])
    print(f"Dealer is showing {dealer_hand[0]} - {handVal}")
    return

  elif flag == 1:
    handVal = hand_value(dealer_hand)
    cards = "/".join(dealer_hand)
    print(f"Dealer has {cards} - {handVal}" )
    return

def showHand(player_hand):

  handVal = hand_value(player_hand)
  cards = "/".join(player_hand)
  print(f"Your hand is {cards} - {handVal}")
  return

def isBust(player_hand):
  return hand_value(player_hand) > 21





def main():

  wins = 0
  push = 0
  games = 0
  userInput = ""
  roundOver = False

  print("Welcome to BlackJack!")

  # Create deck instance
  deck = create_deck()
  random.shuffle(deck)

  #deal player and dealer
  player_hand, dealer_hand = [], []
  for _ in range(2):  # deal two rounds
    player_hand.append(deal_card(deck))
    dealer_hand.append(deal_card(deck))

  showHand(player_hand)
  showDealerHand(dealer_hand,0)


  while userInput != "6":

    if roundOver:

      player_hand.clear()
      dealer_hand.clear()

      #need to create a check to see if deck has enough cards
      if len(deck) < 10:
        deck = create_deck()
        random.shuffle(deck)

      for _ in range(2):  # deal two rounds
        player_hand.append(deal_card(deck))
        dealer_hand.append(deal_card(deck))
      games+=1
      roundOver = False

    print("Please select one of the following options...")
    print("1. Repeat dealer's hand")
    print("2. Repeat your hand")
    print("3. Hit")
    print("4. Stand")
    print("5. Display Win percentage")
    print("6. Exit game and display final win percentage")

    userInput = input("Enter choice: ")

    match userInput:

      case "1":
        showDealerHand(dealer_hand,0)

      case "2":
        showHand(player_hand)

      case "3":
        player_hand.append(deal_card(deck))

        if isBust(player_hand):

          print("Bust!")
          showHand(player_hand)
          showDealerHand(dealer_hand,1)
          roundOver = True

        else:
          showHand(player_hand)

      case "4":
        #show dealer's hand, hit until 17 or higher, compare scores
        showDealerHand(dealer_hand,1)
        dealer_play(deck, dealer_hand)

        showHand(player_hand)

        player_score = hand_value(player_hand)
        dealer_score = hand_value(dealer_hand)

        #bust condition is handled in the hit selection

        if player_score == 21:
          wins+=1
        elif dealer_score > 21:
          wins+=1
        elif player_score > dealer_score:
          wins+=1
        elif player_score < dealer_score:
          games+=1
        else:
          push+=1

        roundOver = True

      case "5":
        if games == 0:
          print("No games have been played yet")
        else:
          print((wins/games)*100)
          #print push percentage later
      case _:

        print("Invalid choice")





print("Thanks for playing!")
#create function


main()

