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

def random_color(): #returns a tuple of randomly generated integers for rgb functions
    return randint(1, 192), randint(1, 192), randint(1, 192)

class Tile(Square):
    def __init__(self, display, *args, **kwargs):
        b_size = WIDTH / SIZE
        Square.__init__(self, *args, **kwargs)
        self.rect = pygame.Rect(self.x * b_size, self.y * b_size, b_size, b_size)
        self.surface = pygame.Surface((b_size, b_size))
        self.surface.fill(random_color())
        #self.display = kwargs.get('display')
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

def message(s):
    msg = FONTOBJ.render(s, True, white, black)
    DISPLAY_SURF.blit(msg, msg.get_rect())

def gameexit(s, delay):
    cd = 3 #holds the count down timer value
    for tile in board: #loop that redraws the current state of the board to clear out previous messages
        tile.draw()
    message(s) #prints message from the argument variable to the display
    pygame.display.update() #updates the display
    sleep(delay)
    s = 'Closing game...'
    for tile in board:
        tile.draw()
    message(s) #prints message to the display
    pygame.display.update()
    while cd != 0: #while loop counts down to program closing
        message(s + str(cd))
        pygame.display.update()
        sleep(1)
        cd -= 1; #count down variable decreased until while loop condition is met
    pygame.quit() #close pygame modules
    sysexit() #closes program

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
                        game.next()
                    if board.has_three_in_a_row():
                        #sleep(4) #adds a delay before the next message
                        gameexit('game over, player %d won!' % game.current_turn, 4)
                    #game.next()
    DISPLAY_SURF.fill(black)
    for tile in board:
        tile.draw()
    message("Player %s, it's your turn" % game.current_turn)
    pygame.display.flip()
    clock.tick(60)
