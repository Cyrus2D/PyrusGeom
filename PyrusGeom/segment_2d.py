"""
  file segment_2d.py
  brief 2D segment line File.
"""
from __future__ import annotations
from typing import Union
from PyrusGeom.triangle_2d import Triangle2D
from PyrusGeom.line_2d import Line2D
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
import math
from PyrusGeom.math_values import *


class Segment2D:
    def __init__(self, *args) -> None:
        """
        LEN = 2
        brief construct from 2 points
        param origin 1st point of segment edge
        param terminal 2nd point of segment edge
        LEN = 3
        brief construct using origin, and length
        param origin origin point
        param length length of line segment
        param direction line direction from origin point
        LEN = 4
        brief construct directly using raw coordinate values
        param originx() 1st point x value of segment edge
        param originy() 1st point x value of segment edge
        param terminalx() 2nd point y value of segment edge
        param terminaly() 2nd point y value of segment edge
        Len = none
        Default
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

    def assign(self, *args) -> None:
        """
        LEN = 2
        brief construct from 2 points
        param origin first point
        param terminal second point
        LEN = 3
        brief construct using origin, and length
        param origin origin point
        param length length of line segment
        param direction line direction from origin point
        LEN = 4
        brief construct directly using raw coordinate values
        param originx() 1st point x value of segment edge
        param originy() 1st point x value of segment edge
        param terminalx() 2nd point y value of segment edge
        param terminaly() 2nd point y value of segment edge
        """
        self.__init__(args)

    def is_valid(self) -> bool:
        """
        brief check if self line segment is valid or not.
        origin's coordinates value have to be different from terminal's one.
        return checked result.
        """
        return not self._origin.equals_weakly(self._terminal)

    def origin(self) -> Vector2D:
        """
        brief get 1st point of segment edge
        return  reference to the vector object
        """
        return self._origin

    def terminal(self) -> Vector2D:
        """
        brief get 2nd point of segment edge
        return  reference to the vector object
        """
        return self._terminal

    def line(self) -> Line2D:
        """
        brief get line generated from segment
        return line object
        """
        return Line2D(self._origin, self._terminal)

    def length(self) -> float:
        """
        brief get the length of self segment
        return distance value
        """
        return self._origin.dist(self._terminal)

    def direction(self) -> AngleDeg:
        """
        brief get the direction angle of self line segment
        return angle object
        """
        return (self._terminal - self._origin).th()

    def swap(self) -> Segment2D:
        """
        brief swap segment edge point
        return  reference to self object
        """
        tmp = self._origin
        self._origin = self._terminal
        self._terminal = tmp
        return self

    def copy(self) -> Segment2D:
        return Segment2D(self.origin(), self.terminal())

    def reverse(self) -> Segment2D:
        """
        brief swap segment edge point. This method is equivalent to swap(), for convenience.
        return  reference to self object
        """
        return self.swap()

    def reversed_segment(self) -> Segment2D:
        """
        brief get the reversed line segment.
        return  reference to self object
        """
        return Segment2D(self._origin, self._terminal).reverse()

    def perpendicular_bisector(self) -> Line2D:
        """
        brief make perpendicular bisector line from segment points
        return line object
        """
        return Line2D.perpendicular_bisector(self._origin, self._terminal)

    def contains(self, p: Vector2D) -> bool:
        """
        brief check if the point is within the rectangle defined by self segment as a diagonal line.
        return True if rectangle contains p
        """
        return ((p.x() - self._origin.x()) * (p.x() - self._terminal.x()) <= CALC_ERROR and
                (p.y() - self._origin.y()) * (p.y() - self._origin.y()) <= CALC_ERROR)

    def equals(self, other: Segment2D) -> bool:
        """
        brief check if self line segment has completely same value as input line segment.
        param other compared object.
        return checked result.
        """
        return self._origin.equals(other.origin()) and self._terminal.equals(other.terminal())

    def equals_weakly(self, other: Segment2D) -> bool:
        """
        brief check if self line segment has weakly same value as input line segment.
        param other compared object.
        return checked result.
        """
        return self._origin.equals_weakly(other.origin()) and self._terminal.equals_weakly(other.terminal())

    def projection(self, p: Vector2D) -> Vector2D:
        """
        brief calculates projection point from p
        param p input point
        return projection point from p. if it does not exist, the invalidated value vector is returned.
        """
        direction = self._terminal - self._origin
        length = direction.r()

        if length < EPSILON:
            return self._origin

        direction /= length  # normalize

        d = direction.inner_product(p - self._origin)
        if -EPSILON < d < length + EPSILON:
            direction *= d
            tmp_vec = Vector2D(self._origin)
            tmp_vec += direction
            return tmp_vec

        return Vector2D.invalid()

    def intersection(self, *args) -> Vector2D:
        """
        LEN = 1
        brief check & get the intersection point with other line
        param l checked line object
        return intersection point. if it does not exist, the invalidated value vector is returned.
        LEN = 2
        brief check & get the intersection point with other line segment
        param other checked line segment
        param allow_end_point if self value is False, end point is disallowed as an intersection.
        return intersection point. if it does not exist, the invalidated value vector is returned.
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

    def exist_intersection(self, *args) -> bool:
        """
        Segment2D:
        brief check if segments cross each other or not.
        param other segment for cross checking
        return True if self segment crosses, returns False.
        Line2D:
        brief check if self line segment intersects with target line.
        param l checked line
        return checked result
        """
        if isinstance(args[0], Segment2D):
            segment = args[0]
            a0 = Triangle2D.double_signed_area(self._origin, self._terminal, segment.origin())
            a1 = Triangle2D.double_signed_area(self._origin, self._terminal, segment.terminal())
            b0 = Triangle2D.double_signed_area(segment.origin(), segment.terminal(), self._origin)
            b1 = Triangle2D.double_signed_area(segment.origin(), segment.terminal(), self._terminal)

            if a0 * a1 < 0.0 and b0 * b1 < 0.0:
                return True

            if self._origin == self._terminal:
                if segment.origin() == segment.terminal():
                    return self._origin == segment.origin()

                return b0 == 0.0 and segment.check_intersects_on_line(self._origin)

            elif segment.origin() == segment.terminal():
                return a0 == 0.0 and self.check_intersects_on_line(segment.origin())

            if a0 == 0.0 and self.check_intersects_on_line(segment.origin()) or (
                    a1 == 0.0 and self.check_intersects_on_line(segment.terminal())) or (
                    b0 == 0.0 and segment.check_intersects_on_line(self._origin)) or (
                    b1 == 0.0 and segment.check_intersects_on_line(self._terminal)):
                return True
            return False
        elif isinstance(args[0], Line2D):
            line = args[0]
            a0 = line.a() * self._origin.x() + line.b() * self._origin.y() + line.c()
            a1 = line.a() * self._terminal.x() + line.b() * self._terminal.y() + line.c()
            return a0 * a1 <= 0.0

    def check_intersects_on_line(self, p: Vector2D) -> bool:
        """
        brief check is that point Intersects On Line
        param p Vector2D for that point
        return True and False :D
        """
        if self._origin.x() == self._terminal.x():
            return (self._origin.y() <= p.y() <= self._terminal.y()) or (
                    self._terminal.y() <= p.y() <= self._origin.y())
        else:
            return (self._origin.x() <= p.x() <= self._terminal.x()) or (
                    self._terminal.x() <= p.x() <= self._origin.x())

    def exist_intersection_except_endpoint(self, other: Segment2D) -> bool:
        """
        brief check if segments intersect each other on non terminal point.
        param other segment for cross checking
        return True if segments intersect and intersection point is not a
          terminal point of segment.
          False if segments do not intersect or intersect on terminal point of segment.
        """
        return (Triangle2D.double_signed_area(self._origin,
                                              self._terminal,
                                              other.origin()) * Triangle2D.double_signed_area(self._origin,
                                                                                              self._terminal,
                                                                                              other.terminal()) < 0.0) \
               and (Triangle2D.double_signed_area(other.origin(),
                                                  other.terminal(),
                                                  self._origin) * Triangle2D.double_signed_area(other.origin(),
                                                                                                other.terminal(),
                                                                                                self._terminal) < 0.0)

    def intersects_except_endpoint(self, other: Segment2D) -> bool:
        """
        brief check if segments intersect each other on non terminal point. This method is equivalent to
          existIntersectionExceptEndpoint(), for convenience.
        param other segment for cross checking
        return True if segments intersect and intersection point is not a
          terminal point of segment.
          False if segments do not intersect or intersect on terminal point of segment.
        """
        return self.exist_intersection_except_endpoint(other)

    def nearest_point(self, p: Vector2D) -> Vector2D:
        """
        brief get a point on segment where distance of point is minimal.
        param p point
        return nearest point on segment. if multiple nearest points found.
           returns one of them.
        """
        vec_tmp = self._terminal - self._origin

        len_square = vec_tmp.r2()

        if len_square == 0.0:
            return self._origin

        inner_product = vec_tmp.inner_product((p - self._origin))

        if inner_product <= 0.0:
            return self._origin

        elif inner_product >= len_square:
            return self._terminal

        return self._origin + vec_tmp * inner_product / len_square

    def dist(self, *args) -> float:
        """
        Line2D:
        brief get minimum distance between self segment and point
        param p point
        return minimum distance between self segment and point
        Segment2D:
        brief get minimum distance between 2 segments
        param seg segment
        return minimum distance between 2 segments
        """
        if len(args) == 1 and isinstance(args[0], Vector2D):
            vec: Vector2D = args[0]
            length = self.length()
            if length == 0.0:
                return self._origin.dist(vec)
            tmp_vec = self._terminal - self._origin
            prod = tmp_vec.inner_product(vec - self._origin)
            if 0.0 <= prod <= length * length:
                return math.fabs(Triangle2D.double_signed_area(self._origin, self._terminal, vec) / length)
            return math.sqrt(min(self._origin.dist2(vec),
                                 self._terminal.dist2(vec)))

        elif len(args) == 1:
            seg: Segment2D = args[0]
            if self.exist_intersection(seg):
                return 0.0
            return min(self.dist(seg.origin()), self.dist(seg.terminal()), seg.dist(self._origin),
                       seg.dist(self._terminal))

    def farthest_dist(self, p: Vector2D) -> float:
        """
        brief get maximum distance between self segment and point
        param p point
        return maximum distance between self segment and point
        """
        return math.sqrt(max(self._origin.dist2(p), self._terminal.dist2(p)))

    def on_segment(self, p: Vector2D) -> float:
        """
        brief strictly check if point is on segment or not
        param p checked point
        return True if point is on self segment
        """
        return Triangle2D.double_signed_area(self._origin, self._terminal, p) == 0.0 \
               and self.check_intersects_on_line(p)

    def on_segment_weakly(self, p: Vector2D) -> bool:
        """
        brief weakly check if point is on segment or not
        param p checked point
        return True if point is on self segment
        """
        projection = self.projection(p)
        return projection.is_valid() and p.equals_weakly(projection)

    def __repr__(self):
        """
        brief make a logical print.
        return print_able str
        """
        return "[{},{}]".format(self._origin, self._terminal)

    def to_str(self, ostr):
        ostr += ' (line {} {} {} {})'.format(round(self.origin().x(), 3), round(self.origin().y(), 3),
                                             round(self.terminal().x(), 3), round(self.terminal().y(), 3))
