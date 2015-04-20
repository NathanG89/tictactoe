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

FONTOBJ = pygame.font.Font('lato.ttf', 48)

#players = Player(0, 'X'), Player(1, 'O'), Player(2, 'W'), Player(3, 'H')
players = Player(0, 'X'), Player(1, 'O')

white = 204, 204, 204
black = 54, 54, 54 
tblack = 54, 54, 54, 128

def random_color():
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

def exit(s):
    for tile in board:
        tile.draw()
    message(s)
    pygame.display.update()
    sleep(3)
    sysexit()

board = create_graphic_board(SIZE)
clock = pygame.time.Clock()
game = Game(players)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            for tile in board:
                if tile.is_clicked():
                    if tile.toggle(game.players[game.current_turn].symbol):
                        if board.has_three_in_a_row():
                            exit('game over, player %d won' % game.current_turn)
                        game.next_player_turn()
    DISPLAY_SURF.fill(black)
    for tile in board:
        tile.draw()
    message("Player %s, it's your turn" % game.current_turn)
    pygame.display.flip()
    clock.tick(60)
