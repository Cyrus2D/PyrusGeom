"""
  file sector_2d.py
  brief 2D sector region File.
"""
from __future__ import annotations
from typing import Union
from PyrusGeom.region_2d import Region2D
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
from PyrusGeom.math_values import *


class Sector2D(Region2D):
    def __init__(self, c: Vector2D, min_r: float, max_r: float, start: AngleDeg, end: AngleDeg) -> None:
        """
        brief constructor with all variables
        @param c center point
        @param min_r smaller radius
        @param max_r bigger radius
        @param start start angle(turn clockwise)
        @param end end angle(turn clockwise)
        """
        super().__init__()

        self._center = c
        if min_r < 0.0:
            self._min_r = 0.0
        else:
            self._min_r = min_r
        if min_r > max_r:
            self._max_r = self._min_r
        else:
            self._max_r = max_r
        self._start = start
        self._end = end
        self.is_valid = True

    def assign(self, c: Vector2D, min_r: float, max_r: float, start: AngleDeg, end: AngleDeg) -> None:
        """
        brief assign new value
        param c center point
        param min_r smaller radius
        param max_r bigger radius
        param start start angle(turn clockwise)
        param end end angle(turn clockwise)
        """
        if type(end) != AngleDeg:
            end = AngleDeg(end)
        if type(start) != AngleDeg:
            start = AngleDeg(start)

        self._center = c
        if min_r < 0.0:
            self._min_r = 0.0
        else:
            self._min_r = min_r
        if min_r > max_r:
            self._max_r = self._min_r
        else:
            self._max_r = max_r
        self._start = start
        self._end = end

    def center(self) -> Vector2D:
        """
        brief get the center point
        @return  reference to the member variable
        """
        return Vector2D(self._center)

    def center_(self) -> Vector2D:
        """
        brief get the center point
        @return  reference to the member variable
        """
        return self._center

    def radius_min(self) -> float:
        """
        brief get the small side radius
        @return  reference to the member variable
        """
        return self._min_r

    def radius_max(self) -> float:
        """
        brief get the big side radius
        @return  reference to the member variable
        """
        return self._min_r

    def angle_left_start(self) -> AngleDeg:
        """
        brief get the left start angle
        @return  reference to the member variable
        """
        return AngleDeg(self._start)

    def angle_right_end(self) -> AngleDeg:
        """
        brief get the right end angle
        @return  reference to the member variable
        """
        return AngleDeg(self._end)

    def angle_left_start_(self) -> AngleDeg:
        """
        brief get the left start angle
        @return  reference to the member variable
        """
        return self._start

    def angle_right_end_(self) -> AngleDeg:
        """
        brief get the right end angle
        @return  reference to the member variable
        """
        return self._end

    def area(self):
        """
        brief calculate the area of self region
        @return the value of area
        """
        pass

    def contains(self, point: Vector2D) -> bool:
        """
        brief check if point is within self region
        param point considered point
        @return True or False
        """
        rel = point - self._center
        d2 = rel.r2()
        return (self._min_r * self._min_r <= d2 <= self._max_r * self._max_r and rel.th().is_within(self._start,
                                                                                                    self._end))

    def get_circumference_min(self) -> float:
        """
        brief get smaller side circumference
        @return the length of circumference
        """
        div = (self._end - self._start).degree()
        if div < 0.0:
            div += 360.0
        return (2.0 * self._min_r * PI) * (div / 360.0)

    def get_circumference_max(self) -> float:
        """
        brief get bigger side circumference
        @return the length of circumference
        """
        div = (self._end - self._start).degree()
        if div < 0.0:
            div += 360.0

        return (2.0 * self._max_r * PI) * (div / 360.0)

    def __repr__(self) -> str:
        """
        brief make a logical print.
        return print_able str
        """
        return f'[v({self._center}) a({self._start}, {self._end}) r({self._min_r}, {self._max_r})]'


""" """


def test():
    a = Sector2D(Vector2D(0, 0), 0, 0, AngleDeg(0), AngleDeg(0))
    b = a.center()
    b.set_x(10)
    print(a.center())

    print(a)


if __name__ == "__main__":
    test()
