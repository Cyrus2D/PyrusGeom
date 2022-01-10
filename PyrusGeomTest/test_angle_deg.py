from unittest import TestCase
from PyrusGeom.angle_deg import AngleDeg


class TestAngleDeg(TestCase):
    def test_degree(self):
        a = AngleDeg()
        self.assertEqual(a.degree(), 0)
        a = AngleDeg(10)
        self.assertEqual(a.degree(), 10)
        a = AngleDeg(-90)
        self.assertEqual(a.degree(), -90)
        a = AngleDeg(360)
        self.assertEqual(a.degree(), 0)
        a = AngleDeg(-360)
        self.assertEqual(a.degree(), 0)

    def test_set_degree(self):
        a = AngleDeg(20)
        a.set_degree(30)
        self.assertEqual(a.degree(), 30)

    def test_set_angle(self):
        a = AngleDeg(20)
        b = AngleDeg(30)
        a.set_angle(b)
        self.assertEqual(a.degree(), 30)
        b.set_degree(10)
        self.assertEqual(a.degree(), 30)

    def test_is_within(self):
        a = AngleDeg(30)
        b = AngleDeg(50)
        c = AngleDeg(40)
        self.assertTrue(c.is_within(a, b))
        self.assertFalse(c.is_within(b, a))

    def test_is_left_equal_of(self):
        a = AngleDeg(20)
        b = AngleDeg(30)
        self.fail()

    def test_abs(self):
        a = AngleDeg(-20)
        self.assertEqual(a.abs(), 20)

    def test_radian(self):
        self.fail()

    def test_reverse(self):
        a = AngleDeg(-20)
        self.assertEqual(a.reverse().degree(), 160)
        self.assertEqual(a.degree(), 160)

    def test_reverse_angle(self):
        a = AngleDeg(-20)
        self.assertEqual(a.reverse_angle().degree(), 160)
        self.assertNotEqual(a.degree(), 160)

    def test_is_left_of(self):
        self.fail()

    def test_is_right_of(self):
        self.fail()

    def test_copy(self):
        a = AngleDeg(10)
        b = a.copy()
        b.set_degree(20)
        self.assertNotEqual(a.degree(), 20)

    def test_get_normalized(self):
        a = AngleDeg(90)
        self.assertEqual(a.get_normalized(), 0.75)

    def test_cos(self):
        self.fail()

    def test_sin(self):
        self.fail()

    def test_tan(self):
        self.fail()

    def test_rad2deg(self):
        self.fail()

    def test_deg2rad(self):
        self.fail()

    def test_cos_deg(self):
        self.fail()

    def test_sin_deg(self):
        self.fail()

    def test_tan_deg(self):
        self.fail()

    def test_acos_deg(self):
        self.fail()

    def test_asin_deg(self):
        self.fail()

    def test_atan_deg(self):
        self.fail()

    def test_atan2_deg(self):
        self.fail()

    def test_bisect(self):
        self.fail()
