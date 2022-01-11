"""

  \ file ray_2d.py
  \ brief 2D ray line class File.

"""
from __future__ import annotations
from PyrusGeom.line_2d import Line2D
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
from typing import Union


class Ray2D:
    def __init__(self, *args):
        """
        AngleDeg:
        brief constructor with origin and direction else default constructor. all values are set to 0.
        param __o origin point
        param __d direction angle
        Vector2D:
        brief constructor with origin and direction else default constructor. all values are set to 0.
        param __o origin point
        param __d direction angle
        """
        self._origin: Vector2D = Vector2D()
        self._direction: AngleDeg = AngleDeg()
        self._is_valid = False
        if len(args) == 2:
            if isinstance(args[0], Vector2D) and isinstance(args[1], Vector2D):
                self._origin = Vector2D(args[0])
                self._direction = (args[1] - args[0]).th()
                self._is_valid = True
            elif isinstance(args[0], Vector2D) and isinstance(args[1], (AngleDeg, float, int)):
                self._origin = Vector2D(args[0])
                self._direction = AngleDeg(args[1])
                self._is_valid = True

        if not self._is_valid:
            raise Exception('The input should be (two Vector2D) or (A Vector2D and an AngleDeg')

    def origin(self) -> Vector2D:
        """
        brief get origin point
        return const reference to the member variable
        """
        return Vector2D(self._origin)

    def dir(self) -> AngleDeg:
        """
        brief get the angle of this ray line
        return const reference to the member variable
        """
        return AngleDeg(self._direction)

    def origin_(self) -> Vector2D:
        """
        brief get origin point
        return const reference to the member variable
        """
        return self._origin

    def dir_(self) -> AngleDeg:
        """
        brief get the angle of this ray line
        return const reference to the member variable
        """
        return self._direction

    def copy(self) -> Ray2D:
        return Ray2D(self.origin(), self.dir())

    def line(self) -> Line2D:
        """
        brief get line generated from this ray
        return new line object
        """
        return Line2D(self._origin, self._direction)

    def in_right_dir(self, point: Vector2D, thr=10.0) -> bool:
        """
        brief check whether p is on the direction of this Ray
        param point considered point
        param thr threshold angle buffer
        return true or false
        """
        return ((point - self._origin).th() - self._direction).abs() < thr

    def intersection(self, *args) -> Vector2D:
        """
        Line2D
         brief get the intersection point with 'line'
         param other considered line
         return intersection point. if it does not exist, the invalidated value vector is returned.
        Ray2D
         brief get the intersection point with 'ray'
         param other considered line
         return intersection point. if it does not exist, the invalidated value vector is returned.
        """
        if isinstance(args[0], Ray2D):
            tmp_sol = self.line().intersection(args[0].line())
            if not tmp_sol.is_valid():
                return Vector2D.invalid()

            if not self.in_right_dir(tmp_sol) or not args[0].in_right_dir(tmp_sol):
                return Vector2D.invalid()

            return tmp_sol
        if isinstance(args[0], Line2D):
            tmp_sol = self.line().intersection(args[0])
            if not tmp_sol.is_valid():
                return Vector2D.invalid()

            if not self.in_right_dir(tmp_sol):
                return Vector2D.invalid()

            return tmp_sol

    def __repr__(self):
        """
        brief make a logical print.
        return print_able str
        origin point + direction Angle Deg
        """
        return str(self._origin) + " dir : " + str(self._direction)
