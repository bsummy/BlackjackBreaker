#Author: Bennett Summy
#Blackjack Assistant: Recommends best move in a blackjack game based on available odds.
from ClassCardDeckHand import *

def start_game():
    deck = Deck()
    return deck

def input_card(quick_format):
    if quick_format:
        user_card = input("Enter a card. Use '(Rank) (Suit)' format: ")
        split_card = user_card.split(" ")
        rank, suit = split_card
        rank = int(rank)
    elif not quick_format:
        user_card = input("Enter a card in your hand? Enter in '(Rank) of (Suit)' format: ")
        split_card = user_card.split(" of ")
        rank, suit = split_card
    card_obj = Card(rank, suit)
    return card_obj

if __name__ == "__main__":
    card = input_card(True)