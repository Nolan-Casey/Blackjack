#IMPORT MODULES AND DEFINE VARIABLES


import random

suits = ('Hearts','Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True 

# CLASSES

class Card:       # Creates all the cards
    
    def __init__ (self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__ (self):
        return self.rank + ' of ' + self.suit
 
    
class Deck:       # Creates a deck of cards
    
    def __init__ (self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                
    def __str__ (self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The deck has: ' + deck_comp
    
    def shuffle (self):       # Shuffles the deck of cards
         random.shuffle(self.deck)
         
    def deal (self):       # Pick out a card from the deck
        single_card = self.deck.pop()
        return single_card
    

class Hand:      # SHow all the cards that the dearler and player have
    
    def __init__ (self):
        self.cards = []
        self.value = 0
        self.aces = 0     
        
    def add_card (self, card):      # Add a card to the player's or dealer's hand
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
            
    def adjust_for_ace (self):    
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
            
class Chips:      # Keep track of chips
    
    def __init__ (self):
        self.total = 0 
        self.bet = 0
        
    def win_bet (self):
        self.total += self.bet
        
    def lose_bet (self):
        self.total -= self.bet
    
        
# FUNCTIONS

def take_bet(chips):     # Ask for the user's bet
    
    while True:
        try:
            chips.total = int(input("Dealer: How much money would you like to buy in with: $"))
            print("\nYou have $", chips.total, "to play with." )
            chips.bet = int(input("How much would you like to bet? $"))
        except ValueError: 
            print("Sorry! Please can you type in a number: ")
        else:
            if chips.bet > chips.total:
                print("Your bet can't exceed your total amount of money!")
            else:
                break
     
            
def hit (deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
    
def hit_or_stand(deck, hand):       # Hit or Stand
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

    

def show_some (player, dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden> ")
    print("", dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')
    
    
def show_all (player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep = '\n ')
    print("Dealer's Hand = ", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep = '\n ')
    print("Player's Hand = ", player.value)
    
    
# game endings

def player_bust (player, dealer, chips):
    print("Player Busts!")
    chips.lose_bet()
    
    
def player_wins (player, dealer, chips):
    print("Player Wins!")
    chips.win_bet()
    

def delaer_bust (player, dealer, chips):
    print("Dealer Busts!")
    chips.win_bet()
             

def dealer_wins (player, dealer, chips):
    print("Dealer Wins!")
    chips.lose_bet()
    
    
def push(player, dealer):
    print("It's a push! Player and Dealer tie!")
    
    
# Gameplay

print("Welcome to Blackjack!")

while True:    
    
    # create an shuffle deck
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # Set up the player's chips
    player_chips = Chips()
    
    # Ask player for bet
    take_bet(player_chips)
    
    # Show cards
    show_some(player_hand, dealer_hand)
    
    while playing: 
        # Ask player to hit or stand
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        
        if player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
            break
    
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
            
        show_all(player_hand, dealer_hand)
        
        if dealer_hand.value > 21:
            delaer_bust(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
            
        elif player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
            
    print("\nPlayer's winnings stand at", player_chips.total)
    
    continue_game = input("Would you like to continue playing? Enter 'y' or 'n': ")
    print('-' * 75)    
    if continue_game[0].lower() == 'y':
        playing = True
        
    else: 
        print('Thanks for playing!')
        break
    
    
