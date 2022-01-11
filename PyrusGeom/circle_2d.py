"""
  \ file circle_2d.py
  \ brief 2D circle region File.
"""
from __future__ import annotations
from typing import Union
from PyrusGeom.segment_2d import Segment2D
from PyrusGeom.ray_2d import Ray2D
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.line_2d import Line2D
from PyrusGeom.triangle_2d import Triangle2D
from PyrusGeom.math_values import *
import math


def quadratic_f(a, b, c) -> list:
    """
    brief solve quadratic formula
    @param a formula constant A
    @param b formula constant B
    @param c formula constant C
    @return number of solution, sol1 reference to the result variable, sol2 reference to the result variable
    """
    d = b * b - 4.0 * a * c
    sol1 = 0.0
    sol2 = 0.0
    if math.fabs(d) < EPSILON:
        sol1 = -b / (2.0 * a)
        ans = 1
    elif d < 0.0:
        ans = 0
    else:
        d = math.sqrt(d)
        sol1 = (-b + d) / (2.0 * a)
        sol2 = (-b - d) / (2.0 * a)
        ans = 2
    return [ans, sol1, sol2]


class Circle2D:
    def __init__(self, center=Vector2D(), radius=0.0):
        """
        Default:
        brief create a zero area circle at (0,0)
        brief construct with center point and radius value.
        @param center center point
        @param radius radius value
        """
        self._center: Vector2D = center
        self._radius: float = radius
        if radius < 0.0:
            self._radius = 0.0
        self._is_valid = True

    def assign(self, c: Vector2D, r: float):
        """
        brief assign value.
        @param c center point
        @param r radius value
        """
        self._center = c
        self._radius = r
        if r < 0.0:
            self._radius = 0.0

    def area(self) -> float:
        """
        brief get the area value of self circle
        @return value of the area
        """
        return PI * self._radius * self._radius

    def contains(self, point: Vector2D) -> bool:
        """
        brief check if point is within self region
        @param point considered point
        @return True if point is contained by self circle
        """
        return self._center.dist2(point) < self._radius * self._radius

    def center(self):
        """
        brief get the center point
        @return center point coordinate value
        """
        return self._center

    def radius(self):
        """
        brief get the radius value
        @return radius value
        """
        return self._radius

    def intersection(self, other: Union[Line2D, Ray2D, Segment2D, Circle2D]) -> list[Vector2D]:
        """
        brief calculate the intersection with straight line
        @param other considered line or ray or segment or circle
        return the number of solution + solutions
        """
        if isinstance(other, Line2D):
            if math.fabs(other.a()) < EPSILON:
                if math.fabs(other.b()) < EPSILON:
                    return []

                n_sol = quadratic_f(1.0,
                                    -2.0 * self._center.x(),
                                    (math.pow(self._center.x(), 2)
                                     + math.pow(other.c() / other.b() + self._center.y(), 2)
                                     - math.pow(self._radius, 2)))
                x1 = n_sol[1]
                x2 = n_sol[2]
                if n_sol[0] > 0:
                    y1 = -other.c() / other.b()
                    sol_list = [Vector2D(x1, y1), Vector2D(x2, y1)]
                    if x1 == x2:
                        del sol_list[1]
                else:
                    sol_list = []
                return sol_list

            else:
                m = other.b() / other.a()
                d = other.c() / other.a()

                a = 1.0 + m * m
                b = 2.0 * (-self._center.y() + (d + self._center.x()) * m)
                c = (d + self._center.x()) ** 2 + (self._center.y()) ** 2 - self._radius ** 2

            n_sol = quadratic_f(a, b, c)
            y1 = n_sol[1]
            y2 = n_sol[2]
            if n_sol[0] > 0:
                sol_list = [Vector2D(other.get_x(y1), y1), Vector2D(other.get_x(y2), y2)]
                if sol_list[0].equals_weakly(sol_list[1]):
                    del sol_list[1]
            else:
                sol_list = []

            return sol_list
        elif isinstance(other, Ray2D):
            line_tmp = Line2D(other.origin(), other.dir())
            sol_list = self.intersection(line_tmp)
            if len(sol_list) > 1 and not other.in_right_dir(sol_list[1], 1.0):
                del sol_list[1]

            if len(sol_list) > 0 and not other.in_right_dir(sol_list[0], 1.0):
                sol_list[0] = sol_list[1]
                del sol_list[1]

            return sol_list

        elif isinstance(other, Segment2D):
            line = other.line()
            sol_list = self.intersection(line)
            if len(sol_list) > 1 and not other.contains(sol_list[1]):
                del sol_list[1]

            if len(sol_list) > 0 and not other.contains(sol_list[0]):
                del sol_list[0]

            return sol_list
        elif isinstance(other, Circle2D):
            rel_x = other.center().x() - self._center.x()
            rel_y = other.center().y() - self._center.y()
            center_dist2 = rel_x * rel_x + rel_y * rel_y
            center_dist = math.sqrt(center_dist2)
            if center_dist < math.fabs(self._radius - other.radius()) or self._radius + other.radius() < center_dist:
                return []

            line = Line2D(-2.0 * rel_x, -2.0 * rel_y,
                          other.center().r2() - other.radius() * other.radius()
                          - self._center.r2() + self._radius * self._radius)
            sol_list = self.intersection(line)
            return sol_list

    def intersection_with_line(self, line: Line2D) -> list[Vector2D]:
        return self.intersection(line)

    def intersection_with_ray(self, ray: Ray2D) -> list[Vector2D]:
        return self.intersection(ray)

    def intersection_with_segment(self, segment: Segment2D) -> list[Vector2D]:
        return self.intersection(segment)

    def intersection_with_circle(self, circle: Circle2D) -> list[Vector2D]:
        return self.intersection(circle)

    @staticmethod
    def circum_circle(p0: Vector2D, p1: Vector2D, p2: Vector2D) -> Circle2D:
        """
        brief get the circle through three points (circum_circle of the triangle).
        @param p0 triangle's 1st vertex
        @param p1 triangle's 2nd vertex
        @param p2 triangle's 3rd vertex
        @return coordinates of circumcenter
        """

        center = Triangle2D.tri_circumcenter(p0, p1, p2)

        if not center.is_valid():
            return Circle2D()

        return Circle2D(center, center.dist(p0))

    @staticmethod
    def circum_circle_contains(point: Vector2D, p0: Vector2D, p1: Vector2D, p2: Vector2D) -> bool:
        """
        brief check if the circum_circle contains the input point
        @param point input point
        @param p0 triangle's 1st vertex
        @param p1 triangle's 2nd vertex
        @param p2 triangle's 3rd vertex
        @return True if circum_circle contains the point, False.
        """
        a = p1.x() - p0.x()
        b = p1.y() - p0.y()
        c = p2.x() - p0.x()
        d = p2.y() - p0.y()

        e = a * (p0.x() + p1.x()) + b * (p0.y() + p1.y())
        f = c * (p0.x() + p2.x()) + d * (p0.y() + p2.y())

        g = 2.0 * (a * (p2.y() - p1.y()) - b * (p2.x() - p1.x()))
        if math.fabs(g) < 1.0e-10:
            return False

        center = Vector2D((d * e - b * f) / g, (a * f - c * e) / g)
        return center.dist2(point) < center.dist2(p0) - EPSILON * EPSILON

    def __repr__(self):
        """
        brief make a logical print.
        @return print_able str
        """
        return "({} , {})".format(self._center, self._radius)

    def to_str(self, ostr):
        ostr += ' (circle {} {} {})'.format(round(self.center().x(), 3), round(self.center().y(), 3), round(self.radius(), 3))
