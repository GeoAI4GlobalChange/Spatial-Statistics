import bisect
from collections import namedtuple
from scipy.spatial.distance import euclidean

NO_QUADRANT = -1
NORTH_WEST = 1
NORTH_EAST = 2
SOUTH_EAST = 3
SOUTH_WEST = 4
delta=pow(10,-7)

# Constants for tuple access optimzation
CENTER = 0
DIMENSION = 1
X = 0
Y = 1

Point = namedtuple('Point', ['x', 'y','key'])
Boundary = namedtuple('Boundary', ['center', 'dimension'])#dimension=1/2*cell size

def belongs(boundary, point):
    """ Check if the point belongs to the boundary """
    if not point:
        return False

    d = boundary[DIMENSION]
    cx, cy = boundary[CENTER]
    px, py = point

    return (py <= cy + d and py >= cy - d) and (px <= cx + d and px >= cx - d)

def quadrants(boundary, point):
    """ Find in which quadrant the point belongs to """
    """
             y
            /|\
    NorthWest|NorthEast
    ---------------------->x
   SourthWest|SourthEast
    """
    if not isinstance(boundary, Boundary) or \
       not isinstance(point, Point):
        return False
    
    d = boundary[DIMENSION]
    cx, cy,key = boundary[CENTER]
    px, py,key = point

    if (py <= cy + d+delta and py >= cy) and (px >= cx - d-delta and px <= cx):
        return NORTH_WEST

    if (py <= cy + d+delta and py >= cy) and (px <= cx + d+delta and px >= cx):
        return NORTH_EAST

    if (py >= cy - d-delta and py <= cy) and (px <= cx + d+delta and px >= cx):
        return SOUTH_EAST

    if (py >= cy - d-delta and py <= cy) and (px >= cx - d-delta and px <= cx):
        return SOUTH_WEST

    return NO_QUADRANT

def intersects(boundary0, boundary1):
    """ Check if the given boundary intersects this boundary """
    if not boundary0 or not boundary1:
        return False

    ad      = boundary0[DIMENSION]
    aleft   = boundary0[CENTER][X] - ad
    aright  = boundary0[CENTER][X] + ad
    atop    = boundary0[CENTER][Y] + ad
    abottom = boundary0[CENTER][Y] - ad

    bd      = boundary1[DIMENSION]
    bleft   = boundary1[CENTER][X] - bd
    bright  = boundary1[CENTER][X] + bd
    btop    = boundary1[CENTER][Y] + bd
    bbottom = boundary1[CENTER][Y] - bd

    intersect_left  = bright > aleft and bleft < aleft
    intersect_right = bleft < aright and bright > aright
    intersect_top   = bbottom < atop and btop > atop
    intersect_bottom= btop > abottom and bbottom < abottom

    intersect_inside = (atop > btop and abottom < bbottom) or\
                       (aleft < bleft and aright > bright)

    return intersect_top and intersect_left  or\
           intersect_top and intersect_right or\
           intersect_bottom and intersect_left  or\
           intersect_bottom and intersect_right or\
           intersect_inside

def compute_knn(points, point, k):
    neighbors = []
    distant_neighbor = None

    for p in points:
        if p == point: continue

        dist = euclidean(point, p)
        neighbor = (dist, p)

        if len(neighbors) < k:
            if not distant_neighbor:
                distant_neighbor = neighbor
            if neighbor[0] > distant_neighbor[0]:
                distant_neighbor = neighbor
            bisect.insort(neighbors, neighbor)
            continue

        if neighbor[0] < distant_neighbor[0]:
            del neighbors[-1]
            bisect.insort(neighbors, neighbor)
            distant_neighbor = neighbors[-1]

    return neighbors
