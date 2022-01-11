"""
  file size_2d.py
  brief 2d size class  File.
"""

import math


class Size2D:
    def __init__(self, length: float = 0.0, width: float = 0.0) -> None:
        """
        brief constructor with variables
        @param length x range
        @param width y range
        Default 0.0 0.0
        """
        self._length = math.fabs(length)
        self._width = math.fabs(width)

    def assign(self, length: float, width: float) -> None:
        """
        brief assign range directly.
        @param length X range
        @param width Y range
        """
        self._length = math.fabs(length)
        self._width = math.fabs(width)

    def set_length(self, length: float) -> None:
        """
        brief set X range
        @param length X range
        """
        self._length = math.fabs(length)

    def set_width(self, width: float) -> None:
        """
        brief set Y range
        @param width Y range
        @return reference to itself
        """
        self._width = math.fabs(width)

    def length(self) -> float:
        """
        brief get the value of X range
        @return value of X range
        """
        return self._length

    def width(self) -> float:
        """
        brief get the value of Y range
        @return value of Y range
        """
        return self._width

    def diagonal(self) -> float:
        """
        brief get the length of diagonal line
        @return length of diagonal line
        """
        return math.sqrt(self._length * self._length + self._width * self._width)

    def is_valid(self) -> float:
        """
        brief check if size is valid or not.
        @return True if the area of self rectangle is not 0.
        """
        return self._length > 0.0 and self._width > 0.0

    def __repr__(self) -> str:
        """
        brief make a logical print.
        @return print_able str
        """
        return "[len:{},wid:{}]".format(self._length, self._width)
