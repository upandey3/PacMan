import sys

if len(sys.argv) < 2:
    raise Exception("Need two arguments: script.py maze.txt")
print(sys.argv)
maze_fname = sys.argv[1]

with open(maze_fname) as mFile:
    grid = mFile.readlines() # 2D Matrix
    # print(grid[1])
    # grid =
    # for row in rows:
    #     print(row)
    # # for lines
# print(maze)
print(grid)

catch IOError as instance:
    print("Unable to open file" + instance.filename)
