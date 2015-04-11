from nose.tools import *
from actors import Game

def test_init():
    game = Game()
    assert len(game.players) == 2

def test_player_turns():
    game = Game()
    # set player 0 to go first
    game.players[0].turn = True
    assert game.current_turn == 0
    game.next_player_turn()
    assert game.current_turn == 1
    game.next_player_turn()
    assert game.current_turn == 0
    game.next_player_turn()
    assert game.current_turn == 1
    game.next_player_turn()
    assert game.current_turn == 0
    game.next_player_turn()
    assert game.current_turn == 1
    game.next_player_turn()

@raises(AssertionError)
def test_game_fails():
    game = Game()
    game.players[0].turn = False
    assert game.current_turn == 0
    game.next_player_turn()
    assert game.current_turn == 1
    game.next_player_turn()
    assert game.current_turn == 0
    game.next_player_turn()
    assert game.current_turn == 1
    game.next_player_turn()
