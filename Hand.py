""" Author: Bennett Summy
Class Hand

Class to simulate a blackjack hand. Takes inheritiance from ClassDeck class. Initializes with two cards 
using .draw_card() for auto, but user mode will accept card input. More cards can be added to the Hand 
over time, and accessed through cards_in_hand. Specifically built for use in Blackjack, so aspects are
customized for that purpose.
"""
from Deck import *
from Card import *

#for conversion between names of cards and blackjack value cards
#ace can be either 1 or 11 in blackjack, so the value is a tup which must be accessed at index 0: 1 and index 1: 11
#all face cards are worth 10 in blackjack
RANKS_NAMES = {"ace": (11, 1), "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "jack": 10, "queen": 10, "king": 10}

class Hand(Deck):
    """ Hand Class with inheritance from Deck. remove_card, shuffle_deck, and draw_card can all be used. 
    """
    def __init__(self, deck, card1 = None, card2 = None, dealer = False):
        self.dealer = dealer
        self.deck = deck
        self.num_cards_in_hand = 2
        
        if card1 == None:
            card1 = deck.draw_card()
        if card2 == None:
            card2 = deck.draw_card()  

        self.card1 = card1
        self.card2 = card2
        self.cards_in_hand = [self.card1, self.card2]
        
    def __str__(self):
        """ () -> str
        Similar to the print method for a users hand, but adds code to hide the dealers second card. 
        """
        if self.dealer: #when capability for inputting user card is added, make sure card1 isn't the same for dealer and user
            return f"Dealer's Hand: {str(self.card1)} and ???"
        return f"Your Hand: {str(self.card1)} and {str(self.card2)}"
    
    def add_card(self):
        """ () -> Hand

        >>> random.seed(11)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> hand.add_card().print_hand()
        ['Five of Diamonds', 'Two of Spades', 'Five of Hearts']

        >>> random.seed(12)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> hand.add_card().print_hand()
        ['Six of Spades', 'Ace of Clubs', 'Three of Spades']

        >>> random.seed(13)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> hand.add_card().print_hand()
        ['Eight of Clubs', 'Nine of Hearts', 'King of Clubs']
        """
        #only last card will be accessable with self.addtl_card
        card_drawn = (self.deck).draw_card()
        self.addtl_card = card_drawn
        self.cards_in_hand.append(self.addtl_card)
        return self
  
    def print_hand(self): 
        """ () -> Hand
        Prints the hand of the user to avoid printing the location of the memory. Very similar to print_deck(). 
        
        >>> random.seed(11)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> hand.print_hand()
        ['Five of Diamonds', 'Two of Spades']

        >>> random.seed(12)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> hand.print_hand()
        ['Six of Spades', 'Ace of Clubs']

        >>> random.seed(13)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> hand.print_hand()
        ['Eight of Clubs', 'Nine of Hearts']
        """
        str_hand = []
        for card in self.cards_in_hand:
            str_hand.append(str(card))
        return str_hand    
    
    def calculate_hand(self):
        """ () -> int
        Method to calculate the value of a given hand. Aces are assumed to be 11, unless the total value is above 21. 

        >>> random.seed(11)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> print(hand.calculate_hand())
        7
        
        >>> random.seed(12)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> print(hand.calculate_hand())
        17

        >>> random.seed(13)
        >>> deck = ClassDeck()
        >>> hand = Hand(deck)
        >>> print(hand.calculate_hand())
        17
        """
        #local vars
        value = 0
        ace_count = 0
        index = 0 

        for card in self.cards_in_hand: #getting value for each card.
            if card.rank != "ace":
                value += RANKS_NAMES.get(card.rank)
            elif card.rank == "ace":
                value += RANKS_NAMES.get(card.rank)[0]
                ace_count += 1

        while index < ace_count and value > 21: #aces can be 1 or 11, so if value > 21, aces converted to 1. 
            ace_values = RANKS_NAMES.get("ace")
            value -= ace_values[0] 
            value += ace_values[1]
            index += 1 
        return value

    def is_better_hand(self, other):
        """ (Hand) -> bool
        Compares the users hand against the dealers hand, and checks if the user has a better hand. 
        Returns a boolean. Ties are False.
        """
        #compares the users hand against the dealers, and checks if user is greater than. Ties are false.
        return self.calculate_hand() > other.calculate_hand()

    def is_soft_hand(self):
        """ () -> bool
        Checks if the hand contains an ace. If it does contain an ace, this is said to be a "soft" hand.
        Returns a boolean. 
        """
        soft_hand = False
        for card in self.cards_in_hand:
            if card.rank == "ace" and self.calculate_hand() > 21:
                return soft_hand
        return soft_hand

