from board import Grid

def test_init():
    row0 = Grid()
    assert row0.size == 0
    row1 = Grid(None, None, None)
    assert row1.size == 3
    row2 = Grid(None, None)
    assert row2.size == 2
    row3 = Grid(None)
    assert row3.size == 1
    print row2

def test_getitem():
    row0 = Grid(1, None, None)
    assert row0[0] == 1

def test_setitem():
    row = Grid(1, 2, 3)
    assert (row[0], row[1], row[2]) == (1, 2, 3)
    row[0] = 4
    assert row[0] == 4
