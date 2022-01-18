Blackjack Breaker
---
Author: Bennett Summy


Purpose: 
Virtual blackjack assistant to recommend optimal moves for the user. Moves are recommended based on blackjack "basic strategy." It is based on a standard
dealer versus user blackjack match, with standard blackjack rules.


When complete, the program will have two modes, Auto mode and Live mode.

Auto Mode: 
  Developed primarily for testing and evaluation purposes of the user algorithm. Runs a given number of game tests and outputs the results. Results can be
  "Dealer Win", "User Win", and "Push." For instances where the user is recommended to "double", two wins are countered in one match. Similarly, for "Split"
  the user can win zero, one, or two hands in one match. Therefore, the program will output a "Tests" dictionary, which will show the number of additional hands
  played.
  
Live Mode (incomplete): 
  Usable in a live blackjack game to recommend the optimal move to the user. The user simply needs to enter their own hand, and the dealers up-card to begin 
  the sequence. From there a move will be recommended, and the result of that move will need to be input as well. (For example, if the first move recommends
  "Hit", the user will need to input the card that is drawn.)


This project is coded completely in Python.

Construtcted with self-created classes named Card, Deck, Hand. (Files Card.py, Hand.py, and Deck.py, respectively.) 
Included also is the BlackjackBreakerChart.xls which has all available moves in basic stratagy.
Finally, the BlackjackBreaker.py file which contains the bulk of the game code.


Completed Updates (most recent update first):

  The Housekeeping Update:
      It's like right after you've hosted an racoon birthday party in your home. Everything is strewn everywhere, it looks disgusting, 
      there is trash lying about. So what do you do? You clean it all up! There's still much more cleaning to be done, but it's better. (not clean enough
      to show your parents, but clean enough to invite a couple friends over.)
      
          -Class files were seperated from one large class file ClassCardDeckHand.py to seperate files.
          -Code was re-organized to show a more logical flow of work.
          -Comments and type contracts were updated and clarifed
          -Unnessesary code was removed
          -This README was created!


Later Updates (in no particular order)

  -The Speed Update:
     Code is optimized to have a quicker runtime in Auto mode. 
     
  -The Auto Update:
     The Live Mode is completed to allow games in real time. 
     
  -The Cheater Update:
     Introducing card counting to actively adjust odds based on what cards were drawn in previous hand. Will only make for slight improvements 
     in games with "old" decks, but an improvement nonetheless.
     
  -The Friends Update:
     Playing with multiple people in Live Mode, and the user can input others hands to remove those cards from the stored deck. The more cards
     that are input increases the winning ability of the user.

