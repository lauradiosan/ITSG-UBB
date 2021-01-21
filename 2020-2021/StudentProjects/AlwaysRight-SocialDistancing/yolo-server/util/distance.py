from typing import List, Tuple
from math import sqrt, pow


def euclidean_distance(centroid1: Tuple[int, int], centroid2: Tuple[int, int]) -> int:
    x1, y1 = centroid1
    x2, y2 = centroid2
    dx = x1 - x2
    dy = x1 - y1
    return sqrt(pow(dx, 2) + pow(dy, 2))
