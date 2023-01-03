""" segment_2d.py file
    Segment2D: class name
    Class attributes: _origin,_terminal
    TODO: fix the circular import tri-segmant

"""
from __future__ import annotations
from typing import Union
import math

from pyrusgeom.triangle_2d import Triangle2D
from pyrusgeom.line_2d import Line2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.math_values import CALC_ERROR, EPSILON


class Segment2D:
    """ Handling segments in SS2D

    Attributes:
        _origin: a Vector2D for orgin point
        _terminal: a Vector2D for terminal point
    """

    def __init__(self, *args) -> None:
        """This is the class init function for Segment2D.

        Defualt:
            create a segment starts at (0,0) and ends at (0,0)
        OR:
            bulid a segment2d with given values

        Args:
            four:
                4 float:
                    float: origin_x 1st point x value of segment edge
                    float: origin_y 1st point y value of segment edge
                    float: terminal_x 2nd point x value of segment edge
                    float: terminal_y 2nd point y value of segment edge
            three:
                1 vector 2 float:
                    Vector2D: origin point
                    float: length of line segment
                    float: line direction from origin point
            two:
                2 vector:
                    Vector2D: origin 1st point of segment edge
                    Vector2D: terminal 2nd point of segment edge
            none:
                Default

        Raises:
            Exception: input must be (4 float) or (1 vector2d , 2 float) or (2 vector2d) or nothing
        """
        self._origin: Vector2D = Vector2D(0, 0)
        self._terminal: Vector2D = Vector2D(0, 0)
        if len(args) == 2:
            self._origin = Vector2D(args[0])
            self._terminal = Vector2D(args[1])
        elif len(args) == 3:
            self._origin = Vector2D(args[0])
            self._terminal = args[0] + Vector2D.from_polar(args[1], args[2])
        elif len(args) == 4:
            self._origin = Vector2D(args[0], args[1])
            self._terminal = Vector2D(args[2], args[3])
        elif len(args) == 0:
            self._origin: Vector2D = Vector2D(0, 0)
            self._terminal: Vector2D = Vector2D(0, 0)
        else:
            raise Exception("input must be (4 float) or \
                (1 vector2d , 2 float) or (2 vector2d) or nothing")

    def assign(self, *args) -> None:
        """same as __init__

        Defualt:
            reset the segment starts at (0,0) and ends at (0,0)
        OR:
            refill the segment2d with given values

        Args:
            four:
                4 float:
                    float: origin_x 1st point x value of segment edge
                    float: origin_y 1st point y value of segment edge
                    float: terminal_x 2nd point x value of segment edge
                    float: terminal_y 2nd point y value of segment edge
            three:
                1 vector 2 float:
                    Vector2D: origin point
                    float: length of line segment
                    float: line direction from origin point
            two:
                2 vector:
                    Vector2D: origin 1st point of segment edge
                    Vector2D: terminal 2nd point of segment edge
            none:
                Default

        Raises:
            Exception: input must be (4 float) or (1 vector2d , 2 float) or (2 vector2d) or nothing
        """
        # self.__init__(args)
        self._origin: Vector2D = Vector2D(0, 0)
        self._terminal: Vector2D = Vector2D(0, 0)
        if len(args) == 2:
            self._origin = Vector2D(args[0])
            self._terminal = Vector2D(args[1])
        elif len(args) == 3:
            self._origin = Vector2D(args[0])
            self._terminal = args[0] + Vector2D.from_polar(args[1], args[2])
        elif len(args) == 4:
            self._origin = Vector2D(args[0], args[1])
            self._terminal = Vector2D(args[2], args[3])
        elif len(args) == 0:
            self._origin: Vector2D = Vector2D(0, 0)
            self._terminal: Vector2D = Vector2D(0, 0)
        else:
            raise Exception("input must be (4 float) or \
                (1 vector2d , 2 float) or (2 vector2d) or nothing")

    def is_valid(self) -> bool:
        """check if self line segment is valid or not.

        origin's coordinates value have to be different from terminal's one.

        Returns:
            bool: True if origin is not equal with terminal. else False.
        """
        return not self._origin.equals_weakly(self._terminal)

    def origin(self) -> Vector2D:
        """get a copy of 1st point segment edge

        Returns:
            Vector2D: a Vector1d with the 1st point segment values
        """

        return Vector2D(self._origin)

    def origin_(self) -> Vector2D:
        """get 1st point of segment edge

        Returns:
            Vector2D: reference to the vector object
        """
        return self._origin

    def terminal(self) -> Vector2D:
        """get a copy of 2nd point segment edge

        Returns:
            Vector2D: a Vector1d with the 2nd point segment values
        """

        return Vector2D(self._terminal)

    def terminal_(self) -> Vector2D:
        """get og 2nd point of segment edge

        Returns:
            Vector2D: reference to the vector object
        """
        return self._terminal

    def line(self) -> Line2D:
        """get line generated from segment

        Returns:
            Line2D: generated line object
        """
        return Line2D(self._origin, self._terminal)

    def length(self) -> float:
        """get the length of this segment

        Returns:
            float: distance value
        """
        return self._origin.dist(self._terminal)

    def direction(self) -> AngleDeg:
        """get the direction angle of self line segment

        Returns:
            AngleDeg: angle object
        """
        return (self._terminal - self._origin).th()

    def swap(self) -> Segment2D:
        """swaps segment edge point and returns it

        Returns:
            Segment2D: self object
        """

        tmp = self._origin
        self._origin = self._terminal
        self._terminal = tmp
        return self

    def copy(self) -> Segment2D:
        """get a copy of this Segment

        Returns:
            Segment2D: copy object
        """
        return Segment2D(self.origin(), self.terminal())

    def reverse(self) -> Segment2D:
        """swap segment edge point and returns it.

        This method is equivalent to swap()

        Returns:
            Segment2D: self object
        """
        return self.swap()

    def reversed_segment(self) -> Segment2D:
        """create a copy reversed line segment.

        Returns:
            Segment2D: reversed copy object
        """
        return Segment2D(self._origin, self._terminal).reverse()

    def perpendicular_bisector(self) -> Line2D:
        """make perpendicular bisector line from segment points

        Returns:
            Line2D: line object
        """
        return Line2D.perpendicular_bisector(self._origin, self._terminal)

    def contains(self, point: Vector2D) -> bool:
        """check if the point is within the CALC_ERROR rectangle
            defined by this segment as a diagonal line.
        Args:
            point (Vector2D): considered point

        Returns:
            bool: True if rectangle contains point. else False
        """
        return (point.x() - self._origin.x()) * (point.x() - self._terminal.x()) <= CALC_ERROR and (
        point.y() - self._origin.y()) * (point.y() - self._terminal.y()) <= CALC_ERROR

    def __eq__(self, other: Segment2D) -> bool:
        """check if self line segment has completely same value as input line segment.

        Args:
            other (Segment2D): compared object.

        Returns:
            bool: true if same. false if not.
        """
        return self._origin == other.origin_() and self._terminal == other.terminal_()

    def equals_weakly(self, other: Segment2D) -> bool:
        """check if self line segment has weakly same value as input line segment.

        Args:
            other (Segment2D): compared object.

        Returns:
            bool: true if almostequals. false if not.
        """
        return self._origin.equals_weakly(other.origin()) and \
            self._terminal.equals_weakly(other.terminal())

    def projection(self, point: Vector2D) -> Vector2D:
        """calculates projection point from input point

        if it does not exist, the invalidated value vector is returned.

        Args:
            point (Vector2D): input point

        Returns:
            Vector2D: projection point from input point.
        """
        direction = self._terminal - self._origin
        length = direction.r()

        if length < EPSILON:
            return self._origin

        direction /= length  # normalize

        direction_ip = direction.inner_product(point - self._origin)
        if -EPSILON < direction_ip < length + EPSILON:
            direction *= direction_ip
            tmp_vec = Vector2D(self._origin)
            tmp_vec += direction
            return tmp_vec

        return Vector2D.invalid()

    def intersection(self, *args) -> Vector2D:
        """check & get the intersection point with other line or segment

        Args:
            one:
                Line2D: checked line object
            two:
                Segment2D: checked segment
                Boolean: if it value is False, end point is disallowed as an intersection.

        if it does not exist, the invalidated value vector is returned.

        Returns:
            Vector2D: intersection point.
        """
        if isinstance(args[0], Line2D):
            tmp_line = self.line()
            sol = tmp_line.intersection(args[0])
            if not sol.is_valid() or not self.contains(sol):
                return Vector2D.invalid()
            return sol

        elif isinstance(args[0], Segment2D):
            allow_end_point = False
            if len(args) == 2 and isinstance(args[1], bool):
                allow_end_point = args[1]
            sol = self.line().intersection(args[0].line())
            if not sol.is_valid() or not self.contains(sol) or not args[0].contains(sol):
                return Vector2D.invalid()
            if not allow_end_point and not self.exist_intersection_except_endpoint(args[0]):
                return Vector2D.invalid()
            return sol

        else:
            return Vector2D.invalid()

    def exist_intersection(self, other: Union[Segment2D, Line2D]) -> bool:
        """check if segment and other(line/segment) cross each other or not.

        Args:
            other (Union[Segment2D,Line2D]): other object for cross checking

        Returns:
            bool: True if this segment crosses. else returns False
        """

        if isinstance(other, Segment2D):
            tri_a0 = Triangle2D.double_signed_area_st(
                self._origin, self._terminal, other.origin())
            tri_a1 = Triangle2D.double_signed_area_st(
                self._origin, self._terminal, other.terminal())
            tri_b0 = Triangle2D.double_signed_area_st(
                other.origin(), other.terminal(), self._origin)
            tri_b1 = Triangle2D.double_signed_area_st(
                other.origin(), other.terminal(), self._terminal)

            if tri_a0 * tri_a1 < 0.0 and tri_b0 * tri_b1 < 0.0:
                return True

            if self._origin == self._terminal:
                if other.origin() == other.terminal():
                    return self._origin == other.origin()

                return tri_b0 == 0.0 and other.check_intersects_on_line(self._origin)

            if other.origin() == other.terminal():
                return tri_a0 == 0.0 and self.check_intersects_on_line(other.origin())

            if tri_a0 == 0.0 and self.check_intersects_on_line(other.origin()) or (
                    tri_a1 == 0.0 and self.check_intersects_on_line(other.terminal())) or (
                    tri_b0 == 0.0 and other.check_intersects_on_line(self._origin)) or (
                    tri_b1 == 0.0 and other.check_intersects_on_line(self._terminal)):
                return True
            return False
        if isinstance(other, Line2D):
            tri_a0 = other.a() * self._origin.x() + other.b() * self._origin.y() + other.c()
            tri_a1 = other.a() * self._terminal.x() + other.b() * \
                self._terminal.y() + other.c()
            return tri_a0 * tri_a1 <= 0.0

    def check_intersects_on_line(self, point: Vector2D) -> bool:
        """check if given point intersects on line

        Args:
            point (Vector2D): input point

        Returns:
            bool: True if intersects. else False
        """
        if self._origin.x() == self._terminal.x():
            return (self._origin.y() <= point.y() <= self._terminal.y()) or (
                self._terminal.y() <= point.y() <= self._origin.y())
        return (self._origin.x() <= point.x() <= self._terminal.x()) or (
            self._terminal.x() <= point.x() <= self._origin.x())

    def exist_intersection_except_endpoint(self, other: Segment2D) -> bool:
        """check if segments intersect each other on non terminal point.

        Args:
            other (Segment2D): other segment

        Returns:
            bool: True if segments intersect and intersection point is not a
                terminal point of segment.
                False if segments do not intersect or intersect on terminal point of segment.
        """
        return (Triangle2D.double_signed_area_st(
            self._origin,
            self._terminal,
            other.origin())
            * Triangle2D.double_signed_area_st(
                self._origin,
            self._terminal,
            other.terminal()) < 0.0) and (
            Triangle2D.double_signed_area_st(
                other.origin(),
                other.terminal(),
                self._origin)
            * Triangle2D.double_signed_area_st(
                other.origin(),
                other.terminal(),
                self._terminal) < 0.0)

    def intersects_except_endpoint(self, other: Segment2D) -> bool:
        """check if segments intersect each other on non terminal point.

        This method is equivalent to exist_intersection_except_endpoint()

        Args:
            other (Segment2D): other segment

        Returns:
            bool: True if segments intersect and intersection point is not a
                terminal point of segment.
                False if segments do not intersect or intersect on terminal point of segment.
        """
        return self.exist_intersection_except_endpoint(other)

    def nearest_point(self, point: Vector2D) -> Vector2D:
        """find minimal distance point on segment from input point.

        Args:
            point (Vector2D): input point.

        Returns:
            Vector2D: nearest point on segment. if multiple nearest points found.
                    returns one of them.
        """
        vec_tmp = self._terminal - self._origin

        len_square = vec_tmp.r2()

        if len_square == 0.0:
            return self._origin

        inner_product = vec_tmp.inner_product((point - self._origin))

        if inner_product <= 0.0:
            return self._origin

        if inner_product >= len_square:
            return self._terminal

        return self._origin + vec_tmp * inner_product / len_square

    def dist(self, other: Union[Segment2D, Vector2D]) -> float:
        """get minimum distance between this segment and other input

        Args:
            other (Union[Segment2D, Vector2D]): point or another segment

        Raises:
            Exception: Input must be a Vector2D or a Segement2D

        Returns:
            float: minimum distance between these two
        """

        if isinstance(other, Vector2D):
            other: Vector2D = other
            length = self.length()
            if length == 0.0:
                return self._origin.dist(other)
            tmp_vec = self._terminal - self._origin
            prod = tmp_vec.inner_product(other - self._origin)
            if 0.0 <= prod <= length * length:
                return math.fabs(Triangle2D.double_signed_area_st(
                    self._origin,
                    self._terminal,
                    other) / length)
            return math.sqrt(min(self._origin.dist2(other),
                                 self._terminal.dist2(other)))

        if isinstance(other, Segment2D):
            other: Segment2D = other
            if self.exist_intersection(other):
                return 0.0
            return min(self.dist(other.origin()),
                       self.dist(other.terminal()),
                       other.dist(self._origin),
                       other.dist(self._terminal))

        raise Exception("Input must be a Vector2D or a Segement2D")

    def farthest_dist(self, point: Vector2D) -> float:
        """get maximum distance between this segment and input point

        Args:
            point (Vector2D): input point

        Returns:
            float: maximum distance between this segment and point
        """
        return math.sqrt(max(self._origin.dist2(point), self._terminal.dist2(point)))

    def on_segment(self, point: Vector2D) -> float:
        """strictly check if point is on segment or not

        Args:
            point (Vector2D): input point

        Returns:
            float: True if point is on this segment. else False.
        """
        return Triangle2D.double_signed_area_st(self._origin, self._terminal, point) == 0.0 \
            and self.check_intersects_on_line(point)

    def on_segment_weakly(self, point: Vector2D) -> bool:
        """weakly check if point is on segment or not

        Args:
            point (Vector2D): input point

        Returns:
            bool: True if point is on this segment. else False.
        """
        projection = self.projection(point)
        return projection.is_valid() and point.equals_weakly(projection)

    def __repr__(self) -> str:
        """represent Segment2D as a string

        Returns:
            str: Circle2D's _origin and _terminal as string
        """
        return f"[{self._origin},{self._terminal}]"

    def to_str(self, ostr: str) -> None:
        """add segment to the ostr

        Args:
            ostr (str): str to add to it
        """
        ostr += f' (line {round(self.origin().x(), 3)} {round(self.origin().y(), 3)} \
            {round(self.terminal().x(), 3)} {round(self.terminal().y(), 3)})'
