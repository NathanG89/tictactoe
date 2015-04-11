from nose.tools import *
from board import Square

def test_init():
    s = Square(1,2)
    p = (3,4)
    t = Square(p, value=1)
    assert s.x == 1
    assert s.y == 2
    assert t.x == 3
    assert t.y == 4

def test_toggle():
    s = Square((0,0))
    s.toggle(1)
    assert s.value == 1

@raises(AttributeError)
def test_toggle_fails():
    s = Square((1,2), value=0)
    s.toggle(2)
