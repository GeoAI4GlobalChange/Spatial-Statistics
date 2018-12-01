
from common import *


class TreeNode:
    def __init__(self, center, dimension, max_points, max_depth, depth):
        self.boundary = Boundary(center, dimension)
        self.max_depth = max_depth
        self.max_points = max_points
        self._depth = depth
        self._points = set([])
        self.PtNum=0
        self._nodes = {}

    @property
    def splitted(self):
        return len(self._nodes) > 0

    def __len__(self):
        if not self.splitted:
            return len(self._points)
        return sum(len(v) for v in self._nodes.values() if v)

    def __str__(self):
        s  = 'Depth={}\t'
        s += 'Length={}\t'
        s += 'Partitions={}'
        return s.format(self._depth, len(self._points), len(self._nodes))

    def __iter__(self):
        points = []
        stack = [self]
        while stack:
            node = stack.pop()
            for n in node._nodes.values():
                stack.append(n)
            points += node._points
        return iter(points)

    def split(self, quadrant):
        x, y,key = self.boundary.center
        dm = self.boundary.dimension / 2
        mp = self.max_points
        md = self.max_depth
        dp = self._depth + 1

        if quadrant == NORTH_WEST:
            center = Point(x - dm, y + dm,key)
        elif quadrant == NORTH_EAST:    
            center = Point(x + dm, y + dm,key)
        elif quadrant == SOUTH_EAST:
            center = Point(x + dm, y - dm,key)
        elif quadrant == SOUTH_WEST:
            center = Point(x - dm, y - dm,key)

        self._nodes[quadrant] = TreeNode(center, dm, mp, md, dp)
    def split2four(self):
        x, y, key = self.boundary.center
        dm = self.boundary.dimension / 2
        mp = self.max_points
        md = self.max_depth
        dp = self._depth + 1
        center = Point(x - dm, y + dm, key)
        self._nodes[NORTH_WEST] = TreeNode(center, dm, mp, md, dp)
        center = Point(x + dm, y + dm, key)
        self._nodes[NORTH_EAST] = TreeNode(center, dm, mp, md, dp)
        center = Point(x + dm, y - dm, key)
        self._nodes[SOUTH_EAST] = TreeNode(center, dm, mp, md, dp)
        center = Point(x - dm, y - dm, key)
        self._nodes[SOUTH_WEST] = TreeNode(center, dm, mp, md, dp)
    @property
    def _has_max_points(self):
        return self.PtNum >= self.max_points

    @property
    def _is_max_depth(self):
        return self._depth >= self.max_depth

    def _insert_at(self, point, quadrant):
        self.PtNum+=1
        if quadrant not in self._nodes or self._is_max_depth:
            self._points.add(point)
        else:
            self._nodes[quadrant].insert(point)

    def insert(self, point):
        quadrant = quadrants(self.boundary, point)

        if quadrant == NO_QUADRANT:
            return False

        if not self._has_max_points or self._is_max_depth:
            self._insert_at(point, quadrant)
            return True
        elif len(self._nodes)>0:
            self._insert_at(point, quadrant)
            return True
        else:
            self.split2four()
            """
        if quadrant not in self._nodes:
            self.split(quadrant)
            """
        for p in self._points.copy():
            #if quadrants(self.boundary, p) == quadrant:
                self._points.remove(p)
                quadrant_temp=quadrants(self.boundary, p)
                self._nodes[quadrant_temp].insert(p)

        return self._nodes[quadrant].insert(point)

    def remove(self, point):
        quadrant = quadrants(self.boundary, point)

        if quadrant == NO_QUADRANT:
            return False

        if quadrant in self._nodes:
            return self._nodes[quadrant].remove(point)

        try:
            self._points.remove(point)
            return True
        except: pass

        return False

    def update(self, new_point, old_point):
        quadrant = quadrants(self.boundary, old_point)

        if quadrant == NO_QUADRANT:
            return False

        if quadrant not in self._nodes:
            try:
                self._points.remove(old_point)
                self._points.add(new_point)
                return True
            except:
                return False

        return self._nodes[quadrant].update(new_point, old_point)

    def exist(self, point):
        quadrant = quadrants(self.boundary, point)

        if quadrant == NO_QUADRANT:
            return False

        if quadrant not in self._nodes:
            return point in self._points

        return self._nodes[quadrant].exist(point)

    def quadrants(self, point):
        return quadrants(self.boundary, point)

    def depth(self, point):
        quadrant = quadrants(self.boundary, point)

        if quadrant == NO_QUADRANT:
            return False

        if quadrant not in self._nodes:
            return self._depth if point in self._points else -1

        return self._nodes[quadrant].depth(point)

    def query_range(self, boundary):
        points = set([])

        if not intersects(self.boundary, boundary):
            return points

        for quadrant in self._nodes:
            for p in self._nodes[quadrant].query_range(boundary):
                if belongs(boundary, p):
                    points.add(p)

        for p in self._points:
            if belongs(boundary, p):
                points.add(p)

        return points

    def _count_points(self, boundary):
        if not intersects(self.boundary, boundary):
            return 0

        count = 0
        for quadrant in self._nodes:
            count += self._nodes[quadrant]._count_points(boundary)

        return sum(1 for p in self._points if belongs(boundary, p)) + count

    def knn(self, point, k, factor=.1):
        if len(self) < k:
            points = self.query_range(self.boundary)
            return compute_knn(points, point, k)

        points_count = 0
        dimension = factor

        while points_count <= k:
            dimension += factor
            points_count = self._count_points(Boundary(point, dimension))

        points = self.query_range(Boundary(point, dimension))
        return compute_knn(points, point, k)
