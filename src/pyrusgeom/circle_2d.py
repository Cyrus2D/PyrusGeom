""" circle_2d.py file
    Circle2D: class name
    Class attributes: _center, _radius, _is_valid
    TODO: add eq hash

"""
from __future__ import annotations
from typing import Union
import math

from pyrusgeom.segment_2d import Segment2D
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.line_2d import Line2D
from pyrusgeom.triangle_2d import Triangle2D
from pyrusgeom.math_values import PI, EPSILON


class Circle2D:
    """ handling circles in SS2D
    Attributes:
        _center: a Vector2D for center point
        _radius: a non-negetive float for radius value
        _is_valid: a boolean for validation
    """

    def __init__(self, center: Vector2D = Vector2D(), radius: float = 0.0):
        """This is the class init function for Circle2D.

        Defualt:
            create a zero area circle at (0,0) which has zero radius
        OR:
            bulid a circle2d
        Args:
            center (Vector2D, optional): center point. Defaults to Vector2D().
            radius (float, optional): a non-negetive radius value. Defaults to 0.0.
        """
        self._center: Vector2D = Vector2D(center)
        self._radius: float = radius
        if radius < 0.0:
            self._radius = 0.0
        self._is_valid = True

    def assign(self, center: Vector2D, radius: float):
        """set a new circle for Circle2D

        Args:
            center (Vector2D): center point
            radius (float): radius value
        """
        self._center = Vector2D(center)
        self._radius = radius
        if radius < 0.0:
            self._radius = 0.0
        self._is_valid = True

    def area(self) -> float:
        """get the area value of this circle

        Returns:
            float: value of area of circle
        """
        return PI * self._radius * self._radius

    def contains(self, point: Vector2D) -> bool:
        """check if point is within this circle

        Args:
            point (Vector2D): considered point

        Returns:
            bool: True if point is contained by self circle
        """
        return self._center.dist2(point) < self._radius * self._radius

    def center(self) -> Vector2D:
        """get the center point copy

        Returns:
            Vector2D: center point coordinate value
        """
        return Vector2D(self._center)

    def center_(self) -> Vector2D:
        """get the center point

        Returns:
            Vector2D: center point coordinate
        """
        return self._center

    def radius(self) -> float:
        """get the radius value

        Returns:
            float: radius value
        """
        return self._radius

    def intersection(self, other: Union[Line2D, Ray2D, Segment2D, Circle2D]) -> list[Vector2D]:
        """calculate the intersection with Line2D, Ray2D, Segment2D, Circle2D
        Args:
            other (Union[Line2D, Ray2D, Segment2D, Circle2D]): considered line
                    or ray or segment or circle

        Returns:
            list[Vector2D]: a list contains solutions if there is none return an empty list
        Raises:
            Exception: Input must be one of Line2D, Ray2D, Segment2D, Circle2D
        """
        if isinstance(other, Line2D):
            if math.fabs(other.a()) < EPSILON:
                if math.fabs(other.b()) < EPSILON:
                    return []

                n_sol = quadratic_f(1.0,
                                    -2.0 * self._center.x(),
                                    (math.pow(self._center.x(), 2)
                                     + math.pow(other.c() /
                                                other.b() + self._center.y(), 2)
                                     - math.pow(self._radius, 2)))

                if len(n_sol):
                    sol_tmp_1 = -other.c() / other.b()
                    sol_1 = n_sol[0]
                    sol_2 = n_sol[1]
                    sol_list = [Vector2D(sol_1, sol_tmp_1),
                                Vector2D(sol_2, sol_tmp_1)]
                    if sol_list[0].equals_weakly(sol_list[1]):
                        del sol_list[1]
                else:
                    sol_list = []
                return sol_list

            b_a = other.b() / other.a()
            c_a = other.c() / other.a()

            line_a = 1.0 + b_a * b_a
            line_b = 2.0 * (-self._center.y() + (c_a + self._center.x()) * b_a)
            line_c = (c_a + self._center.x()) ** 2 + \
                (self._center.y()) ** 2 - self._radius ** 2

            n_sol = quadratic_f(line_a, line_b, line_c)
            if len(n_sol):
                sol_tmp_1 = n_sol[0]
                sol_tmp_2 = n_sol[1]
                sol_list = [Vector2D(other.get_x(sol_tmp_1), sol_tmp_1),
                            Vector2D(other.get_x(sol_tmp_2), sol_tmp_2)]
                if sol_list[0].equals_weakly(sol_list[1]):
                    del sol_list[1]
            else:
                sol_list = []

            return sol_list
        if isinstance(other, Ray2D):
            line_tmp = Line2D(other.origin(), other.dir())
            sol_list = self.intersection(line_tmp)
            if len(sol_list) > 1 and not other.in_right_dir(sol_list[1], 1.0):
                del sol_list[1]

            if len(sol_list) > 0 and not other.in_right_dir(sol_list[0], 1.0):
                del sol_list[0]

            return sol_list

        if isinstance(other, Segment2D):
            line = other.line()
            sol_list = self.intersection(line)
            if len(sol_list) > 1 and not other.contains(sol_list[1]):
                del sol_list[1]

            if len(sol_list) > 0 and not other.contains(sol_list[0]):
                del sol_list[0]

            return sol_list

        if isinstance(other, Circle2D):
            rel_x = other.center().x() - self._center.x()
            rel_y = other.center().y() - self._center.y()
            center_dist2 = rel_x * rel_x + rel_y * rel_y
            center_dist = math.sqrt(center_dist2)
            if (center_dist < math.fabs(self._radius - other.radius()) or
                    self._radius + other.radius() < center_dist):
                return []

            line = Line2D(-2.0 * rel_x, -2.0 * rel_y,
                          other.center().r2() - other.radius() * other.radius()
                          - self._center.r2() + self._radius * self._radius)
            sol_list = self.intersection(line)
            return sol_list

        raise Exception(
            'The input should be one of Line2D, Ray2D, Segment2D, Circle2D')

    def intersection_with_line(self, line: Line2D) -> list[Vector2D]:
        """calculate the intersection with Line2D

        Args:
            line (Line2D): considered line

        Returns:
            list[Vector2D]: a list contains solutions if there is none return an empty list
        """
        return self.intersection(line)

    def intersection_with_ray(self, ray: Ray2D) -> list[Vector2D]:
        """calculate the intersection with Ray2D

        Args:
            line (Ray2D): considered ray

        Returns:
            list[Vector2D]: a list contains solutions if there is none return an empty list
        """
        return self.intersection(ray)

    def intersection_with_segment(self, segment: Segment2D) -> list[Vector2D]:
        """calculate the intersection with Segment2D

        Args:
            line (Segment2D): considered segment

        Returns:
            list[Vector2D]: a list contains solutions if there is none return an empty list
        """
        return self.intersection(segment)

    def intersection_with_circle(self, circle: Circle2D) -> list[Vector2D]:
        """calculate the intersection with Circle2D

        Args:
            line (Circle2D): considered circle

        Returns:
            list[Vector2D]: a list contains solutions if there is none return an empty list
        """
        return self.intersection(circle)

    @staticmethod
    def circum_circle(point_0: Vector2D, point_1: Vector2D, point_2: Vector2D) -> Circle2D:
        """get the circle through three points (circum_circle of the triangle).

        Args:
            point_0 (Vector2D): triangle's 1st vertex
            point_1 (Vector2D): triangle's 2nd vertex
            point_2 (Vector2D): triangle's 3rd vertex

        Returns:
            Circle2D: coordinates of circumcenter
        """

        center = Triangle2D.tri_circumcenter(point_0, point_1, point_2)

        if not center.is_valid():
            return Circle2D()

        return Circle2D(center, center.dist(point_0))

    @staticmethod
    def circum_circle_contains(input_point: Vector2D, point_0: Vector2D,
                               point_1: Vector2D, point_2: Vector2D) -> bool:
        """check if the circum_circle contains the input point

        Args:
            input_point (Vector2D): input point
            point_0 (Vector2D): triangle's 1st vertex
            point_1 (Vector2D): triangle's 2nd vertex
            point_2 (Vector2D): triangle's 3rd vertex

        Returns:
            bool: True if circum_circle contains the point, False.
        """

        p_1_0_x = point_1.x() - point_0.x()
        p_1_0_y = point_1.y() - point_0.y()
        p_2_0_x = point_2.x() - point_0.x()
        p_2_0_y = point_2.y() - point_0.y()

        p_1_0_avg = p_1_0_x * (point_0.x() + point_1.x()) + \
            p_1_0_y * (point_0.y() + point_1.y())
        p_2_0_avg = p_2_0_x * (point_0.x() + point_2.x()) + \
            p_2_0_y * (point_0.y() + point_2.y())

        calc_area = 2.0 * (p_1_0_x * (point_2.y() - point_1.y()) -
                           p_1_0_y * (point_2.x() - point_1.x()))
        if math.fabs(calc_area) < 1.0e-10:
            return False

        center = Vector2D((p_2_0_y * p_1_0_avg - p_1_0_y * p_2_0_avg) / calc_area,
                          (p_1_0_x * p_2_0_avg - p_2_0_x * p_1_0_avg) / calc_area)
        return center.dist2(input_point) < center.dist2(point_0) - EPSILON * EPSILON

    def __repr__(self) -> str:
        """represent Circle2D as a string

        Returns:
            str: Circle2D's center and radius as string
        """
        return f"({self._center} , {self._radius})"

    def to_str(self, ostr: str) -> None:
        """add circle to the ostr

        Args:
            ostr (str): str to add to it
        """
        ostr += f'(circle {round(self.center().x(), 3)} \
            {round(self.center().y(), 3)} {round(self.radius(), 3)})'


def quadratic_f(qf_a: float, qf_b: float, qf_c: float) -> list[float]:
    """solve quadratic equation
    Args:
        qf_a (float): formula constant A
        qf_b (float): formula constant B
        qf_c (float): formula constant C

    Returns:
        list[float]: sol1 reference to the result variable, sol2 reference to the result variable
    """

    delta = qf_b * qf_b - 4.0 * qf_a * qf_c
    sol1 = 0.0
    sol2 = 0.0
    if qf_a == 0:
        raise Exception('Dvided by zero in quadratic_f')
    if math.fabs(delta) < EPSILON:
        sol1 = -qf_b / (2.0 * qf_a)
        return [sol1,sol1]
    elif delta < 0.0:
        return []
    else:
        delta = math.sqrt(delta)
        sol1 = (-qf_b + delta) / (2.0 * qf_a)
        sol2 = (-qf_b - delta) / (2.0 * qf_a)
        return [sol1, sol2]
