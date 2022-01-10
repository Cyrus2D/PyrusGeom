from unittest import TestCase
from PyrusGeom.circle_2d import Circle2D
from PyrusGeom.vector_2d import Vector2D


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
        self.fail()

    def test_circum_circle(self):
        self.fail()

    def test_circle_contains(self):
        self.fail()
