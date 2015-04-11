from actors import Player

def test_init():
    p = Player(0)
    assert p.id == 0
    assert not p.turn
    assert not p.is_my_turn()
    p.toggle_turn()
    assert p.turn
    assert p.symbol == '-'
