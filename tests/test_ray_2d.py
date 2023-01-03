from unittest import TestCase
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.ray_2d import Ray2D


class TestRay2D(TestCase):
    def test_origin(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(10, 0)
        ray = Ray2D(point_0, point_1)
        self.assertEqual(ray.origin().x(), 0)
        self.assertEqual(ray.dir().degree(), 0)
        point_0.set_x(20)
        self.assertEqual(ray.origin().x(), 0)
        self.assertEqual(ray.dir().degree(), 0)

    def test_dir(self):
        point_0 = Vector2D(10, 0)
        point_1 = Vector2D(0, 0)
        ray_0 = Ray2D(point_0, point_1)
        self.assertEqual(ray_0.origin().x(), 10)
        self.assertEqual(ray_0.dir().degree(), 180)

    def test_copy(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(10, 0)
        ray_0 = Ray2D(point_0, point_1)
        ray_1 = ray_0.copy()
        ray_1.origin_().set_x(15)
        self.assertEqual(ray_0.origin().x(), 0)

    def test_line(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(10, 10)
        ray_0 = Ray2D(point_0, point_1)
        line = ray_0.line()
        self.assertTrue(abs(line.b() + line.a()) < 0.1)
        self.assertEqual(line.c(), 0)

    def test_in_right_dir(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(10, 10)
        point_2 = Vector2D(1, 10)
        point_3 = Vector2D(15,13)
        ray_0 = Ray2D(point_0, point_1)
        self.assertTrue(ray_0.in_right_dir(point_1))
        self.assertFalse(ray_0.in_right_dir(point_2))
        self.assertTrue(ray_0.in_right_dir(point_3))
        self.assertFalse(ray_0.in_right_dir(point_3,2.0))

    def test_intersection(self):
        point_0 = Vector2D(-10, 0)
        point_1 = Vector2D(0, 0)
        ray_0 = Ray2D(point_0, point_1)
        point_2 = Vector2D(1, 10)
        point_3 = Vector2D(1, 5)
        ray_1 = Ray2D(point_2, point_3)
        i = ray_0.intersection(ray_1)
        self.assertTrue(abs(i.x() - 1) < 0.001)
        self.assertTrue(abs(i.y()) < 0.001)
