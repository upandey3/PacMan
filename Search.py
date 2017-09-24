import sys

# Analyzes a new maze to return the row,col positions of all the dots
def getDotPositions(grid):
    return [(j, i) for j, r in enumerate(grid) for i, c in enumerate(r) if c == '.']

# if len(sys.argv) < 2:
#     raise Exception("Need two arguments: script.py maze.txt")
# print(sys.argv)
# maze_fname = sys.argv[1]
maze_fname = "MediumMaze.txt"
maze_fname = "BigMaze.txt"
maze_fname = "TinySearch.txt"

with open(maze_fname) as mFile:
    grid = mFile.readlines() # 2D Matrix

print(getDotPositions(grid))
