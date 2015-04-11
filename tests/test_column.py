from board import Column

def test_init():
    column = Column()
    assert column.size == 0
    column = Column(None, None, None)
    assert column.size == 3
    column = Column(None, None)
    assert column.size == 2
    column = Column(None)
    assert column.size == 1
    print column

def test_getitem():
    column = Column(1, None, None)
    assert column[0] == 1

def test_setitem():
    column = Column(1, 2, 3)
    assert (column[0], column[1], column[2]) == (1, 2, 3)
    column[0] = 4
    assert column[0] == 4
