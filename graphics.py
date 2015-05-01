#!/usr/bin/python
from sys import exit as sysexit
import pygame
from time import sleep
from random import randint
from board import Square, Grid, Column
from actors import Player, Game
from menu import Menu, Button, Messenger

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

def message(s, coords=(0,0)):
    messenger.offset = coords
    messenger.draw(DISPLAY_SURF)
    
def create_menu(buttons, offset=(0,0)):
    menu = Menu()
    #buttons = [('quit', sysexit),
    #           ('goodbye', lambda: message),
    #           ('filler option', sysexit),
    #           ('return [doesn\'t work]', sysexit),]
    for i, args in enumerate(buttons):
        b = Button((16,i*FONTSIZE),offset,*args)
        menu.buttons.add(b)
    return menu

"""method runs before the main loop and displays 3 buttons that allow the player
to choose whether they are playing alone, with a friend on the same machine
or over a network, or exit the game."""   

def intro_menu(s):
    """need to have the rest of the game features
    freeze besides menu components"""
    messenger.message = s
    messenger.offset = 32, len(menu.buttons) * 64
    singlePlayBtns = Button((HEIGHT-16,i*FONTSIZE),(0,0))
    buttons = [('Single Player', single_player),
               ('Multi-Player', single_player),
               ('Quit', gameexit)]
    menu = create_menu(buttons, (0,0))
    board = create_graphic_board(SIZE)
    clock = pygame.time.Clock()
    game = Game(players)

    while True:
        DISPLAY_SURF.fill(black)
        redraw_board()
        menu.draw(DISPLAY_SURF)
        messenger.draw(DISPLAY_SURF)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if menu.check_clicked(pygame.mouse.get_pos()):
                    menu.action()
        pygame.display.update()
        clock.tick(FPS)    
        
def single_player(buttons, game, board):
    clock = pygame.time.Clock()
    menu = create_menu(buttons)
    while True:
        DISPLAY_SURF.fill(black)
        redraw_board()
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
                if menu.check_clicked(pygame.mouse.get_pos()):
                    menu.action()
        messenger.message = "Player %s, it's your turn" % game.current_turn
        messenger.draw(DISPLAY_SURF)
        #pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
        
        
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

messenger = Messenger()
intro_menu('Choose an option.')

"""while True:
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
            buttons.is_clicked(buttons)
    DISPLAY_SURF.fill(black)
    redraw_board()
    messenger.message = "Player %s, it's your turn" % game.current_turn
    messenger.draw(DISPLAY_SURF)
    #pygame.display.update()
    pygame.display.flip()
    clock.tick(60)"""
