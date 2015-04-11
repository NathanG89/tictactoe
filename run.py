from board import Square, Grid, Column

SIZE = 3

grid = Grid([Column([(i,j) for j in range(SIZE)]) for i in range(SIZE)])

print grid
