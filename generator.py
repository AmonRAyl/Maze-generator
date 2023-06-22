import numpy as np
import copy

def main(rowcol):
    # Generate random matrix to use its values as weights
    matrix = np.random.randint(1, rowcol*rowcol, size=(rowcol, rowcol))

    # Select the first and last node as the start and end
    matrix[0][0] = 0
    matrix[matrix.shape[0]-1][matrix.shape[1]-1] = matrix.shape[0]*matrix.shape[1]+100

    # Implementation of prims algorithm
    # Steps:
    # 1. Select the start node and added to the visited list
    # 2. Look for the smallest weight node that surrounds any of the visited nodes list, without it being part of the visited list
    # 3. Repeat step 2 until all nodes are visited

    visited = [(0, 0)]
    paths = [[(0, 0)]]
    while len(visited) != matrix.size:
        min = 10000000
        father = None
        for x in visited:
            # Check the surrounding nodes
            # Check right
            if x[0]+1 < matrix.shape[0]:
                if (x[0]+1, x[1]) not in visited and matrix[x[0]+1][x[1]] < min:
                    pos = (x[0]+1, x[1])
                    min = matrix[x[0]+1][x[1]]
                    father = x
            # Check left
            if x[0]-1 >= 0:
                if (x[0]-1, x[1]) not in visited and matrix[x[0]-1][x[1]] < min:
                    pos = (x[0]-1, x[1])
                    min = matrix[x[0]-1][x[1]]
                    father = x
            # Check up
            if x[1]+1 < matrix.shape[1]:
                if (x[0], x[1]+1) not in visited and matrix[x[0]][x[1]+1] < min:
                    pos = (x[0], x[1]+1)
                    min = matrix[x[0]][x[1]+1]
                    father = x
            # Check down
            if x[1]-1 >= 0:
                if (x[0], x[1]-1) not in visited and matrix[x[0]][x[1]-1] < min:
                    pos = (x[0], x[1]-1)
                    min = matrix[x[0]][x[1]-1]
                    father = x
        visited.append(pos)
        #Locate father and save new path
        for x in paths:
            if x[-1] == father:
                paths.append(x + [pos])
                break
    finalpaths = copy.deepcopy(paths)
    
    for i in range(len(finalpaths) - 1, -1, -1):
        current_path = finalpaths[i]
        
        # Check if the current path is a subset of any following paths
        for j in range(i + 1, len(finalpaths)):
            following_path = finalpaths[j]
            if set(current_path).issubset(set(following_path)):
                finalpaths.pop(i)
                break      
    return matrix, finalpaths

main(10)
#the values that you use should be from 1 to 30, 40 would be really big and it will take a lot of time.