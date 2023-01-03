""" rect_2d.py file
    Rect2D: class name
    Class attributes: _top_left, _size, _is_valid
    TODO: add test for RECT2D
    TODO: add eq hash neq
    The model and naming rules are depend on soccer simulator environment
              -34.0
                |
                |
    -52.5 ------+------- 52.5
                |
                |
               34.0
"""
from __future__ import annotations
from typing import Union
import math

from pyrusgeom.size_2d import Size2D
from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.region_2d import Region2D
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.line_2d import Line2D
from pyrusgeom.math_values import EPSILON


class Rect2D(Region2D):
    """ handling rectangles in SS2D
    Attributes:
        _top_left: a Vector2D for top left corner point
        _size: a Size2D for size value
        _is_valid: a boolean for validation
    """

    def __init__(self, *args) -> None:
        """This is the class init function for Rect2D.

        Defualt:
            bulid a Rect2D with args
            Even if argument point has incorrect values,
            the assigned values are normalized automatically.

        Raises:
            Exception: The input must be (4 float) or
            (vector2d and 2 float) or (vector2d and size2d) or (2 vector2d) or (1 rect2d)

        Args:
            four:
                four float:
                    float: left x
                    float: top y
                    float: length (x-range)
                    float: width (y-range)
            three:
                Vector and two float:
                    Vector2D: top left point
                    float: length X range
                    float: width Y range
            two:
                Vector, Size:
                    Vector2D: top left point
                    Size2D: size XY range
                two Vectors:
                    Vector2D: top left vertex
                    Vector2D: bottom right vertex
            one:
                Rect2D: just another rectangle
        """
        super().__init__()
        self._top_left: Vector2D = Vector2D()
        self._size: Size2D = Size2D()
        self._is_valid = True
        if len(args) == 4:
            self._top_left = Vector2D(args[0], args[1])
            self._size = Size2D(args[2], args[3])
            self._is_valid = True
        elif len(args) == 3:
            self._top_left = Vector2D(args[0])
            self._size = Size2D(args[1], args[2])
            self._is_valid = True
        elif len(args) == 2 and isinstance(args[1], Vector2D):
            self._top_left = Vector2D(args[0])
            bottom_right = Vector2D(args[1])
            top_left = Vector2D(args[0])
            self._size = Size2D(bottom_right.x() - top_left.x(),
                                bottom_right.y() - top_left.y())
            if bottom_right.x() - top_left.x() < 0.0:
                self._top_left.set_x(bottom_right.x())

            if bottom_right.y() - top_left.y() < 0.0:
                self._top_left.set_y(bottom_right.y())
                self._size = Size2D()
                self._is_valid = True
            else:
                self._top_left = Vector2D()
                self._size = Size2D()
                self._is_valid = True
        elif len(args) == 2:
            self._top_left = Vector2D(args[0])
            self._size = args[1]
            self._is_valid = True
        elif len(args) == 1 and isinstance(args[0], Rect2D):
            self._top_left = args[0].top_left()
            self._size = args[0].size()
            self._is_valid = args[0].is_valid()
        else:
            raise Exception("The input must be (4 float) or \
            (vector2d and 2 float) or (vector2d and size2d) or (2 vector2d) or (1 rect2d)")

    def assign(self, *args) -> Rect2D:
        """assign values directly

        Raises:
            Exception: The input must be (4 float) or
            (vector2d and 2 float) or (vector2d and size2d) or (2 vector2d) or (1 rect2d)

        Args:
            four:
                four float:
                    float: left x
                    float: top y
                    float: length (x-range)
                    float: width (y-range)
            three:
                Vector and two float:
                    Vector2D: top left point
                    float: length X range
                    float: width Y range
            two:
                Vector, Size:
                    Vector2D: top left point
                    Size2D: size XY range
                two Vectors:
                    Vector2D: top left vertex
                    Vector2D: bottom right vertex
            one:
                Rect2D: just another rectangle

        Returns:
            Rect2D: return self
        """

        if len(args) == 4:
            self._top_left.assign(args[0], args[1])
            self._size.assign(args[0], args[3])
        elif len(args) == 3:
            self._top_left = Vector2D(args[0])
            self._size.assign(args[1], args[2])
        elif len(args) == 2 and isinstance(args[1], Vector2D):
            self._top_left = Vector2D(args[0])
            bottom_right = Vector2D(args[1])
            top_left = Vector2D(args[0])
            self._size = Size2D(bottom_right.x() - top_left.x(),
                                bottom_right.y() - top_left.y())
            if bottom_right.x() - top_left.x() < 0.0:
                self._top_left.set_x(bottom_right.x())

            if bottom_right.y() - top_left.y() < 0.0:
                self._top_left.set_y(bottom_right.y())
                self._size = Size2D()
            else:
                self._top_left = Vector2D()
                self._size = Size2D()
        elif len(args) == 2:
            self._top_left = Vector2D(args[0])
            self._size = args[1]
        elif len(args) == 1 and isinstance(args[0], Rect2D):
            self._top_left = args[0].top_left()
            self._size = args[0].size()
        else:
            raise Exception("The input must be (4 float) or \
            (vector2d and 2 float) or (vector2d and size2d) or (2 vector2d)")
        return self

    def move_center(self, point: Vector2D) -> None:
        """move the center of rectangle to move whole rect.

        the center point is set to the given position.
        the size is unchanged.

        Args:
            point (Vector2D): center coordinates
        """
        self._top_left.assign(point.x() - self._size.length()
                              * 0.5, point.y() - self._size.width() * 0.5)

    def move_top_left(self, point: Vector2D) -> None:
        """move the top-left of rectangle to move whole rect.

        the top-left corner is set to the given position.
        the size is unchanged.

        Args:
            point (Vector2D): top-left corner
        """
        self._top_left = Vector2D(point)

    def move_bottom_right(self, point: Vector2D) -> None:
        """move the bottom-right of rectangle to move whole rect.

        the bottom-right corner is set to the given position.
        the size is unchanged.

        Args:
            point (Vector2D): bottom-right corner
        """
        self._top_left.assign(point.x() - self._size.length(),
                              point.y() - self._size.width())

    def move_left(self, left_x: float) -> None:
        """move the rectangle by moving left side

        the left line is set to the given position.
        the size is unchanged.

        Args:
            left_x (float): left side value
        """
        self._top_left.set_x(left_x)

    def move_min_x(self, left_x: float) -> None:
        """alias of moveLeft

        move the rectangle by moving left side.
        the left line is set to the given position.
        the size is unchanged.

        Args:
            left_x (float): left value
        """
        self.move_left(left_x)

    def move_right(self, right_x: float) -> None:
        """move the rectangle by moving left side(right given)

        the left line is set to the alterd position.
        the size is unchanged.

        Args:
            right_x (float): right value
        """
        self._top_left.set_x(right_x - self._size.length())

    def move_max_x(self, right_x: float) -> None:
        """alias of moveRight.

        move the rectangle by moving left side(right given).
        the left line is set to the alterd position.
        the size is unchanged.

        Args:
            right_x (float): right value
        """
        self.move_right(right_x)

    def move_top(self, top_y: float) -> None:
        """move the rectangle by moving top side

        the top line is set to the given value.
        the size is unchanged.

        Args:
            top_y (float): top value
        """
        self._top_left.set_y(top_y)

    def move_min_y(self, top_y: float) -> None:
        """alias of moveTop.

        move the rectangle by moving top side
        the top line is set to the given value.
        the size is unchanged.

        Args:
            top_y (float): top value
        """
        self.move_top(top_y)

    def move_bottom(self, bottom_y: float) -> None:
        """move the rectangle by moving top side(bottom given)

        the top line is set to the alterd value.
        the size is unchanged.

        Args:
            bottom_y (float): bottom value
        """
        self._top_left.set_y(bottom_y - self._size.width())

    def move_max_y(self, bottom_y: float) -> None:
        """alias of move_bottom.

        move the rectangle by moving top side(bottom given)
        the top line is set to the alterd value.
        the size is unchanged.

        Args:
            bottom_y (float): bottom value
        """
        self.move_bottom(bottom_y)

    def set_top_left(self, *args) -> Rect2D:
        """set the top-left corner of the rectangle.

        the size may be changed, the bottom-right corner will never be changed.

        Args:
            two:
                2 float:
                    float: x coordinate
                    float: y coordinate
            one:
                1 Vector:
                Vector2D: point coordinate
        Returns:
            Rect2D: this rect
        """
        point_x = 0.0
        point_y = 0.0
        if len(args) == 1:
            point_x = args[0].x()
            point_y = args[0].y()
        elif len(args) == 2:
            point_x = args[0]
            point_y = args[1]
        new_left = min(self.right(), point_x)
        new_right = max(self.right(), point_x)
        new_top = min(self.bottom(), point_y)
        new_bottom = max(self.bottom(), point_y)
        return self.assign(new_left, new_top, new_right - new_left, new_bottom - new_top)

    def set_bottom_right(self, *args) -> Rect2D:
        """set the bottom-right corner of the rectangle.

        the size may be changed, the top-left corner will never be changed.

        Args:
            two:
                2 float:
                    float: x coordinate
                    float: y coordinate
            one:
                1 Vector:
                Vector2D: point coordinate
        Returns:
            Rect2D: this rect
        """
        point_x = 0.0
        point_y = 0.0
        if len(args) == 1:
            point_x = args[0].x()
            point_y = args[0].y()
        elif len(args) == 2:
            point_x = args[0]
            point_y = args[1]
        new_left = min(self.left(), point_x)
        new_right = max(self.left(), point_x)
        new_top = min(self.top(), point_y)
        new_bottom = max(self.top(), point_y)
        return self.assign(new_left, new_top, new_right - new_left, new_bottom - new_top)

    def set_left(self, left_x: float) -> None:
        """set the left side of rectangle.

        the size may be changed, the right side will never be changed.

        Args:
            left_x (float): left value
        """
        new_left = min(self.right(), left_x)
        new_right = max(self.right(), left_x)
        self._top_left.set_x(new_left)
        self._size.set_length(new_right - new_left)

    def set_min_x(self, left_x: float) -> None:
        """alias of setLeft.

        set the left side of rectangle.
        the size may be changed, the right side will never be changed.

        Args:
            left_x (float): left value
        """
        self.set_left(left_x)

    def set_right(self, right_x: float) -> None:
        """set the right side of rectangle.

        the size may be changed, the left side will never be changed.

        Args:
            right_x (float): right value
        """
        new_left = min(self.left(), right_x)
        new_right = max(self.left(), right_x)

        self._top_left.set_x(new_left)
        self._size.set_length(new_right - new_left)

    def set_max_x(self, right_x: float) -> None:
        """ alias of setRight.

        set the right side of rectangle.
        the size may be changed, the left side will never be changed.

        Args:
            right_x (float): right value
        """
        self.set_right(right_x)

    def set_top(self, top_y: float) -> None:
        """set the top side of rectangle.

        the size may be changed, the bottom side will never be changed.

        Args:
            top_y (float): top value
        """
        new_top = min(self.bottom(), top_y)
        new_bottom = max(self.bottom(), top_y)

        self._top_left.set_y(new_top)
        self._size.set_width(new_bottom - new_top)

    def set_min_y(self, top_y: float) -> None:
        """alias of setTop.

        set the top side of rectangle.
        the size may be changed, the bottom side will never be changed.

        Args:
            top_y (float): top value
        """
        self.set_top(top_y)

    def set_bottom(self, bottom_y: float) -> None:
        """set the bottom side of rectangle.

        the size may be changed, the top side will never be changed.

        Args:
            bottom_y (float): bottom value
        """
        new_top = min(self.top(), bottom_y)
        new_bottom = max(self.top(), bottom_y)

        self._top_left.set_y(new_top)
        self._size.set_width(new_bottom - new_top)

    def set_max_y(self, bottom_y: float) -> None:
        """alias of setBottom.

        set the bottom side of rectangle.
        the size may be changed, the top side will never be changed.

        Args:
            bottom_y (float): bottom value
        """
        self.set_bottom(bottom_y)

    def set_length(self, length: float) -> None:
        """set a x-range - size x

        Args:
            length (float): length range
        """
        self._size.set_length(length)

    def set_width(self, width: float) -> None:
        """set a y-range - size y

        Args:
            length (float): width range
        """
        self._size.set_width(width)

    def set_size(self, *args) -> None:
        """set size of rect

        Raises:
            Exception: input must be two float or one size

        Args:
            two:
                2 float:
                    float: length range
                    float: width range
            one:
                1 size:
                    Size2D: size range
        """
        if len(args) == 2:
            self._size.assign(args[0], args[1])
        elif len(args) == 1 and isinstance(args[0],Size2D):
            self._size = Size2D(args[0].length(),args[0].width())
        else:
            raise Exception("input must be two float or one size")

    def is_valid(self) -> bool:
        """check if self rectangle is valid or not.

        Returns:
            bool: True if the area of self rectangle is not 0. else False
        """
        self._is_valid = self._size.is_valid()
        return self._is_valid

    def area(self) -> float:
        """get the area value of self rectangle.

        Returns:
            float: value of the area
        """
        return self._size.length() * self._size.width()

    def contains(self, point: Vector2D) -> bool:
        """check if point is within self region.

        Args:
            point (Vector2D): considered point

        Returns:
            bool: True if it contains it. else False.
        """
        return self.left() <= point.x() <= self.right() and self.top() <= point.y() <= self.bottom()

    def contains_almost(self, point, error_thr) -> bool:
        """check if point is within self region with error threshold.

        Args:
            point ([type]): considered point
            error_thr ([type]): error threshold

        Returns:
            bool: True if it almost contains it. else False.
        """
        return self.left() - error_thr <= point.x <= self.right() + error_thr and \
            self.top() - error_thr <= point.y <= self.bottom() + error_thr

    def left(self) -> float:
        """get the left x coordinate of this rectangle.

        Returns:
            float: x coordinate value
        """
        return self._top_left.x()

    def right(self) -> float:
        """get the right x coordinate of this rectangle.

        Returns:
            float: x coordinate value
        """
        return self.left() + self._size.length()

    def top(self) -> float:
        """get the top y coordinate of this rectangle.

        Returns:
            float: y coordinate value
        """
        return self._top_left.y()

    def bottom(self) -> float:
        """get the bottom y coordinate of this rectangle.

        Returns:
            float: y coordinate value
        """
        return self.top() + self._size.width()

    def min_x(self) -> float:
        """get minimum value of x coordinate of this rectangle

        Returns:
            float: x coordinate value (equivalent to left())
        """
        return self.left()

    def max_x(self) -> float:
        """get maximum value of x coordinate of this rectangle

        Returns:
            float: x coordinate value (equivalent to right())
        """
        return self.right()

    def min_y(self) -> float:
        """get minimum value of y coordinate of this rectangle

        Returns:
            float: y coordinate value (equivalent to top())
        """
        return self.top()

    def max_y(self) -> float:
        """get maximum value of y coordinate of this rectangle

        Returns:
            float: y coordinate value (equivalent to bottom())
        """
        return self.bottom()

    def size(self) -> Size2D:
        """get the XY copy range of self rectangle

        Returns:
            Size2D: new size object
        """
        return Size2D(self._size.length(),self._size.width())

    def size_(self) -> Size2D:
        """get the OG XY range of self rectangle

        Returns:
            Size2D: original size object
        """
        return self._size

    def center(self) -> Vector2D:
        """get center point of this rectangle

        Returns:
            Vector2D: coordinate value by vector object
        """
        return Vector2D((self.left() + self.right()) * 0.5,
                        (self.top() + self.bottom()) * 0.5)

    def top_left(self) -> Vector2D:
        """get the top-left corner copy vector point

        Returns:
            Vector2D: coordinate value by vector object copy
        """
        return Vector2D(self._top_left)

    def top_left_(self) -> Vector2D:
        """get the og top-left corner vector point

        Returns:
            Vector2D: coordinate value by og vector object
        """
        return self._top_left

    def top_right(self) -> Vector2D:
        """get the top-right corner point

        Returns:
            Vector2D: coordinate value by vector object
        """
        return Vector2D(self.right(), self.top())

    def bottom_left(self) -> Vector2D:
        """get the bottom-left corner point

        Returns:
            Vector2D: coordinate value by vector object
        """
        return Vector2D(self.left(), self.bottom())

    def bottom_right(self) -> Vector2D:
        """get the bottom-right corner point

        Returns:
            Vector2D: coordinate value by vector object
        """
        return Vector2D(self.right(), self.bottom())

    def left_edge(self) -> Line2D:
        """get the left edge line

        Returns:
            Line2D: line object
        """
        return Line2D(self.top_left(), self.bottom_left())

    def right_edge(self) -> Line2D:
        """get the right edge line

        Returns:
            Line2D: line object
        """
        return Line2D(self.top_right(), self.bottom_right())

    def top_edge(self) -> Line2D:
        """get the top edge line

        Returns:
            Line2D: line object
        """
        return Line2D(self.top_left(), self.top_right())

    def bottom_edge(self) -> Line2D:
        """get the bottom edge line

        Returns:
            Line2D: line object
        """
        return Line2D(self.bottom_left(), self.bottom_right())

    def intersection(self, other:Union[Line2D,Ray2D,Segment2D]) -> list[Vector2D]:
        """calculate intersection point with line.
        Raises:
            Exception: Input must be Line/Ray/Segment
        Args:
            other (Union[Line2D,Ray2D,Segment2D]):
                Line2D:  considered line.
                Ray2D: considered ray line.
                Segment2D: considered line segment.

        TODO: check this full

        Returns:
            list[Vector2D]: intersection Points
        """
        if isinstance(other, Line2D):
            n_sol = 0
            t_sol = [Vector2D(0, 0), Vector2D(0, 0)]
            left_x = self.left()
            right_x = self.right()
            top_y = self.top()
            bottom_y = self.bottom()
            t_sol[n_sol] = self.left_edge().intersection(other)
            if n_sol < 2 and t_sol[n_sol].is_valid() and top_y <= t_sol[n_sol].y() <= bottom_y:
                n_sol += 1
            t_sol[n_sol] = self.right_edge().intersection(other)
            if n_sol < 2 and t_sol[n_sol].is_valid() and top_y <= t_sol[n_sol].y() <= bottom_y:
                n_sol += 1
            t_sol[n_sol] = self.top_edge().intersection(other)
            if n_sol < 2 and (t_sol[n_sol]).is_valid() and left_x <= t_sol[n_sol].x() <= right_x:
                n_sol += 1
            t_sol[n_sol] = self.top_edge().intersection(other)
            if n_sol < 2 and (t_sol[n_sol]).is_valid() and left_x <= t_sol[n_sol].x() <= right_x:
                n_sol += 1
            if n_sol == 2 and math.fabs(t_sol[0].x() - t_sol[1].x()) < EPSILON and math.fabs(
                    t_sol[0].y() - t_sol[1].y()) < EPSILON:
                n_sol = 1
            if n_sol == 0:
                sol_list = []
            elif n_sol == 1:
                sol_list = [t_sol[0]]
            else:
                sol_list = [t_sol[0], t_sol[1]]
            return sol_list
        if isinstance(other, Ray2D):
            n_sol = self.intersection(other.line())

            if len(n_sol) > 1 and not other.in_right_dir(n_sol[2], 1.0):
                del n_sol[1]

            if len(n_sol) > 0 and not other.in_right_dir(n_sol[1], 1.0):
                n_sol[0] = n_sol[1]
                del n_sol[1]
            return n_sol
        if isinstance(other, Segment2D):
            n_sol = self.intersection(other.line())
            if len(n_sol) > 1 and not other.contains(n_sol[2]):
                del n_sol[1]

            if len(n_sol) > 0 and not other.contains(n_sol[1]):
                n_sol[0] = n_sol[1]
                del n_sol[1]
            return n_sol
        raise Exception("Input must be Line/Ray/Segment")

    def intersected(self, other:Rect2D) -> Rect2D:
        """get the intersected rectangle of self rectangle and the other rectangle.

        If no intersection between rectangles,empty rectangle is returned.

        Args:
            other (Rect2D): other rectangle

        Returns:
            [Rect2D]: rectangle instance
        """
        if not self.is_valid or not other.is_valid():
            self._top_left.assign(0.0, 0.0)
            self._size.assign(0.0, 0.0)

        left = max(self.left(), other.left())
        top = max(self.top(), other.top())
        width = min(self.right(), other.right()) - left
        length = min(self.bottom(), other.bottom()) - top

        if width <= 0.0 or length <= 0.0:
            self._top_left.assign(0.0, 0.0)
            self._size.assign(0.0, 0.0)

        self._top_left.assign(left, top)
        self._size.assign(width, length)

        return self

    def united(self, other:Rect2D) -> Rect2D:
        """get the united rectangle of self rectangle and the other rectangle.

        Args:
            other (Rect2D): other rectangle

        Returns:
            Rect2D: rectangle instance.
        """
        if not self.is_valid or not other.is_valid():
            self._top_left.assign(0.0, 0.0)
        self._size.assign(0.0, 0.0)

        left = max(self.left(), other.left())
        top = max(self.top(), other.top())
        width = min(self.right(), other.right()) - left
        length = min(self.bottom(), other.bottom()) - top

        if width <= 0.0 or length <= 0.0:
            self._top_left.assign(0.0, 0.0)
            self._size.assign(0.0, 0.0)

        self._top_left.assign(left, top)
        self._size.assign(width, length)

        return self

    @staticmethod
    def from_center(*args)->Rect2D:
        """create rectangle with center point and size.

        Raises:
            Exception: Input must be 4 float or one vector and two float

        Args:
            four:
                4 float:
                    float: x value of center point of rectangle.
                    float: y value of center point of rectangle.
                    float: length(x-range) of rectangle.
                    float: width(y-range) of rectangle.
            three:
                1 vector and 2 float:
                    Vector2D: center point of rectangle.
                    float: length(x-range) of rectangle.
                    float: width(y-range) of rectangle.

        Returns:
            Rect2D: created rectangle
        """
        if len(args) == 4:
            return Rect2D(args[0] - args[2] * 0.5, args[1] - args[3] * 0.5, args[2], args[3])
        if len(args) == 3:
            return Rect2D(args[0] - args[1] * 0.5, args[0] - args[2] * 0.5, args[1], args[2])
        raise Exception("Input must be 4 float or one vector and two float")

    def __repr__(self) -> str:
        """represent Rect2D as a string

        Returns:
            str: Rect2D's top_left corner and length and width as string
        """
        return f"[topleft:{self._top_left},len:{self._size.length()},wid:{self._size.width()}]"

    def to_str(self, ostr) -> str:
        """add rectangle to the ostr

        Args:
            ostr (str): str to add to it
        """
        ostr += f'(rect {round(self.left(), 3)} {round(self.top(), 3)} \
            f{round(self.right(), 3)} {round(self.bottom(), 3)})'
