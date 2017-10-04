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
        self.explored = set()  # Set of all the nodes that have been already explored
        self.dotPositions = self.getDotPositions()          # Get a set of tuples of dot positions
        self.dotCount = len(self.dotPositions)              # Numbers of dots to find (used for goal test)
        self.start = self.getStartPosition()                # Start position as a tuple
        self.parents = {}
        self.frontierMap = {}    # Creating a map of all the nodes that are in the frontier for finding purposes

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

    # Check whether a node has not been visited yet
    def isUnexplored(self, node):
        return node not in self.explored and node not in self.frontierSet

    # Gets a list of all the non-wall neighboring that current node can move to
    def getNeighbors(self, pos):
        assert (isinstance(pos, tuple)) # Making sure pos is a type
        l = []     # Initialize the list
        y, x = pos # x = pos[1]; y = pos[0];
        up = (y-1, x)
        right = (y, x+1)
        down = (y+1, x)
        left = (y, x-1)

        # Check if the surrounding nodes are not walls and are unexplored
        if self.grid[up[0]][up[1]] != '%': # Upper
            l.append((y-1, x))
        if self.grid[right[0]][right[1]] != '%': # Right
            l.append((y, x+1))
        if self.grid[down[0]][down[1]] != '%': # Down
            l.append((y+1, x))
        if self.grid[left[0]][left[1]] != '%': # Left
                l.append((y, x-1))

        return l

    # Solves a maze based on a given algorithm and returns (grid, path cost, number of nodes expanded)
    def solve(self, algo):

        if algo is Algo.A_STAR or algo is Algo.GREEDY:
            return self.solveAG(algo)

        # Intialize the data structure depending on the Algorithm
        dots = self.getDotPositions()
        frontier = Queue(maxsize=0) if(algo is Algo.BFS) else LifoQueue(maxsize=0)
        frontier.put((self.start, 0, dots))   # Frontier: ((x, y), path cost) : tuple(tuple(x, y), int)
        frontierSet = {self.start} # Creating a set of all the nodes that are in the frontier for finding purposes
        self.explored = set()           # Set of all the nodes that have been already explored
        self.parents[self.start] = -1

        while not frontier.empty():
            t = frontier.get()      # Remove from frontier

            ##### Visualize the maze solving ######
            # time.sleep(0.05)
            # print(''.join(self.grid))
            ######################################
            node, cost, dots = t
            frontierSet.remove(node)
            self.explored.add(node)    # Add to Explored set
            if node in dots:
                dots = set(dots)   # Create a dots set
                dots.remove(node)  # If a dot position is found, remove it from the dots set
                if len(dots) == 0: # Goal test - if all the dot positions have been found
                    self.markSolutionDB(node)
                    return self.grid, cost, len(self.explored)

            #### Code for printing all explored paths. Helps in Visualization #####
            # y, x = node; row = self.grid[y] # Get coordinates an corresponding row
            # if self.grid[y][x] != 'P':                   # Don't replace the 'P'
            #     self.grid[y] = row[:x] + '.' + row[x+1:] # Mark the visted node with a '.'
            #####################################################################

            neighbors = self.getNeighbors(node)
            for n in neighbors:           # Put all the valid neighbors in the frontier
                if n in self.explored or n in frontierSet:
                    continue
                self.parents[n] = node
                frontier.put((n, cost+1, dots)) # Put in the incremented cost
                frontierSet.add(n)
        raise Exception('Frontier became empty without a solution')

    # Returns the average of distances for all the dots from the current node
    def averageDistance(self, node, dotPositions):
        totalDist = 0
        for d in dotPositions:
            totalDist += self.mDistance(node, d)
        return totalDist / len(dotPositions)

    # Helper function to solve the maze using A* and Greed. Returns (grid, path cost, number of nodes expanded)
    def solveAG(self, algo):

        ignoreMap = dict()         # IgnoreMap
        frontier = PriorityQueue() # Intialize the a priority queue
        dots = self.getDotPositions()
        score = self.averageDistance(self.start, list(dots)) # Manhattan distance for Greedy, MDist + Cost(0) for A*
        parents = [self.start]
        # parents = {self.start : -1}
        frontier.put((score, self.start, 0, dots, parents))   # Frontier: ((x, y), path cost) : tuple(tuple(x, y), int, {dots})
        self.frontierMap[(self.start, tuple(dots))] = 0 # Map of nodes to path cost

        while not frontier.empty():
            t = frontier.get()       # Remove from frontier
            _, node, cost, dots, parents = t  # (score, (y, x), cost, dots)

            if node in ignoreMap and ignoreMap[node] == cost: # If node has inefficient path cost
                continue

            if (node, tuple(dots)) in self.frontierMap:
                del self.frontierMap[(node, tuple(dots))]
            self.explored.add((node, tuple(dots)))
            # explored = set(explored)
            # explored.add((node, tuple(dots)))#, len(dots)))
            # self.explored.add((node, tuple(dots)))    # Add to Explored set: ((y, x), R)

            if node in dots:
                dots = set(dots)   # Create a dots set
                dots.remove(node)  # If a dot position is found, remove it from the dots set
                if len(dots) == 0:  # Goal test - if all the dot positions have been found
                    self.markSolution(node, parents)
                    return self.grid, cost, len(self.explored)

            neighbors = self.getNeighbors(node)
            for n in neighbors:           # Put all the valid neighbors in the frontier
                # Check if already explored
                if (n, tuple(dots)) in self.explored:
                    continue

                if algo is Algo.A_STAR: # if A*, score is f = g(cost) + h(mDist)
                    score = cost+1 + self.averageDistance(n, dots)
                else: # if Greedy, score is Manhattan distance
                    score = self.averageDistance(n, dots)

                # Check if already in frontier and if yes, check it has a better path cost
                if (n, tuple(dots)) in self.frontierMap:
                    if self.frontierMap[(n, tuple(dots))] > cost+1: #Exisitng path cost is worse, then replace
                        ignoreMap[n] = self.frontierMap[(n, tuple(dots))]
                    else:
                        continue

                p = list(parents)
                p.append(n)
                frontier.put((score, n, cost+1, dots, p)) # Put in the incremented cost
                self.frontierMap[(n, tuple(dots))] = cost+1

        raise Exception('Frontier became empty without a solution')

    # Prints the final solution path and numbers all the dot positions in the order explored
    def markSolution(self, curr, parents):
        s = '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        chars = list(s)
        idx = 0

        for n in parents:
            y, x = n; row = self.grid[y] # Get coordinates an corresponding row
            if self.grid[y][x] == 'P':
                continue
            if (y, x) in self.dotPositions and grid[y][x] == '.':
                self.grid[y] = row[:x] + chars[idx] + row[x+1:] #  Mark the visted dot with the dot number%10
                idx += 1
            else:
                self.grid[y] = row[:x] + '.' + row[x+1:] # Mark the visted node with a '.'
            # print(''.join(self.grid))

    def markSolutionDB(self, curr, parents=None):
        parents = self.parents if parents is None else parents
        dotCount = self.dotCount
        while (curr != -1):
            y, x = curr; row = self.grid[y] # Get coordinates an corresponding row
            if self.grid[y][x] == 'P':
                return
            if (y, x) in self.dotPositions:
                self.grid[y] = row[:x] + str(dotCount) + row[x+1:] #  Mark the visted dot with the dot number%10
                dotCount -= 1
            else:
                self.grid[y] = row[:x] + '.' + row[x+1:] # Mark the visted node with a '.'
            curr = parents[curr]

if __name__ == "__main__":

    if len(sys.argv) < 3:
        raise Exception("Need two arguments: script.py maze.txt algo: astar, greedy, bfs, or dfs")

    maze_fname = sys.argv[1]; a = sys.argv[2]
    algoMap = {'bfs': Algo.BFS, 'dfs': Algo.DFS, 'astar': Algo.A_STAR, 'greedy': Algo.GREEDY}
    if a in algoMap:
        algo = algoMap[a]
    else:
        raise Exception("Algorithm not valid; Use astar, greedy, bfs, or dfs")

    with open(maze_fname) as mFile:
        grid = mFile.readlines() # 2D Matrix of rows(string per line) and cols(character per string)

    maze = MazeSearch(grid)
    start = time.time()
    newGrid, cost, nodes_expanded = maze.solve(algo)
    end = time.time()
    newMaze = ''.join(newGrid)
    print(newMaze)
    print ("The path cost is "+ str(cost) + " steps")
    print("The number of nodes expanded is "+str(nodes_expanded))
    print ("Elapsed time: " + str(end - start))

    with open("output.text", "w") as oFile:
        oFile.write(newMaze)
