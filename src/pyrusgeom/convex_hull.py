""" convex_hull.py file
    ConvexHull: class name
"""
from __future__ import annotations
from enum import Enum, unique, auto
import functools
import math

from pyrusgeom.triangle_2d import Triangle2D
from pyrusgeom.polygon_2d import Polygon2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.math_values import EPSILON


@unique
class MethodType(Enum):
    """ MethodType
        Algorithm types:
            DIRECT_METHOD: don't use it need fixing
            WRAPPING_METHOD
            GRAHAN_SCAN
    """
    DIRECT_METHOD = auto()
    WRAPPING_METHOD = auto()
    GRAHAN_SCAN = auto()


def list2set(list_: list) -> list:
    """function to convert a list to a set with unique values

    Args:
        list_ (list): list with duplicate items

    Returns:
        list: a set with unique values
    """
    sub = []
    for item in list_:
        # check if exists in sub or not
        if item not in sub:
            sub.append(item)
    return sub

# Base for angle_sort_predicate
# base = Vector2D()


class AngleSortPredicate:
    """angle_sort_predicate cmp key for sort
    """

    def __init__(self, obj, base_in, *args):
        self.obj = obj
        self.base_in = base_in
        self.args = args

    def __lt__(self, other):
        return angle_sort_predicate(self.obj, other.obj, base=self.base_in) < 0

    def __gt__(self, other):
        return angle_sort_predicate(self.obj, other.obj, base=self.base_in) > 0

    def __eq__(self, other):
        return angle_sort_predicate(self.obj, other.obj, base=self.base_in) == 0

    def __le__(self, other):
        return angle_sort_predicate(self.obj, other.obj, base=self.base_in) <= 0

    def __ge__(self, other):
        return angle_sort_predicate(self.obj, other.obj, base=self.base_in) >= 0

    def __ne__(self, other):
        return angle_sort_predicate(self.obj, other.obj, base=self.base_in) != 0


def angle_sort_predicate(lhs: Vector2D, rhs: Vector2D, base: Vector2D = Vector2D()) -> int:
    """compare and check the base[(0,0) by default] and lhs and rhs to find are they
        in a counter clockwise order or not
        base - lhs - rhs

    Args:
        lhs (Vector2D): first point
        rhs (Vector2D): second point
        base (Vector2D): Base for angle_sort_predicate

    Returns:
        bool: if counter clockwise return 1. else -1
    """
    area = Triangle2D.double_signed_area_st(base, lhs, rhs)

    if area < 0.0:
        return -1
    if area < EPSILON:
        if base.get_y() < lhs.get_y():
            if base.dist2(lhs) > base.dist2(rhs):
                return -1
        else:
            if base.dist2(lhs) < base.dist2(rhs):
                return -1
    return 1


def is_clockwise(point0: Vector2D, point1: Vector2D, point2: Vector2D) -> bool:
    """compare and check the point0 and point1 and point2 to find are they
        in a clockwise order or not

    Args:
        point0 (Vector2D): first point
        point1 (Vector2D): second point
        point2 (Vector2D): third point

    Returns:
        bool: if clockwise return true. else false
    """
    area = Triangle2D.double_signed_area_st(point0, point1, point2)

    return area < 0.0 or (area < EPSILON and point0.dist2(point1) > point0.dist2(point2))


class ConvexHull:
    """ handling the Convex Hull in SS2D
    Attributes:
        _input_points: input points
        _vertices: vertices of convex hull [counter clockwise order]
        _edges: edges of convex hull
    """

    def __init__(self, point_list: list):
        """This is the class init function and creates the convex hull.

        Defualt:
            create empty convex hull
        OR
            create convex hull with given points
        Args:
            point_list: array of input points

        """
        self._input_points = point_list
        self._vertices = []
        self._edges = []

    def clear(self) -> None:
        """clear all.
        """
        self.clear_results()
        self._input_points.clear()

    def clear_results(self) -> None:
        """clear result variables.
        """
        self._vertices.clear()
        self._edges.clear()

    def add_point(self, point: Vector2D) -> None:
        """add a point to the set of input point

        Args:
            point(Vector2D) : point to add
        """
        self._input_points.append(point)

    def add_points(self, points: list) -> None:
        """add a point list to the set of input point

        Args:
            points(list) : points to add
        """
        for point in points:
            self._input_points.append(point)

    def compute(self, m_type: MethodType = MethodType.WRAPPING_METHOD) -> None:
        """generate convex hull by specified method
            DIRECT_METHOD: don't use it need fixing
            WRAPPING_METHOD
            GRAHAN_SCAN
        Args:
            m_type(MethodType):the specified method id

        """
        if m_type == MethodType.DIRECT_METHOD:
            self.compute_direct_method()
        elif m_type == MethodType.GRAHAN_SCAN:
            self.compute_graham_scan()
        elif m_type == MethodType.WRAPPING_METHOD:
            self.compute_wrapping_method()

    def input_points(self) -> list:
        """get a copy list from the input point container

        Returns:
            list: a list with input point conrainer values
        """
        input_list_cp = self._input_points.copy()
        return input_list_cp

    def input_points_(self) -> list:
        """ get the reference and og list to the input point container

        Returns:
            list: a reference to the input point container
        """
        return self._input_points

    def vertices(self) -> list[Vector2D]:
        """get a copy list from the vertex container

        Returns:
            list: a list with the vertex container values
        """
        vertices_cp = self._vertices.copy()
        return vertices_cp

    def vertices_(self) -> list:
        """ get the reference and og list to the vertex container

        Returns:
            list: a reference to the vertex container
        """
        return self._vertices

    def edges(self) -> list:
        """get a copy list from the edge container

        Returns:
            list: a list with the edge container values
        """
        edges_cp = self._edges.copy()
        return edges_cp

    def edges_(self) -> list:
        """ get the reference and og list to the edge container

        Returns:
            list: a reference to the edge container
        """
        return self._edges

    def compute_direct_method(self):
        """direct method
            don't use this one until the fix
        """
        self.clear_results()

        point_size = len(self._input_points)

        if point_size < 3:
            return

        for i in range(point_size - 1):
            point_first:Vector2D = self._input_points[i]
            for j in range(i + 1, point_size):
                point_second:Vector2D = self._input_points[j]
                rel = point_second - point_first

                valid = True
                last_value = 0.0

                for k in range(point_size):
                    if k in (i, j):
                        continue

                    point_third = self._input_points[k]
                    outer_prod = rel.outerProduct(point_third - point_first)

                    if math.fabs(outer_prod) < EPSILON:
                        # point is on the line
                        if (point_third - point_first).r2() < rel.r2():
                            # point is on the segment
                            valid = False
                            break
                    # to check if other_prod and last_value don't have a same
                    # sign means one of the points exists in the opposite side
                    if outer_prod ^ last_value < 0.0:
                        valid = False
                        break

                    last_value = outer_prod

                if valid:
                    self._vertices.append(point_first)
                    self._vertices.append(point_second)

                    if last_value < 0.0:
                        self._edges.append(
                            Segment2D(point_first, point_second))

                    else:
                        self._edges.append(
                            Segment2D(point_second, point_first))

        # sort vertices by counter clockwise order

        if len(self._vertices) > 0:
            self._vertices.sort(key=functools.cmp_to_key(angle_sort_predicate))
            # TODO: Need to pass the base to the cmp-key fnction
            # base is the line bellow the last member of _vertices
            # until then avoid this method. we are open to
            # any suggetion for solving this cmp-key problem
            # base = self._vertices[len(self._vertices) - 1]
            # functools.cmp_to_key(angle_sort_predicate)
            # AngleSortPredicate(base_in=base)
            # (base:self._vertices[len(self._vertices) - 1])

            self._vertices = list2set(self._vertices)

    def compute_wrapping_method(self):
        """wrapping method
        """
        self.clear_results()

        point_size = len(self._input_points)
        min_index = self.get_min_point_index()

        if point_size < 3 or min_index == -1:
            return

        vertices_index = []  # temporal set for checking already used vertices.

        self._vertices.append(self._input_points[min_index])

        current_index = min_index
        current_point:Vector2D = self._input_points[min_index]
        for _ in range(point_size + 1):
            candidate = 0
            for i in range(point_size):
                if i == current_index or i in vertices_index:
                    continue

                candidate = i
                break
            for i in range(candidate + 1, point_size):
                if i == current_index or i in vertices_index:
                    continue

                point_first:Vector2D = self._input_points[candidate]
                point_second:Vector2D = self._input_points[i]

                area = Triangle2D.double_signed_area_st(
                    current_point, point_first, point_second)

                if area < 0.0:
                    candidate = i

                elif (area < EPSILON and
                        current_point.dist2(point_first) > current_point.dist2(point_second)):
                    candidate = i
            current_index = candidate
            current_point = self._input_points[current_index]
            vertices_index.append(current_index)
            self._vertices.append(current_point)

            if current_index == min_index:
                break
        for i in range(len(self._vertices)):
            if self._vertices[i] != self._vertices[-1]:
                self._edges.append(
                    Segment2D(self._vertices[i], self._vertices[i + 1]))

        self._vertices.pop()

    def compute_graham_scan(self):
        """Graham scan method
        """
        self.clear_results()

        point_size = len(self._input_points)
        min_index = self.get_min_point_index()

        if point_size < 3 or min_index == -1:
            return

        self.sort_points_angle_from(min_index)

        self._vertices = self._input_points

        top = 1
        for i in range(2, point_size):
            while not is_clockwise(self._vertices[top - 1],
                self._vertices[top], self._input_points[i]):
                top -= 1

            top += 1
            tmp = self._vertices[top]
            self._vertices[top] = self._vertices[i]
            self._vertices[i] = tmp

        top += 1

        del self._vertices[top:len(self._vertices)]

        for i in range(len(self._vertices)):
            if self._vertices[i] != self._vertices[-1]:
                self._edges.append(
                    Segment2D(self._vertices[i], self._vertices[i + 1]))
        self._edges.append(Segment2D(self._vertices[0], self._vertices[-1]))

    def get_min_point_index(self) -> int:
        """get the index of minimum coordinate point

        Returns:
            int: if there is no point return -1 else index of minimum coord
        """
        point_size = len(self._input_points)

        if point_size == 0:  # or point_size < 3:
            return -1

        min_index = 0

        min_point: Vector2D = self._input_points[0]
        for i in range(point_size):
            point: Vector2D = self._input_points[i]

            if min_point.x() > point.x() or (min_point.x() == point.x() and
                                             min_point.y() > point.y()):
                min_point = point
                min_index = i

        return min_index

    def sort_points_angle_from(self, index):
        """sort points by anlge from base(0,0)
        """
        if len(self._input_points) <= index:
            return

        tmp = self._input_points[0]
        self._input_points[0] = self._input_points[index]
        self._input_points[index] = tmp

        # base is (0,0)
        self._input_points.sort(key=functools.cmp_to_key(angle_sort_predicate))

    def to_polygon(self) -> Polygon2D:
        """create and get the convex hull polygon

        Returs:
            Polygon2D: a ploygon from the convex hull _vertices
        """
        return Polygon2D(self._vertices)

    def __repr__(self) -> str:
        """represent the convex hull as a string

        Returns:
            str: contains _vertices and _edges
        """
        return f"({self._vertices} , {self._edges})"


# def test():
#     point_list = [Vector2D(), Vector2D(1, 1), Vector2D(0, 1)]
#     c = ConvexHull(point_list)
#     print(c)
