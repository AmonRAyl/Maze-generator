import pygame
import numpy as np
import copy
import colorsys

def prims(rowcol):
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

def generate_distinct_colors(num_colors):
    colors = []
    golden_ratio_conjugate = (5 ** 0.5 - 1) / 2

    for i in range(num_colors - 1):
        hue = (i * golden_ratio_conjugate) % 1
        r, g, b = colorsys.hsv_to_rgb(hue, 0.5, 0.95)
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    colors.append((0,255,0))
    return colors

def viewMaze(matrix, paths):
    # Colour all white
    for j in range(matrix.shape[0]):
        for i in range(matrix.shape[1]):
            matrix[i][j] = 0

    # Colour the start and end in green
    matrix[0][0] = len(paths) + 1   
    matrix[matrix.shape[0]-1][matrix.shape[1]-1] = len(paths) + 1  

def viewAnswer(matrix, paths):
    # Colour each path
    for j in range(matrix.shape[0]):
        for i in range(matrix.shape[1]):
            for x in paths:
                if (i, j) in x:
                    matrix[i][j] = paths.index(x) + 1
    # Colour the correct path in green
    for x in paths:
        if (matrix.shape[0]-1, matrix.shape[1]-1) in x:
            for y in x:
                matrix[y[0]][y[1]] = len(paths) + 1

def main():
    # Initialize pygame
    pygame.init()

    # Define the screen dimensions
    WIDTH = 400
    HEIGHT = 400

    # Define the matrix, you can edit the size of the matrix it will work fine till 30x30
    rowcol = 15
    matrix, paths = prims(rowcol)

    #Comment one of the viewers, one shows you the answer and the other one shows you the maze
    viewAnswer(matrix, paths)
    # viewMaze(matrix, paths)

    x = len(paths) + 1  # Number of colors

    color_list = generate_distinct_colors(x)

    color_mapping = {i + 1: color_list[i] for i in range(x)}

    # Calculate the size of each cell based on the screen dimensions and matrix size
    cell_size = min(WIDTH // len(matrix[0]), HEIGHT // len(matrix))

    # Calculate the offset to center the matrix on the screen
    x_offset = (WIDTH - len(matrix[0]) * cell_size) // 2
    y_offset = (HEIGHT - len(matrix) * cell_size) // 2

    # Create the screen surface
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the matrix cells
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                # Calculate the cell position
                x = j * cell_size + x_offset
                y = i * cell_size + y_offset

                # Get the color for the cell value
                color = color_mapping.get(value, (255, 255, 255))  # Default to white if value not found in mapping
                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
        # Draw the walls of each cell
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                # Calculate the cell position
                x = j * cell_size + x_offset
                y = i * cell_size + y_offset
                
                futuredirections = ["up", "down", "left", "right"]
                for z in paths:
                    if (j, i) in z:
                        index=z.index((j, i))+1
                        indexd=z.index((j, i))-1
                        if(index<len(z)):
                            xx,yy=z[index]
                            xx=xx-j
                            yy=yy-i
                            if yy==1:
                                futuredirections[3]="NULL"
                            elif yy==-1:
                                futuredirections[2]="NULL"
                            if xx==1:
                                futuredirections[1]="NULL"
                            elif xx==-1:
                                futuredirections[0]="NULL"
                        if(indexd>=0):
                            xx,yy=z[indexd]
                            xx=xx-j
                            yy=yy-i
                            if yy==1:
                                futuredirections[3]="NULL"
                            elif yy==-1:
                                futuredirections[2]="NULL"
                            if xx==1:
                                futuredirections[1]="NULL"
                            elif xx==-1:
                                futuredirections[0]="NULL"

                # Draw the walls
                if(futuredirections[0]!="NULL"):#up
                    pygame.draw.line(screen, (0, 0, 0), (y, x), (y + cell_size, x), 5)
                if(futuredirections[1]!="NULL"): #down
                    pygame.draw.line(screen, (0, 0, 0), (y, x + cell_size), (y + cell_size, x + cell_size), 5)
                if(futuredirections[2]!="NULL"): #left
                    pygame.draw.line(screen, (0, 0, 0), (y, x), (y, x + cell_size), 5)
                if(futuredirections[3]!="NULL"): #right
                    pygame.draw.line(screen, (0, 0, 0), (y + cell_size, x), (y + cell_size, x + cell_size), 5)
            
        # Update the display
        pygame.display.flip()

    # Quit the game
    pygame.quit()
    
main()
