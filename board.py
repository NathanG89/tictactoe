class Square(object):
    def __init__(self, *args, **kwargs):
        try:
            assert len(args) in (0, 1, 2)
        except AssertionError:
            print 'square objects accepts a tuple or coordinate pair!'
        column = kwargs.get('column')
        row = kwargs.get('row')
        if column is not None and row is not None:
            self.row, self.column = row, column
        self.x, self.y = args[0] if isinstance(args[0], tuple) else args
        self.value = kwargs.get('value', None)

    def __repr__(self):
        return '<Square: %r, %r>' % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Square):
            return self.x == other.x and self.y == other.y
        else:
            #assuming input is a tuple
            return (self.x, self.y) == other

    def toggle(self, symbol):
        """toggles state of symbol (if empty)
        returns True, if tile is occupied, returns false"""
        if self.value is None:
            self.value = symbol
            return True
        return False
        #else:
            #raise AttributeError, 'square has already been assigned!'



class Column(object):
    def __init__(self, *args, **kwargs):
        size = kwargs.get('size')
        if len(args) == 1 and (isinstance(args[0], list) or isinstance(args[0], tuple)):
            args = args[0]
        if size:
            self.items = [Column(None, None, None) for i in range(size)]
        else:
            self.items = list(args)
            size = len(args)
        self.size = size
    
    def __repr__(self):
        return '<Column %r>' % (self.items,)

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def is_filled(self):
        symbols = set([item.value for item in self.items])
        return len(symbols) == 1 and None not in symbols

class Grid(Column):
    def __repr__(self):
        return '<Grid %r>' % (self.items,)

    def __iter__(self):
        for x in range(self.size):
            for y in range(self.size):
                yield self[x][y]

    def has_three_in_a_row(self):
        # verticals
        for col in self.items:
            if col.is_filled():
                return True
        # horizontals
        for row in [[col[i] for col in self.items] for i in range(self.size)]:
            symbols = set([item.value for item in row])
            if len(symbols) == 1 and None not in symbols:
                return True
        # diagonals
        for diagonal in [[item[i] for i, item in enumerate(self.items)], [item[i] for i, item in enumerate(self.items[::-1])]]:
            symbols = set([item.value for item in diagonal])
            if len(symbols) == 1 and None not in symbols:
                return True


class Board(object):
    """Uses everything else so far to create a default board. Call
    an instance of this class to get access to a board-like object
    with tile [square] objects that you can access using x,y
    coordinates. Coordinate origin (0,0) is top-left of grid"""
    def __init__(self, size=3):
        self.size = size
        self.grid = Grid(
                         [Column(
                                 [Square(x,y) for y in range(self.size)]
                         ) for x in range(self.size)])

def create_board(size=3):
    """alternative to the board class, returns a grid default,
    filled grid object"""
    return Grid([Column([Square(x,y) for y in range(size)]) for x in range(size)])
