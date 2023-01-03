""" polygon_2d.py file
    Polygon2D: class name
"""
from __future__ import annotations
import math

from pyrusgeom.rect_2d import Rect2D
from pyrusgeom.region_2d import Region2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.size_2d import Size2D
from pyrusgeom.line_2d import Line2D
from pyrusgeom.segment_2d import Segment2D


class XLessEqual:
    """cmp key class for point.x less or equal than threshold
    """
    def __init__(self, thr:float):
        self._thr = thr

    def __call__(self, point: Vector2D) -> bool:
        """operator <=

        Args:
            point (Vector2D): point to check

        Returns:
            bool: return true if point x is less or equal than threshold
        """
        return point.x() <= self._thr

    def thr(self) -> float:
        """return the threshold

        Returns:
            float: return key threshold
        """
        return self._thr


class XMoreEqual:
    """cmp key class for point.x more or equal than threshold
    """
    def __init__(self, thr:float):
        self._thr = thr

    def __call__(self, point: Vector2D) -> bool:
        """operator >=

        Args:
            point (Vector2D): point to check

        Returns:
            bool: return true if point x is more or equal than threshold
        """
        return point.x() >= self._thr

    def thr(self) -> float:
        """return the threshold

        Returns:
            float: return key threshold
        """
        return self._thr


class YLessEqual:
    """cmp key class for point.y less or equal than threshold
    """
    def __init__(self, thr:float):
        self._thr = thr

    def __call__(self, point: Vector2D) -> bool:
        """operator <=

        Args:
            point (Vector2D): point to check

        Returns:
            bool: return true if point y is less or equal than threshold
        """
        return point.y() <= self._thr

    def thr(self) -> float:
        """return the threshold

        Returns:
            float: return key threshold
        """
        return self._thr


class YMoreEqual:
    """cmp key class for point.y more or equal than threshold
    """
    def __init__(self, thr:float):
        self._thr = thr

    def __call__(self, point: Vector2D) -> bool:
        """operator >=

        Args:
            point (Vector2D): point to check

        Returns:
            bool: return true if point y is more or equal than threshold
        """
        return point.y() >= self._thr

    def thr(self) -> float:
        """return the threshold

        Returns:
            float: return key threshold
        """
        return self._thr


class Polygon2D(Region2D):
    """ handling polygons in SS2D

    Args:
        Region2D (mother class): each polygon is a region

    Attributes:
        _vertices : a list of vectors
    """

    def __init__(self, *args):
        """This is the class init function and creates the polygon.

            Defualt:
                create an empty polygon with one point (0,0).
            OR
                create a polygon with given points
            Args:
                none: for default empty polygon
                one:
                    list: array of input points
                else:
                    bunch of vector2D

        """
        super().__init__()
        if len(args) == 0:
            self._vertices = [Vector2D()]
        elif len(args[0]) > 0:
            self._vertices = args[0].copy()
        else:
            self._vertices = args # TODO:Check this for object init change

    def clear(self) -> None:
        """clear all data.
        """
        self._vertices = [Vector2D()]

    def assign(self, points:list[Vector2D]) -> Polygon2D:
        """set polygon with given points and returns a reference to itself
        Args:
            points(list) : points to assign
        Returns:
            Polygon2D: rturn itself
        """
        if len(points) > 0:
            self._vertices = points.copy()
        return self

    def add_vertex(self, point: Vector2D) -> None:
        """append point to polygon

        Args:
            point(Vector2d): point to add
        """
        self._vertices.append(point)

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

    def get_bounding_box(self) -> Rect2D:
        """get bounding box of this polygon

        Returns:
            bounding box of this polygon
        """
        if len(self._vertices) == 0:
            return Rect2D()
        x_min = float("inf")
        x_max = - float("inf")
        y_min = float("inf")
        y_max = - float("inf")
        for point in self._vertices:
            if point.x() > x_max:
                x_max = point.x()

            if point.x() < x_min:
                x_min = point.x()

            if point.y() > y_max:
                y_max = point.y()

            if point.y() < y_min:
                y_min = point.y()
        return Rect2D(Vector2D(x_min, y_min), Size2D(x_max - x_min, y_max - y_min))

    def contains(self, point: Vector2D, allow_on_segment:bool=True) :#-> bool:
        # TODO : how to OverLoad in python
        """check if given point is in this polygon or not

        Args:
            point(Vector2D): point to check
            allow_on_segment(bool): allows points on the outline

        Returns:
            bool: True if point is in this polygon (or on the line)
        """

        if len(self._vertices) <= 0:
            return False
        if len(self._vertices) == 1:
            return allow_on_segment and (self._vertices[0] == point)

        bounding_box = self.get_bounding_box()
        if not bounding_box.contains(point):
            return False

        # make virtual half line
        line = Segment2D(point, Vector2D(point.x() + ((
            bounding_box.right() - bounding_box.left() + bounding_box.bottom() - bounding_box.top())
            + (self._vertices[0] - point).r()) * 3.0, point.y()))

        # check intersection with all segments
        inside = False
        min_line_x = bounding_box.right() + 1.0
        for i in range(len(self._vertices)):
            p1_index = i + 1

            if p1_index >= len(self._vertices):
                p1_index = 0

            p_0 = self._vertices[i]
            p_1 = self._vertices[p1_index]

            if not allow_on_segment and Segment2D(p_0, p_1).on_segment(point):
                return False

            if allow_on_segment and point == p_0:
                return True

            if line.exist_intersection(Segment2D(p_0, p_1)):
                if p_0.y() == point.y() or p_1.y() == point.y():
                    if p_0.y() == point.y():
                        if p_0.x() < min_line_x:
                            min_line_x = p_0.x()

                    if p_1.y() == point.y():
                        if p_1.x() < min_line_x:
                            min_line_x = p_1.x()

                    if p_0.y() == p_1.y() or p_0.y() < point.y() or p_1.y() < point.y():
                        continue
                inside = not inside # inside * -2 #

        return inside

    def bounding_box_center(self) -> Vector2D:
        """get center of bounding box of this polygon

        Returns:
            Vector2D: center of bounding box of this polygon
        """
        return self.get_bounding_box().center()

    def dist(self, point: Vector2D, check_as_plane=True) -> float:
        """get minimum distance between this polygon and point

        Args:
            point(Vector2d): point to check
            check_as_plane(bool): if this parameter is true, the polygon
            counts as a plane polygon otherwise as a polyline polygon.

        Returns:
            float: minimum distance between this polygon and point
        """
        size = len(self._vertices)

        if size == 1:
            return (self._vertices[0] - point).r()

        if check_as_plane and self.contains(point):
            return 0.0

        min_dist = float('inf')
        for i in range(size - 1):

            seg = Segment2D(self._vertices[i],
                            self._vertices[i + 1])

            point_dist = seg.dist(point)

            if point_dist < min_dist:
                min_dist = point_dist

        if size >= 3:
            seg = Segment2D(self._vertices[size - 1], self._vertices[0])

            point_dist = seg.dist(point)

            if point_dist < min_dist:
                min_dist = point_dist

        return min_dist


    def area(self) -> float:
        """get area of this polygon

        Returns:
            float: value of area with sign.
        """
        return math.fabs(self.double_signed_area() * 0.5)

    def double_signed_area(self) -> float:
        """calculate doubled signed area value

        If vertices are placed counterclockwise order, positive number.
        If vertices are placed clockwise order, negative number.
        Otherwise, 0.

        Returns:
            float: value of doubled signed area.
        """
        size = len(self._vertices)
        ds_area_value = 0.0

        if size < 3:
            return ds_area_value

        for i in range(size):
            n_count = i + 1
            if n_count == size:
                n_count = 0
            ds_area_value += (self._vertices[i].x() * self._vertices[n_count].y()
                              - self._vertices[n_count].x() * self._vertices[i].y())

        return ds_area_value

    def is_counter_clockwise(self) -> bool:
        """check vertexes of self polygon is placed counterclockwise ot not

        Returns:
            bool: True if counterclockwise. else false
        """
        return self.double_signed_area() > 0.0

    def is_clockwise(self) -> bool:
        """check vertexes of self polygon is placed clockwise ot not

        Returns:
            bool: True if clockwise. else false
        """
        return self.double_signed_area() < 0.0

    def get_rectangle_clipped_polygon(self, rect: Rect2D) -> Polygon2D:
        """get a polygon clipped and cropped by a rectangle

        if polygon is divided into more by edges of rectangle, each
        separated polygon is going to connect to the frist polygon.

        Args:
            rect (Rect2D): rectangle for clipping

        Returns:
            Polygon2D: a united polygon
        """
        if len(self._vertices) == 0:
            return Polygon2D()

        points = self._vertices
        clipped_p_1 = []
        clipped_p_2 = []
        clipped_p_3 = []
        clipped_p_4 = []
        clipped_p_1 = Polygon2D.get_line_clipped_polygon(XLessEqual(rect.right()),
                                                points,
                                                Line2D(Vector2D(rect.right(), 0.0), AngleDeg(90.0)))

        clipped_p_2 = Polygon2D.get_line_clipped_polygon(YLessEqual(rect.bottom()),
                                                clipped_p_1,
                                                Line2D(Vector2D(0.0, rect.top()), AngleDeg(0.0)))

        clipped_p_3 = Polygon2D.get_line_clipped_polygon(XMoreEqual(rect.left()),
                                                clipped_p_2,
                                                Line2D(Vector2D(rect.left(), 0.0), AngleDeg(90.0)))

        clipped_p_4 = Polygon2D.get_line_clipped_polygon(YMoreEqual(rect.top()),
                                                clipped_p_3,
                                                Line2D(Vector2D(0.0, rect.top()), AngleDeg(0.0)))

        return Polygon2D(clipped_p_4)

    @staticmethod
    def get_line_clipped_polygon(in_region, points:list[Vector2D], line:Line2D) -> list[Vector2D]:
        """get points clipped by a line

        Args:
            in_geion(side_class): cmp key class - XLessEqual,YLessEqual,XMoreEqual,YMoreEqual
            points(list[Vector2D]): list of points
            line(Line2D): line for clipping

        Returns:
            list[Vector2D]: a list contains the final points
        """
        new_points = []
        in_rectangle = []
        for point in points:
            in_rectangle.append(in_region(point))
        for i in range(len(points)):
            index_0 = i
            index_1 = i + 1
            if index_1 >= len(points):
                index_1 = 0

            p_0 = points[index_0]
            p_1 = points[index_1]

            if in_rectangle[index_0]:
                if in_rectangle[index_1]:
                    new_points.append(p_1)
                else:
                    cuted = line.intersection(Line2D(p_0, p_1))

                    if not cuted.is_valid():
                        return new_points
                    new_points.append(cuted)
            else:
                if in_rectangle[index_1]:
                    cuted = line.intersection(Line2D(p_0, p_1))

                    if not cuted.is_valid():
                        return new_points

                    new_points.append(cuted)
                    new_points.append(p_1)
        return new_points

    def __repr__(self):
        """represent the polygon as a string

        Returns:
            str: contains _vertices
        """
        return f"({self._vertices})"


# def test():
#     p = Polygon2D([Vector2D(0, 0), Vector2D(0, 4), Vector2D(4, 4), Vector2D(4, 0)])
#     v = [Vector2D(2, 2), Vector2D(5, 5)]
#     print(p)
#     print(p.is_clockwise(), p.is_counter_clockwise())
#     print(p.double_signed_area(), p.area())
#     print(p.get_bounding_box())
#     print(p.contains(v[0]), p.contains(v[1]))
