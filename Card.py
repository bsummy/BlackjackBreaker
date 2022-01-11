""" Author: Bennett Summy
Class Card

Class to simulate a single card. Created with a rank and a suit, despite the fact suits aren't nescessary
in blackjack. Class Card is used to construct the Deck and Hand classes. Doesn't have any specific methods,
just a constructor and __str__ method. Specifically built for use in Blackjack, so aspects are customized
for that purpose.
"""

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
        if rank not in RANKS_VALUES and rank.lower() not in RANKS_NAMES: #either str or int can be input (ex: three or 3)
            raise AssertionError("The given rank is not a valid rank, please try again.")
        elif suit.lower() not in SUITS: 
            raise AssertionError("The given suit is not a valid suit, please try again.")
        if type(rank) == int: #if a int, transfers to a str.
            rank = RANKS_VALUES.get(rank) 
        
        #assignment of rank & suit
        self.rank = rank
        self.suit = suit
    
    def __str__(self): #fancy print format of a single card
        return f"{self.rank.capitalize()} of {self.suit.capitalize()}"
   