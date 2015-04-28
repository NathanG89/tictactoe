#!/usr/bin/python
from sys import exit as sysexit
import pygame
from time import sleep
from random import randint
from board import Square, Grid, Column
from actors import Player, Game

pygame.init()

WIDTH, HEIGHT = 640, 640
SIZE = 3
DISPLAY_SURF = pygame.display.set_mode((WIDTH,HEIGHT))

FONTOBJ = pygame.font.SysFont('Sans', 48, False, False)#('lato.ttf', 48)

#players = Player(0, 'X'), Player(1, 'O'), Player(2, 'W'), Player(3, 'H')
players = Player(0, 'X'), Player(1, 'O')

white = 204, 204, 204
black = 54, 54, 54 
tblack = 54, 54, 54, 128
gray = 128, 128, 128

def random_color(): #returns a tuple of randomly generated integers for rgb functions
    return randint(1, 192), randint(1, 192), randint(1, 192)

class Tile(Square):
    def __init__(self, display, *args, **kwargs):
        b_size = WIDTH / SIZE
        Square.__init__(self, *args, **kwargs)
        self.rect = pygame.Rect(self.x * b_size, self.y * b_size, b_size, b_size)
        self.surface = pygame.Surface((b_size, b_size))
        self.surface.fill(random_color())
        self.display = display

    def draw(self):
        self.display.blit(self.surface, self.rect)
        symbol = FONTOBJ.render(self.value, True, white)
        self.display.blit(symbol, (self.rect.centerx - symbol.get_rect().centerx, self.rect.centery - symbol.get_rect().centery))

    def is_clicked(self):
        x,y = pygame.mouse.get_pos()
        return self.rect.collidepoint(x,y)

def create_graphic_board(size=SIZE):
    return Grid([Column([Tile(DISPLAY_SURF, x,y) for y in range(size)]) for x in range(size)])

def redraw_board():
    for tile in board: #loop that redraws the current state of the board to clear out previous messages
        tile.draw()

"""takes a required argument 's' containing a string, and an optional 
keyword argument 'coordsBtn' containing a dictionary of keywords accepted by the 
pygame Rect function"""

def message(s, coords={"left": 0,"top": 0}):
    #for tile in board: #loop that redraws the current state of the board to clear out previous messages
        #tile.draw()
    msg = FONTOBJ.render(s, True, white, black)
    DISPLAY_SURF.blit(msg, msg.get_rect(**coords))
    #pygame.display.update() #updates the display
    
"""Button class.  Initializes each instance with textBtn passed in the argument
'textBtn' and the coordinates from the passed keyword argument 'coordsBtn'.
If the coordinates are not passed as a keyword argument, then the default is
set to the center of the screen.  A function is also passed to the 'action'
argument that the button class uses to run a function when clicked"""

"""The 'coordsBtn' keyword accepts a dictionary of keywords used by the pygame
Rect function, which is then passed as a set of keywords in and of itself.

~Nate"""    
    
class Button(object):
    def __init__(self, text="Button", disabled=True, coords={'centerx': 0, 'centery': 0}):
        self.textBtn = text
        self.coordsBtn = coords
        self.disabledBtn = disabled
        if self.disabledBtn == True:
            self.button = FONTOBJ.render(self.textBtn, True, black, gray)
        else:
            self.button = FONTOBJ.render(self.textBtn, True, black, white)
    
#    @setter
#    def disabledBtn(self):
#        if self.disabledBtn == True:
#            self.button = FONTOBJ.render(self.textBtn, True, black, gray)
#        else:
#            self.button = FONTOBJ.render(self.textBtn, True, black, white)
    
#    def set_action(self, args=None, kwargs=None, action=None):
#        if action is None:
#            self.button = FONTOBJ.render(self.textBtn, True, black, gray)
#        else:
#            self.button = FONTOBJ.render(self.textBtn, True, black, white)
#        self.action = action
#        self.args = args
#        self.kwargs = kwargs
        
    def draw(self):
        DISPLAY_SURF.blit(self.button, self.button.get_rect(**self.coordsBtn))
        
    def is_clicked(self): #checks to see if the button was clicked
        x,y = pygame.mouse.get_pos()
        if self.disabledBtn == False:
            return self.button.get_rect().collidepoint(x,y)
        else:
            return False
    
#    def run(self):
#        if self.args == None and self.kwargs == None:
#            self.action()
#        elif not self.args == None and self.kwargs == None:
#            self.action(*self.args)
#        elif self.args == None and not self.kwargs == None:
#            self.action(**self.kwargs)
#        else:
#            self.action(*self.args, **self.kwargs)
        
"""method that renders messages to the display surface before closing the program.

messages are passed to the method as an array of tuples, where the first 
item in the tuple is the string message and the second is the amount of delay
set before the next message can be rendered.

the coordsBtn keyword sets where the messages will be displayed in relation to 
the display surface.  At this time I have only implemented passing 1 set of 
coordinates, so all the messages will display in one location.  the closing
message is set to displayin the center by default.

~Updates By: Nate
~Original Author: James"""

def gameexit(info, coords={"left":0,"right":0}):
    cd = 3 #holds the count down timer value
    for text, delay in info: #while loop counts down to program closing
        redraw_board()
        message(text, coords) #prints message from the argument variable to the display
        pygame.display.update()
        sleep(delay)
    while cd != 0:
        redraw_board()
        message("Closing game in" + str(cd), coords={"centerx": WIDTH/2, "centery": HEIGHT/2})
        pygame.display.update()
        cd -= 1; #count down variable decreased until while loop condition is met
        sleep(1)
    pygame.quit() #close pygame modules
    sysexit() #closes program
    
"""method runs before the main loop and displays 2 buttons that allow the player
to choose whether they are playing alone or with a friend on the same machine
or over a network."""
    
def mode():
    mode = None
    modeButtons = {'single':Button(text="Single Player",disabled=False,coords={'centerx':WIDTH/2,'centery':(HEIGHT/2)-30}), 
           'multi':Button(text="Multiplayer",disabled=False,coords={'centerx':WIDTH/2,'centery':(HEIGHT/2)+30})}
    DISPLAY_SURF.fill(black)
    redraw_board()
    modeButtons['multi'].draw()
    modeButtons['single'].draw()
    pygame.display.flip()
    while mode == None:
        for button in modeButtons:
            if modeButtons[button].is_clicked():
                mode = button
                #modeButtons[button].run()
    redraw_board()
    return mode        

buttons = {}
board = create_graphic_board(SIZE)
clock = pygame.time.Clock()
game = Game(players)
mode = mode()
text = 'Currently playing in ' + mode  + ' player mode'
message(text, coords)
sleep(4)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameexit([('Closing game...', 1)], coords={"centerx": WIDTH/2, "centery": HEIGHT/2})
        if event.type == pygame.MOUSEBUTTONUP:
            for tile in board:
                if tile.is_clicked():
                    if tile.toggle(game.players[game.current_turn].symbol):
                        game.next_player_turn()
                    if board.has_three_in_a_row():
                        gameexit([('game over, player %d won!' % game.current_turn, 4)])
            for button in buttons:
                if buttons[button].is_clicked():
                    buttons[button].run()
    DISPLAY_SURF.fill(black)
    redraw_board()
    message("Player %s, it's your turn" % game.current_turn)
    #pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
