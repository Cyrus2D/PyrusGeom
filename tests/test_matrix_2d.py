""" test_matrix_2d.py file
    to test pyrusgeom Matrix2D class
"""
from unittest import TestCase
from pyrusgeom.matrix_2d import Matrix2D
from pyrusgeom.matrix_2d import Vector2D


class TestMatrix2D(TestCase):
    """TestMatrix2D class

    Args:
        TestCase (UnitTest): fail if any of tests falis
    """

    def test_matrix_init_assign_reset(self):
        mat_0 = Matrix2D()
        mat_1 = Matrix2D(1, 0, 0, 1, 0, 0)
        mat_2 = Matrix2D(1, 1, 1, 1, 1, 1)
        self.assertEqual(mat_0, mat_1)
        self.assertNotEqual(mat_0, mat_2)
        mat_2.reset()
        self.assertEqual(mat_0, mat_2)

    def test_det_invertible(self):
        mat_0 = Matrix2D()
        mat_1 = Matrix2D(2, 0, 2, 2, 2, 1)
        mat_2 = Matrix2D(5, 4, 5, 4, 0, 0)
        self.assertEqual(mat_0.det(), 1)
        self.assertEqual(mat_1.det(), 4)
        self.assertEqual(mat_2.det(), 0)
        self.assertTrue(mat_0.invertible())
        self.assertTrue(mat_1.invertible())
        self.assertFalse(mat_2.invertible())

    def test_inverted(self):
        mat_0 = Matrix2D()
        mat_1 = Matrix2D(2.0, 0.0, 2.0, 2.0, 2.0, 1.0)
        mat_2 = Matrix2D(5, 4, 5, 4, 0, 0)
        self.assertEqual(mat_0.inverted(), mat_0)
        self.assertTrue(mat_1.inverted(), Matrix2D(0.5, 0.0, -0.5, 0.5, -1.0, 0.5))
        self.assertEqual(mat_2.inverted(), Matrix2D(1.0, 0.0, 0.0, 1.0, 0.0, 0.0))

    def test_tranform(self):
        mat_0 = Matrix2D()
        mat_1 = Matrix2D(2.0, 0.0, 2.0, 2.0, 2.0, 1.0)
        vec_1 = Vector2D(10,10)
        self.assertEqual(mat_0.transform(vec_1),vec_1)
        self.assertEqual(mat_1.transform(vec_1),Vector2D(22,41))

    def test_mul(self):
        mat_0 = Matrix2D()
        mat_1 = mat_0 * mat_0
        # mat_1 = Matrix2D(2.0, 0.0, 2.0, 2.0, 2.0, 1.0)
        self.assertEqual(mat_1, Matrix2D())
