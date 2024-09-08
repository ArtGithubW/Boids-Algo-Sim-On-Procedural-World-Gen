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

def find_clumps(matrix):
    visited = set()
    clumps = []
    for x in range(matrix.shape[0]):
        for y in range(matrix.shape[1]):
            if matrix[x, y] == 5 and (x, y) not in visited:
                component = bfs(matrix, (x, y), visited)
                clumps.append(component)
    return clumps

def get_clump_centers(clumps):
    centers = []
    for clump in clumps:
        coords = np.array(clump)
        avg_x = np.mean(coords[:, 0])
        avg_y = np.mean(coords[:, 1])
        centers.append((int(round(avg_x)), int(round(avg_y))))
    return centers


def findCenters(matrix):

    # Convert the matrix to a NumPy array
    matrix_np = np.array(matrix)

    # Find clumps and their centers
    clumps = find_clumps(matrix_np)
    centers = get_clump_centers(clumps)

    # Print the centers
    return centers