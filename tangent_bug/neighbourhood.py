import numpy as np
from icecream import ic

def neighbours_for_point(x: int, y: int)->  tuple[np.ndarray, np.ndarray]:
    """
    Based on the coordinates of a point, calculates two sets of coordinates of its neighbours.

    Args:
        x (int): X coordinate of a point.
        y (int): Y coordinate of a point.

    Returns: 
        tuple[np.ndarray, np.ndarray]: Arrays of point[0] and border[1] neighbour point coordinates.
    """
    all_neighbours = [
                      (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                      (x, y - 1), (x, y + 1),
                      (x + 1, y - 1), (x + 1, y), (x + 1, y + 1),
                     ]
    point_neighbours = []
    border_neighbours = []
    
    for neighbour in all_neighbours:
        if neighbour[0] >= 0 and  neighbour[0] <= 999 and neighbour[1] >= 0 and  neighbour[1] <= 999:
            point_neighbours.append(neighbour)

    for neighbour in point_neighbours:
        if abs(x - neighbour[0]) + abs(y - neighbour[1]) == 1:
            border_neighbours.append(neighbour)

    return np.array(point_neighbours), np.array(border_neighbours)


if __name__ == "__main__":
    ic(neighbours_for_point(1, 1))