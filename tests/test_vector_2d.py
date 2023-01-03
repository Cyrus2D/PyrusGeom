import unittest
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg


class Vector2DTest(unittest.TestCase):
    def test_general_test(self):
        a = Vector2D(1, 2)
        self.assertEqual(a.x(), 1)

    def test_constractor(self):
        a = Vector2D(1.1, 2.1)
        self.assertEqual(a.x(), 1.1)
        b = Vector2D(1, 1)
        c = Vector2D(b)
        self.assertEqual(c.x(), 1)

    def test_assign(self):
        a = Vector2D(1.1, 2.1)
        a.assign(1, 2)
        self.assertEqual(a.x(), 1)
        self.assertEqual(a.y(), 2)

    def test_set_functions(self):
        a = Vector2D(0, 0)
        a.set_x(1)
        self.assertEqual(a.x(), 1)
        a.set_y(2)
        self.assertEqual(a.y(), 2)
        a.set_x_y(3, 5)
        self.assertEqual(a.x(), 3)
        self.assertEqual(a.y(), 5)

        b = Vector2D(0, 0)
        b.set_polar(10, 45)
        self.assertTrue(7 <= b.x() <= 7.1)
        self.assertTrue(7 <= b.y() <= 7.1)
        b.set_polar(10, AngleDeg(45))
        self.assertTrue(7 <= b.x() <= 7.1)
        self.assertTrue(7 <= b.y() <= 7.1)
        b.set_polar(10, -45)
        self.assertTrue(7 <= b.x() <= 7.1)
        self.assertTrue(-7.1 <= b.y() <= -7)
        b.set_polar(10, AngleDeg(-135))
        self.assertTrue(-7.1 <= b.x() <= -7)
        self.assertTrue(-7.1 <= b.y() <= -7)
        b.set_polar(10, AngleDeg(225))
        self.assertTrue(-7.1 <= b.x() <= -7)
        self.assertTrue(-7.1 <= b.y() <= -7)
        b.set_polar(10, 225)
        self.assertTrue(-7.1 <= b.x() <= -7)
        self.assertTrue(-7.1 <= b.y() <= -7)
        b.set_polar(10, 360)
        self.assertTrue(9.9 <= b.x() <= 10.1)
        self.assertTrue(-0.1 <= b.y() <= 0.1)
        a = Vector2D(4, 4)
        a.set_dir(0)
        self.assertEqual(a.th().degree(), 0)
        self.assertTrue(5.6 < a.x() < 5.7)

    def test_th(self):
        a = Vector2D(10, 10)
        b = a.th()
        self.assertIsInstance(b, AngleDeg)
        c = b.degree()
        self.assertTrue(44 <= c <= 46)

    def test_add(self):
        a = Vector2D(0, 0)
        b = Vector2D(2, 4)
        a.add(b)
        self.assertEqual(a.x(), 2)
        self.assertEqual(a.y(), 4)
        a.add_x(1)
        a.add_y(2)
        self.assertEqual(a.x(), 3)
        self.assertEqual(a.y(), 6)

    def test_scale(self):
        a = Vector2D(2, 3)
        a.scale(2)
        self.assertEqual(a.x(), 4)
        self.assertEqual(a.y(), 6)

    def test_copy(self):
        a = Vector2D(0, 0)
        b = a.copy()
        b.set_x(10)
        self.assertFalse(a.x() == 10)

    def test_dist(self):
        a = Vector2D(10, 0)
        b = Vector2D(20, 0)
        self.assertEqual(a.dist(b), 10)

    def test_length(self):
        a = Vector2D(2, 0)
        a.set_length(8)
        self.assertEqual(a.x(), 8)
        self.assertEqual(a.y(), 0)
        a.normalize()
        self.assertEqual(a.x(), 1)
        self.assertEqual(a.y(), 0)

    def test_rotate(self):
        a = Vector2D(10, 0)
        a.rotate(90)
        self.assertEqual(a.y(), 10)
        self.assertTrue(-0.01 < a.x() < 0.01)
        a = Vector2D(10, 0)
        a.rotate(AngleDeg(90))
        self.assertEqual(a.y(), 10)
        self.assertTrue(-0.01 < a.x() < 0.01)

    def test_operation(self):
        a = Vector2D(1, 1)
        b = Vector2D(4, 4)
        c = a + b
        self.assertEqual(c.x(), 5)
        self.assertEqual(c.y(), 5)
        c = b - a
        self.assertEqual(c.x(), 3)
        self.assertEqual(c.y(), 3)
        c = b / 2
        self.assertEqual(c.x(), 2)
        self.assertEqual(c.y(), 2)
        c = b * 2
        self.assertEqual(c.x(), 8)
        self.assertEqual(c.y(), 8)
        b = Vector2D(4, 4)
        b *= 2
        self.assertEqual(b.x(), 8)
        self.assertEqual(b.y(), 8)
        self.assertEqual(c.x(), 8)
        self.assertEqual(c.y(), 8)
        b = Vector2D(4, 4)
        b /= 2
        self.assertEqual(b.x(), 2)
        self.assertEqual(b.y(), 2)
        b = Vector2D(4, 4)
        b += Vector2D(1, 1)
        self.assertEqual(b.x(), 5)
        self.assertEqual(b.y(), 5)
        b = Vector2D(4, 4)
        b -= Vector2D(1, 1)
        self.assertEqual(b.x(), 3)
        self.assertEqual(b.y(), 3)

    def test_static(self):
        a = Vector2D.polar2vector(3, 0)
        self.assertEqual(a.x(), 3)
        self.assertEqual(a.y(), 0)
        a = Vector2D.from_polar(3, 0)
        self.assertEqual(a.x(), 3)
        self.assertEqual(a.y(), 0)


    def test_kwargs(self):
        a = Vector2D(y=1, x=2)
        self.assertEqual(a.x(), 2)
        self.assertEqual(a.y(), 1)

    def test_kwargs_polar(self):
        a = Vector2D(r=3, a=0)
        self.assertEqual(a.x(), 3)
        self.assertEqual(a.y(), 0)
        self.assertEqual(a.th(), 0)
        self.assertEqual(a.r(), 3)
        a = Vector2D(r=10, a=45)
        self.assertEqual(a.th(), 45)
        self.assertEqual(a.r(), 10)

if __name__ == '__main__':
    unittest.main()
