from unittest import TestCase
from pyrusgeom.circle_2d import Circle2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.line_2d import Line2D
from pyrusgeom.ray_2d import Ray2D
from pyrusgeom.segment_2d import Segment2D


class TestCircle2D(TestCase):
    def test_assign(self):
        c = Circle2D(Vector2D(0, 0), 2)
        self.assertEqual(c.radius(), 2)
        self.assertEqual(c.center().x(), 0)
        self.assertEqual(c.center().y(), 0)

    def test_area(self):
        c = Circle2D(Vector2D(0, 0), 2)
        self.assertTrue(12.56 < c.area() < 12.57)

    def test_contains(self):
        c = Circle2D(Vector2D(0, 0), 2)
        self.assertTrue(c.contains(Vector2D(1, 1)))
        self.assertFalse(c.contains(Vector2D(10, 10)))

    def test_center(self):
        pass

    def test_radius(self):
        pass

    def test_intersection(self):
        c = Circle2D(Vector2D(0, 0), 2)
        line = Line2D(Vector2D(0, 0), 0)
        sols = c.intersection(line)
        self.assertEqual(len(sols), 2)
        self.assertEqual(sols[0].x(), 2)
        self.assertEqual(sols[1].x(), -2)
        self.assertEqual(sols[0].y(), 0)
        self.assertEqual(sols[1].y(), 0)

        line = Line2D(Vector2D(0, 2), 0)
        sols = c.intersection(line)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].x(), 0)
        self.assertEqual(sols[0].y(), 2)

        line = Line2D(Vector2D(0, 3), 0)
        sols = c.intersection(line)
        self.assertEqual(len(sols), 0)

        ray = Ray2D(Vector2D(0, 0), Vector2D(3, 0))
        sols = c.intersection(ray)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].x(), 2)
        self.assertEqual(sols[0].y(), 0)

        ray = Ray2D(Vector2D(3, 3), Vector2D(5, 3))
        sols = c.intersection(ray)
        self.assertEqual(len(sols), 0)

        ray = Ray2D(Vector2D(-3, 0), Vector2D(3, 0))
        sols = c.intersection(ray)
        self.assertEqual(len(sols), 2)
        self.assertEqual(sols[0].x(), 2)
        self.assertEqual(sols[0].y(), 0)
        self.assertEqual(sols[1].x(), -2)
        self.assertEqual(sols[1].y(), 0)

        ray = Ray2D(Vector2D(-2, 2), Vector2D(2, 2))
        sols = c.intersection(ray)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].x(), 0)
        self.assertEqual(sols[0].y(), 2)

        seg = Segment2D(Vector2D(0, 0), Vector2D(3, 0))
        sols = c.intersection(seg)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].x(), 2)
        self.assertEqual(sols[0].y(), 0)

        seg = Segment2D(Vector2D(5, 5), Vector2D(8, 8))
        sols = c.intersection(seg)
        self.assertEqual(len(sols), 0)

        seg = Segment2D(Vector2D(-3, 0), Vector2D(3, 0))
        sols = c.intersection(seg)
        self.assertEqual(len(sols), 2)
        self.assertEqual(sols[0].x(), 2)
        self.assertEqual(sols[0].y(), 0)
        self.assertEqual(sols[1].x(), -2)
        self.assertEqual(sols[1].y(), 0)

        seg = Segment2D(Vector2D(-2, 2), Vector2D(2, 2))
        sols = c.intersection(seg)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].x(), 0)
        self.assertEqual(sols[0].y(), 2)

        c2 = Circle2D(Vector2D(4, 0), 2)
        sols = c.intersection(c2)
        self.assertEqual(len(sols), 1)
        self.assertEqual(sols[0].x(), 2)
        self.assertEqual(sols[0].y(), 0)

        c2 = Circle2D(Vector2D(4, 0), 10)
        sols = c.intersection(c2)
        self.assertEqual(len(sols), 0)

        c2 = Circle2D(Vector2D(4, 0), 3)
        sols = c.intersection(c2)
        self.assertEqual(len(sols), 2)
        print(sols)
        self.assertEqual(sols[0].x(), 1.375)
        self.assertTrue(abs(sols[0].y() - 1.45) < 0.1)

    def test_circum_circle(self):
        v1 = Vector2D(0, 0)
        v2 = Vector2D(1, 0)
        v3 = Vector2D(0, 1)
        circle = Circle2D.circum_circle(v1, v2, v3)
        self.assertEqual(circle.center().x(), 0.5)
        self.assertEqual(circle.center().y(), 0.5)
        self.assertAlmostEqual(circle.radius(), 0.70710678)

    def test_circle_contains(self):
        v1 = Vector2D(0, 0)
        v2 = Vector2D(1, 0)
        v3 = Vector2D(0, 1)
        self.assertTrue(Circle2D.circum_circle_contains(Vector2D(0.5, 0.5), v1, v2, v3))
        self.assertFalse(Circle2D.circum_circle_contains(Vector2D(2, 2), v1, v2, v3))
