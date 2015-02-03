#Blackjack
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("https://www.dropbox.com/s/6qcj93jak68sdk3/cards.jfitz.png?dl=1")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("https://www.dropbox.com/s/hhpvjbcsc7ci73k/card_back.png?dl=1")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
pc_sum = 0
player_sum = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.lst = []
        # create Hand object
    def __str__(self):    

        ans = ""
        for i in range(len(self.lst)):
            
            ans += str(self.lst[i]) + " "
        return ans
    def add_card(self, card):
        card = Card(random.choice(SUITS),random.choice(RANKS))
        self.lst.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = [0,0]
        hand_ranks =[]
        for card in self.lst:  
            hand_value[0] += VALUES[card.get_rank()]
            hand_value[1] += VALUES[card.get_rank()]
            hand_ranks.append(card.get_rank())
        if "A" in hand_ranks :
            hand_value[1] += 10
        return hand_value
             
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_offset = 80
        offset = 0
        for card in self.lst:
            card.draw(canvas, [pos[0] + offset, pos[1]])
            offset += card_offset
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck=[]# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
        
    def shuffle(self):
        # shuffle the deck 
         # use random.shuffle()
        random.shuffle(self.deck)
        return self.deck

    def deal_card(self):
        # deal a card object from the deck
        for card in self.deck:
            deal_card= card(suit,rank)
            self.deck.remove(deal_card)
            return deal_card
    
    def __str__(self):
        # return a string representing the deck
        test = ""
        for card in self.deck:
            test += str(card)+""
        return test 

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, pc_hand,score,pc_sum,player_sum

    # your code goes here    
    in_play = True
    player_hand = Hand()
    pc_hand = Hand()
    deck = Deck()
    player_hand.add_card(deck.deal_card)
    player_hand.add_card(deck.deal_card)
    
    pc_hand.add_card(deck.deal_card)
    
    ans1 = pc_hand.get_value()
    if ans1[1] <= 21:
        pc_sum = ans1[1]
    else:
        pc_sum = ans1[0]
      
    ans = player_hand.get_value()
    if ans[1] <= 21:
        player_sum = ans[1]
    else:
        player_sum = ans[0]  
    if ans[1] == 21:
        outcome = "Blackjack !    You win !"
        score += 1
        in_play = False
    elif ans[0] < 21:
        outcome = "Hit or Stand ?"
    

def hit():

    # if the hand is in play, hit the player   
    # if busted, assign a message to outcome, update in_play and score
    global player_sum, outcome, score, in_play
    deck = Deck()
    if in_play == True:
        player_hand.add_card(deck.deal_card)
    else:
        score -= 0
    ans = player_hand.get_value()  
    if ans[1] <= 21:
        player_sum = ans[1]
    else:
        player_sum = ans[0]
    
    if player_sum > 21:
        outcome = "You are busted!"
        score -=1
        in_play = False
        
def stand():
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    global score,outcome,in_play,pc_sum
    if in_play == False:
        score -= 0
    else:
        
        ans1 = pc_hand.get_value()
        if ans1[1] <= 21:
            pc_sum = ans1[1]
        else:
            pc_sum = ans1[0]
        if pc_sum == 21 and len(pc_hand.lst) == 2:
            outcome = "Blackjack ! Computer wins !"
            score -= 1
            in_play = False
        deck = Deck()
        while pc_sum <= 16:
            pc_hand.add_card(deck.deal_card)
            ans1 = pc_hand.get_value()
            if ans1[1] <= 21:
                pc_sum = ans1[1]
            else:
                pc_sum = ans1[0]
        if pc_sum > 21:
             outcome = " Computer is busted! You win!"
             score += 1
             in_play = False
        elif player_hand.get_value == pc_hand.get_value:
             outcome = "Even"
             in_play = False
        elif pc_sum < player_sum:
             outcome = "You win !"
             score += 1
             in_play = False
        elif pc_sum > player_sum and pc_sum <= 21:
             outcome = "Computer wins !"
             score += -1
             in_play = False
    if in_play == False:
            score += 0
           
                             
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK",(160,60),45,"AQUA")
    canvas.draw_text("Score = "+str(score), (400,100),27,"black")
    canvas.draw_text(outcome,(150,450),20,"blue")
    canvas.draw_text("Dealer's cards",(50,130),18,"white")
    canvas.draw_text("Sum: "+str(pc_sum),(250,130),18,"white")
    canvas.draw_text("Player's cards",(50,280),18,"white")
    canvas.draw_text("Sum: "+str(player_sum),(250,280),18,"white")
    pc_hand.draw(canvas,(50,140))
    player_hand.draw(canvas,(50,290))
    
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)



# get things rolling
deal()
frame.start()


# remember to review the gradic rubric