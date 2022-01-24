""" Author: Bennett Summy
Blackjack Assistant: Recommends best move in a blackjack game based on available odds.
"""
import copy
import random
from datetime import datetime

import xlrd

from Card import *
from Deck import *
from Hand import *

RANKS_AXIS = {"ace": "A", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10", "jack": "10", "queen": "10", "king": "10"}

''' Dictionaries used to convert from the format of the user axis, to a row in the "BlackjackBreakerChart.xls" file. Divided between
"Hard" hands, "Soft" hands, and "Split" hands for simplicity. Meant to exchange for user hands/rows.
'''
USER_AXIS_HARD = {"H 21" : 1, "H 20" : 2, "H 19" : 3, "H 18" : 4, "H 17" : 5, "H 16" : 6, "H 15" : 7, "H 14" : 8, "H 13" : 9, "H 12" : 10,\
"H 11" : 11, "H 10" : 12, "H 9" : 13, "H 8" : 14, "H 7" : 15, "H 6" : 16, "H 5" : 17, "H 4": 37}

USER_AXIS_SOFT = {"S 21" : 19, "S 20" : 20, "S 19" : 21, "S 18" : 22, "S 17" : 23, "S 16" : 24, "S 15" : 25, "S 14" : 26, "S 13" : 27}

USER_AXIS_SPLIT = {"A-A" : 28, "10-10" : 29, "9-9" : 30, "8-8" : 31, "7-7" : 32, "6-6" : 33, "5-5" : 34, "4-4" : 35, "3-3" : 36, "2-2" : 37, "bust": 38}


''' All of these card have a value of ten in Blackjack, so they are swapped out to get the result of the dealer axis. Dictionaries used to
convert from the format of the dealer, to a column in the "BlackjackBreakerChart.xls" file. Exchanges for the dealer up-card/column.
'''
value_ten = ("ten", "jack", "queen", "king")
dealer_axis = {"two" : 1, "three" : 2, "four" : 3, "five" : 4, "six" : 5, "seven" : 6, "eight" : 7, "nine" : 8, "ten" : 9, "ace" : 10}

#Used to keep track of results in Auto Mode.
test_results = {"Dealer Wins" : 0, "Player Wins" : 0, "Push" : 0}
tests_counter = {"Tests": 0, "Splits/Double occurances": 0}

def input_card(deck, auto, quick_format):
    ''' (Deck, bool, bool) -> tup <Card, Deck>
    Function for taking in cards from the user. Takes a deck as parameter. 
    
    If auto evaluates to true, it will draw a card randomly for testing purposes. 

    If quick_format == True, cards are input in '(Rank) (Suit)' format, with Rank being a number 1-13
    (ace low) corresponding to a card. 
    
    If quick_format == False, cards are input in '(Rank) of (Suit)' format with both 
    being fully spelled out. 
    '''
    if auto: #Auto Mode
        card_drawn = deck.draw_card()
        return card_drawn, deck
    elif not auto: #Live Mode
        if quick_format: #rank doesn't actually refer to rank, but to the rank key (1-13) which is associated with a card
            user_card = input("Enter a card. Use '(Rank) (Suit)' format: ")
            split_card = user_card.split(" ")
            rank, suit = split_card
            rank = int(rank)
        elif not quick_format: #Slower format for inputting cards, but more specific
            user_card = input("Enter a card in your hand? Enter in '(Rank) of (Suit)' format: ")
            split_card = user_card.split(" of ")
            rank, suit = split_card
        
        #creates card objs from input cards
        card_obj = Card(rank, suit)
        reduced_deck = deck.remove_card(card_obj)
        return card_obj, reduced_deck

def chart_load(): 
    ''' () -> list
    Loads the BlackjackBreakerChart.xls cell values into a list. Moves are then pulled from the list and returned. 
    This is significantly faster than calling into the chart each time a move is needed.
    '''
    book = xlrd.open_workbook("BlackjackBreakerChart.xls")
    sheet = book.sheet_by_index(0)
    chart_list = []
    for row_index in range(sheet.nrows):
        chart_list.append(sheet.row_values(row_index))
    return chart_list

def start_game():
    ''' () -> Tup
    Begins a game by creating a deck and dealing hands. 
    '''
    deck = Deck()
    user_hand, dealer_hand = deal_cards(deck)
    return deck, user_hand, dealer_hand

def deal_cards(deck):
    ''' (Deck) -> Tup <Hand, Hand>
    Deals cards in order to the user and the dealer (for a two player game). Creates both hands, and returns them in a packed tuple.
    '''
    user_card1 = deck.draw_card()
    dealer_card2 = deck.draw_card()
    user_card2 = deck.draw_card()
    dealer_card1 = deck.draw_card()

    user_hand = Hand(deck, user_card1, user_card2, False)
    dealer_hand = Hand(deck, dealer_card1, dealer_card2, True)
    return user_hand, dealer_hand

def remove_card(card_obj, deck):
    ''' (Card, Deck) -> Deck
    Removes card_obj from deck, and returns the deck object. 
    '''
    return deck.remove_card(card_obj)

def hit_to_threshold(hand, value):
    ''' (Hand, int) -> Hand
    Adds to the hand until value is met or exceeded. Generally used for the dealer to hit to 17.
    '''
    while hand.calculate_hand() < value:
        hand.add_card()
    return hand

def process_to_user_axis(user_hand, split_active, chart_list):
    ''' (Hand, bool) -> str
    Takes a Hand user_hand, and a bool split active to turn a card rank into the format of the blackjack chart.
    Deals with hard or soft hands, and splits.
    '''
    user_axis = ""

    card1_rank = user_hand.card1.rank
    card2_rank = user_hand.card2.rank

    #turns a user_hand into the format of user_axis 
    if card1_rank == card2_rank and split_active:
        both_rank = RANKS_AXIS.get(card1_rank)
        user_axis = f"{both_rank}-{both_rank}"
    elif user_hand.is_soft_hand() == True and user_hand.calculate_hand() <= 21:
        user_axis = f"S {user_hand.calculate_hand()}"
    elif user_hand.is_soft_hand() == False and user_hand.calculate_hand() <= 21:
        user_axis = f"H {user_hand.calculate_hand()}"
    else: 
        user_axis = "bust"
    return user_axis

def rec_move(deck, user_hand, dealer_hand, split_active, chart_list):
    """ (Deck, Hand, Hand, bool) -> str
    Takes two hands, one from the user and one from the dealer, and returns a move to the user from the chart.
    """
    
    user_axis = process_to_user_axis(user_hand, split_active, chart_list)
    
    #many cards equal ten in backjack, changing as such to simplify
    dealer_up_card = dealer_hand.card1.rank
    if dealer_up_card in value_ten:
        dealer_up_card = "ten"

    chart_result = chart_call(user_axis, dealer_up_card, chart_list)
    return chart_result.lower()

def complete_hands(deck, user_hand, dealer_hand, chart_result, chart_list):
    """ (Deck, Hand, Hand, str) -> list <Hand>
    Starts with a hand from the user and the dealer, and the recommended move from the chart on the user_hand.
    Then uses later chart calls to complete hands. if initial chart_result == 'split', there will be two hands in user_hands.
    """
    completed_hands = user_hand
    if chart_result == "split": #splits out the hand into two hands, and adds an extra card per hand
        user_hands = split(deck, user_hand)

        for hand in user_hands: #completes each hand one at a time
            while chart_result != "stand": #continues until a stand
                chart_result = rec_move(deck, hand, dealer_hand, False, chart_list)
                if chart_result == "split":
                    chart_result = "hit"
                chart_result_func = eval(chart_result)
                hand = chart_result_func(deck, hand)
                if chart_result == "double": #ends on a double
                    break
        completed_hands = user_hands   
    
    elif chart_result == "stand": #nothing happens here
        completed_hands = user_hand
    
    elif chart_result == "hit": #card is hit once
        if len(user_hand.cards_in_hand) == 2:
            split_active = True
        else:
            split_active = False
        
        while chart_result != "stand": #loops until a stand is encountered
            if type(user_hand) == list:
                print("hello")
            chart_result = rec_move(deck, user_hand, dealer_hand, split_active, chart_list)
            split_active = False
            chart_result_func = eval(chart_result)
            user_hands = chart_result_func(deck, user_hand)
            if chart_result == "double": #can end on a double
                break
        completed_hands = user_hand
   
    elif chart_result == "double": #doubled bet, only one card added to the hand
        chart_result = eval(chart_result)
        user_hand = chart_result(deck, user_hand)
        completed_hands = [user_hand, user_hand] #hand is copied to show two wins for one hand - signifying a doubled bet
    else:
        raise AssertionError("There was a problem, somewhere, somehow.")
    
    if type(completed_hands) == list: #for splits and doubles to not add two lists
        return completed_hands
    return [completed_hands]

def hit(deck, user_hand):
    '''(Deck, Hand) -> Hand
    Takes a deck and a hand, and returns the hand with a card added. Exact same as double.
    '''
    return user_hand.add_card()

def split(deck, user_hand): 
    '''(Deck, Hand) -> list
    Takes a deck and user_hand. Uses card1 from user_hand and a new card from the deck to create one hand, 
    and card2 to create a second hand. Returns these two hands in a list.
    '''
    user_hand1 = Hand(deck, user_hand.card1, deck.draw_card())
    user_hand2 = Hand(deck, user_hand.card2, deck.draw_card())
    return [user_hand1, user_hand2]

def double(deck, user_hand):
    '''(Deck, Hand) -> Hand
    Takes a deck and a hand, and returns the hand with a card added. Exact same as hit, but exists to prevent errors.
    '''
    return user_hand.add_card()

def stand(deck, user_hand):
    '''(Deck, Hand) -> Hand
    Takes a deck and a hand and returns a hand with no changes made.
    '''
    return user_hand


def chart_call(user_axis, dealer_up_card, chart_list):
    ''' (str, str) -> str
    Converts the strings of user_axis and dealer_up_card into an index in the chart. 
    Uses the indices to get the optimal results from the chart and returns them as a move
    '''
    #turns the user axis into the style of the row names
    if user_axis[0] == "H":
        user_row = USER_AXIS_HARD.get(user_axis)
    elif user_axis[0] == "S":
        user_row = USER_AXIS_SOFT.get(user_axis)
    else: 
        user_row = USER_AXIS_SPLIT.get(user_axis)

    #turns the dealer axis into the style of columns
    dealer_col = dealer_axis.get(dealer_up_card)

    chart_result = (chart_list[user_row] [dealer_col])
    return chart_result

def add_to_score(user_score, dealer_score):
    """ (int, int) -> None
    Controls the automated testing system and logging the wins if the user/dealer/ties
    """
    #print("User: " + str(user_score))
    #print("Dealer: " + str(dealer_score))
    if user_score > 21 or (user_score < dealer_score and dealer_score <= 21):
        test_results["Dealer Wins"] += 1
    elif dealer_score > 21 or (user_score > dealer_score and user_score <= 21):
        test_results["Player Wins"] += 1
    else:
        test_results["Push"] += 1
    
    #everything over test runs means a double or a split occured
    tests_counter["Tests"] += 1 

def test_game(chart_list):
    """ () -> None
    Simulates one game of Blackjack, with results added into the score. 
    """
    #creates deck, deals cards, and loads in the blackjack chart
    deck, user_hand, dealer_hand = start_game()

    #checks into the chart for the first move, completes user_hand(s)
    chart_result = rec_move(deck, user_hand, dealer_hand, True, chart_list)
    user_hands = complete_hands(deck, user_hand, dealer_hand, chart_result, chart_list)

    #ends dealers turn that's automated to 17
    dealer_done = hit_to_threshold(dealer_hand, 17)
    dealer_score = dealer_done.calculate_hand()
    
    for hand in user_hands: #if split or double means two hands are in user_hand
        user_score = hand.calculate_hand()
        add_to_score(user_score, dealer_score)

def test(test_runs):
    """ (int) -> None
    Runs through a number of tests to check for bugs and validity of the movements.
    """
    
    chart_list = chart_load()
    for index in range(test_runs):
        test_game(chart_list)
    percent_test_results = test_results.copy()
    for key in test_results:
        percent_test_results[key] = round(test_results.get(key)/tests_counter.get("Tests")*100, 2)
    
    #prints results of the run
    print(test_results) #number of wins
    print(percent_test_results) #percent wins

    tests_counter["Splits/Double occurances"] = tests_counter.get("Tests") - test_runs
    tests_counter["Tests"] = test_runs
    print(tests_counter) #prints the number of tests

if __name__ == "__main__":
    start_time = datetime.now()
    test(100000)
    end_time = datetime.now()
    print('BJB Runtime Duration: {}'.format(end_time - start_time))
