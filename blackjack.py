"""
Blackjack Game
--------------
Author: Nolan Casey

Description:
This program simulates the classic card game of Blackjack. Players start by buying in with a certain amount of chips 
and placing their bets. The game follows traditional Blackjack rules, where the goal is to have a hand value closest 
to 21 without going over. The player is dealt two cards and can choose to 'hit' (receive another card) or 'stand' 
(end their turn). The dealer then plays, trying to beat the player's hand. Players win, lose, or tie based on the 
comparison of their hand to the dealer's. Winnings and losses are tracked using a virtual chip system.

Features:
- Player can buy in with a desired amount of money.
- Player places bets before each round.
- Comprehensive error handling for invalid inputs.
- Game handles card shuffling, dealing, and hand value calculations, including adjustments for aces.
- Clear display of player and dealer hands, as well as game outcomes.
- Option to play multiple rounds until the player decides to quit or runs out of money.

Enjoy the game and good luck!
"""





# IMPORT MODULES AND DEFINE VARIABLES
import random

# Define suits, ranks, and their corresponding values
suits = ('Hearts','Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

# Initial game state
playing = True 

# CLASSES

# Represents a single card with a suit and rank
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

# Represents a deck of cards
class Deck:
    def __init__(self):
        # Initialize an empty deck
        self.deck = []  
        # Populate the deck with all combinations of suits and ranks
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        # Represent the deck as a string
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The deck has: ' + deck_comp

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.deck)

    # Deal a card from the deck
    def deal(self):
        return self.deck.pop()

# Represents a hand of cards for a player or dealer
class Hand:
    def __init__(self):
        self.cards = []  # List of cards in hand
        self.value = 0   # Total value of cards in hand
        self.aces = 0    # Number of aces in hand

    # Add a card to the hand
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    # Adjust for aces when total value is over 21
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Represents chips for betting
class Chips:
    def __init__(self):
        self.total = 0  # Total chips available
        self.bet = 0    # Current bet amount

    # Player won the bet
    def win_bet(self):
        self.total += self.bet

    # Player lost the bet
    def lose_bet(self):
        self.total -= self.bet

# FUNCTIONS

# Ask the player for a bet
def take_bet(chips):
    if chips.total == 0:
        while True:
            try:
                chips.total = int(input("How much money would you like to buy in with: $"))
                print(f"\nYou have ${chips.total} to play with.")
                break
            except ValueError:
                print("Sorry! Please can you type in a number: ")

    while True:
        try:
            chips.bet = int(input("How much would you like to bet? $"))
            if chips.bet > chips.total:
                print("Your bet can't exceed your total amount of money!")
            else:
                break
        except ValueError: 
            print("Sorry! Please can you type in a number: ")

# Add a card to the hand and adjust for aces if needed
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Ask the player if they want to hit or stand
def hit_or_stand(deck, hand):
    global playing
    while True: 
        ask = input("\nWould you like to hit or stand? Please enter 'h' or 's': ")
        if ask and ask[0].lower() == 'h':
            hit(deck, hand)
        elif ask and ask[0].lower() == 's':
            print("Player stands, Dealer is playing.")
            playing = False 
        else:
            print("Sorry I did not understand that! Please try again!")
            continue
        break

# Show one of the dealer's cards and all of the player's cards
def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden> ")
    print("", dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')

# Show all cards for both the player and dealer
def show_all(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep = '\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')
    print("Player's Hand =", player.value)

# Different game endings
def player_bust(player, dealer, chips):
    print("Player Busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player Wins!")
    chips.win_bet()

def dealer_bust(player, dealer, chips):
    print("Dealer Busts!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer Wins!")
    chips.lose_bet()

def push(player, dealer):
    print("It's a push! Player and Dealer tie!")

# Gameplay
print("Welcome to Blackjack!")
player_chips = Chips()  # Initialize player's chips

while True:    
    deck = Deck()  # Create and shuffle deck
    deck.shuffle()
    
    # Initialize hands for player and dealer
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Ask player for bet and show cards
    take_bet(player_chips)
    show_some(player_hand, dealer_hand)

    # Player's turn
    while playing: 
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        # Check if player busts
        if player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
            break

    # Dealer's turn if player hasn't busted
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)

        # Determine game outcome
        if dealer_hand.value > 21:
            dealer_bust(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
        

    print(f"\nPlayer's winnings stand at: ${player_chips.total}")
    if player_chips.total <= 0:
        print("Game Over you ran out of money.")
        break

    # Ask if player wants to continue
    continue_game = input("Would you like to continue playing? Enter 'y' or 'n': ")
    print('-' * 75)    
    if continue_game[0].lower() == 'y':
        playing = True
    else: 
        print('Thanks for playing!')
        break
