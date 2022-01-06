#Author: Bennett Summy
#Contains 3 classes: Card, Deck, and Hand
#Specifically designed for use in a Blackjack Bot, so certian aspects are customized for that purpose.

import random
import doctest

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

class Card:
    """ Represents a standard playing card, with a rank and suite. If a number is input, it is turned into a word.
    """
    def __init__(self, rank, suit): #creating a single card
        #input validation of ranks & suits in Card creation
        if rank not in RANKS_VALUES and rank.lower() not in RANKS_NAMES: #either word or number can be input (ex: three or 3)
            raise AssertionError("The given rank is not a valid rank, please try again.")
        elif suit.lower() not in SUITS: 
            raise AssertionError("The given suit is not a valid suit, please try again.")
        if type(rank) == int: #if a number, transfers to a word.
            rank = RANKS_VALUES.get(rank) 
        
        #assignment of rank & suit
        self.rank = rank
        self.suit = suit
    
    def __str__(self): #fancy print format of a single card
        return f"{self.rank.capitalize()} of {self.suit.capitalize()}"
    
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
    
class Hand(Deck):
    """ Hand Class with inheritance from Deck. remove_card, shuffle_deck, and draw_card can all be used. 
    """
    def __init__(self, deck, card1 = None, card2 = None, dealer = False):
        self.dealer = dealer
        self.deck = deck
        self.num_cards_in_hand = 2
        #to play games with this deck, these can be changed to be inputs
        self.card1 = deck.draw_card()
        self.card2 = deck.draw_card()
        self.cards_in_hand = [self.card1, self.card2]
        
    def __str__(self):
        """ () -> str
        Similar to the print method for a users hand, but adds code to hide the dealers second card. 
        """
        if self.dealer: #when capability for inputting user card is added, make sure card1 isn't the same for dealer and user
            return f"Dealer's Hand: {str(self.card1)} and ???"
        return f"Your Hand: {str(self.card1)} and {str(self.card2)}"
    
    def print_hand(self): 
        """ () -> Hand
        Prints the hand of the user to avoid printing the location of the memory. Very similar to print_deck(). 
        
        >>> random.seed(11)
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> hand.print_hand()
        ['Five of Diamonds', 'Two of Spades']

        >>> random.seed(12)
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> hand.print_hand()
        ['Six of Spades', 'Ace of Clubs']

        >>> random.seed(13)
        >>> deck = Deck()
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
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> print(hand.calculate_hand())
        7
        
        >>> random.seed(12)
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> print(hand.calculate_hand())
        17

        >>> random.seed(13)
        >>> deck = Deck()
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

    def is_better_hand(self, other): #compares the users hand against the dealers, and checks if user is greater than. Ties are false.
        return self.calculate_hand() > other.calculate_hand()

    def is_soft_hand(self):
        soft_hand = False
        for card in self.cards_in_hand:
            if card.rank == "ace" and self.calculate_hand() > 21:
                soft_hand = True
        return soft_hand

    def add_card(self):
        """ () -> Hand but maybe list of strs

        >>> random.seed(11)
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> hand.add_card().print_hand()
        ['Five of Diamonds', 'Two of Spades', 'Five of Hearts']

        >>> random.seed(12)
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> hand.add_card().print_hand()
        ['Six of Spades', 'Ace of Clubs', 'Three of Spades']

        >>> random.seed(13)
        >>> deck = Deck()
        >>> hand = Hand(deck)
        >>> hand.add_card().print_hand()
        ['Eight of Clubs', 'Nine of Hearts', 'King of Clubs']
        """
        #only last card will be accessable with self.addtl_card
        card_drawn = (self.deck).draw_card()
        self.addtl_card = card_drawn
        self.cards_in_hand.append(self.addtl_card)
        return self

    
if __name__ == "__main__":
    doctest.testmod()
    #could add multiple decks in Deck Class
