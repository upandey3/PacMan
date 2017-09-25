import sys
from queue import *
# Analyzes a new maze to return the row,col positions of all the dots
def getDotPositions(grid):
    return {(j, i) for j, r in enumerate(grid) for i, c in enumerate(r) if c == '.'}

def getStartPosition(grid):
    return [(j, i) for j, r in enumerate(grid) for i, c in enumerate(r) if c == 'P']

def getValidNeighbors(grid, pos, explored, frontierList):
    # assert (type(position) == 'tuple')
    x = pos[1]
    y = pos[0]
    l = []
    # for row in grid:
    #     print(row)
    up = (y-1, x)
    right = (y, x+1)
    down = (y+1, x)
    left = (y, x-1)

    if (grid[up[0]][up[1]] != '%' and up not in explored and up not in frontierList): # Upper
        l.append((y-1, x))
    if (grid[right[0]][right[1]] != '%' and right not in explored and right not in frontierList): # Right
        l.append((y, x+1))
    if (grid[down[0]][down[1]] != '%' and down not in explored and down not in frontierList): # Down
        l.append((y+1, x))
    if (grid[left[0]][left[1]] != '%' and left not in explored and left not in frontierList): # Left
        l.append((y, x-1))
    return l

# Returns a grid
def graphSearch(grid, bfs = True):
    dotPositions = getDotPositions(grid)
    dotCount = len(dotPositions)
    # print(dotCount)
    start = getStartPosition(grid)
    frontier = Queue(maxsize=0) if(bfs) else LifoQueue(maxsize=0)
    frontier.put(start[0])
    frontierList = [start[0]]
    explored = set()

    while not frontier.empty():
        node = frontier.get()
        explored.add(node)
        frontierList.remove(node)
        if node in dotPositions:
            dotCount -= 1 #decrease

            if dotCount == 0: # Goal test
                return grid
        x = node[1]
        y = node[0]
        row = grid[y]
        if grid[y][x] != 'P':
            grid[y] = row[:x] + '.' + row[x+1:]
        # row = grid[y]
        neighbors = getValidNeighbors(grid, node, explored, frontierList)
        for n in neighbors:
            frontier.put(n)
            frontierList.append(n)

# if len(sys.argv) < 2:
#     raise Exception("Need two arguments: script.py maze.txt")
# print(sys.argv)
# maze_fname = sys.argv[1]
maze_fname = "MediumMaze.txt"
# maze_fname = "BigMaze.txt"
# maze_fname = "TinySearch.txt"

with open(maze_fname) as mFile:
    grid = mFile.readlines() # 2D Matrix
# for row in grid:
#     print(row)
# print(grid)

# a = Queue(maxsize = 0)
# b = LifoQueue(maxsize = 0)
# startPosition = getStartPosition(grid)
# print(startPosition)
newMaze = ''.join(graphSearch(grid, False))
print(newMaze)
