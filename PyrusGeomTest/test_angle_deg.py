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

    def test_abs(self):
        a = AngleDeg(-20)
        self.assertEqual(a.abs(), 20)

    def test_radian(self):
        a = AngleDeg(30)
        self.assertAlmostEquals(a.radian(), 0.523599 , 6)

    def test_reverse(self):
        a = AngleDeg(-20)
        a.reverse()
        self.assertEqual(a.degree(), 160)
        self.assertEqual(a.degree(), 160)

    def test_reverse_angle(self):
        a = AngleDeg(-20)
        self.assertEqual(a.reverse_angle().degree(), 160)
        self.assertNotEqual(a.degree(), 160)

    def test_is_left_of(self):
        a = AngleDeg(20)
        b = AngleDeg(30)
        c = AngleDeg(30)
        d = AngleDeg(45)
        self.assertFalse(c.is_left_of(b))
        self.assertTrue(c.is_left_of(d))
        self.assertFalse(c.is_left_of(a))

    def test_is_right_of(self):
        a = AngleDeg(20)
        b = AngleDeg(30)
        c = AngleDeg(30)
        d = AngleDeg(45)
        self.assertFalse(c.is_right_of(b))
        self.assertFalse(c.is_right_of(d))
        self.assertTrue(c.is_right_of(a))
    
    def test_is_left_equal_of(self):
        a = AngleDeg(20)
        b = AngleDeg(30)
        c = AngleDeg(30)
        d = AngleDeg(45)
        self.assertTrue(c.is_left_equal_of(b))
        self.assertTrue(c.is_left_equal_of(d))
        self.assertFalse(c.is_left_equal_of(a))

    def test_is_right_equal_of(self):
        a = AngleDeg(20)
        b = AngleDeg(30)
        c = AngleDeg(30)
        d = AngleDeg(45)
        self.assertTrue(c.is_right_equal_of(b))
        self.assertFalse(c.is_right_equal_of(d))
        self.assertTrue(c.is_right_equal_of(a))
    def test_copy(self):
        a = AngleDeg(10)
        b = a.copy()
        b.set_degree(20)
        self.assertNotEqual(a.degree(), 20)

    def test_get_normalized(self):
        a = AngleDeg(90)
        self.assertEqual(a.get_normalized(), 0.75)

    def test_cos(self):
        a = AngleDeg(-30)
        b = AngleDeg(30)
        self.assertAlmostEquals(a.cos(), 0.8660254038)
        self.assertAlmostEquals(b.cos(), 0.8660254038)

    def test_sin(self):
        a = AngleDeg(-30)
        b = AngleDeg(30)
        self.assertAlmostEquals(a.sin(), -0.5)
        self.assertAlmostEquals(b.sin(), 0.5)


    def test_tan(self):
        a = AngleDeg(-30)
        b = AngleDeg(30)
        self.assertAlmostEquals(a.tan(), -0.5773502692)
        self.assertAlmostEquals(b.tan(),0.5773502692)

    def test_rad2deg(self):
        self.assertAlmostEquals(AngleDeg.rad2deg(0.52359877), 30 , 5)

    def test_deg2rad(self):
        self.assertAlmostEquals(AngleDeg.deg2rad(30), 0.523599 , 6)

    def test_cos_deg(self):
        self.assertAlmostEquals(AngleDeg.cos_deg(30), 0.8660254038)

    def test_sin_deg(self):
        self.assertAlmostEquals(AngleDeg.sin_deg(30), 0.5)

    def test_tan_deg(self):
        self.assertAlmostEquals(AngleDeg.tan_deg(30), 0.5773502692)

    def test_acos_deg(self):
        self.assertAlmostEquals(AngleDeg.acos_deg(0.8660254038), 30)

    def test_asin_deg(self):
        self.assertAlmostEquals(AngleDeg.asin_deg(0.5), 30)

    def test_atan_deg(self):
        self.assertAlmostEquals(AngleDeg.atan_deg(0.5773502692), 30)

    def test_atan2_deg(self):
        self.assertAlmostEquals(AngleDeg.atan2_deg(10,10), 45)

    def test_bisect(self):
        a = AngleDeg(30)
        b = AngleDeg(0)
        c = AngleDeg(15)
        self.assertEqual(AngleDeg.bisect(a,b), c)
