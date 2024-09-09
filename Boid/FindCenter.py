import numpy as np
from collections import deque

def bfs(matrix, start, visited):
    queue = deque([start])
    component = []
    while queue:
        x, y = queue.popleft()
        if (x, y) not in visited:
            visited.add((x, y))
            component.append((x, y))
            # Check all 4-connected neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and matrix[nx, ny] == 5:
                    queue.append((nx, ny))
    return component

# This function returns a list of (x,y) coords that have the map_int value of 5 that are connected to each other
def find_clumps(matrix):
    visited = set()
    clumps = []
    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            if matrix[x, y] == 5 and (x, y) not in visited:
                component = bfs(matrix, (x, y), visited)
                clumps.append(component)
    return clumps


# This function returns the center,left,right,top,and bottom coords of all the clumps
def get_clump_centers_and_extremes(clumps):
    centers_and_extremes = []
    for clump in clumps:
        
        leftmost = min(clump, key=lambda p: p[1])  
        rightmost = max(clump, key=lambda p: p[1]) 
        topmost = min(clump, key=lambda p: p[0])   
        bottommost = max(clump, key=lambda p: p[0])
        center = ((bottommost[0]+topmost[0])//2,(rightmost[1]+leftmost[1])//2)
        centers_and_extremes.append({
            'center': center,
            'leftmost': leftmost,
            'rightmost': rightmost,
            'topmost': topmost,
            'bottommost': bottommost
        })
    return centers_and_extremes


# This function returns a list of dicts that contain a clump's center, top,left,right,bottom coords
def findCoords(matrix):

    # Convert the matrix to a NumPy array
    matrix_np = np.array(matrix)
    clumps = find_clumps(matrix_np)
    centers_and_extremes = get_clump_centers_and_extremes(clumps)

    # Return the centers and extreme points
    return centers_and_extremes
