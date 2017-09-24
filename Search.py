import sys

if len(sys.argv) < 2:
    raise Exception("Need two arguments: script.py maze.txt")

maze_fname = sys.argv[1]

with open(maze_fname) as mFile:
    maze = mFile.read()
print(maze)
