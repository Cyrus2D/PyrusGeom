""" test_angle_deg.py file
    to test pyrusgeom AngleDeg class
"""
from unittest import TestCase
from pyrusgeom.angle_deg import AngleDeg


class TestAngleDeg(TestCase):
    """TestAnlgeDeg class

    Args:
        TestCase (UnitTest): fail if any of tests falis
    """
    def test_degree(self):
        alpha_angle = AngleDeg()
        self.assertEqual(alpha_angle.degree(), 0)
        alpha_angle = AngleDeg(10)
        self.assertEqual(alpha_angle.degree(), 10)
        alpha_angle = AngleDeg(-90)
        self.assertEqual(alpha_angle.degree(), -90)
        alpha_angle = AngleDeg(360)
        self.assertEqual(alpha_angle.degree(), 0)
        alpha_angle = AngleDeg(-360)
        self.assertEqual(alpha_angle.degree(), 0)
        alpha_angle = AngleDeg(AngleDeg(10))
        self.assertEqual(alpha_angle.degree(), 10)
        alpha_angle = AngleDeg(af=-90)
        self.assertEqual(alpha_angle.degree(), -90)


    def test_set_degree(self):
        alpha_angle = AngleDeg(20)
        alpha_angle.set_degree(30)
        self.assertEqual(alpha_angle.degree(), 30)

    def test_set_angle(self):
        alpha_angle = AngleDeg(20)
        beta_angle = AngleDeg(30)
        alpha_angle.set_angle(beta_angle)
        self.assertEqual(alpha_angle.degree(), 30)
        beta_angle.set_degree(10)
        self.assertEqual(alpha_angle.degree(), 30)

    def test_is_within(self):
        alpha_angle = AngleDeg(30)
        beta_angle = AngleDeg(50)
        gamma_angle = AngleDeg(40)
        self.assertTrue(gamma_angle.is_within(alpha_angle, beta_angle))
        self.assertFalse(gamma_angle.is_within(beta_angle, alpha_angle))

    def test_abs(self):
        alpha_angle = AngleDeg(-20)
        self.assertEqual(alpha_angle.abs(), 20)

    def test_radian(self):
        alpha_angle = AngleDeg(30)
        self.assertAlmostEqual(alpha_angle.radian(), 0.523599 , 6)

    def test_reverse(self):
        alpha_angle = AngleDeg(-20)
        alpha_angle.reverse()
        self.assertEqual(alpha_angle.degree(), 160)
        self.assertEqual(alpha_angle.degree(), 160)

    def test_reverse_angle(self):
        alpha_angle = AngleDeg(-20)
        self.assertEqual(alpha_angle.reverse_angle().degree(), 160)
        self.assertNotEqual(alpha_angle.degree(), 160)

    def test_is_left_of(self):
        alpha_angle = AngleDeg(20)
        beta_angle = AngleDeg(30)
        gamma_angle = AngleDeg(30)
        delta = AngleDeg(45)
        self.assertFalse(gamma_angle.is_left_of(beta_angle))
        self.assertTrue(gamma_angle.is_left_of(delta))
        self.assertFalse(gamma_angle.is_left_of(alpha_angle))

    def test_is_right_of(self):
        alpha_angle = AngleDeg(20)
        beta_angle = AngleDeg(30)
        gamma_angle = AngleDeg(30)
        delta = AngleDeg(45)
        self.assertFalse(gamma_angle.is_right_of(beta_angle))
        self.assertFalse(gamma_angle.is_right_of(delta))
        self.assertTrue(gamma_angle.is_right_of(alpha_angle))

    def test_is_left_equal_of(self):
        alpha_angle = AngleDeg(20)
        beta_angle = AngleDeg(30)
        gamma_angle = AngleDeg(30)
        delta = AngleDeg(45)
        self.assertTrue(gamma_angle.is_left_equal_of(beta_angle))
        self.assertTrue(gamma_angle.is_left_equal_of(delta))
        self.assertFalse(gamma_angle.is_left_equal_of(alpha_angle))

    def test_is_right_equal_of(self):
        alpha_angle = AngleDeg(20)
        beta_angle = AngleDeg(30)
        gamma_angle = AngleDeg(30)
        delta = AngleDeg(45)
        self.assertTrue(gamma_angle.is_right_equal_of(beta_angle))
        self.assertFalse(gamma_angle.is_right_equal_of(delta))
        self.assertTrue(gamma_angle.is_right_equal_of(alpha_angle))
    def test_copy(self):
        alpha_angle = AngleDeg(10)
        beta_angle = alpha_angle.copy()
        beta_angle.set_degree(20)
        self.assertNotEqual(alpha_angle.degree(), 20)

    def test_get_normalized(self):
        alpha_angle = AngleDeg(90)
        self.assertEqual(alpha_angle.get_normalized(), 0.75)

    def test_cos(self):
        alpha_angle = AngleDeg(-30)
        beta_angle = AngleDeg(30)
        self.assertAlmostEqual(alpha_angle.cos(), 0.8660254038)
        self.assertAlmostEqual(beta_angle.cos(), 0.8660254038)

    def test_sin(self):
        alpha_angle = AngleDeg(-30)
        beta_angle = AngleDeg(30)
        self.assertAlmostEqual(alpha_angle.sin(), -0.5)
        self.assertAlmostEqual(beta_angle.sin(), 0.5)


    def test_tan(self):
        alpha_angle = AngleDeg(-30)
        beta_angle = AngleDeg(30)
        self.assertAlmostEqual(alpha_angle.tan(), -0.5773502692)
        self.assertAlmostEqual(beta_angle.tan(),0.5773502692)

    def test_rad2deg(self):
        self.assertAlmostEqual(AngleDeg.rad2deg(0.52359877), 30 , 5)

    def test_deg2rad(self):
        self.assertAlmostEqual(AngleDeg.deg2rad(30), 0.523599 , 6)

    def test_cos_deg(self):
        self.assertAlmostEqual(AngleDeg.cos_deg(30), 0.8660254038)

    def test_sin_deg(self):
        self.assertAlmostEqual(AngleDeg.sin_deg(30), 0.5)

    def test_tan_deg(self):
        self.assertAlmostEqual(AngleDeg.tan_deg(30), 0.5773502692)

    def test_acos_deg(self):
        self.assertAlmostEqual(AngleDeg.acos_deg(0.8660254038), 30)

    def test_asin_deg(self):
        self.assertAlmostEqual(AngleDeg.asin_deg(0.5), 30)

    def test_atan_deg(self):
        self.assertAlmostEqual(AngleDeg.atan_deg(0.5773502692), 30)

    def test_atan2_deg(self):
        self.assertAlmostEqual(AngleDeg.atan2_deg(10,10), 45)

    def test_bisect(self):
        alpha_angle = AngleDeg(30)
        beta_angle = AngleDeg(0)
        gamma_angle = AngleDeg(15)
        self.assertEqual(AngleDeg.bisect(alpha_angle,beta_angle), gamma_angle)
