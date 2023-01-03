""" triangle_2d.py file
    Triangle2D: class name
    Class attributes : _a,_b,_c
    TODO: add test and reverse fix intersection
    TODO: fix the circular import tri-segmant
"""

from __future__ import annotations
# from typing import Union
import math

# from pyrusgeom.segment_2d import Segment2D (removed most likely due to a circular import)
from pyrusgeom.region_2d import Region2D
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg
from pyrusgeom.line_2d import Line2D
from pyrusgeom.math_values import EPSILON


class Triangle2D(Region2D):
    """handling tiiangles in SS2D

    Args:
        Region2D ([type]): created from Region2D class

    Attributes:
        _a: 1st vertex point
        _b: 2nd vertex point
        _c: 3rd vertex point
    """

    def __init__(self, *args) -> None:
        """This is the class init function for Triangle2D

        Args:
            two:
                1 segment 1 vector2D
                (Segment2D, Vector2D)
                Segment2D: segment consist of triangle
                Vector2D: 3rd vertex point
            three:
                (float, float, float)
                float: first vertex point
                float: second vertex point
                float: third vertex point

        Raises:
            Exception: The input must be (three Vector2D) or
                       (one vector 2D and one segment)
        """

        super().__init__()
        if len(args) == 3:
            self._a: Vector2D = Vector2D(args[0])
            self._b: Vector2D = Vector2D(args[1])
            self._c: Vector2D = Vector2D(args[2])
        elif len(args) == 2:  # and isinstance(args[0], Segment2D):
            self._a = Vector2D(args[0].origin_())
            self._b = Vector2D(args[0].terminal_())
            self._c = Vector2D(args[1])
        else:
            raise Exception("The input must be (three Vector2D) or\
                            (one vector 2D and one segment)")

    def assign(self, *args) -> Triangle2D:
        """assign vertex points

        Args:
            two:
                1 segment 1 vector2D
                (Segment2D, Vector2D)
                Segment2D: segment consist of triangle
                Vector2D: 3rd vertex point
            three:
                (float, float, float)
                float: first vertex point
                float: second vertex point
                float: third vertex point

        Raises:
            Exception: The input must be (three Vector2D) or
                       (one vector 2D and one segment)

        Returns:
            Triangle2D: reference to itself
        """
        if len(args) == 3:
            self._a: Vector2D = Vector2D(args[0])
            self._b: Vector2D = Vector2D(args[1])
            self._c: Vector2D = Vector2D(args[2])
        elif len(args) == 2:  # and isinstance(args[0], Segment2D):
            self._a = Vector2D(args[0].origin_())
            self._b = Vector2D(args[0].terminal_())
            self._c = Vector2D(args[1])
        else:
            raise Exception("The input must be (three Vector2D) or\
                            (one vector 2D and one segment)")
        return self

    def is_valid(self) -> bool:
        """check if self triangle is valid or not.

        Returns:
            bool: True if triangle is valid. else False.
        """
        return (self._a.is_valid() and self._b.is_valid() and self._c.is_valid() and
                self._a != self._b and self._b != self._c and self._a != self._a)

    def a(self) -> Vector2D:
        """get 1st point copy

        Returns:
            Vector2D: a Vector2D with point values
        """
        return Vector2D(self._a)

    def b(self) -> Vector2D:
        """get 2nd point copy

        Returns:
            Vector2D: a Vector2D with point values
        """
        return Vector2D(self._b)

    def c(self) -> Vector2D:
        """get 3rd point copy

        Returns:
            Vector2D: a Vector2D with point values
        """
        return Vector2D(self._c)

    def a_(self) -> Vector2D:
        """get 1st point

        Returns:
            Vector2D: reference to the member variable
        """
        return self._a

    def b_(self) -> Vector2D:
        """get 2nd point

        Returns:
            Vector2D: reference to the member variable
        """
        return self._b

    def c_(self) -> Vector2D:
        """get 3rd point

        Returns:
            Vector2D: reference to the member variable
        """
        return self._c

    def area(self) -> float:
        """get the area of self region

        Returns:
            float: value of the area
        """
        return math.fabs((self._b - self._a).outer_product(self._c - self._a)) * 0.5

    def signed_area(self) -> float:
        """get a signed area.

        method is equivalent to signed_area_st().

        If points a, b, are placed counterclockwise order, positive number.
        If points a, b, are placed clockwise order, negative number.
        If points a, b, are placed on a line, 0.

        Returns:
            float: signed area value
        """
        return Triangle2D.signed_area_st(self._a, self._b, self._c)

    def double_signed_area(self) -> float:
        """get a double of signed area value.

        method is equivalent to double_signed_area_st().

        If points a, b, are placed counterclockwise order, positive number.
        If points a, b, are placed clockwise order, negative number.
        If points a, b, are placed on a line, 0.

        Returns:
            float: double of signed area value
        """
        return Triangle2D.double_signed_area_st(self._a, self._b, self._c)

    def ccw(self) -> bool:
        """check if self triangle's vertices are placed counterclockwise order.

        Returns:
            bool: True if counterclockwise. else False
        """
        return Triangle2D.tri_ccw(self._a, self._b, self._c)

    def contains(self, point: Vector2D) -> bool:
        """check if self triangle contains 'point'.

        Args:
            point (Vector2D): considered point

        Returns:
            bool: True if contains. else False.
        """
        rel1 = Vector2D(self._a - point)
        rel2 = Vector2D(self._b - point)
        rel3 = Vector2D(self._c - point)

        outer1 = rel1.outer_product(rel2)
        outer2 = rel2.outer_product(rel3)
        outer3 = rel3.outer_product(rel1)

        if (outer1 >= 0.0 and outer2 >= 0.0 and
            outer3 >= 0.0) or (outer1 <= 0.0 and
                               outer2 <= 0.0 and outer3 <= 0.0):
            return True
        return False

    def centroid(self) -> Vector2D:
        """get the center of gravity(centroid)

        Returns:
            Vector2D: coordinates of gravity center
        """
        return Triangle2D.tri_centroid(self._a, self._b, self._c)

    def incenter(self) -> Vector2D:
        """get the center of inscribed circle

        Returns:
            Vector2D: coordinates of inner center
        """
        return Triangle2D.tri_incenter(self._a, self._b, self._c)

    def circumcenter(self) -> Vector2D:
        """get the center of circumscribed circle

        Returns:
            Vector2D: coordinates of outer center
        """
        return Triangle2D.tri_circumcenter(self._a, self._b, self._c)

    def orthocenter(self) -> Vector2D:
        """get the orthocenter

        Returns:
            Vector2D: coordinates of orthocenter
        """
        return Triangle2D.tri_orthocenter(self._a, self._b, self._c)

    def intersection(self, other): # Union[Line2D, Ray2D, Segment2D]) -> list:
        """
        TODO: Need to rewrite. fixed TriBug
            Line2D
        brief calculate intersection point with line.
        param line considered line.
        return number of intersection + sol 1 + sol 2
            Ray2D
        brief calculate intersection point with ray.
        param ray considered ray line.
        return number of intersection + sol 1 + sol 2
            Segment2D
        brief calculate intersection point with line segment.
        param segment considered line segment.
        return number of intersection + sol 1 + sol 2
        """
        if isinstance(other, Line2D):
            n_sol = 0
            t_sol = [Vector2D(), Vector2D()]
            from pyrusgeom.segment_2d import Segment2D
            t_sol[n_sol] = Segment2D(self._a, self._b).intersection(other)
            if n_sol < 2 and t_sol[n_sol].is_valid():
                n_sol += 1

            t_sol[n_sol] = Segment2D(self._b, self._c).intersection(other)
            if n_sol < 2 and t_sol[n_sol].is_valid():
                n_sol += 1

            t_sol[n_sol] = Segment2D(self._c, self._a).intersection(other)
            if n_sol < 2 and t_sol[n_sol].is_valid():
                n_sol += 1

            if n_sol == 2 and math.fabs(t_sol[0].x() - t_sol[1].x()) < EPSILON and math.fabs(
                    t_sol[0].y() - t_sol[1].y()) < EPSILON:
                n_sol = 1
            sol_list = [n_sol, t_sol[0], t_sol[1]]

            return sol_list
        if isinstance(other, Ray2D):
            n_sol = self.intersection(other.line())

            if n_sol[0] > 1 and not other.in_right_dir(n_sol[1], 1.0):
                n_sol[0] -= 1

            if n_sol[0] > 0 and not other.in_right_dir(n_sol[1], 1.0):
                n_sol[1] = n_sol[2]
                n_sol[0] -= 1

            return n_sol

        if isinstance(other, Segment2D):
            n_sol = self.intersection(other.line())

            if n_sol[0] > 1 and not other.contains(n_sol[2]):
                n_sol[0] -= 1

            if n_sol > 0 and not other.contains(n_sol[1]):
                n_sol[1] = n_sol[2]
                n_sol[0] -= 1

            return n_sol
        return [0]

    # static methods

    @staticmethod
    def double_signed_area_st(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> float:
        """get a double signed area value (area of parallelogram)

        If points a, b, are placed counterclockwise order, positive number.
        If points a, b, are placed clockwise order, negative number.
        If points a, b, are placed on a line, 0.

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            float: double singed area value.
        """
        return ((v_a.x() - v_c.x()) * (v_b.y() - v_c.y())
                + (v_b.x() - v_c.x()) * (v_c.y() - v_a.y()))

    @staticmethod
    def signed_area_st(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> float:
        """get a signed area value

        If points a, b, are placed counterclockwise order, positive number.
        If points a, b, are placed clockwise order, negative number.
        If points a, b, are placed on a line, 0.

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            float: signed area value
        """
        return Triangle2D.double_signed_area_st(v_a, v_b, v_c) * 0.5

    @staticmethod
    def tri_ccw(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> bool:
        """check if input vertices are placed counterclockwise order.

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            bool: True if counterclockwise. else False
        """
        return Triangle2D.double_signed_area_st(v_a, v_b, v_c) > 0.0

    @staticmethod
    def tri_centroid(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> Vector2D:
        """ get the center of gravity

        centroid = (a + b + c) / 3

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            Vector2D: coordinates of gravity center
        """
        return Vector2D(v_a).add(v_b).add(v_c) / 3.0

    @staticmethod
    def tri_incenter(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> Vector2D:
        """get the incenter point

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            Vector2D: coordinates of incenter
        """
        a_b = v_b - v_a
        a_c = v_c - v_a
        bisect_a = Line2D(v_a, AngleDeg.bisect(a_b.th(), a_c.th()))

        b_a = v_a - v_b
        b_c = v_c - v_b
        bisect_b = Line2D(v_b, AngleDeg.bisect(b_a.th(), b_c.th()))

        return bisect_a.intersection(bisect_b)

    @staticmethod
    def tri_circumcenter(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> Vector2D:
        """get the circumcenter point

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            Vector2D: coordinates of circumcenter
        """
        perpendicular_ab = Line2D.perpendicular_bisector(v_a, v_b)
        perpendicular_bc = Line2D.perpendicular_bisector(v_b, v_c)

        sol = perpendicular_ab.intersection(perpendicular_bc)

        if not sol.is_valid():
            perpendicular_ca = Line2D.perpendicular_bisector(v_c, v_a)
            sol = perpendicular_ab.intersection(perpendicular_ca)

            if sol.is_valid():
                return sol

            sol = perpendicular_bc.intersection(perpendicular_ca)
            if sol.is_valid():
                return sol

        a_b = v_b - v_a
        c_a = v_c - v_a

        tmp = a_b.outer_product(c_a)
        if math.fabs(tmp) < 1.0e-10:  # The area of parallelogram is 0.
            return Vector2D.invalid()

        inv = 0.5 / tmp
        ab_len2 = a_b.r2()
        ca_len2 = c_a.r2()
        xcc = inv * (ab_len2 * c_a.get_y() - ca_len2 * a_b.get_y())
        ycc = inv * (a_b.get_x() * ca_len2 - c_a.get_x() * ab_len2)

        return Vector2D(v_a.x() + xcc, v_a.y() + ycc)

    @staticmethod
    def tri_orthocenter(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D) -> Vector2D:
        """get the orthocenter point

        orthocenter = a + b + c - 2 * circumcenter

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point

        Returns:
            Vector2D: coordinates of orthocenter
        """
        perpend_a = Line2D(v_b, v_c).perpendicular(v_a)
        perpend_b = Line2D(v_c, v_a).perpendicular(v_b)
        return perpend_a.intersection(perpend_b)

    @staticmethod
    def tri_contains(v_a: Vector2D, v_b: Vector2D, v_c: Vector2D, point: Vector2D) -> bool:
        """ check if triangle(a,b,c) contains the input point.

        Args:
            v_a (Vector2D): triangle's 1st vertex point
            v_b (Vector2D): triangle's 2nd vertex point
            v_c (Vector2D): triangle's 3rd vertex point
            point (Vector2D): checked point

        Returns:
            bool: True if contains. else Fasle.
        """
        rel1 = Vector2D(v_a - point)
        rel2 = Vector2D(v_b - point)
        rel3 = Vector2D(v_c - point)

        outer1 = rel1.outer_product(rel2)
        outer2 = rel2.outer_product(rel3)
        outer3 = rel3.outer_product(rel1)

        if (outer1 >= 0.0 and outer2 >= 0.0 and
            outer3 >= 0.0) or (outer1 <= 0.0 and
                               outer2 <= 0.0 and outer3 <= 0.0):
            return True
        return False

    def __repr__(self) -> str:
        """represent Triangle2D as a string

        Returns:
            str: Triangle2D's _a, _b and _c as string
        """
        return f"[{self._a},{self._b},{self._c}]"

    def to_str(self, ostr: str) -> str:
        """add triangle to the ostr

        Args:
            ostr (str): str to add to it
        """
        ostr += f'(tri {round(self.a().x(), 3)} {round(self.a().y(), 3)} {round(self.b().x(), 3)} \
        {round(self.b().y(), 3)} {round(self.c().x(), 3)} {round(self.c().y(), 3)})'
