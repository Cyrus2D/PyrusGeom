""" sector_2d.py file
    Sector2D: class name
    Class attributes : _center,_min_r,_max_r,_start,_end,is_valid
    TODO: add test and reverse
"""
from __future__ import annotations
import math
from typing import Union

from pyrusgeom.region_2d import Region2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.math_values import EPSILON, PI


class Sector2D(Region2D):
    """handling Sectors in SS2D

    Args:
        Region2D ([type]): created from Region2D class

    Attributes:
        _center: center point
        _min_r: smaller radius
        _max_r: bigger radius
        _start: start angle(turn clockwise)
        _end: end angle(turn clockwise)
        is_valid: is it valid or not
    """

    def __init__(self, center: Vector2D, min_r: float, max_r: float,
                 start: Union[AngleDeg, float], end: Union[AngleDeg, float]) -> None:
        """This is the class init function for sector.

        constructor with all variables

        Args:
            center (Vector2D): center point
            min_r (float): smaller radius
            max_r (float): bigger radius
            start (Union[AngleDeg, float]): start angle(turn clockwise)
            end (Union[AngleDeg, float]): end angle(turn clockwise)
        """
        super().__init__()

        self._center = Vector2D(center)
        self._min_r = min(0.0, min_r)
        self._max_r = max(min_r, max_r)
        self._start = AngleDeg(start)
        self._end = AngleDeg(end)
        self.is_valid = True

    def assign(self, center: Vector2D, min_r: float, max_r: float,
               start: Union[AngleDeg, float], end: Union[AngleDeg, float]) -> None:
        """assign new value

        Args:
            center (Vector2D): center point
            min_r (float): smaller radius
            max_r (float): bigger radius
            start (Union[AngleDeg, float]): start angle(turn clockwise)
            end (Union[AngleDeg, float]): end angle(turn clockwise)
        """
        self._center = Vector2D(center)
        self._min_r = min(0.0, min_r)
        self._max_r = max(min_r, max_r)
        self._start = AngleDeg(start)
        self._end = AngleDeg(end)

    def center(self) -> Vector2D:
        """get the center point copy

        Returns:
            Vector2D: a Vector2D with center point values
        """
        return Vector2D(self._center)

    def center_(self) -> Vector2D:
        """get the center point

        Returns:
            Vector2D: reference to the og member variable
        """
        return self._center

    def radius_min(self) -> float:
        """get the small side radius

        Returns:
            float: the small side radius
        """
        return self._min_r

    def radius_max(self) -> float:
        """get the big side radius

        Returns:
            float: the big side radius
        """
        return self._min_r

    def angle_left_start(self) -> AngleDeg:
        """get the left start angle copy

        Returns:
            AngleDeg: an AngleDeg with start values
        """
        return AngleDeg(self._start)

    def angle_left_start_(self) -> AngleDeg:
        """get the left start angle

        Returns:
            AngleDeg: reference to the og member variable
        """
        return self._start

    def angle_right_end(self) -> AngleDeg:
        """get the right end angle copy

        Returns:
            AngleDeg: an AngleDeg with start values
        """
        return AngleDeg(self._end)

    def angle_right_end_(self) -> AngleDeg:
        """get the right end angle

        Returns:
            AngleDeg: reference to the og member variable
        """
        return self._end

    def area(self) -> float:
        """calculate the area of this sector

        Returns:
            float: the value of area
        """
        circle_area = self._max_r * self._max_r * PI - self._min_r * self._min_r * PI
        div = (self._end - self._start).degree_()
        if div < 0.0:
            div += 360.0
        return circle_area * div / 360.0

    def contains(self, point: Vector2D) -> bool:
        """check if point is within this sector

        Args:
            point (Vector2D): considered point

        Returns:
            bool: True if contains. else False.
        """
        rel = point - self._center
        delta = rel.r2()
        return (self._min_r * self._min_r <= delta <= self._max_r * self._max_r and
                rel.th().is_within(self._start, self._end))

    def get_circumference_min(self) -> float:
        """get smaller side circumference

        Returns:
            float: the length of circumference
        """
        div = (self._end - self._start).degree_()
        if div < 0.0:
            div += 360.0
        return (2.0 * self._min_r * PI) * (div / 360.0)

    def get_circumference_max(self) -> float:
        """get bigger side circumference

        Returns:
            float: the length of circumference
        """
        div = (self._end - self._start).degree_()
        if div < 0.0:
            div += 360.0
        return (2.0 * self._max_r * PI) * (div / 360.0)

    def __eq__(self, other: Sector2D) -> bool:
        """operator == for Sector2D

        Args:
            other (Sector2D): right hand side argument
        Returns:
            bool: true if equal or difference is less than EPSILON. else false
        """
        return (self._center.equals_weakly(other.center_()) and
            self._start == other.angle_left_start_() and
            self._end == other.angle_right_end_() and
            math.fabs(self._min_r - other.radius_min()) < EPSILON and
            math.fabs(self._max_r - other.radius_max()) < EPSILON)
        # return super().__eq__(other)

    def __repr__(self) -> str:
        """represent Sector2D as a string

        Returns:
            str: Sector2D's _center,_start,_end,_min_r and _max_r as string
        """
        return f'[v({self._center}) a({self._start}, {self._end}) \
         r({self._min_r}, {self._max_r})]'
