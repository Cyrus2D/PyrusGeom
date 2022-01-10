from __future__ import annotations
from typing import Union
from PyrusGeom.math_values import *
import math


class AngleDeg:
    def __init__(self, *args) -> None:
        if len(args) == 0:
            self._degree = 0
        elif len(args) == 1:
            if isinstance(args[0], AngleDeg):
                self._degree = args[0].degree()
            else:
                self._degree = args[0]
        else:
            raise Exception('The input should be an AngleDeg or a degree')
        self.normal()

    def degree(self) -> float:
        return self._degree

    def set_degree(self, degree: float) -> None:
        self._degree = degree

    def set_angle(self, angle: AngleDeg) -> None:
        self._degree = angle.degree()

    def normal(self) -> None:
        if self._degree < -360.0 or 360.0 < self._degree:
            self._degree = math.fmod(self._degree, 360.0)

        if self._degree < -180.0:
            self._degree += 360.0

        if self._degree > 180.0:
            self._degree -= 360.0

    def is_within(self, left: Union[AngleDeg, float, int], right: Union[AngleDeg, float, int]) -> bool:
        if not isinstance(left, AngleDeg):
            left = AngleDeg(left)
        if not isinstance(right, AngleDeg):
            right = AngleDeg(right)
        if left.is_left_equal_of(right):
            if left.is_left_equal_of(self) and self.is_left_equal_of(right):
                return True
        else:
            if self.is_left_equal_of(right) or left.is_left_equal_of(self):
                return True
        return False

    def abs(self) -> float:
        return math.fabs(self.degree())

    def radian(self) -> float:
        return self.degree() * DEG2RAD

    def reverse(self) -> AngleDeg:
        if self._degree >= 0:
            self._degree = -(180 - self._degree)
        else:
            self._degree = 180 + self._degree
        return self

    def reverse_angle(self) -> AngleDeg:
        angle = AngleDeg(self.degree())
        angle.reverse()
        return angle

    def is_left_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = angle.degree() - self.degree()
        return (0.0 < diff < 180.0) or diff < -180.0

    def is_right_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = self.degree() - angle.degree()
        return (0.0 < diff < 180.0) or diff < -180.0

    def is_left_equal_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = angle.degree() - self._degree
        return 0.0 <= diff < 180.0 or diff < -180.0

    def is_right_equal_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = self.degree() - angle.degree()
        return (0.0 <= diff < 180.0) or diff < -180.0

    def copy(self) -> AngleDeg:
        return AngleDeg(self._degree)

    def get_normalized(self) -> float:
        return (self.degree() + 180) / 360

    def __iadd__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        if isinstance(other, AngleDeg):
            other = other.degree()
        self._degree += other
        self.normal()
        return self

    def __isub__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        if isinstance(other, AngleDeg):
            other = other.degree()
        self._degree -= other
        self.normal()
        return self

    def __imul__(self, other: Union[float, int]) -> AngleDeg:
        self._degree *= other
        self.normal()
        return self

    def __idiv__(self, other: Union[float, int]) -> AngleDeg:
        self._degree /= other
        self.normal()
        return self

    def __add__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        if type(other) == AngleDeg:
            new_angle_deg = AngleDeg(self._degree + other.degree())
        else:
            new_angle_deg = AngleDeg(self._degree + other)
        return new_angle_deg

    def __sub__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        if type(other) == AngleDeg:
            return AngleDeg(self._degree - other._degree)
        else:
            return AngleDeg(self._degree - other)

    def __mul__(self, other: Union[float, int]) -> AngleDeg:
        new_angle_deg = AngleDeg(self._degree * other)
        return new_angle_deg

    def __floordiv__(self, other: Union[float, int]) -> AngleDeg:
        new_angle_deg = AngleDeg(self._degree / other)
        return new_angle_deg

    def __repr__(self):
        return str(self.degree())

    def __float__(self):
        return float(self.degree())

    def __neg__(self) -> AngleDeg:
        new_angle_deg = AngleDeg(-self._degree)
        return new_angle_deg

    def __eq__(self, other):
        if type(other) == AngleDeg:
            self._degree = other.degree()
        else:
            self._degree = other
            self.normal()

    def cos(self) -> float:
        return math.cos(self._degree * DEG2RAD)

    def sin(self) -> float:
        return math.sin(self._degree * DEG2RAD)

    def tan(self) -> float:
        return math.tan(self._degree * DEG2RAD)

    @staticmethod
    def rad2deg(rad: float) -> float:
        return rad * RAD2DEG

    @staticmethod
    def deg2rad(deg: float) -> float:
        return deg * DEG2RAD

    @staticmethod
    def cos_deg(deg: float) -> float:
        return math.cos(AngleDeg.deg2rad(deg))

    @staticmethod
    def sin_deg(deg: float) -> float:
        return math.sin(AngleDeg.deg2rad(deg))

    @staticmethod
    def tan_deg(deg: float) -> float:
        return math.tan(AngleDeg.deg2rad(deg))

    @staticmethod
    def acos_deg(cosine: float) -> float:
        if cosine >= 1.0:
            return 0.0
        elif cosine <= -1.0:
            return 180.0
        else:
            AngleDeg.rad2deg(math.acos(cosine))

    @staticmethod
    def asin_deg(sine: float) -> float:
        if sine >= 1.0:
            return 90.0
        elif sine <= -1.0:
            return -90.0
        else:
            return AngleDeg.rad2deg(math.asin(sine))

    @staticmethod
    def atan_deg(tangent: float) -> float:
        return AngleDeg.rad2deg(math.atan(tangent))

    @staticmethod
    def atan2_deg(y: float, x: float) -> float:
        if math.fabs(x) < EPSILON and math.fabs(y) < EPSILON:
            return 0.0
        else:
            return AngleDeg.rad2deg(math.atan2(y, x))

    @staticmethod
    def bisect(left: float, right: float) -> Union[AngleDeg, float]:
        result = AngleDeg(left)
        rel = AngleDeg(right - left)
        diff = result.degree() - AngleDeg(right).degree()
        half_deg = rel.degree() * 0.5
        result += half_deg
        if (0.0 < diff < 180.0) or diff < -180.0:
            return result
        return result + 180.0
