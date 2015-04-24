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

"""takes a required argument 's' containing a string, and an optional 
keyword argument 'coords' containing a dictionary of keywords accepted by the 
pygame Rect function"""

def message(s, coords={"left": 0,"top": 0}):
    for tile in board: #loop that redraws the current state of the board to clear out previous messages
        tile.draw()
    msg = FONTOBJ.render(s, True, white, black)
    DISPLAY_SURF.blit(msg, msg.get_rect(**coords))
    pygame.display.update() #updates the display
    
"""Button class.  Initializes each instance with text passed in the argument
'text' and the coordinates from the passed keyword argument 'coords'.
If the coordinates are not passed as a keyword argument, then the default is
set to the center of the screen.  A function is also passed to the 'action'
argument that the button class uses to run a function when clicked"""

"""The 'coords' keyword accepts a dictionary of keywords used by the pygame
Rect function, which is then passed as a set of keywords in and of itself."""    
    
class Button(object):
    def __init__(self, text, action=None, coords={'centerx': 0, 'centery': 0}):
        self.text = text
        self.coords = coords
        self.action = action
        if action is None:
            self.button = FONTOBJ.render(self.text, True, black, gray)
        else:
            self.button = FONTOBJ.render(self.text, True, black, white)
    
    def set_action(self, action=None):
        if action is None:
            self.button = FONTOBJ.render(self.text, True, black, gray)
        else:
            self.button = FONTOBJ.render(self.text, True, black, white)
        self.action = action
    
    def get_action(self):
        return self.action
    
    def set_text(self, text):
        self.text = text
    
    def get_text(self):
        return self.text
    
    def set_coords(self, coords={'centerx': 0, 'centery': 0}):
        self.coords = coords
        
    def get_coords(self):
        return self.coords
        
    def draw(self):
        DISPLAY_SURF.blit(self.button, self.button.get_rect(**self.coords))
        pygame.display.update()
        
    def is_clicked(self): #checks to see if the button was clicked
        x,y = pygame.mouse.get_pos()
        return self.button.get_rect().collidepoint(x,y)
    
    def run(self):
        self.action

def gameexit(s, delay):
    cd = 3 #holds the count down timer value
    message(s) #prints message from the argument variable to the display
    sleep(delay)
    s = 'Closing game...'
    message(s, coords={"centerx": WIDTH/2, "centery": HEIGHT/2}) #prints message to the display
    while cd != 0: #while loop counts down to program closing
        message(s + str(cd), coords={"centerx": WIDTH/2, "centery": HEIGHT/2})
        sleep(1)
        cd -= 1; #count down variable decreased until while loop condition is met
    pygame.quit() #close pygame modules
    sysexit() #closes program

buttons = {'single':Button("Single Player",coords={'centerx':WIDTH/2,'centery':(HEIGHT/2)+30}), 
           'multi':Button("Multiplayer",coords={'centerx':WIDTH/2,'centery':(HEIGHT/2)-30})}
buttons['single'].draw()
buttons['multi'].draw()
board = create_graphic_board(SIZE)
clock = pygame.time.Clock()
game = Game(players)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameexit('Closing game...', 1)
        if event.type == pygame.MOUSEBUTTONUP:
            for tile in board:
                if tile.is_clicked():
                    if tile.toggle(game.players[game.current_turn].symbol):
                        game.next_player_turn()
                    if board.has_three_in_a_row():
                        gameexit('game over, player %d won!' % game.current_turn, 4)
            for button in buttons:
                if buttons[button].is_clicked():
                    buttons[button].run()
    DISPLAY_SURF.fill(black)
    message("Player %s, it's your turn" % game.current_turn)
    pygame.display.flip()
    clock.tick(60)
