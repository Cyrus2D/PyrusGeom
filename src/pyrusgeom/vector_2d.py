""" vector_2d.py
    Vector2D: class name
    Clase attributes: _x, _y, _is_valid
"""
from __future__ import annotations
from typing import Union
import math

from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.math_values import EPSILON, DEG2RAD


class Vector2D:
    """ handling vectors and points in SS2D
    Attributes:
        _x: x-coordinate
        _y: y-coordinate
        _is_valid: a boolean for validation
    """

    def __init__(self, *args, **kwargs) -> None:
        """brief default constructor : create a Vector2D with XY value directly.

        Defualt:
            create a Vector2D at (0,0)
        Or
            create a Vector2D at (X,Y)

        Args:
            Two:
                float, float:
                    x: a float for x
                    y: a float for y
            One:
                Vector2D:
                    point: a Vector2D to bulid from.
            None:
                create a Vector2D at (0,0)

        Kwargs:
            x: a float for x
            y: a float for y
            r (Union[int, float]): vector's radius
            a (Union[int, float, AngleDeg]): vector's angle

        Raises:
            Exception: The input should be a Vector2D or two numbers or no input
        """
        self._is_valid = True
        if len(kwargs.keys()) == 0:
            if len(args) == 2 and isinstance(args[0],
                                            (int, float)) and isinstance(args[1], (int, float)):
                self._x = args[0]
                self._y = args[1]
            elif len(args) == 1 and isinstance(args[0], Vector2D):
                self._x = args[0].x()
                self._y = args[0].y()
            elif len(args) == 0:
                self._x = 0
                self._y = 0
            else:
                raise Exception('The input should be a Vector2D or two numbers')
        elif len(kwargs) == 2:
            if 'x' in kwargs and 'y' in kwargs:
                self._x = kwargs['x']
                self._y = kwargs['y']
            elif 'r' in kwargs and 'a' in kwargs:
                self.set_polar(kwargs['r'], kwargs['a'])
            else:
                raise Exception('The input should be a Vector2D or two numbers')
        else:
            raise Exception('The input should be a Vector2D or two numbers')


    def x(self) -> float:
        """accessor to x

        Returns:
            float: X coordinate
        """
        return self._x

    def y(self) -> float:
        """accessor to y

        Returns:
            float: Y coordinate
        """
        return self._y

    def get_x(self) -> float:
        """accessor to x

        Returns:
            float: X coordinate
        """
        return self._x

    def get_y(self) -> float:
        """accessor to y

        Returns:
            float: Y coordinate
        """
        return self._y

    def copy(self) -> Vector2D:
        """returns copy of this Vector2D

        Returns:
           Vector2D: Copy of this Vector 2D
        """
        return Vector2D(self._x, self._y)

    def get_copy(self) -> Vector2D:
        """returns copy of this Vector2D

        Returns:
           Vector2D: Copy of this Vector 2D
        """
        return self.copy()

    def assign(self, p_x: float, p_y: float) -> Vector2D:
        """assign XY value directly.

        Args:
            p_x (float): assigned x value
            p_y (float): assigned y value

        Returns:
            Vector2D: reference to itself
        """
        self._x = p_x
        self._y = p_y
        return self

    def set_x(self, p_x: Union[int, float]) -> None:
        """set x of this object to new x.

        Args:
            p_x (Union[int, float]): assigned x value
        """
        self._x = p_x

    def set_y(self, p_y: Union[int, float]) -> None:
        """set y of this object to new y.

        Args:
            p_y (Union[int, float]): assigned y value
        """
        self._y = p_y

    def set_x_y(self, p_x: Union[int, float], p_y: Union[int, float]) -> None:
        """brief set x and y of this object to new x and y.

        Args:
            p_x (Union[int, float]): assigned x value
            p_y (Union[int, float]): assigned y value
        """
        self._x = p_x
        self._y = p_y

    def set_vector(self, other: Vector2D) -> None:
        """set x and y of this object to the x and y of the new object.

        Args:
            other (Vector2D): A vector 2D
        """
        self._x = other.x()
        self._y = other.y()
        self._is_valid = other.is_valid()

    def set_polar(self, radius: Union[int, float], angle: Union[int, float, AngleDeg]) -> None:
        """assign XY value from POLAR value.

        Args:
            radius (Union[int, float]): vector's radius
            angle (Union[int, float, AngleDeg]): vector's angle
        """
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        self._x = radius * angle.cos()
        self._y = radius * angle.sin()

    def validate(self) -> None:
        """validate this object

        _is_valid = True
        """
        self._is_valid = True

    def invalidate(self) -> None:
        """invalidate this object

        _is_valid = False
        """
        self._is_valid = False

    def is_valid(self) -> bool:
        """check this object is valid

        Returns:
            bool: True if valid. else False
        """
        return self._is_valid

    def r2(self) -> float:
        """get the squared length of vector.
        Returns:
            float: squared length value
        """
        return self._x * self._x + self._y * self._y

    def r(self) -> float:
        """get the length of vector.

        Returns:
            float: length value
        """
        return math.sqrt(self.r2())

    def length(self) -> float:
        """get the length of vector.

        this method is equivalent to r().

        Returns:
            float: length value
        """
        return self.r()

    def length2(self):
        """get the squared length of vector.

        this method is equivalent to r2().

        Returns:
            float: squared length value
        """
        return self.r2()

    def th(self) -> AngleDeg:
        """get the angle of vector.

        Returns:
            AngleDeg: the angle
        """
        return AngleDeg(AngleDeg.atan2_deg(self._y, self._x))

    def dir(self) -> AngleDeg:
        """get the angle of vector.

        this method is equivalent to th().

        Returns:
            AngleDeg: the angle
        """
        return self.th()

    def abs(self) -> Vector2D:
        """get new vector that XY values were set to absolute value.

        Returns:
            Vector2D:a new vector with absolute values.
        """
        return Vector2D(abs(self._x), abs(self._y))

    def abs_x(self) -> float:
        """get absolute x value

        Returns:
            float: absolute x value
        """
        return math.fabs(self._x)

    def abs_y(self):
        """get absolute y value

        Returns:
            float: absolute y value
        """
        return math.fabs(self._y)

    def add(self, *args) -> None:
        """adds given x and y to this Vector2D

        Args:
            Two:
                float, float:
                    x: a float for x
                    y: a float for y
            One:
                Vector2D:
                    point: a Vector2D to add from.

        Raises:
            Exception: The input should be a Vector2D or two numbers
        """
        if len(args) == 1 and isinstance(args[0], Vector2D):
            self._x += args[0].x()
            self._y += args[0].y()
        elif len(args) == 2:
            self._x += args[0]
            self._y += args[1]
        else:
            raise Exception("The input should be a Vector2D or two numbers")

    def add_x(self, p_x: Union[int, float]) -> None:
        """adds p_x to this Vector's X

        Args:
            p_x (Union[int, float]): a float for x
        """
        self._x += p_x

    def add_y(self, p_y: Union[int, float]) -> None:
        """adds p_y to this Vector's Y

        Args:
            p_y (Union[int, float]): a float for y
        """
        self._y += p_y

    def sub(self, *args) -> None:
        """subtracts x and y from this vector 2d

        Args:
            Two:
                float, float:
                    x: a float for x
                    y: a float for y
            One:
                Vector2D:
                    point: a Vector2D to add from.

        Raises:
            Exception: The input should be a Vector2D or two numbers
        """
        if len(args) == 1:
            self._x -= args[0].x()
            self._y -= args[0].y()
        elif len(args) == 2:
            self._x -= args[0]
            self._y -= args[1]
        else:
            raise Exception("The input should be a Vector2D or two numbers")

    def sub_x(self, p_x: Union[int, float]) -> None:
        """subtracts p_x from this Vector's X

        Args:
            p_x (Union[int, float]): a float for x
        """
        self._x -= p_x

    def sub_y(self, p_y: Union[int, float]) -> None:
        """subtracts p_y from this Vector's Y

        Args:
            p_y (Union[int, float]): a float for y
        """
        self._y -= p_y

    def scale(self, scalar: Union[int, float]) -> None:
        """scale this vector

        Args:
            scalar (Union[int, float]): scaling factor
        """
        self._x *= scalar
        self._y *= scalar

    def dist2(self, other: Vector2D) -> float:
        """get the squared distance from this to 'other'.

        Args:
            other (Vector2D): target point

        Returns:
            float: squared distance to 'other'
        """
        return math.pow(self._x - other.x(), 2) + math.pow(self._y - other.y(), 2)

    def dist(self, other: Vector2D) -> float:
        """get the distance from this Vector2D to the 'other' Vector2D.

        Args:
            other (Vector2D): target point

        Returns:
            float: distance to 'other'
        """
        return math.sqrt(self.dist2(other))

    def reverse(self) -> Vector2D:
        """reverse this vector components

        Returns:
            Vector2D: self
        """
        self._x *= (-1.0)
        self._y *= (-1.0)
        return self

    def reverse_vector(self) -> Vector2D:
        """get reversed vector.

        Returns:
            Vector2D: new reversed vector object
        """
        return Vector2D(self._x, self._y).reverse()

    def set_length(self, length: Union[int, float]) -> None:
        """set vector length to 'length'

        Args:
            length (Union[int, float]): new length to set
        """
        mag = self.r()
        if mag > EPSILON:
            self.scale(length / mag)

    def set_length_vector(self, length: Union[int, float]) -> Vector2D:
        """create a new vector from this vertor with the length is set to 'length'

        Args:
            length (Union[int, float]): new length

        Returns:
            Vector2D: new vector that the length is set to 'length'
        """
        new_vector = Vector2D(self._x, self._y)
        new_vector.set_length(length)
        return new_vector

    def normalize(self) -> None:
        """normalize vector.

        length is set to 1.0.
        """
        self.set_length(1)

    def normalize_vector(self) -> Vector2D:
        """get new normalized vector that the length is set to 1.0 with the same angle as this
        Returns:
            Vector2D: new normalized vector
        """
        vector = Vector2D(self._x, self._y)
        vector.set_length(1)
        return vector

    def inner_product(self, point: Vector2D) -> float:
        """get inner(dot) product with 'point'.

        |this| * |point| * (this - point).th().cos()

        Args:
            point (Vector2D): target vector

        Returns:
            float: value of inner product
        """
        return self._x * point.x() + self._y * point.y()

    def outer_product(self, point: Vector2D) -> float:
        """get virtual outer(cross) product with 'point'.

        xn = self.y * point.z - self.z * point.y;
        yn = self.z * point.x - self.x * point.z;
        zn = self.x * point.y - self.y * point.x;

        |this| * |point| * (this - point).th().sin()

        Args:
            point (Vector2D): target vector

        Returns:
            float: value of outer product
        """
        return self._x * point.y() - self._y * point.x()

    def equals(self, other: Vector2D) -> bool:
        """check if this vector is strictly same as given vector.

        Args:
            other (Vector2D): compared vector

        Returns:
            bool: true if strictly same, otherwise false.
        """
        return self._x == other.x() and self._y == other.y()

    def equals_weakly(self, other: Vector2D) -> bool:
        """check if this vector is weakly same as given vector.

        Args:
            other (Vector2D): compared vector.

        Returns:
            bool: true if weakly same, otherwise false.
        """
        return math.fabs(self._x - other.x()) < EPSILON and math.fabs(self._y - other.y()) < EPSILON

    def rotate(self, deg: Union[int, float, AngleDeg]) -> Vector2D:
        """rotate this vector with 'deg'

        Args:
            deg (Union[int, float, AngleDeg]): rotated angle.

        Returns:
            Vector2D: rotated vector
        """
        if isinstance(deg, AngleDeg):
            deg = deg.degree()
        cos_tmp = math.cos(deg * DEG2RAD)
        sin_tmp = math.sin(deg * DEG2RAD)
        return self.assign(self._x * cos_tmp - self._y * sin_tmp,
                           self._x * sin_tmp + self._y * cos_tmp)

    def rotated_vector(self, deg: Union[int, float, AngleDeg]) -> Vector2D:
        """get new vector that is rotated by 'deg'.

        Args:
            deg (Union[int, float, AngleDeg]): rotated angle.

        Returns:
            Vector2D: new rotated vector by 'deg'
        """
        return Vector2D(self._x, self._y).rotate(deg)

    def set_dir(self, direction: Union[int, float, AngleDeg]) -> None:
        """set vector's angle to 'angle'

        Args:
            direction (Union[int, float, AngleDeg]): new angle to be set
        """
        if not isinstance(direction, AngleDeg):
            direction = AngleDeg(direction)
        radius = self.r()
        self._x = radius * direction.cos()
        self._y = radius * direction.sin()

    #  __ operator section __

    __hash__ = None

    def __eq__(self, other: Vector2D) -> bool:
        return isinstance(other, Vector2D) and self._x == other.x() and self._y == other.y()

    def __add__(self, other: Vector2D) -> Vector2D:
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
        return f"({self._x},{self._y})"

    @staticmethod
    def invalid() -> Vector2D:
        """make an invalid vector2D

        Returns:
            Vector2D: invalid vector
        """
        vec_invalid = Vector2D()
        vec_invalid.invalidate()
        return vec_invalid

    @staticmethod
    def from_polar(mag: Union[int, float], theta: Union[int, float, AngleDeg]) -> Vector2D:
        """get new Vector created by POLAR value.

        Args:
            mag (Union[int, float]): length of vector
            theta (Union[int, float, AngleDeg]): angle of vector

        Returns:
            Vector2D: new vector object
        """
        if not isinstance(theta, AngleDeg):
            theta = AngleDeg(theta)
        return Vector2D(mag * theta.cos(), mag * theta.sin())

    @staticmethod
    def polar2vector(radius: Union[int, float], direction: Union[int, float, AngleDeg]) -> Vector2D:
        """get new Vector created by POLAR value.

        Args:
            radius (Union[int, float]): length of vector
            direction (Union[int, float, AngleDeg]): angle of vector

        Returns:
            Vector2D: new vector object
        """
        return Vector2D.from_polar(radius, direction)

    @staticmethod
    def inner_product_static(vec_1: Vector2D, vec_2: Vector2D) -> float:
        """get inner(dot) product for vec_1 and vec_2.

        Args:
            vec_1 (Vector2D): 1st vector
            vec_2 (Vector2D): 2nd vector

        Returns:
            float: value of inner product
        """
        return vec_1.inner_product(vec_2)

    @staticmethod
    def outer_product_static(vec_1: Vector2D, vec_2: Vector2D) -> float:
        """get outer(cross) product for vec_1 and vec_2.

        Args:
            vec_1 (Vector2D): 1st vector
            vec_2 (Vector2D): 2nd vector

        Returns:
            float: value of outer product
        """
        return vec_1.outer_product(vec_2)
