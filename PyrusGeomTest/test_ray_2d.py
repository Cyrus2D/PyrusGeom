from unittest import TestCase
from PyrusGeom.vector_2d import Vector2D
from PyrusGeom.angle_deg import AngleDeg
from PyrusGeom.ray_2d import Ray2D
from PyrusGeom.line_2d import Line2D


class TestRay2D(TestCase):
    def test_origin(self):
        a = Vector2D(0, 0)
        b = Vector2D(10, 0)
        r = Ray2D(a, b)
        self.assertEqual(r.origin().x(), 0)
        self.assertEqual(r.dir().degree(), 0)
        a.set_x(20)
        self.assertEqual(r.origin().x(), 0)
        self.assertEqual(r.dir().degree(), 0)

    def test_dir(self):
        a = Vector2D(10, 0)
        b = Vector2D(0, 0)
        r = Ray2D(a, b)
        self.assertEqual(r.origin().x(), 10)
        self.assertEqual(r.dir().degree(), 180)

    def test_copy(self):
        a = Vector2D(0, 0)
        b = Vector2D(10, 0)
        r = Ray2D(a, b)
        r2 = r.copy()
        r2._origin.set_x(15)
        self.assertEqual(r.origin().x(), 0)

    def test_line(self):
        a = Vector2D(0, 0)
        b = Vector2D(10, 10)
        r = Ray2D(a, b)
        l = r.line()
        self.assertTrue(abs(l.b() + l.a()) < 0.1)
        self.assertEqual(l.c(), 0)

    def test_in_right_dir(self):
        self.fail()

    def test_intersection(self):
        a = Vector2D(-10, 0)
        b = Vector2D(0, 0)
        r1 = Ray2D(a, b)
        c = Vector2D(1, 10)
        d = Vector2D(1, 5)
        r2 = Ray2D(c, d)
        i = r1.intersection(r2)
        self.assertTrue(abs(i.x() - 1) < 0.001)
        self.assertTrue(abs(i.y()) < 0.001)
