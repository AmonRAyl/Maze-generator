# Maze-generator
Here, you'll find my maze generation program utilizing Prim's algorithm. The project consists of two files: visual.py and generator.py.  
In visual.py, I use the pygame library to visualize the maze.  
In generator.py focuses solely on the implementation of Prim's algorithm. This file contains the logic behind generating the maze.

## Brief Description of how I implemented prim's Algorithm:
1. First, I initialized a matrix with random values from 1 to X (normally I use rows * columns). This represents the nodes of the maze and their weights (the starting node is set as 0, and the last node is set to have the highest weight so that the solution is a long path).
2. Now we select from the visited nodes list the unvisited surrounding node with the minimum weight and visit it, creating a new path and adding the new node to the visited nodes list.
3. Repeat step 2 until all the nodes have been visited.
Once all this has been done, I have a list with all the paths that will represent my maze.
