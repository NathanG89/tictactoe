from board import Grid, Column, Square, Board, create_board

def test_grids_init():
    column0 = Column(None, None, None)
    grid = Grid([Column(None,None,None) for i in range(3)])
    print type(grid[0])
    assert isinstance(grid[0], Column)

def test_grids_assignment():
    grid = Grid([Column(i, i, i) for i in range(3)])
    assert isinstance(grid[0], Column)
    assert grid[0][0] == 0

    print grid[0][1]
    assert grid[0][1] == 0

    print grid [0][2]
    assert grid[0][2] == 0

    print grid[2][1]
    assert grid[2][1] == 2

def test_grid_assignment0():
    SIZE = 3
    grid = Grid([Column([(x,y) for y in range(SIZE)]) for x in range(SIZE)])
    assert grid[0][0] == (0,0)
    assert grid[1][2] == (1,2)
    for x in range(SIZE):
        for y in range(SIZE):
            assert grid[x][y] == (x, y)

def test_grid_and_squares():
    SIZE = 3
    grid = Grid([Column([Square(x,y) for y in range(SIZE)]) for x in range(SIZE)])
    assert isinstance(grid[0][0], Square)
    square = grid[0][0]
    print square
    assert (square.x, square.y) == (0,0)
    square0 = grid[1][2]
    print square0
    assert (square0.x, square0.y) == (1,2)

def test_iter():
    grid = create_board()
    for square in grid:
        print square

def test_board_grid():
    board = Board()
    print board.grid
    square = board.grid[1][1] 
    assert square == (1,1)

def test_create_board():
    size = 3
    board = create_board(size)
    for x in range(size):
        for y in range(size):
            assert board[x][y] == (x,y)
