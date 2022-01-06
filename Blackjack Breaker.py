#Author: Bennett Summy
#Blackjack Assistant: Recommends best move in a blackjack game based on available odds.

#Later Updates to be made:
#import the spreadsheet into the code at the beginning to speed up the process.
#add type contracts and descriptions to all functions
#publish update to github, and add readme on potential updates to come - whenever I have time
#auto-mode is roughly complete, need to make user-mode to make it usable in a real blackjack game
#multiple decks?

from ClassCardDeckHand import *
import copy
import xlrd

RANKS_AXIS = {"ace": "A", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10", "jack": "10", "queen": "10", "king": "10"}

#could probably convert these to code by incrimenting one each way - split prob needs to stay as dict
#converts a card result into a row on my blackjack chart
user_axis_hard = {"H 21" : 1, "H 20" : 2, "H 19" : 3, "H 18" : 4, "H 17" : 5, "H 16" : 6, "H 15" : 7, "H 14" : 8, "H 13" : 9, "H 12" : 10,\
"H 11" : 11, "H 10" : 12, "H 9" : 13, "H 8" : 14, "H 7" : 15, "H 6" : 16, "H 5" : 17, "H 4": 38}

user_axis_soft = {"S 21" : 18, "S 20" : 19, "S 19" : 20, "S 18" : 21, "S 17" : 22, "S 16" : 23, "S 15" : 24, "S 14" : 25, "S 13" : 26}

user_axis_split = {"A-A" : 27, "10-10" : 28, "9-9" : 29, "8-8" : 30, "7-7" : 31, "6-6" : 32, "5-5" : 33, "4-4" : 34, "3-3" : 35, "2-2" : 36, "bust": 37}

#all of these cards have a value of ten in Blackjack
value_ten = ("ten", "jack", "queen", "king")

#converts a dealer result to a collum in the blackjack chart
dealer_axis = {"two" : 1, "three" : 2, "four" : 3, "five" : 4, "six" : 5, "seven" : 6, "eight" : 7, "nine" : 8, "ten" : 9, "ace" : 10}

test_results = {"Dealer Wins" : 0, "Player Wins" : 0, "Push" : 0}
tests_counter = {"Tests": 0, "Splits/Double occurances": 0}

def start_game():
    """ () -> Tup
    Begins a game by creating a deck, dealing hands, and anything else that needs to be done
    """
    deck = Deck()
    return deck

def input_card(deck, auto, quick_format):
    ''' (Deck, bool, bool) -> tup <Card, Deck>
    Function for taking in cards from the user. Takes a deck as parameter. 
    
    If Auto is true, it will draw a card randomly for testing purposes. 

    If quick_format == True, cards are input in '(Rank) (Suit)' format, with Rank being a number 1-13
    (ace low) corresponding to a card. 
    
    If quick_format == False, cards are input in '(Rank) of (Suit)' format with both 
    being fully spelled out. 
    '''
    if auto: #automated for testing mode
        card_drawn = deck.draw_card()
        return card_drawn, deck
    elif not auto: #for use in normal blackjack games
        if quick_format: #rank doesn't actually refer to rank, but to the rank key (1-13) which is associated with a card
            user_card = input("Enter a card. Use '(Rank) (Suit)' format: ")
            split_card = user_card.split(" ")
            rank, suit = split_card
            rank = int(rank)
        elif not quick_format: #slower format but more specific
            user_card = input("Enter a card in your hand? Enter in '(Rank) of (Suit)' format: ")
            split_card = user_card.split(" of ")
            rank, suit = split_card
        
        #creates card objs from input cards
        card_obj = Card(rank, suit)
        reduced_deck = deck.remove_card(card_obj)
        return card_obj, reduced_deck

def remove_card(card_obj, deck):
    ''' (Card, Deck) -> Deck
    Removes card_obj from deck, and returns the deck object. 
    '''
    return deck.remove_card(card_obj)

def hit_to_threshold(hand, value):
    ''' (Hand, int) -> Hand
    Adds to the hand until value is met or exceeded.
    '''
    while hand.calculate_hand() < value:
        hand.add_card()
    return hand

def deal_cards(deck): #later, add capabilites for multiplayer modes using less hard-coded dealing. Just automated section
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
    
def display_hands(user_hand, dealer_hand):
    ''' (Hand, Hand) -> None
    Void funtion to print out each hand and their values. 
    '''
    print("Dealer hand:", dealer_hand)
    print("Dealer score:", dealer_hand.calculate_hand())
    print("User score:", user_hand)
    print("User score:", user_hand.calculate_hand())

def process_to_user_axis(user_hand, split_active):
    """ (Hand, bool) -> str
    Takes a Hand user_hand, and a bool split active to turn a card rank into the format of the blackjack chart.
    Deals with hard or soft hands, and splits.
    """
    user_axis = ""
    
    card1_rank = user_hand.card1.rank
    card2_rank = user_hand.card2.rank

    #turns a user_hand into the user_axis 
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

def rec_first_move(deck, user_hand, dealer_hand, split_active):
    """ (Deck, Hand, Hand, bool) -> str
    Takes two hands, one from the user and one from the dealer, and returns a move to the user from the chart.
    """
    user_axis = process_to_user_axis(user_hand, split_active)
    
    #many cards equal ten in backjack, changing as such to simplify
    dealer_up_card = dealer_hand.card1.rank
    if dealer_up_card in value_ten:
        dealer_up_card = "ten"

    chart_result = chart_call(user_axis, dealer_up_card)
    return chart_result.lower()

def complete_hands(deck, user_hand, dealer_hand, chart_result): #dealing with infinite loops here
    """ (Deck, Hand, Hand, str) -> list <Hand>
    Starts with a hand from the user and the dealer, and the recommended move from the chart on the user_hand.
    Then uses later chart calls to complete hands. if initial chart_result == 'split', there will be two hands in user_hands
    """
    completed_hands = user_hand

    if chart_result == "split": #splits out the hand into two hands
        user_hands = split(deck, user_hand)
        for hand in user_hands: #completes each hand one at a time
            while chart_result != "stand": #continues until a stand, might need to cross out double
                chart_result = rec_first_move(deck, hand, dealer_hand, False)
                chart_result_func = eval(chart_result)
                hand = chart_result_func(deck, hand)
                if chart_result == "double": #ends on a double
                    break
        completed_hands = user_hands   
    
    elif chart_result == "stand": #nothing happens here
        completed_hands = user_hand
    
    elif chart_result == "hit": #card is hit once
        split_active = True
        while chart_result != "stand": #loops until a stand is encountered
            chart_result = rec_first_move(deck, user_hand, dealer_hand, split_active)
            split_active = False
            chart_result_func = eval(chart_result)
            user_hands = chart_result_func(deck, user_hand)
            if chart_result == "double": #ends on a double
                break
        completed_hands = user_hand
   
    elif chart_result == "double": #doubled bet, only one card added to the deck
        chart_result = eval(chart_result)
        user_hand = chart_result(deck, user_hand)
        completed_hands = [user_hand, user_hand] #hand is copied to get accurate results
    else:
        raise AssertionError("There was a problem, somewhere, somehow.")
    
    if type(completed_hands) == list: #for splits and doubles to not add two lists
        return completed_hands
    return [completed_hands]

def hit(deck, user_hand): #adds one card to the hand, and continues 
    return user_hand.add_card()

def split(deck, user_hand): #turns one hand into two hands using the same card
    user_hand1 = Hand(deck, user_hand.card1, deck.draw_card)
    user_hand2 = Hand(deck, user_hand.card2, deck.draw_card)
    return [user_hand1, user_hand2]

def double(deck, user_hand): #same as hit, but hand is doubled later
    user_hand.add_card()
    return user_hand

def stand(deck, user_hand): #does nothing but prevents errors
    return user_hand

def chart_call(user_axis, dealer_up_card):
    """ (str, str) -> str
    Converts the strings of user_axis and dealer_up_card into an index in the chart. 
    Uses the indices to get the optimal results from the chart and returns them as a move
    """
    #turns the user axis into the style of the row names
    if user_axis[0] == "H":
        user_row = user_axis_hard.get(user_axis)
    elif user_axis[0] == "S":
        user_row = user_axis_soft.get(user_axis)
    else: 
        user_row = user_axis_split.get(user_axis)
    
    #turns the dealer axis into the style of columns
    dealer_col = dealer_axis.get(dealer_up_card)

    #calls into the book
    book = xlrd.open_workbook("BlackjackBreakerChart.xls")
    sh = book.sheet_by_index(0)
    chart_result = sh.cell_value(rowx = user_row, colx = dealer_col)
    
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

def test_game():
    """ () -> None
    Simulates one game of Blackjack, with results added into the score. 
    """
    #creates deck, and deals cards
    deck = Deck()
    user_hand, dealer_hand = deal_cards(deck)
    
    #checks into the chart for the first move, completes user_hand(s)
    chart_result = rec_first_move(deck, user_hand, dealer_hand, True)
    user_hands = complete_hands(deck, user_hand, dealer_hand, chart_result)

    #ends dealers turn that's automated to 17
    dealer_done = hit_to_threshold(dealer_hand, 17)
    dealer_score = dealer_done.calculate_hand()
    
    for hand in user_hands: #if split or double means two hands made
        user_score = hand.calculate_hand()
        add_to_score(user_score, dealer_score)

def test(test_runs):
    """ (int) -> None
    Runs through a number of tests to check for bugs and validity of the movements.
    """
    for index in range(test_runs):
        test_game()
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
    test(1000)