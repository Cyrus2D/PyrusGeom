"""
  file rect_2d.py
  brief 2D rectangle region File.
"""
from __future__ import annotations

from PyrusGeom.size_2d import Size2D
from PyrusGeom.segment_2d import Segment2D
from PyrusGeom.region_2d import Region2D
from PyrusGeom.ray_2d import Ray2D
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
from PyrusGeom.line_2d import Line2D
from PyrusGeom.math_values import *
import math

"""
    The model and naming rules are depend on soccer simulator environment
          -34.0
            |
            |
-52.5 ------+------- 52.5
            |
            |
          34.0
"""


class Rect2D(Region2D):
    def __init__(self, *args) -> None:
        """
        4 num
        brief constructor
        param left_x left x
        param top_y top y
        param length length (x-range)
        param width width (y-range)
        Vector / 2 num
        brief constructor with variables
        param top_left top left point
        param length X range
        param width Y range
        Vector / Size
        brief constructor with variables
        param top_left top left point
        param size XY range
        2 Vector
        brief constructor with 2 points.
        param top_left top left vertex
        param bottom_right bottom right vertex

        Even if argument point has incorrect values,
        the assigned values are normalized automatically.
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
        elif len(args) == 2 and type(args[1]) == Vector2D:
            self._top_left = Vector2D(args[0])
            bottom_right: Vector2D = args[1]
            top_left: Vector2D = args[0]
            self._size = Size2D(bottom_right.x() - top_left.x(), bottom_right.y() - top_left.y())
            if bottom_right.x() - top_left.x() < 0.0:
                self._top_left._x = bottom_right.x()

            if bottom_right.y() - top_left.y() < 0.0:
                self._top_left._y = bottom_right.y()
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

    def assign(self, *args) -> Rect2D:
        """
        4 NUM
        brief assign values
        param left_x left x
        param top_y top y
        param length X range
        param width Y range
        Vector / 2 NUM
        brief assign values
        param top_left top left point
        param length X range
        param width Y range
        Vector / Size
        brief assign values
        param top_left top left
        param size XY range
        """
        super().__init__()
        if len(args) == 4:
            self._top_left.assign(args[0], args[1])
            self._size.assign(args[0], args[3])
        elif len(args) == 3:
            self._top_left = Vector2D(args[0])
            self._size.assign(args[1], args[2])
        elif len(args) == 2:
            self._top_left = Vector2D(args[0])
            self._size = args[1]
        return self

    def move_center(self, point: Vector2D) -> None:
        """
        brief move the rectangle.
        the center point is set to the given position.
        the size is unchanged.
        param point center coordinates
        """
        self._top_left.assign(point.x() - self._size.length() * 0.5, point.y() - self._size.width() * 0.5)

    def move_top_left(self, point: Vector2D) -> None:
        """
        brief move the rectangle.
        the top-left corner is set to the given position.
        the size is unchanged.
        param point top-left corner
        """
        self._top_left = Vector2D(point)

    def move_bottom_right(self, point: Vector2D) -> None:
        """
        brief move the rectangle.
        the bottom-right corner is set to the given position.
        the size is unchanged.
        param point bottom-right corner
        """
        self._top_left.assign(point.x() - self._size.length(), point.y() - self._size.width())

    def move_left(self, x: float) -> None:
        """
        brief move the rectangle.
        the left line is set to the given position.
        the size is unchanged.
        param x left value
        """
        self._top_left._x = x

    def move_min_x(self, x: float) -> None:
        """
        brief alias of moveLeft.
        param x left value
        """
        self.move_left(x)

    def move_right(self, x: float) -> None:
        """
        brief move the rectangle.
        the right line is set to the given value.
        the size is unchanged.
        param x right value
        """
        self._top_left._x = x - self._size.length()

    def move_max_x(self, x: float) -> None:
        """
        brief alias of moveRight.
        param x right value
        """
        self.move_right(x)

    def move_top(self, y: float) -> None:
        """
        brief move the rectangle.
        the top line is set to the given value.
        the size is unchanged.
        param y top value
        """
        self._top_left._y = y

    def move_min_y(self, y: float) -> None:
        """
        brief alias of moveTop.
        param y top value
        """
        self.move_top(y)

    def move_bottom(self, y: float) -> None:
        """
        brief move the rectangle.
        the top line is set to the given value.
        the size is unchanged.
        param y top value
        """
        self._top_left._y = y - self._size.width()

    def move_max_y(self, y: float) -> None:
        """
        brief alias of moveTop.
        param y top value
        """
        self.move_bottom(y)

    def set_top_left(self, *args) -> Rect2D:
        """
        2 Num
        brief set the top-left corner of the rectangle.
        param x x coordinate
        param y y coordinate
        Vector
        brief set the top-left corner of the rectangle.
        param point coordinate
        the size may be changed, the bottom-right corner will never be changed.
        """
        x = 0.0
        y = 0.0
        if len(args) == 1:
            x = args[0].x()
            y = args[0].y()
        elif len(args) == 2:
            x = args[0]
            y = args[1]
        new_left = min(self.right(), x)
        new_right = max(self.right(), x)
        new_top = min(self.bottom(), y)
        new_bottom = max(self.bottom(), y)
        return self.assign(new_left, new_top, new_right - new_left, new_bottom - new_top)

    def set_bottom_right(self, *args) -> Rect2D:
        """
        2 Num
        brief set the bottom-right corner of the rectangle.
        param x x coordinate
        param y y coordinate
        Vector
        brief set the bottom-right corner of the rectangle.
        param point coordinate
        the size may be changed, the top-left corner will never be changed.
        """
        x = 0.0
        y = 0.0
        if len(args) == 1:
            x = args[0].x()
            y = args[0].y()
        elif len(args) == 2:
            x = args[0]
            y = args[1]
        new_left = min(self.left(), x)
        new_right = max(self.left(), x)
        new_top = min(self.top(), y)
        new_bottom = max(self.top(), y)
        return self.assign(new_left, new_top, new_right - new_left, new_bottom - new_top)

    def set_left(self, x: float) -> None:
        """
        brief set the left of rectangle.
        the size may be changed, the right will never be changed.
        param x left value
        """
        new_left = min(self.right(), x)
        new_right = max(self.right(), x)
        self._top_left._x = new_left
        self._size.set_length(new_right - new_left)

    def set_min_x(self, x: float) -> None:
        """
        brief alias of setLeft.
        param x left value
        """
        self.set_left(x)

    def set_right(self, x: float) -> None:
        """
        brief set the right of rectangle.
        the size may be changed, the left will never be changed.
        param x right value
        """
        new_left = min(self.left(), x)
        new_right = max(self.left(), x)

        self._top_left._x = new_left
        self._size.set_length(new_right - new_left)

    def set_max_x(self, x: float) -> None:
        """
        brief alias of setRight.
        param x right value
        """
        self.set_right(x)

    def set_top(self, y: float) -> None:
        """
        brief set the top of rectangle.
        the size may be changed, the bottom will never be changed.
        param y top value
        """
        new_top = min(self.bottom(), y)
        new_bottom = max(self.bottom(), y)

        self._top_left._y = new_top
        self._size.set_width(new_bottom - new_top)

    def set_min_y(self, y: float) -> None:
        """
        brief alias of setTop.
        param y top value
        """
        self.set_top(y)

    def set_bottom(self, y: float) -> None:
        """
        brief set the bottom of rectangle.
        the size may be changed, the top will never be changed.
        param y bottom value
        """
        new_top = min(self.top(), y)
        new_bottom = max(self.top(), y)

        self._top_left._y = new_top
        self._size.set_width(new_bottom - new_top)

    def set_max_y(self, y: float) -> None:
        """
        brief alias of setBottom.
        param y top value
        """
        self.set_bottom(y)

    def set_length(self, length: float) -> None:
        """
        brief set a x-range
        param length range
        """
        self._size.set_length(length)

    def set_width(self, width: float) -> None:
        """
        brief set a y-range
        param width range
        """
        self._size.set_width(width)

    def set_size(self, *args) -> None:
        """
        2 NUM
        brief set a size
        param length range
        param width range
        1 Size
        brief set a size
        param size range
        """
        if len(args) == 2:
            self._size.assign(args[0], args[1])
        elif len(args) == 1:
            self._size = args[0]

    def is_valid(self) -> bool:
        """
        brief check if self rectangle is valid or not.
        return True if the area of self rectangle is not 0.
        """
        return self._size.is_valid()

    def area(self) -> float:
        """
        brief get the area value of self rectangle.
        return value of the area
        """
        return self._size.length() * self._size.width()

    def contains(self, point: Vector2D) -> bool:
        """
        brief check if point is within self region.
        param point considered point
        return True or False
        """
        return self.left() <= point.x() <= self.right() and self.top() <= point.y() <= self.bottom()

    def contains_weakly(self, point, error_thr) -> bool:
        """
        brief check if point is within self region with error threshold.
        param point considered point
        param error_thr error threshold
        return True or False
        """
        return self.left() - error_thr <= point.x <= self.right() + error_thr and \
               self.top() - error_thr <= point.y <= self.bottom() + error_thr

    def left(self) -> float:
        """
        brief get the left x coordinate of self rectangle.
        return x coordinate value
        """
        return self._top_left.x()

    def right(self) -> float:
        """
        brief get the right x coordinate of self rectangle.
        return x coordinate value
        """
        return self.left() + self._size.length()

    def top(self) -> float:
        """
        brief get the top y coordinate of self rectangle.
        return y coordinate value
        """
        return self._top_left.y()

    def bottom(self) -> float:
        """
        brief get the bottom y coordinate of self rectangle.
        return y coordinate value
        """
        return self.top() + self._size.width()

    def min_x(self) -> float:
        """
        brief get minimum value of x coordinate of self rectangle
        return x coordinate value (equivalent to left())
        """
        return self.left()

    def max_x(self) -> float:
        """
        brief get maximum value of x coordinate of self rectangle
        return x coordinate value (equivalent to right())
        """
        return self.right()

    def min_y(self) -> float:
        """
        brief get minimum value of y coordinate of self rectangle
        return y coordinate value (equivalent to top())
        """
        return self.top()

    def max_y(self) -> float:
        """
        brief get maximum value of y coordinate of self rectangle
        return y coordinate value (equivalent to bottom())
        """
        return self.bottom()

    def size(self) -> Size2D:
        """
        brief get the XY range of self rectangle
        return size object
        """
        return self._size

    def center(self) -> Vector2D:
        """
        brief get center point
        return coordinate value by vector object
        """
        return Vector2D((self.left() + self.right()) * 0.5,
                        (self.top() + self.bottom()) * 0.5)

    def top_left(self) -> Vector2D:
        """
        brief get the top-left corner point
        return coordinate value by vector object
        """
        return self._top_left

    def top_right(self) -> Vector2D:
        """
        brief get the top-right corner point
        return coordinate value by vector object
        """
        return Vector2D(self.right(), self.top())

    def bottom_left(self) -> Vector2D:
        """
        brief get the bottom-left corner point
        return coordinate value by vector object
        """
        return Vector2D(self.left(), self.bottom())

    def bottom_right(self) -> Vector2D:
        """
        brief get the bottom-right corner point
        return coordinate value by vector object
        """
        return Vector2D(self.right(), self.bottom())

    def left_edge(self) -> Line2D:
        """
        brief get the left edge line
        return line object
        """
        return Line2D(self.top_left(), self.bottom_left())

    def right_edge(self) -> Line2D:
        """
        brief get the right edge line
        return line object
        """
        return Line2D(self.top_right(), self.bottom_right())

    def top_edge(self) -> Line2D:
        """
        brief get the top edge line
        return line object
        """
        return Line2D(self.top_left(), self.top_right())

    def bottom_edge(self) -> Line2D:
        """
        brief get the bottom edge line
        return line object
        """
        return Line2D(self.bottom_left(), self.bottom_right())

    def intersection(self,
                     line: Line2D = None,
                     ray: Ray2D = None,
                     segment: Segment2D = None):
        """
        Line2D
        brief calculate intersection point with line.
        param line considered line.
        param sol1 pointer to the 1st solution variable
        param sol2 pointer to the 2nd solution variable
        return number of intersection
        Ray2D
        brief calculate intersection point with ray.
        param ray considered ray line.
        param sol1 pointer to the 1st solution variable
        param sol2 pointer to the 2nd solution variable
        return number of intersection
        Segment2D
        brief calculate intersection point with line segment.
        param segment considered line segment.
        param sol1 pointer to the 1st solution variable
        param sol2 pointer to the 2nd solution variable
        return number of intersection
        """
        if line is not None:
            n_sol = 0
            t_sol = [Vector2D(0, 0), Vector2D(0, 0)]
            left_x = self.left()
            right_x = self.right()
            top_y = self.top()
            bottom_y = self.bottom()

            t_sol[n_sol] = self.left_edge().intersection(line)

            if n_sol < 2 and t_sol[n_sol].is_valid() and top_y <= t_sol[n_sol].y() <= bottom_y:
                n_sol += 1

            t_sol[n_sol] = self.right_edge().intersection(line)

            if n_sol < 2 and t_sol[n_sol].is_valid() and top_y <= t_sol[n_sol].y() <= bottom_y:
                n_sol += 1

            t_sol[n_sol] = self.top_edge().intersection(line)

            if n_sol < 2 and (t_sol[n_sol]).is_valid() and left_x <= t_sol[n_sol].x() <= right_x:
                n_sol += 1

            t_sol[n_sol] = self.top_edge().intersection(line)

            if n_sol < 2 and (t_sol[n_sol]).is_valid() and left_x <= t_sol[n_sol].x() <= right_x:
                n_sol += 1

            if n_sol == 2 and math.fabs(t_sol[0].x() - t_sol[1].x()) < EPSILON and math.fabs(
                    t_sol[0].y() - t_sol[1].y()) < EPSILON:
                n_sol = 1

            sol_list = [n_sol, t_sol[0], t_sol[1]]

            return sol_list

        elif ray is not None:
            n_sol = self.intersection(ray.line())

            if n_sol[0] > 1 and not ray.in_right_dir(n_sol[2], 1.0):
                n_sol[0] -= 1

            if n_sol[0] > 0 and not ray.in_right_dir(n_sol[1], 1.0):
                n_sol[1] = n_sol[2]
                n_sol[0] -= 1

            return n_sol
        elif segment is not None:
            n_sol = self.intersection(segment.line())
            if n_sol[0] > 1 and not segment.contains(n_sol[2]):
                n_sol[0] -= 1

            if n_sol[0] > 0 and not segment.contains(n_sol[1]):
                n_sol[1] = n_sol[2]
                n_sol[0] -= 1

            return n_sol

    def intersected(self, other):
        """
        brief get the intersected rectangle of self rectangle and the other rectangle.
        If no intersection between rectangles,empty rectangle is returned.
        param other other rectangle
        return rectangle instance.
        """
        if not self.is_valid or not other.is_valid():
            self._top_left.assign(0.0, 0.0)
            self._size.assign(0.0, 0.0)

        left = max(self.left(), other.left())
        top = max(self.top(), other.top())
        w = min(self.right(), other.right()) - left
        h = min(self.bottom(), other.bottom()) - top

        if w <= 0.0 or h <= 0.0:
            self._top_left.assign(0.0, 0.0)
            self._size.assign(0.0, 0.0)

        self._top_left.assign(left, top)
        self._size.assign(w, h)

    def united(self, other):
        """
        brief get the united rectangle of self rectangle and the other rectangle.
        param other other rectangle
        return rectangle instance.
        """
        if not self.is_valid or not other.is_valid():
            self._top_left.assign(0.0, 0.0)
        self._size.assign(0.0, 0.0)

        left = max(self.left(), other.left())
        top = max(self.top(), other.top())
        w = min(self.right(), other.right()) - left
        h = min(self.bottom(), other.bottom()) - top

        if w <= 0.0 or h <= 0.0:
            self._top_left.assign(0.0, 0.0)
            self._size.assign(0.0, 0.0)

        self._top_left.assign(left, top)
        self._size.assign(w, h)

    @staticmethod
    def from_center(*args):
        """
        4 NUM
        brief create rectangle with center point and size.
        param center_x x value of center point of rectangle.
        param center_y y value of center point of rectangle.
        param length length(x-range) of rectangle.
        param width width(y-range) of rectangle.
        """
        if len(args) == 4:
            return Rect2D(args[0] - args[2] * 0.5, args[1] - args[3] * 0.5, args[2], args[3])
        elif len(args) == 3:
            return Rect2D(args[0] - args[2] * 0.5, args[1] - args[3] * 0.5)

    @staticmethod
    def from_corners(*args):
        """
        brief create rectangle with 2 corner points. just call one of constructor.
        """
        return Rect2D(args)

    def __repr__(self):
        """
        brief make a logical print.
        return print_able str
        """
        return "[len:{},wid:{}]".format(self._top_left, self._size)

    def to_str(self, ostr):
        ostr += ' (rect {} {} {} {})'.format(round(self.left(), 3), round(self.top(), 3),
                                             round(self.right(), 3), round(self.bottom(), 3))
