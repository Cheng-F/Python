## paste to run here http://www.codeskulptor.org/
import simplegui
import random
import math

#Global Variables
    
pair1 = [0,1,2,3,4,5,6,7] #first pair of cards
pair2 = [0,1,2,3,4,5,6,7] #second pair of cards
full_deck = [] #here we randomly add the two pair of cards, wich we then shuffle
exposed = []
state = 0 #keep track of current state of the game
card1 = [0,0]
card2 = [0,0]
moves = 0


# helper function to initialize globals
def init():
    global exposed, state, moves
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    state = 0 #keep track of current state of the game
    label.set_text("Moves = 0")
    moves = 0
    #The program creates the deck of cards comprised of
    #the 2 original decks. It fills the full deck while
    #eliminating the elements of the 2 original decks.
    #this simplifies checking for repeated members.

    #elements of pair1 being inserted
    while len(pair1)!=0:
        full_deck.append( pair1.pop( random.randrange( len( pair1))))
    
    #elements of pair2 being inserted
    while len(pair2)!=0:
        full_deck.append( pair2.pop( random.randrange( len( pair2))))
    
    random.shuffle(full_deck)
    
    return  

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    #To know and pair the position of the canvas clicked and the card that is being clicked
    #we divide the pos[0] vs the number 50 and then we round down the result. that will give
    #us the index number o the card on wich we are clicking
    global exposed,state, moves, card1, card2
    
    y = math.floor( pos[0] / 50)
    
    #the program keeps track of how many cards are face up
    #and the moment when it needs to face down and up cards
    #it uses two lists in wich to store the number flipped and its position
    
    if exposed[y] == False and state == 0:
        exposed[y] = True
        card1[0] = full_deck[y]
        card1[1] = y
        state = 1
    elif exposed[y] == False and state == 1:
        exposed[y] = True  
        card2[0] = full_deck[y]
        card2[1] = y
        moves+=1
        if card1[0] == card2[0]:
            exposed[card1[1]] = "Found"
            exposed[y] = "Found"
        state = 2  

    elif exposed[y] == "Found":
        state = state
    else:
        v = 0
        while v <=15: 
            if exposed[v] == True and exposed[v] != "Found":
                exposed[v] = False
            v+=1
            
        exposed[y] = True
        state = 1
        card1[0] = full_deck[y]
        card1[1] = y
        
    label.set_text("Moves = "+str(moves))
    return
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    #here the programs each member of the full_deck
    #in a nice orderly fashion through a for loop
    #if the exposed index is true, the number is shown. Else, the back of the card appears
    global full_deck,exposed
    positionator = 0
    index= 0
    for x in full_deck:
        if exposed[index] == True or exposed[index] == "Found":
            canvas.draw_text(str(x), (1+positionator, 80), 100, "White")
            canvas.draw_line((0+positionator,0), (0+positionator,100), 1,"Red")
            canvas.draw_line((50+positionator,0), (50+positionator,100), 1,"Red")
            positionator+=50
        elif exposed[index] == False or exposed[index] == "Found":
            canvas.draw_polygon([(0+positionator,0),(50+positionator,0),(50+positionator,100),(0+positionator,100)], 1, "Red", "Green")
            positionator+=50
        index+=1
    return


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves =0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()