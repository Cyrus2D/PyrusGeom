""" line_2d.py file
    Line2D: class name
    Line Formula: aX + bY + c = 0
"""
from __future__ import annotations
import math

from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.math_values import EPSILON, ERROR_VALUE


class Line2D:
    """ handling 2D straight line is SS2D.
    Attributes:
        _a,_b,_c
        Line Formula: aX + bY + c = 0
    """

    def __init__(self, *args, **kwargs) -> None:
        """This is the class init function for Line2D

        Args:
            one:
                copy from line
                Line2D: line
            two:
                constructed from 2 points
                (Vector2D, Vector2D)
                Vector2D: first point
                Vector2D: second point

                constructed from origin point + direction
                (Vector2D, AngleDeg)
                Vector2D: org origin point
                AngleDeg: line dir direction from origin point
            three:
                (float, float, float)
                float: assigned a value
                float: assigned b value
                float: assigned c value

        Raises:
            Exception: The input must be (two Vector2D) or (3 float) or
                        (one vector 2D and one angle)
        """
        self._a = 0.0
        self._b = 0.0
        self._c = 0.0
        self._is_valid = False
        if len (kwargs) == 0:
            if len(args) == 3:
                if isinstance(args[0], (float, int)) and \
                        isinstance(args[1], (float, int)) and \
                        isinstance(args[2], (float, int)):
                    self._a = args[0]
                    self._b = args[1]
                    self._c = args[2]
                    self._is_valid = True
            elif len(args) == 2:
                if isinstance(args[0], Vector2D) and isinstance(args[1], (AngleDeg, float, int)):
                    line_dir = args[1] if isinstance(
                        args[1], AngleDeg) else AngleDeg(args[1])
                    self._a = -line_dir.sin()
                    self._b = line_dir.cos()
                    self._c = -self._a * args[0].x() - self._b * args[0].y()
                    self._is_valid = True
                elif isinstance(args[0], Vector2D) and isinstance(args[1], Vector2D):
                    self._a = -(args[1].y() - args[0].y())
                    self._b = args[1].x() - args[0].x()
                    self._c = -self._a * args[0].x() - self._b * args[0].y()
                    self._is_valid = True
            elif len(args) == 1:
                if isinstance(args[0], Line2D):
                    self._a = args[0].a()
                    self._b = args[0].b()
                    self._c = args[0].c()
                    self._is_valid = True
        else:
            if {'a','b','c'} <= set(kwargs):
                self._a = kwargs['a']
                self._b = kwargs['b']
                self._c = kwargs['c']
                self._is_valid = True
            elif {'p1','p2'} <= set(kwargs):
                self._a = -(kwargs['p2'].y() - kwargs['p1'].y())
                self._b = kwargs['p2'].x() - kwargs['p1'].x()
                self._c = -self._a * kwargs['p1'].x() - self._b * kwargs['p1'].y()
                self._is_valid = True
            elif {'p','a'} <= set(kwargs):
                line_dir = kwargs['a'] if isinstance(
                        kwargs['a'], AngleDeg) else AngleDeg(kwargs['a'])
                self._a = -line_dir.sin()
                self._b = line_dir.cos()
                self._c = -self._a * kwargs['p'].x() - self._b * kwargs['p'].y()
                self._is_valid = True
            elif 'l' in kwargs:
                self._a = kwargs['l'].a()
                self._b = kwargs['l'].b()
                self._c = kwargs['l'].c()
                self._is_valid = True
        if not self._is_valid:
            raise Exception('The input should be(2 vector2d) or (3 float) \
                            or (vector 2d and angle)')

    def a(self) -> float:
        """accessor coefficient 'A'

        Returns:
            float:  coefficient 'A'  of line formula
        """
        return self._a

    def b(self) -> float:
        """accessor coefficient 'B'

        Returns:
            float:  coefficient 'B'  of line formula
        """
        return self._b

    def c(self) -> float:
        """accessor coefficient 'C'

        Returns:
            float:  coefficient 'C'  of line formula
        """
        return self._c

    def get_x(self, f_y: float) -> float:
        """get X-coordinate correspond to 'f_y'

        Args:
            f_y (float): considered Y

        Returns:
            float: X coordinate
        """
        if math.fabs(self._a) < EPSILON:
            return ERROR_VALUE
        return -(self._b * f_y + self._c) / self._a

    def get_y(self, f_x) -> float:
        """get Y-coordinate correspond to 'f_x'

        Args:
            f_x (float): considered X

        Returns:
            float: Y coordinate
        """
        if math.fabs(self._b) < EPSILON:
            return ERROR_VALUE
        return -(self._a * f_x + self._c) / self._b

    def copy(self) -> Line2D:
        """return a copy of this line

        Returns:
            Line2D: copy of this line
        """
        return Line2D(self._a, self._b, self._c)

    def dist(self, point: Vector2D) -> float:
        """calculate distance from point to this line

        Args:
            point (Vector2D): considered point

        Returns:
            float: distance value
        """
        return math.fabs(
            (self._a * point.x() + self._b * point.y() + self._c) /
            math.sqrt(self._a * self._a + self._b * self._b))

    def dist2(self, point: Vector2D) -> float:
        """get squared distance from this line to point

        Args:
            point (Vector2D): considered point

        Returns:
            float: squared distance value
        """
        delta = self._a * point.x() + self._b * point.y() + self._c
        return (delta * delta) / (self._a * self._a + self._b * self._b)

    def is_parallel(self, other: Line2D) -> bool:
        """check if the slope of this line is parallel to the slope of 'other'

        Args:
            other (Line2D): considered line

        Returns:
            bool: true if almost parallel. else false
        """
        return math.fabs(self._a * other.b() - other.a() * self._b) < EPSILON

    def intersection(self, other: Line2D) -> Vector2D:
        """get the intersection point with 'other' line

        Args:
            other (Line2D): considered line

        Returns:
            Vector2D: intersection point. if it does not exist,
             the invalidated value vector is returned.
        """
        return Line2D.line_intersection(self, other)

    def perpendicular(self, point: Vector2D) -> Line2D:
        """calculate perpendicular line

        Args:
            point (Vector2D): the point that perpendicular line pass through

        Returns:
            Line2D: perpendicular line
        """
        return Line2D(self._b, -self._a, self._a * point.y() - self._b * point.x())

    def projection(self, point: Vector2D) -> Vector2D:
        """calculate projection point from point

        Args:
            point (Vector2D): base point

        Returns:
            Vector2D: projection point
        """
        return self.intersection(self.perpendicular(point))

    @staticmethod
    def line_intersection(line1: Line2D, line2: Line2D) -> Vector2D:
        """get the intersection point of 2 lines

        Args:
            line1 (Line2D): the first line
            line2 (Line2D): the second line

        Returns:
            Vector2D: the intersection point. if no intersection, invalidated vector is returned.
        """
        tmp = line1.a() * line2.b() - line1.b() * line2.a()
        if math.fabs(tmp) < EPSILON:
            return Vector2D.invalid()

        return Vector2D((line1.b() * line2.c() - line2.b() * line1.c()) / tmp,
                        (line2.a() * line1.c() - line1.a() * line2.c()) / tmp)

    @staticmethod
    def angle_bisector(origin: Vector2D, left: AngleDeg, right: AngleDeg) -> Line2D:
        """make angle bisector line from two angles

        Args:
            origin (Vector2D): point that is passed through by result line
            left (AngleDeg): left angle
            right (AngleDeg):  right angle

        Returns:
            Line2D: line object
        """
        return Line2D(origin, AngleDeg.bisect(left, right))

    @staticmethod
    def perpendicular_bisector(point1: Vector2D, point2: Vector2D) -> Line2D:
        """make perpendicular bisector line from twt points

        Args:
            point1 (Vector2D): 1st point
            point2 (Vector2D): 2nd point

        Returns:
            Line2D: line object
        """
        if (math.fabs(point2.x() - point1.x()) < EPSILON and
                math.fabs(point2.y() - point1.y()) < EPSILON):
            print("Error : points have same coordinate values")
            tmp_vec = Vector2D(point1.x() + 1, point2.y())
            return Line2D(point1, tmp_vec)
        tmp = (point2.x() * point2.x() - point1.x() * point1.x()
               + point2.y() * point2.y() - point1.y() * point1.y()) * -0.5
        return Line2D(point2.x() - point1.x(), point2.y() - point1.y(), tmp)

    def __eq__(self, other: Line2D) -> bool:
        """operator == for Line2D

        Args:
            other (Line2D): right hand side argument
        Returns:
            bool: true if equal or difference is less than EPSILON. else false
        """
        return (math.fabs(self._a * other.b() - other.a() * self._b)
                < EPSILON and self._c == other.c())

    def __repr__(self) -> str:
        """represent Line2D as a string
           aX + bY + c = 0
        Returns:
            str: Line as string
        """

        if self._c == 0:
            return f"({self._a} X + {self._b} Y = 0)"
        return f"({self._a} X + {self._b} Y + {self._c} = 0)"
