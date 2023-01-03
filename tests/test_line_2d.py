from unittest import TestCase
from pyrusgeom.line_2d import Line2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg


class TestLine2D(TestCase):
    def test_general(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        self.assertEqual(line.a(), -10)
        self.assertEqual(line.b(), 0)
        self.assertEqual(line.c(), 0)

        line = Line2D(Vector2D(0, 0), 90)
        self.assertEqual(line.a(), -1)
        self.assertTrue(abs(line.b()) < 0.01)
        self.assertEqual(line.c(), 0)

    def test_get_x(self):
        line = Line2D(Vector2D(0, 0), Vector2D(10, 10))
        self.assertEqual(line.get_x(5), 5)

    def test_get_y(self):
        line = Line2D(Vector2D(0, 0), Vector2D(10, 10))
        self.assertEqual(line.get_y(5), 5)

    def test_copy(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        l2 = line.copy()
        self.assertEqual(l2.a(), -10)
        self.assertEqual(l2.b(), 0)
        self.assertEqual(l2.c(), 0)

    def test_dist(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        self.assertEqual(line.dist(Vector2D(0, -1)), 0)
        self.assertEqual(line.dist(Vector2D(2, 2)), 2)

    def test_dist2(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        self.assertEqual(line.dist2(Vector2D(0, -1)), 0)
        self.assertEqual(line.dist2(Vector2D(2, 2)), 4)

    def test_is_parallel(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        l2 = Line2D(Vector2D(1, 0), Vector2D(1, -10))
        self.assertTrue(line.is_parallel(l2))

    def test_intersection(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        l2 = Line2D(Vector2D(1, 0), Vector2D(1, -10))
        self.assertFalse(line.intersection(l2).is_valid())
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        l2 = Line2D(Vector2D(1, 1), Vector2D(-1, 1))
        self.assertTrue(line.intersection(l2).x() == 0)
        self.assertTrue(line.intersection(l2).y() == 1)

    def test_perpendicular(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        p = Vector2D(5, 5)
        per = line.perpendicular(p)
        self.assertEqual(per.get_y(2), 5)

    def test_projection(self):
        line = Line2D(Vector2D(0, 0), Vector2D(0, 10))
        p = Vector2D(5, 5)
        pro = line.projection(p)
        self.assertEqual(pro.x(), 0)
        self.assertEqual(pro.y(), 5)

    def test_line_intersection(self):
        pass

    def test_angle_bisector(self):
        line = Line2D.angle_bisector(Vector2D(1, 1), 0, 90)
        self.assertTrue(abs(line.get_x(5) - 5) < 0.01)

    def test_perpendicular_bisector(self):
        line = Line2D.perpendicular_bisector(Vector2D(-5, 0), Vector2D(5, 0))
        self.assertEqual(line.get_x(5), 0)

    def test_kwargs(self):
        line = Line2D(p1=Vector2D(0, 0), p2=Vector2D(0, 10))
        self.assertEqual(line.a(), -10)
        self.assertEqual(line.b(), 0)
        self.assertEqual(line.c(), 0)

        line = Line2D(p=Vector2D(0, 0), a=90)
        self.assertEqual(line.a(), -1)
        self.assertTrue(abs(line.b()) < 0.01)
        self.assertEqual(line.c(), 0)

        line2 = Line2D(line)

        self.assertEqual(line2.a(), -1)
        self.assertTrue(abs(line2.b()) < 0.01)
        self.assertEqual(line2.c(), 0)

        line = Line2D(p=Vector2D(0, 0), a=AngleDeg(90))
        self.assertEqual(line.a(), -1)
        self.assertTrue(abs(line.b()) < 0.01)
        self.assertEqual(line.c(), 0)
