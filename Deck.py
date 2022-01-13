#Author: Bennett Summy
#Contains 3 classes: Card, Deck, and Hand
#Specifically designed for use in a Blackjack Bot, so certian aspects are customized for that purpose.

import random
import doctest
from Card import *



#global variables
#change to display ranks with first as capital letter
RANKS = ("ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king")
RANKS_NUM = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
SUITS = ("spades", "hearts", "diamonds", "clubs")

#for conversion between values and names of cards
#ace can be either 1 or 11 in blackjack, so the value is a tup which must be accessed at index 0: 1 and index 1: 11
#all face cards are worth 10 in blackjack
RANKS_NAMES = {"ace": (11, 1), "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "jack": 10, "queen": 10, "king": 10}

#does not correspond to the actual values of the cards, just shortcuts to inputting cards
RANKS_VALUES = {1 : "ace", 2 : "two", 3 : "three", 4 : "four", 5 : "five", 6 : "six", 7 : "seven", 8 : "eight", 9: "nine", 10 : "ten", 11: "jack", 12: "queen", 13 : "king"}

class Deck:
    """ Represents a standard deck of cards, out of Cards. Initializes a full deck of cards, and methods reduce cards over time.
    """
    #could add RANKS and SUITS from global variables here to be accessable as a class attribute in deck and hand if needed

    def __init__(self, shuffle = True): #constructor to create a deck
        self.deck_of_cards = []
        for rank_value in RANKS:
            for suit_value in SUITS:
                card = Card(rank_value, suit_value)
                self.deck_of_cards.append(card)
        
        if shuffle: #unless otherwise stated, the deck is shuffled automatically
            self.shuffle_deck()
        
    def print_deck(self):
        """ () -> Deck (possibly list of str)
        Can print an entire deck if needed. Used to avoid memory print. Very similar to print_hand, might be redundant
        >>> deck = Deck(False)
        >>> print_deck = deck.print_deck()
        >>> print_deck[0]
        'Ace of Spades'

        >>> print_deck[51]
        'King of Clubs'

        >>> print_deck[34]
        'Nine of Diamonds'
        """
        str_deck = []
        for card in self.deck_of_cards:
            str_deck.append(str(card))
        return str_deck
    
    def draw_card(self):
        """ () -> Card
        Takes the first card out of the deck and returns the drawn card. That card is no longer in the deck.
        >>> random.seed(11)
        >>> deck = Deck()
        >>> str(deck.draw_card())
        'Five of Diamonds'
        
        >>> random.seed(12)
        >>> deck = Deck()
        >>> str(deck.draw_card())
        'Six of Spades'
        
        >>> random.seed(13)
        >>> deck = Deck()
        >>> str(deck.draw_card())
        'Eight of Clubs'
        """
        card_drawn = self.deck_of_cards[0] #remove top card from the deck, not a random card
        self.deck_of_cards.pop(self.deck_of_cards.index(card_drawn))
        return card_drawn
    
    def shuffle_deck(self):
        """ () -> None
        Shuffles the deck into a new order. Does not return anything. 
        >>> random.seed(11)
        >>> deck = Deck(False)
        >>> deck.shuffle_deck()
        >>> str(deck.draw_card())
        'Five of Diamonds'
        
        >>> random.seed(12)
        >>> deck = Deck(False)
        >>> deck.shuffle_deck()
        >>> str(deck.draw_card())
        'Six of Spades'
        
        >>> random.seed(13)
        >>> deck = Deck(False)
        >>> deck.shuffle_deck()
        >>> str(deck.draw_card())
        'Eight of Clubs'
        """
        random.shuffle(self.deck_of_cards)
    
    def remove_card(self, card_remove):
        print(card_remove)
        print(self.deck_of_cards)
        print(self.deck_of_cards.index(card_remove))
        self.deck_of_cards.pop(self.deck_of_cards.index(card_remove))
        return self.deck_of_cards

    
if __name__ == "__main__":
    doctest.testmod()
    #could add multiple decks in Deck Class
