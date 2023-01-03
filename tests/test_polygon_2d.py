""" test_polygon_2d.py file
    to test pyrusgeom Polygon2D class
"""
from cmath import sqrt
from unittest import TestCase
from pyrusgeom.polygon_2d import Polygon2D
from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.rect_2d import Rect2D

class TestPolygon2D(TestCase):
    """Polygon2D class

    Args:
        TestCase (UnitTest): fail if any of tests falis
    """
    input_points_0 = [Vector2D(7, 7), Vector2D(7, -7), Vector2D(-7, -7), Vector2D(-7, 7),
                      Vector2D(9, 0), Vector2D(-9, 0), Vector2D(0, 9), Vector2D(0, -9)]
    input_points_1 = [Vector2D(0,0),Vector2D(0,3),Vector2D(4,0)]
    input_points_2 = [Vector2D(10, 10), Vector2D(0, 15) , Vector2D(-10, 10),
                      Vector2D(-10, -10), Vector2D(10, -10)]
    input_points_3 = [Vector2D(10, 10), Vector2D(-10, 10), Vector2D(-10, -10), Vector2D(10, -10)]

    def test_polygon_init_assign(self):
        plg_0 = Polygon2D()
        plg_1 = Polygon2D(self.input_points_0)
        plg_2 = Polygon2D()
        plg_2.assign(self.input_points_0)
        self.assertCountEqual(plg_0.vertices(),[Vector2D(0,0)])
        self.assertCountEqual(plg_1.vertices(),self.input_points_0)
        self.assertCountEqual(plg_2.vertices(),self.input_points_0)

    def test_add_vertex(self):
        plg_1 = Polygon2D(self.input_points_3)
        plg_1.add_vertex(Vector2D(0,15))
        self.assertCountEqual(plg_1.vertices(),self.input_points_2)

    def test_get_bounding_box(self):
        plg_0 = Polygon2D(self.input_points_0)
        rect_0 = plg_0.get_bounding_box()
        rect_ans = Rect2D(Vector2D(-9,-9),18,18)
        self.assertEqual(rect_0.top_right(),rect_ans.top_right())
        self.assertEqual(rect_0.bottom_left(),rect_ans.bottom_left())

    def test_bounding_box_center(self):
        plg_0 = Polygon2D(self.input_points_0)
        rect_0 = plg_0.bounding_box_center()
        rect_ans = Rect2D(Vector2D(-9,-9),18,18)
        self.assertEqual(rect_0,rect_ans.center())

    def test_contains(self):
        plg_0 = Polygon2D(self.input_points_2)
        alpha_point = Vector2D(14,-11)
        beta_point = Vector2D(0,0)
        gamma_point = Vector2D(5,14)
        delta_point = Vector2D(-10,10)
        self.assertFalse(plg_0.contains(alpha_point))
        self.assertTrue(plg_0.contains(beta_point))
        self.assertFalse(plg_0.contains(gamma_point))
        self.assertTrue(plg_0.contains(delta_point))
        self.assertFalse(plg_0.contains(delta_point,False))

    def test_dist(self):
        plg_0 = Polygon2D(self.input_points_2)
        alpha_point = Vector2D(0,-15)
        beta_point = Vector2D(0,0)
        gamma_point = Vector2D(-11,11)
        delta_point = Vector2D(10,15)
        self.assertEqual(plg_0.dist(alpha_point),5)
        self.assertEqual(plg_0.dist(beta_point),0)
        self.assertEqual(plg_0.dist(beta_point,False),10)
        self.assertEqual(plg_0.dist(gamma_point),sqrt(2))
        self.assertEqual(plg_0.dist(delta_point),50/sqrt(125))

    def test_double_signed_area(self):
        plg_0 = Polygon2D()
        plg_1 = Polygon2D(self.input_points_0)
        plg_2 = Polygon2D(self.input_points_1)
        plg_3 = Polygon2D(self.input_points_2)
        plg_4 = Polygon2D(self.input_points_3)

        self.assertEqual(plg_0.double_signed_area(),0)
        self.assertEqual(plg_1.double_signed_area(),-375)
        self.assertEqual(plg_2.double_signed_area(),-12)
        self.assertEqual(plg_3.double_signed_area(),900)
        self.assertEqual(plg_4.double_signed_area(),800)

    def test_get_rectangle_clipped_polygon(self):
        plg_3 = Polygon2D(self.input_points_2)
        ans_plg = [Vector2D(10, -10), Vector2D(10.0, -20.0),
                   Vector2D(-10.0, -20.0), Vector2D(-10, -10)]
        rect = Rect2D(Vector2D(-10, -20), 20, 20)
        plg_5 = plg_3.get_rectangle_clipped_polygon(rect)
        self.assertEqual(plg_5.vertices(),ans_plg)
