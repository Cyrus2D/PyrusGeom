from __future__ import annotations
from typing import Union
from PyrusGeom.angle_deg import AngleDeg
from PyrusGeom.math_values import *
import math


class Vector2D:
    def __init__(self, *args) -> None:
        """
        brief default constructor : create Vector with XY value directly.
        Args:
            param1: number for x
            param2: number for y
            or
            param1: Vector2D
            or
            no param
            if no params is passed, x and y will be 0
        Raises:
            The input should be a Vector2D or two numbers or no input
        """
        self._is_valid = True
        if len(args) == 0:
            self._x = 0
            self._y = 0
        elif len(args) == 1 and isinstance(args[0], Vector2D):
            self._x = args[0].x()
            self._y = args[0].y()
        elif len(args) == 2 and isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)):
            self._x = args[0]
            self._y = args[1]
        else:
            raise Exception('The input should be a Vector2D or two numbers')

    def x(self) -> float:
        """
        brief accessor to x
        Returns:
             X coordinate
        """
        return self._x

    def y(self) -> float:
        """
        brief accessor
        Returns:
             Y coordinate
        """
        return self._y

    def get_x(self) -> float:
        """
        brief accessor to x
        Returns:
             X coordinate
        """
        return self._x

    def get_y(self) -> float:
        """
        brief accessor to y
        Returns:
             Y coordinate
        """
        return self._y

    def copy(self) -> Vector2D:
        """
        brief returns copy of this Vector2D

        Returns:
            Copy of this Vector 2D
        """
        return Vector2D(self._x, self._y)

    def get_copy(self):
        """
        brief returns copy of this Vector2D

        Returns:
            Copy of this Vector 2D
        """
        return self.copy()

    def assign(self, x: float, y: float) -> Vector2D:
        """
        brief assign XY value directly.
        Args:
            x: assigned x value
            y: assigned y value
        Return:
             reference to itself
        """
        self._x = x
        self._y = y
        return self

    def set_x(self, x: Union[int, float]) -> None:
        """
        brief set x of the object to new x.
        Args:
            x: assigned x value
        """
        self._x = x

    def set_y(self, y: Union[int, float]) -> None:
        """
        brief set y of the object to new y.
        Args:
            y: assigned y value
        """
        self._y = y

    def set_x_y(self, x: Union[int, float], y: Union[int, float]) -> None:
        """
        brief set x and y of the object to new x and y.
        Args:
            x: assigned x value
            y: assigned y value
        """
        self._x = x
        self._y = y

    def set_vector(self, other: Vector2D) -> None:
        """
        brief set x and y of the object to the x and y of the new object.
        Args:
            other: A vector 2D
        """
        self._x = other.x()
        self._y = other.y()
        self._is_valid = other.is_valid()

    def set_polar(self, radius: Union[int, float], angle: Union[int, float, AngleDeg]) -> None:
        """
        brief assign XY value from POLAR value.
        Args:
            radius: vector's radius
            angle: vector's angle
        """
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        self._x = radius * angle.cos()
        self._y = radius * angle.sin()

    def validate(self) -> None:
        """
        brief validate this object
        """
        self._is_valid = True

    def invalidate(self) -> None:
        """
        brief invalidate this object
        """
        self._is_valid = False

    def is_valid(self) -> bool:
        """
        brief check is the object valid

        Return:
            is_valid
        """
        return self._is_valid

    def r2(self) -> float:
        """
        brief get the squared length of vector.
        Return:
            squared length value
        """
        return self._x * self._x + self._y * self._y

    def r(self) -> float:
        """
        brief get the length of vector.
        Return:
            length value
        """
        return math.sqrt(self.r2())

    def length(self) -> float:
        """
        brief get the length of vector. this method is equivalent to r().
        Return:
            length value
        """
        return self.r()

    def length2(self):
        """
        brief get the squared length of vector. this method is equivalent to r2().
        Return:
             squared length value
        """
        return self.r2()

    def th(self) -> AngleDeg:
        """
        brief get the angle of vector.
        Return:
            angle
        """
        return AngleDeg(AngleDeg.atan2_deg(self._y, self._x))

    def dir(self) -> AngleDeg:
        """
        brief get the angle of vector. this method is equivalent to th().
        Return:
             angle
        """
        return self.th()

    def abs(self) -> Vector2D:
        """
        brief get new vector that XY values were set to absolute value.
        Return:
            new vector that all values are absolute.
        """
        return Vector2D(abs(self._x), abs(self._y))

    def abs_x(self) -> float:
        """
        brief get absolute x value
        Return:
            absolute x value
        """
        return math.fabs(self._x)

    def abs_y(self):
        """
        brief get absolute y value
        Return:
            absolute y value
        """
        return math.fabs(self._y)

    def add(self, *args) -> None:
        """
        added x and y to the vector 2d

        Args:
            args: (x, y) or another vector 2d
        """
        if len(args) == 1:
            self._x += args[0].x()
            self._y += args[0].y()
        elif len(args) == 2:
            self._x += args[0]
            self._y += args[1]

    def add_x(self, x: Union[int, float]) -> None:
        self._x += x

    def add_y(self, y: Union[int, float]) -> None:
        self._y += y

    def sub(self, *args) -> None:
        """
        sub x and y from the vector 2d

        Args:
            args: (x, y) or another vector 2d
        """
        if len(args) == 1:
            self._x -= args[0].x()
            self._y -= args[0].y()
        elif len(args) == 2:
            self._x -= args[0]
            self._y -= args[1]

    def sub_x(self, x: Union[int, float]) -> None:
        self._x -= x

    def sub_y(self, y: Union[int, float]) -> None:
        self._y -= y

    def scale(self, scalar: Union[int, float]) -> None:
        """
        brief scale this vector

        Args:
            scalar: scaling factor
        """
        self._x *= scalar
        self._y *= scalar

    def dist2(self, other: Vector2D) -> float:
        """
        brief get the squared distance from this to 'other'.

        Args:
            other: target point
        Return:
            squared distance to 'other'
        """
        return math.pow(self._x - other.x(), 2) + math.pow(self._y - other.y(), 2)

    def dist(self, other: Vector2D) -> float:
        """
        brief get the distance from this to 'p'.
        Args:
             other: target point
        Return:
            distance to 'p'
        """
        return math.sqrt(self.dist2(other))

    def reverse(self) -> Vector2D:
        """
        brief reverse vector components
        """
        self._x *= (-1.0)
        self._y *= (-1.0)
        return self

    def reverse_vector(self) -> Vector2D:
        """
        brief get reversed vector.
        Return:
             new vector object
        """
        new_vector = Vector2D(self._x, self._y)
        new_vector.reverse()
        return new_vector

    def set_length(self, length: Union[int, float]) -> None:
        """
        brief set vector length to 'length'.
        Args:
             length: new length to be set
        """
        mag = self.r()
        if mag > EPSILON:
            self.scale(length / mag)

    def set_length_vector(self, length: Union[int, float]) -> Vector2D:
        """
        brief get new vector that the length is set to 'length'
        @param length: new length to be set
        @return: new vector that the length is set to 'length'
        """
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(length)
        return new_vector

    def normalize(self) -> None:
        """
        brief normalize vector. length is set to 1.0.
        """
        self.set_length(1)

    def normalize_vector(self) -> Vector2D:
        """
        brief get new normalized vector that the length is set to 1.0 with the same angle as self
        Return:
             new normalized vector
        """
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(1)
        return new_vector

    def inner_product(self, v: Vector2D) -> float:
        """
        brief get inner(dot) product with 'v'.
        # ==  |this| * |v| * (*this - v).th().cos()
        Args:
             v: target vector
        Return:
             value of inner product
        """
        return self._x * v.x() + self._y * v.y()

    def outer_product(self, v: Vector2D) -> float:
        """
        brief get virtual outer(cross) product with 'v'.
        #   xn = self.y * v.z - self.z * v.y;
        #   yn = self.z * v.x - self.x * v.z;
        #   zn = self.x * v.y - self.y * v.x;
        # == |this| * |v| * (*this - v).th().sin()
        Args:
             v: target vector
        Return:
            value of outer product
        """
        return self._x * v._y - self._y * v._x

    def equals(self, other: Vector2D) -> bool:
        """
        brief check if this vector is strictly same as given vector.
        Args:
             other: compared vector
        Return:
             true if strictly same, otherwise false.
        """

        return self._x == other.x() and self._y == other.y()

    def equals_weakly(self, other: Vector2D) -> bool:
        """
        brief check if this vector is weakly same as given vector.
        Args:
             other: compared vector.
        Return:
             true if weakly same, otherwise false.
        """
        return math.fabs(self._x - other.x()) < EPSILON and math.fabs(self._y - other.y()) < EPSILON

    def rotate(self, deg: Union[int, float, AngleDeg]):
        """
        brief rotate this vector with 'deg'
        Args:
             deg: rotated angle by double type
        """
        if isinstance(deg, AngleDeg):
            self.rotate(deg.degree())
            return self
        cos_tmp = math.cos(deg * DEG2RAD)
        sin_tmp = math.sin(deg * DEG2RAD)
        self.assign(self._x * cos_tmp - self._y * sin_tmp, self._x * sin_tmp + self._y * cos_tmp)

    def rotated_vector(self, deg: Union[int, float, AngleDeg]) -> Vector2D:
        """
        brief get new vector that is rotated by 'deg'.
        Args:
             deg: rotated angle. double type.
        Return:
             new vector rotated by 'deg'
        """
        new_vector = Vector2D(self._x, self._y)
        return new_vector.rotate(deg)

    def set_dir(self, direction: Union[int, float, AngleDeg]) -> None:
        """
        brief set vector's angle to 'angle'
        Args:
             direction: new angle to be set
        Return:
             reference to itself
        """
        if not isinstance(direction, AngleDeg):
            direction = AngleDeg(direction)
        radius = self.r()
        self._x = radius * direction.cos()
        self._y = radius * direction.sin()

    """  __ operator section __"""

    def __add__(self, other) -> Vector2D:
        return Vector2D(self._x + other.x(), self._y + other.y())

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self._x - other._x, self._y - other._y)

    def __truediv__(self, other: Union[int, float]) -> Vector2D:
        return Vector2D(self._x / other, self._y / other)

    def __mul__(self, other: Union[int, float]) -> Vector2D:
        return Vector2D(self._x * other, self._y * other)

    def __iadd__(self, other: Vector2D) -> Vector2D:
        self._x += other.x()
        self._y += other.y()
        return self

    def __isub__(self, other: Vector2D) -> Vector2D:
        self._x -= other.x()
        self._y -= other.y()
        return self

    def __imul__(self, other: Union[int, float]) -> Vector2D:
        self._x *= other
        self._y *= other
        return self

    def __idiv__(self, other: Union[int, float]) -> Vector2D:
        self._x /= other
        self._y /= other
        return self

    def __repr__(self):
        return "({},{})".format(self._x, self._y)

    @staticmethod
    def invalid() -> Vector2D:
        """
        brief make an invalid vector2D
        Return:
             invalid vector2D
        """
        vec_invalid = Vector2D()
        vec_invalid.invalidate()
        return vec_invalid

    @staticmethod
    def from_polar(mag: Union[int, float], theta: Union[int, float, AngleDeg]) -> Vector2D:
        """
        brief get new Vector created by POLAR value.
        Args:
            mag: length of vector
            theta: angle of vector
        Return:
             new vector object
        """
        if not isinstance(theta, AngleDeg):
            theta = AngleDeg(theta)
        return Vector2D(mag * theta.cos(), mag * theta.sin())

    @staticmethod
    def polar2vector(r: Union[int, float], d: Union[int, float, AngleDeg]) -> Vector2D:
        """
        brief get new Vector created by POLAR value.
        Args:
            r: length of vector
            d: angle of vector
        Return:
             new vector object
        """
        return Vector2D.from_polar(r, d)

    @staticmethod
    def inner_product_static(v1: Vector2D, v2: Vector2D) -> float:
        """
        brief get inner(dot) product for v1 and v2.
        Args:
            v1: input 1
            v2: input 2
        Return: value of inner product
        """
        return v1.inner_product(v2)

    @staticmethod
    def outer_product_static(v1: Vector2D, v2: Vector2D) -> float:
        """
        brief get outer(cross) product for v1 and v2.
        Args:
            v1: input 1
            v2: input 2
        Return:
             value of outer product
        """
        return v1.outer_product(v2)
