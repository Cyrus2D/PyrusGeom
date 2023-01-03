""" size_2d.py file
    Size2D: Clase name
    Class attributes: _length, _width

"""
from __future__ import annotations
import math

from pyrusgeom.math_values import EPSILON

class Size2D:
    """ handling size of rectangle in SS2D
    Attributes:
        _length: a non-negative float for X range
        _width: a non-negative float for Y range
    """
    def __init__(self, length: float = 0.0, width: float = 0.0) -> None:
        """This is the class init function for Size2D.

        Defualt:
            create a zero area with length = 0.0 and width = 0.0
        OR:
            bulid a Size2D
        Args:
            length (float, optional): X range. Defaults to 0.0.
            width (float, optional): Y range. Defaults to 0.0.
        """
        self._length = math.fabs(length)
        self._width = math.fabs(width)

    def assign(self, length: float, width: float) -> None:
        """assign range directly.

        Args:
            length (float): X range
            width (float): Y range
        """
        self._length = math.fabs(length)
        self._width = math.fabs(width)

    def set_length(self, length: float) -> None:
        """set X range

        Args:
            length (float): X range
        """
        self._length = math.fabs(length)

    def set_width(self, width: float) -> None:
        """set Y range

        Args:
            width (float): Y range
        """
        self._width = math.fabs(width)

    def length(self) -> float:
        """get the value of X range

        Returns:
            float: value of X range
        """
        return self._length

    def width(self) -> float:
        """get the value of Y range

        Returns:
            float: value of Y range
        """
        return self._width

    def diagonal(self) -> float:
        """get the length of diagonal line

        Returns:
            float: length of diagonal line
        """
        return math.sqrt(self._length * self._length + self._width * self._width)

    def is_valid(self) -> float:
        """check if size is valid or not.

        Returns:
            float: True if the area of self rectangle is not 0. else False.
        """
        return self._length > 0.0 and self._width > 0.0

    def __eq__(self, other: Size2D) -> bool:
        """operator == for Size2D

        Args:
            other (Size2D): right hand side argument

        Returns:
            bool: true if equal or difference is less than EPSILON. else false
        """
        return math.fabs(self._length - other.length()) < EPSILON and (
            math.fabs(self._width - other.width()) < EPSILON)

    def __repr__(self) -> str:
        """represent Size2D as a string

        Returns:
            str: Size2D's _length and _width as string
        """
        return f"[len:{self._length},wid:{self._width}]"
