"""
  file vector_2d.py
  brief 2d vector class
"""
from __future__ import annotations
from typing import Union
from PyrusGeom.angle_deg import AngleDeg
from PyrusGeom.math_values import *
import math


class Vector2D:  # TODO maybe give some bugs because of x and _x and x()
    """
       brief default constructor : create Vector with XY value directly.
       param __x assigned x value
       param __y assigned x value
    """
    def __init__(self, *args):
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

    """
        brief assign XY value directly.
        param x assigned x value
        param y assigned y value
        return reference to itself
    """
    def assign(self, x: float, y: float) -> Vector2D:
        self._x = x
        self._y = y
        return self

    """
     brief accessor
     return X coordinate
    """
    def x(self) -> float:
        return self._x

    """
      brief accessor
      return Y coordinate
    """
    def y(self) -> float:
        return self._y

    """
     brief accessor
     return X coordinate
    """
    def get_x(self) -> float:
        return self._x

    """
     returns copy of this Vector2D
     return X coordinate
    """
    def copy(self) -> Vector2D:
        return Vector2D(self._x, self.y)

    """
      brief accessor
      return Y coordinate
    """
    def get_y(self) -> float:
        return self._y

    """
      set x of the object to new x
    """
    def set_x(self, x: Union[int, float]) -> None:
        self._x = x

    """
      set y of the object to new y
    """
    def set_y(self, y: Union[int, float]) -> None:
        self._y = y

    """
      set y of the object to new y
    """
    def set_x_y(self, x: Union[int, float], y: Union[int, float]) -> None:
        self._x = x
        self._y = y

    """
      set y of the object to new y
    """
    def set(self, x: Union[int, float], y: Union[int, float]) -> None:
        self._x = x
        self._y = y

    """
      brief assign XY value from POLAR value.
      param __r vector's radius
      param __d vector's angle
     """
    def set_polar(self, radius: Union[int, float], angle: Union[int, float, AngleDeg]) -> None:
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        self._x = radius * angle.cos()
        self._y = radius * angle.sin()

    """
      brief validate this object     
    """
    def validate(self) -> None:
        self._is_valid = True

    """
      brief invalidate this object     
    """
    def invalidate(self) -> None:
        self._is_valid = False

    """
      brief check is the object valid
      return is_valid     
    """

    def is_valid(self) -> bool:
        return self._is_valid

    """
      brief get the squared length of vector.
      return squared length value
    """
    def r2(self) -> float:
        return self._x * self._x + self._y * self._y

    """
      brief get the length of vector.
      return length value
    """
    def r(self) -> float:
        return math.sqrt(self.r2())

    """
      brief get the length of vector. this method is equivalent to r().
      return length value 
    """
    def length(self):
        return self.r()

    """
      brief get the squared length of vector. this method is equivalent to r2().
      return squared length value
    """
    def length2(self):
        return self.r2()

    """
      brief get the angle of vector.
      return angle
    """
    def th(self) -> AngleDeg:
        return AngleDeg(AngleDeg.atan2_deg(self._y, self._x))

    """
      brief get the angle of vector. this method is equivalent to th().
      return angle
     """
    def dir(self) -> AngleDeg:
        return self.th()

    """
      brief get new vector that XY values were set to absolute value.
      return new vector that all values are absolute.
    """
    def abs(self) -> Vector2D:
        return Vector2D(abs(self._x), abs(self._y))

    """
      brief get absolute x value
      return absolute x value
    """
    def abs_x(self) -> float:
        return math.fabs(self._x)

    """
      brief get absolute y value
      return absolute y value
    """
    def abs_y(self):
        return math.fabs(self._y)

    """
      Len = 1 / Vector2D
      brief add vector.
      param other added vector
      Len = 2 / XY
      brief add XY values respectively.
      param _x added x value
      param _y added y value
    """
    def add(self, *args) -> None:
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

    """
      brief scale this vector
      param scalar scaling factor
    """
    def scale(self, scalar: Union[int, float]) -> None:
        self._x *= scalar
        self._y *= scalar

    def copy(self):
        return Vector2D(self._x, self._y)

    def get_copy(self):
        return self.copy()

    """
          brief get the squared distance from this to 'other'.
          param other target point
          return squared distance to 'other'
        """

    def dist2(self, other: Vector2D) -> float:
        return math.pow(self._x - other.x(), 2) + math.pow(self._y - other.y(), 2)

    """
      brief get the distance from this to 'p'.
      param p target point
      return distance to 'p'
    """

    def dist(self, other: Vector2D) -> float:
        return math.sqrt(self.dist2(other))

    """
      brief reverse vector components
    """

    def reverse(self) -> None:
        self._x *= (-1.0)
        self._y *= (-1.0)

    """
      brief get reversed vector.
      return new vector object
    """

    def reverse_vector(self) -> Vector2D:
        new_vector = Vector2D(self._x, self._y)
        new_vector.reverse()
        return new_vector

    """
      brief set vector length to 'length'.
      param len new length to be set
    """

    def set_length(self, length: Union[int, float]) -> None:
        mag = self.r()
        if mag > EPSILON:
            self.scale(length / mag)

    """
      brief get new vector that the length is set to 'length'
      param len new length to be set
      return new vector that the length is set to 'length'
    """

    def set_length_vector(self, length: Union[int, float]) -> Vector2D:
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(length)
        return new_vector

    """
      brief normalize vector. length is set to 1.0.
    """

    def normalize(self) -> None:
        self.set_length(1)

    """
      brief get new normalized vector that the length is set to 1.0 with the same angle as self
      return new normalized vector
    """

    def normalize_vector(self) -> Vector2D:
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(1)
        return new_vector

    """
      brief get inner(dot) product with 'v'.
      param v target vector
      return value of inner product
    """

    def inner_product(self, v: Vector2D) -> float:
        return self._x * v.x() + self._y * v.y()
        # ==  |this| * |v| * (*this - v).th().cos()

    """
      brief get virtual outer(cross) product with 'v'.
      param v target vector
      return value of outer product
    """

    def outer_product(self, v: Vector2D) -> float:
        #   xn = self.y * v.z - self.z * v.y;
        #   yn = self.z * v.x - self.x * v.z;
        #   zn = self.x * v.y - self.y * v.x;
        return self._x * v._y - self._y * v._x
        # == |this| * |v| * (*this - v).th().sin()

    """
      brief check if this vector is strictly same as given vector.
      param other compared vector
      return true if strictly same, otherwise false.
    """

    def equals(self, other: Vector2D) -> bool:
        return self._x == other.x() and self._y == other.y()

    """
      brief check if this vector is weakly same as given vector.
      param other compared vector.
      return true if weakly same, otherwise false.
    """

    def equals_weakly(self, other: Vector2D) -> bool:
        return math.fabs(self._x - other.x) < EPSILON and math.fabs(self._y - other.y) < EPSILON

    """
      brief rotate this vector with 'deg'
      param deg rotated angle by double type
    """

    def rotate(self, deg: Union[int, float, AngleDeg]):
        if isinstance(deg, AngleDeg):
            self.rotate(deg.degree())
            return self
        cos_tmp = math.cos(deg * DEG2RAD)
        sin_tmp = math.sin(deg * DEG2RAD)
        self.assign(self._x * cos_tmp - self._y * sin_tmp, self._x * sin_tmp + self._y * cos_tmp)

    """
      brief get new vector that is rotated by 'deg'.
      param deg rotated angle. double type.
      return new vector rotated by 'deg'
    """

    def rotated_vector(self, deg: Union[int, float, AngleDeg]) -> Vector2D:
        new_vector = Vector2D(self._x, self._y)
        return new_vector.rotate(deg)

    """
      brief set vector's angle to 'angle'
      param direction new angle to be set
      return reference to itself
    """

    def set_dir(self, direction: Union[int, float, AngleDeg]) -> None:
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

    """
      brief make an invalid vector2D
      return invalid vector2D   
    """
    @staticmethod
    def invalid() -> Vector2D:
        vec_invalid = Vector2D()
        vec_invalid.invalidate()
        return vec_invalid

    """
      brief get new Vector created by POLAR value.
      param mag length of vector
      param theta angle of vector
      return new vector object
    """
    @staticmethod
    def from_polar(mag: Union[int, float], theta: Union[int, float, AngleDeg]) -> Vector2D:
        if not isinstance(theta, AngleDeg):
            theta = AngleDeg(theta)
        return Vector2D(mag * theta.cos(), mag * theta.sin())

    """
      brief get new Vector created by POLAR value.
      param mag length of vector
      param theta angle of vector
      return new vector object
    """
    @staticmethod
    def polar2vector(r: Union[int, float], d: Union[int, float, AngleDeg]) -> Vector2D:
        return Vector2D.from_polar(r, d)

    """
      brief get inner(dot) product for v1 and v2.
      param v1 input 1
      param v2 input 2
      return value of inner product
    """
    @staticmethod
    def inner_product_static(v1: Vector2D, v2: Vector2D) -> float:
        return v1.inner_product(v2)

    """
      brief get outer(cross) product for v1 and v2.
      param v1 input 1
      param v2 input 2
      return value of outer product
    """
    @staticmethod
    def outer_product_static(v1: Vector2D, v2: Vector2D) -> float:
        return v1.outer_product(v2)
