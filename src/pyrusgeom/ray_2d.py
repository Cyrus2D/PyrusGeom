""" ray_2d.py file
    Ray2D: class name
    Class attributes:_origin,_drirection,_is_valid
"""
from __future__ import annotations
from typing import Union
import math

from pyrusgeom.line_2d import Line2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.math_values import EPSILON


class Ray2D:
    """ handling rays in SS2D
    Attributes:
        _origin: a Vector2D for the orgin point
        _direction: an AngleDeg for the driection the ray goes
        _is_valid = a boolean for validation
    """

    def __init__(self, origin: Vector2D, direction: Union[Vector2D, AngleDeg, float, int]):
        """This is the class init function for Ray2D.

        Defualt:
            create a Ray started at origin point which has a angle at _direction

        Args:
            origin (Vector2D): origin point
            direction (Union[Vector2D,AngleDeg, float, int]): direction angle

        Raises:
            Exception: The input must be (two Vector2D) or (Vector2D and AngleDeg)
        """
        self._origin: Vector2D = Vector2D(origin)
        self._direction: AngleDeg = AngleDeg()
        self._is_valid = False
        if isinstance(direction, Vector2D):
            self._direction = (direction - origin).th()
            self._is_valid = True
        elif isinstance(direction, (AngleDeg, float, int)):
            self._direction = AngleDeg(direction)
            self._is_valid = True
        elif not self._is_valid:
            raise Exception(
                'The input should be (two Vector2D) or (A Vector2D and an AngleDeg)')

    def origin(self) -> Vector2D:
        """get origin point copy

        Returns:
            Vector2D: origin point value
        """
        return Vector2D(self._origin)

    def dir(self) -> AngleDeg:
        """get the angle copy of this ray line

        Returns:
            AngleDeg: direaction value
        """
        return AngleDeg(self._direction)

    def origin_(self) -> Vector2D:
        """get origin point reference

        Returns:
            Vector2D: og origin point
        """
        return self._origin

    def dir_(self) -> AngleDeg:
        """get the reference direaction of this ray

        Returns:
            AngleDeg: og direaction
        """
        return self._direction

    def copy(self) -> Ray2D:
        """create a copy of this ray

        Returns:
            Ray2D: copy of og ray
        """
        return Ray2D(self.origin(), self.dir())

    def line(self) -> Line2D:
        """get line generated from this ray

        Returns:
            Line2D: new line object
        """
        return Line2D(self._origin, self._direction)

    def in_right_dir(self, point: Vector2D, thr: float = 10.0) -> bool:
        """check whether point is on the direction of this Ray

        Args:
            point (Vector2D): considered point
            thr (float, optional): threshold angle buffer. Defaults to 10.0.

        Returns:
            bool: true if it is on the direction. else false.
        """
        return ((point - self._origin).th() - self._direction).abs() < thr

    def intersection(self, other: Union[Line2D, Ray2D]) -> Vector2D:
        """get the intersection point with line or ray

        Args:
            other (Union[Line2D,Ray2D]): considered line

        Returns:
            Vector2D: intersection point. if it does not exist,
                    the invalidated value vector is returned.
        Raises:
            Exception: The input must be Line2D or Ray2D
        """
        if isinstance(other, Ray2D):
            tmp_sol = self.line().intersection(other.line())
            if not tmp_sol.is_valid():
                return Vector2D.invalid()

            if not self.in_right_dir(tmp_sol) or not other.in_right_dir(tmp_sol):
                return Vector2D.invalid()

            return tmp_sol
        if isinstance(other, Line2D):
            tmp_sol = self.line().intersection(other)
            if not tmp_sol.is_valid():
                return Vector2D.invalid()

            if not self.in_right_dir(tmp_sol):
                return Vector2D.invalid()

            return tmp_sol

        raise Exception("The input should be Line2D or Ray2D")

    def __eq__(self, other: Ray2D) -> bool:
        """operator == for Ray2D

        Args:
            other (Ray2D): right hand side argument
        Returns:
            bool: true if equal or difference is less than EPSILON. else false
        """
        return (math.fabs(self._direction - other.dir_()) < EPSILON
                and self._origin == other.origin_())

    def __repr__(self) -> str:
        """represent Ray2D as a string

        Returns:
            str: Ray2D's origin and direction as string
        """
        return str(self._origin) + " dir : " + str(self._direction)
