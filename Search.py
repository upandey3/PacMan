import sys
from queue import Queue, LifoQueue, PriorityQueue
import time
import math

# Enum for Search Algorithms
class Algo:
    BFS, DFS, A_STAR, GREEDY = range(4)

class MazeSearch:

    # Constructor
    def __init__(self, grid):
        # Initialize the internal variables
        self.grid = grid       # Intialize the maze grid
        self.frontierSet = {}  # Creating a set of all the nodes that are in the frontier for finding purposes
        self.explored = set()  # Set of all the nodes that have been already explored
        self.dotPositions = self.getDotPositions()          # Get a set of tuples of dot positions
        self.dotCount = len(self.dotPositions)              # Numbers of dots to find (used for goal test)
        self.start = self.getStartPosition()                # Start position as a tuple

    # Given a maze, returns a hashset of tuples - (row, col) positions of all the dots
    def getDotPositions(self):
        return {(j, i) for j, r in enumerate(self.grid) for i, c in enumerate(r) if c == '.'}

    # Given a maze, returns the start point identified by 'P' as a tuple - (row, col)
    def getStartPosition(self):
        for j, r in enumerate(self.grid): # Get the idx, row(string) from grid
            for i, c in enumerate(r): # Get the idx, character from the string
                if c == 'P':
                    return (j, i)
        raise Exception("Could not find the start position - \'P\'")

    # Gets the Manhattan Distance between two coordinates
    def mDistance(self, node1, node2):
        assert(isinstance(node1, tuple) and isinstance(node2, tuple))
        y1, x1 = node1
        y2, x2 = node2
        return abs(x2 - x1) + abs(y2 - y1)
        # return math.sqrt((y2 - y1)**2 + (x2 - x1)**2) # Euclidean distance

    # Check whether a node has not been visited yet
    def isUnexplored(self, node):
        return node not in self.explored and node not in self.frontierSet

    # Gets a list of all the valid neighboring nodes that current node can move to
    def getValidNeighbors(self, pos):
        assert (isinstance(pos, tuple)) # Making sure pos is a type
        l = []     # Initialize the list
        y, x = pos # x = pos[1]; y = pos[0];
        up = (y-1, x)
        right = (y, x+1)
        down = (y+1, x)
        left = (y, x-1)
        # Check if the surrounding nodes are not walls and are unexplored
        if (self.grid[up[0]][up[1]] != '%' and self.isUnexplored(up)): # Upper
            l.append((y-1, x))
        if (self.grid[right[0]][right[1]] != '%' and self.isUnexplored(right)): # Right
            l.append((y, x+1))
        if (self.grid[down[0]][down[1]] != '%' and self.isUnexplored(down)): # Down
            l.append((y+1, x))
        if (self.grid[left[0]][left[1]] != '%' and self.isUnexplored(left)): # Left
            l.append((y, x-1))
        return l

    # Solves a maze based on a given algorithm and returns (grid, path cost)
    def solve(self, algo):

        if algo is Algo.A_STAR or algo is Algo.GREEDY:
            return self.solveAG(algo)

        # Intialize the data structure depending on the Algorithm
        frontier = Queue(maxsize=0) if(algo is Algo.BFS) else LifoQueue(maxsize=0)
        frontier.put((self.start, 0))   # Frontier: ((x, y), path cost) : tuple(tuple(x, y), int)
        self.frontierSet = {self.start} # Creating a set of all the nodes that are in the frontier for finding purposes
        self.explored = set()           # Set of all the nodes that have been already explored

        while not frontier.empty():
            t = frontier.get()      # Remove from frontier

            ##### Visualize the maze solving ######
            time.sleep(0.05)
            print(''.join(self.grid))
            ######################################
            node, cost = t
            self.frontierSet.remove(node)
            self.explored.add(node)    # Add to Explored set
            if node in self.dotPositions:
                self.dotCount -= 1     # If a dot position is found, decrement the count
                if self.dotCount == 0: # Goal test - if all the dot positions have been found
                    return self.grid, cost
            y, x = node; row = self.grid[y] # Get coordinates an corresponding row
            if self.grid[y][x] != 'P':                   # Don't replace the 'P'
                self.grid[y] = row[:x] + '.' + row[x+1:] # Mark the visted node with a '.'
            neighbors = self.getValidNeighbors(node)
            for n in neighbors:           # Put all the valid neighbors in the frontier
                frontier.put((n, cost+1)) # Put in the incremented cost
                self.frontierSet.add(n)

    # Helper function to solve the maze using A* and
    def solveAG(self, algo):

        frontier = PriorityQueue() # Intialize the a priority queue
        dot = (list(self.getDotPositions()))[0]
        score = self.mDistance(self.start, dot) # Manhattan distance for Greedy, MDist + Cost(0) for A*

        frontier.put((score, self.start, 0))   # Frontier: ((x, y), path cost) : tuple(tuple(x, y), int)
        self.frontierSet = {self.start} # Creating a set of all the nodes that are in the frontier for finding purposes
        self.explored = set()           # Set of all the nodes that have been already explored

        while not frontier.empty():
            t = frontier.get()      # Remove from frontier

            ##### Visualize the maze solving ######
            time.sleep(0.05)
            print(''.join(self.grid))
            ######################################
            _, node, cost = t
            self.frontierSet.remove(node)
            self.explored.add(node)    # Add to Explored set
            if node in self.dotPositions:
                self.dotCount -= 1     # If a dot position is found, decrement the count
                if self.dotCount == 0: # Goal test - if all the dot positions have been found
                    return self.grid, cost
            y, x = node; row = self.grid[y] # Get coordinates an corresponding row
            if self.grid[y][x] != 'P':                   # Don't replace the 'P'
                self.grid[y] = row[:x] + '.' + row[x+1:] # Mark the visted node with a '.'
            neighbors = self.getValidNeighbors(node)
            for n in neighbors:           # Put all the valid neighbors in the frontier
                if algo is Algo.A_STAR: # if A*, score is f = g(cost) + h(mDist)
                    score = cost+1 + self.mDistance(n, dot)
                else: # if Greedy, score is Manhattan distance
                    score = self.mDistance(n, dot)
                frontier.put((score, n, cost+1)) # Put in the incremented cost
                self.frontierSet.add(n)



if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise Exception("Need two arguments: script.py maze.txt")
    maze_fname = sys.argv[1]

    with open(maze_fname) as mFile:
        grid = mFile.readlines() # 2D Matrix of rows(string per line) and cols(character per string)

    maze = MazeSearch(grid)
    start = time.time()
    newGrid, cost = maze.solve(Algo.A_STAR)
    end = time.time()
    newMaze = ''.join(newGrid)
    print(newMaze)
    print ("The path cost is "+ str(cost) + " steps")
    print ("Elapsed time: " + str(end - start))

    with open("output.text", "w") as oFile:
        oFile.write(newMaze)
