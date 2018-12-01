import bisect

from scipy.spatial.distance import euclidean

from common import (NO_QUADRANT, NORTH_EAST, NORTH_WEST, SOUTH_EAST,
                    SOUTH_WEST, Boundary, Point, belongs, compute_knn,
                    intersects, quadrants)
from node import TreeNode

# Constants for tuple access optimization
BOUNDARY = 0
POINTS = 1

class StaticQuadTree:

    def __init__(self, dimension=1, max_depth=4):
        self.max_depth = max_depth
        self._quadrants = [0] * int(((4 ** (max_depth + 1))-1)/3)
        self._quadrants[0] = (Boundary(Point(0, 0), dimension), set())
        self._decompose(self._quadrants[0][BOUNDARY], 0, 0)

    def _decompose(self, boundary, depth, parent):
        if depth == self.max_depth:
            return

        x, y = boundary.center
        dm = boundary.dimension / 2

        index0 = 4 * parent + NORTH_WEST
        index1 = 4 * parent + NORTH_EAST
        index2 = 4 * parent + SOUTH_EAST
        index3 = 4 * parent + SOUTH_WEST

        self._quadrants[index0] = (Boundary(Point(x - dm, y + dm), dm), set())
        self._quadrants[index1] = (Boundary(Point(x + dm, y + dm), dm), set())
        self._quadrants[index2] = (Boundary(Point(x + dm, y - dm), dm), set())
        self._quadrants[index3] = (Boundary(Point(x - dm, y - dm), dm), set())

        self._decompose(self._quadrants[index0][BOUNDARY], depth + 1, index0)
        self._decompose(self._quadrants[index1][BOUNDARY], depth + 1, index1)
        self._decompose(self._quadrants[index2][BOUNDARY], depth + 1, index2)
        self._decompose(self._quadrants[index3][BOUNDARY], depth + 1, index3)

    def index(self, point):
        idx = 0
        q = quadrants(self._quadrants[idx][BOUNDARY], point)
        if q == NO_QUADRANT: return
        for _ in range(0, self.max_depth):
            idx = 4 * idx + q
            q = quadrants(self._quadrants[idx][BOUNDARY], point)
        return idx

    def __len__(self):
        return sum(len(q[1]) for q in self._quadrants)

    def __iter__(self):
        return (point for quad in self._quadrants for point in quad[POINTS])

    def __contains__(self, point):
        return point in self._quadrants[self.index(point)][POINTS]

    def insert(self, point):
        self._quadrants[self.index(point)][POINTS].add(point)

    def remove(self, point):
        if not isinstance(point):
            return False

        try:
            self._quadrants[self.index(point)][POINTS].remove(point)
            return True
        except:
            return False

    def update(self, new_point, old_point):
        if not isinstance(new_point, Point) or \
           not isinstance(old_point, Point):
            return False

        try:
            self._quadrants[self.index(old_point)][POINTS].remove(old_point)
            self._quadrants[self.index(new_point)][POINTS].add(new_point)
            return True
        except:
            return False

    def query_range(self, boundary):
        if not isinstance(boundary, Boundary):
            return ([])

        for quadrant in self._quadrants:
            if intersects(quadrant[BOUNDARY], boundary):
                for point in quadrant[POINTS]:
                    if belongs(boundary, point):
                        yield point

    def knn(self, point, k, factor=.1):
        if not isinstance(point, Point) or k <= 0 or factor <= 0:
            return []

        if len(self) < k:
            points = self.query_range(self._quadrants[BOUNDARY])
            return compute_knn(points, point, k)
        
        points_count = 0
        dimension = factor

        while points_count <= k:
            dimension += factor
            points_count = self._count_points(Boundary(point, dimension))

        points = self.query_range(Boundary(point, dimension))
        return compute_knn(points, point, k)

    def _count_points(self, boundary):
        count = 0
        for quadrant in self._quadrants:
            if intersects(quadrant[BOUNDARY], boundary):
                for point in quadrant[POINTS]:
                    if belongs(boundary, point):
                        count += 1
        return count


class DynamicQuadTree:

    def __init__(self, centerPt=Point(0, 0,'center'),dimension=1, max_points=1, max_depth=4):
        self.max_points = max_points
        self.max_depth = max_depth
        self.root = TreeNode(centerPt, dimension, max_points, max_depth, 0)

    def __len__(self):
        return len(self.root)

    def __iter__(self):
        return iter(self.root)

    def __contains__(self, point):
        return self.root.exist(point)

    def insert(self, point):
        return self.root.insert(point)

    def remove(self, point):
        return self.root.remove(point)

    def update(self, new_point, old_point):
        return self.root.update(new_point, old_point)

    def query_range(self, boundary):
        return self.root.query_range(boundary)

    def knn(self, point, k):
        return self.root.knn(point, k)
