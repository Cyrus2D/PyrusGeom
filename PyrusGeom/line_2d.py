"""
  \ file line_2d.py
  \ brief 2D straight line class Source File.

    Line Formula: aX + bY + c = 0
"""
from __future__ import annotations
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
from PyrusGeom.math_values import *
from typing import Union
import math


class Line2D:
    def __init__(self, *args) -> None:
        """
        brief construct directly
        param __a assigned a value
        param __b assigned b value
        param __c assigned c value
        2 Vec
        brief construct from 2 points
        param p1 first point
        param p2 second point
        Vec + Ang
        brief construct from origin point + direction
        param org origin point
        param linedir direction from origin point
        """
        self._a = 0.0
        self._b = 0.0
        self._c = 0.0
        self._is_valid = False
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
                line_dir = args[1] if isinstance(args[1], AngleDeg) else AngleDeg(args[1])
                self._a = -line_dir.sin()
                self._b = line_dir.cos()
                self._c = -self._a * args[0].x() - self._b * args[0].y()
                self._is_valid = True
            elif isinstance(args[0], Vector2D) and isinstance(args[1], Vector2D):
                self._a = -(args[1].y() - args[0].y())
                self._b = args[1].x() - args[0].x()
                self._c = -self._a * args[0].x() - self._b * args[0].y()
                self._is_valid = True
        if not self._is_valid:
            raise Exception('The input should be (2 vector2d) or (3 float) or (vector 2d and angle)')

    def a(self) -> float:
        """
        brief accessor
        return coefficient 'A'  of line formula
        """
        return self._a

    def b(self) -> float:
        """
        brief accessor
        return coefficient 'B'  of line formula
        """
        return self._b

    def c(self) -> float:
        """
        brief accessor
        return coefficient 'C'  of line formula
        """
        return self._c

    def get_x(self, y) -> float:
        """
        brief get X-coordinate correspond to 'y'
        param y considered Y
        return X coordinate
        """
        if math.fabs(self._a) < EPSILON:
            return ERROR_VALUE
        return -(self._b * y + self._c) / self._a

    def get_y(self, x) -> float:
        """
        brief get Y-coordinate correspond to 'x'
        param x considered X
        return Y coordinate
        """
        if math.fabs(self._b) < EPSILON:
            return ERROR_VALUE
        return -(self._a * x + self._c) / self._b

    def copy(self) -> Line2D:
        return Line2D(self._a, self._b, self._c)

    def dist(self, p: Vector2D) -> float:
        """
        brief calculate distance from point to this line
        param p considered point
        return distance value
        """
        return math.fabs(
            (self._a * p.x() + self._b * p.y() + self._c) / math.sqrt(self._a * self._a + self._b * self._b))

    def dist2(self, p: Vector2D) -> float:
        """
        brief get squared distance from this line to point
        param p considered point
        return squared distance value
        """
        d = self._a * p.x() + self._b * p.y() + self._c
        return (d * d) / (self._a * self._a + self._b * self._b)

    def is_parallel(self, other) -> bool:
        """
        brief check if the slope of this line is same to the slope of 'other'
        param other considered line
        retval true almost same
        retval false not same
        """
        return math.fabs(self._a * other.b() - other.a() * self._b) < EPSILON

    def intersection(self, other: Union[Line2D]):
        """
        brief get the intersection point with 'other'
        param other considered line
        return intersection point. if it does not exist, the invalidated value vector is returned.
        """
        return Line2D.line_intersection(self, other)

    def perpendicular(self, point):
        """
        brief calc perpendicular line
        param point the point that perpendicular line pass through
        return perpendicular line
        """
        return Line2D(self._b, -self._a, self._a * point.y() - self._b * point.x())

    def projection(self, point: Vector2D) -> Vector2D:
        """
        brief calc projection point from p
        param p base point
        return projection point
        """
        return self.intersection(self.perpendicular(point))

    @staticmethod
    def line_intersection(line1: Line2D, line2: Line2D) -> Vector2D:
        """
        brief get the intersection point of 2 lines
        param line1 the first line
        param line2 the second line
        return the intersection point. if no intersection, invalidated vector is returned.
        """
        tmp = line1.a() * line2.b() - line1.b() * line2.a()
        if math.fabs(tmp) < EPSILON:
            return Vector2D.invalid()

        return Vector2D((line1.b() * line2.c() - line2.b() * line1.c()) / tmp,
                        (line2.a() * line1.c() - line1.a() * line2.c()) / tmp)

    @staticmethod
    def angle_bisector(origin, left, right) -> Line2D:
        """
        brief make angle bisector line from two angles
        param origin origin point that is passed through by result line
        param left left angle
        param right right angle
        return line object
        """
        return Line2D(origin, AngleDeg.bisect(left, right))

    @staticmethod
    def perpendicular_bisector(point1, point2) -> Line2D:
        """
        brief make perpendicular bisector line from twt points
        param point1 1st point
        param point2 2nd point
        return line object
        """
        if math.fabs(point2.x - point1.x) < EPSILON and math.fabs(point2.y - point1.y) < EPSILON:
            print("Error : points have same coordinate values")
            tmp_vec = Vector2D(point1.x + 1, point2.y)
            return Line2D(point1, tmp_vec)
        tmp = (point2.x * point2.x - point1.x * point1.x + point2.y * point2.y - point1.y * point1.y) * -0.5
        return Line2D(point2.x - point1.x, point2.y - point1.y, tmp)

    def __repr__(self):
        """
        brief make a logical print.
        return print_able str
        aX + bY + c = 0
        """
        if self._c == 0:
            return "({} X + {} Y = 0)".format(self._a, self._b)
        return "({} X + {} Y + {} = 0)".format(self._a, self._b, self._c)


def test():
    a = Line2D(Vector2D(1,1), Vector2D(2,2))
    print(a)


if __name__ == "__main__":
    test()
