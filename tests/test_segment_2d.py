from unittest import TestCase
from PyrusGeom.segment_2d import Segment2D
from PyrusGeom.vector_2d import Vector2D


class TestSegment2D(TestCase):
    def test_general(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(10, 2)
        seg_0 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.origin().x(), 0)
        self.assertEqual(seg_0.origin().y(), 1)
        self.assertEqual(seg_0.terminal().x(), 10)
        self.assertEqual(seg_0.terminal().y(), 2)
        seg_0 = Segment2D(0, 1, 10, 2)
        self.assertEqual(seg_0.origin().x(), 0)
        self.assertEqual(seg_0.origin().y(), 1)
        self.assertEqual(seg_0.terminal().x(), 10)
        self.assertEqual(seg_0.terminal().y(), 2)
        seg_0 = Segment2D(point_0, 10, 0)
        self.assertEqual(seg_0.origin().x(), 0)
        self.assertEqual(seg_0.origin().y(), 1)
        self.assertEqual(seg_0.terminal().x(), 10)
        self.assertEqual(seg_0.terminal().y(), 1)

    def test_assign(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(10, 2)
        seg_0 = Segment2D()
        seg_0.assign(point_0, point_1)
        self.assertEqual(seg_0.origin().x(), 0)
        self.assertEqual(seg_0.origin().y(), 1)
        self.assertEqual(seg_0.terminal().x(), 10)
        self.assertEqual(seg_0.terminal().y(), 2)
        seg_0 = Segment2D()
        seg_0.assign(point_0, point_1)
        self.assertEqual(seg_0.origin().x(), 0)
        self.assertEqual(seg_0.origin().y(), 1)
        self.assertEqual(seg_0.terminal().x(), 10)
        self.assertEqual(seg_0.terminal().y(), 2)
        seg_0 = Segment2D(point_0, 10, 0)
        seg_0.assign(point_0, point_1)
        self.assertEqual(seg_0.origin().x(), 0)
        self.assertEqual(seg_0.origin().y(), 1)
        self.assertEqual(seg_0.terminal().x(), 10)
        self.assertEqual(seg_0.terminal().y(), 2)

    def test_is_valid(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, 1)
        seg_0 = Segment2D(point_0, point_1)
        self.assertFalse(seg_0.is_valid())

    def test_line(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(10, 10)
        seg_0 = Segment2D(point_0, point_1)
        line = seg_0.line()
        self.assertEqual(abs(line.a() + line.b()) ,0)

    def test_length(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.length(), 9)

    def test_direction(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.direction().degree(), 90)
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, -10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.direction().degree(), -90)

    def test_swap(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1).swap()
        self.assertEqual(seg_0.direction().degree(), -90)
        self.assertEqual(seg_0.origin().y(), 10)

    def test_reverse(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1).reverse()
        self.assertEqual(seg_0.direction().degree(), -90)
        self.assertEqual(seg_0.origin().y(), 10)

    def test_reversed_segment(self):
        point_0 = Vector2D(0, 1)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = seg_0.reversed_segment()
        self.assertEqual(seg_1.direction().degree(), -90)
        self.assertEqual(seg_1.origin().y(), 10)
        seg_0.assign(Vector2D(2, 2), Vector2D(5, 5))
        self.assertEqual(seg_1.direction().degree(), -90)
        self.assertEqual(seg_1.origin().y(), 10)

    def test_perpendicular_bisector(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        p_line = seg_0.perpendicular_bisector()
        self.assertEqual(p_line.get_y(0), 5)

    def test_contains(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.contains(Vector2D(0, 5)))
        self.assertFalse(seg_0.contains(Vector2D(-1, 5)))
        self.assertFalse(seg_0.contains(Vector2D(0, 11)))

    def test_equals(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = Segment2D(point_0, point_1)
        seg_2 = Segment2D(Vector2D(0, 1), point_1)
        self.assertTrue(seg_0 == seg_1)
        self.assertFalse(seg_0 == seg_2)

    def test_equals_weakly(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = Segment2D(Vector2D(0.000000001, 0), point_1)
        self.assertTrue(seg_0.equals_weakly(seg_1))

    def test_projection(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point = seg_0.projection(Vector2D(1, 5))
        self.assertEqual(point.x(), 0)
        self.assertEqual(point.y(), 5)
        point = seg_0.projection(Vector2D(0, 11))
        self.assertFalse(point.is_valid())
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 0)
        seg_0 = Segment2D(point_0, point_1)
        point = seg_0.projection(Vector2D(1, 5))
        self.assertEqual(point.x(), 0)
        self.assertEqual(point.y(), 0)

    def test_intersection(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        seg_1 = Segment2D(point_0, point_1)
        point_i = seg_0.intersection(seg_1)
        self.assertEqual(point_i.x(), 0)
        self.assertEqual(point_i.y(), 1)
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = Segment2D(point_1, point_0)
        point_i = seg_0.intersection(seg_1.line())
        self.assertEqual(point_i.x(), 0)
        self.assertEqual(point_i.y(), 0)
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 12)
        point_1 = Vector2D(-10, 12)
        seg_1 = Segment2D(point_0, point_1)
        point_i = seg_0.intersection(seg_1)
        self.assertEqual(point_i.is_valid(), False)
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = Segment2D(point_0, point_1)
        point_i = seg_0.intersection(seg_1.line())
        self.assertEqual(point_i.is_valid(), False)

    def test_exist_intersection(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.exist_intersection(seg_1))
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.exist_intersection(seg_1))
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 12)
        point_1 = Vector2D(-10, 12)
        seg_1 = Segment2D(point_0, point_1)
        self.assertFalse(seg_0.exist_intersection(seg_1))
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.exist_intersection(seg_1))

    def test_check_intersects_on_line(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.check_intersects_on_line(point_0))
        self.assertTrue(seg_0.check_intersects_on_line(Vector2D(4,5)))
        self.assertTrue(seg_1.check_intersects_on_line(point_1))
        self.assertFalse(seg_1.check_intersects_on_line(Vector2D(20,13)))

    def test_exist_intersection_except_endpoint(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.exist_intersection_except_endpoint(seg_1))
        point_0 = Vector2D(10, 10)
        point_1 = Vector2D(-10, 10)
        seg_1 = Segment2D(point_0, point_1)
        self.assertFalse(seg_0.exist_intersection_except_endpoint(seg_1))

    def test_intersects_except_endpoint(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.intersects_except_endpoint(seg_1))
        point_0 = Vector2D(10, 10)
        point_1 = Vector2D(-10, 10)
        seg_1 = Segment2D(point_0, point_1)
        self.assertFalse(seg_0.intersects_except_endpoint(seg_1))

    def test_nearest_point(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point = seg_0.nearest_point(Vector2D(5, 12))
        self.assertEqual(point.x(), 0)
        self.assertEqual(point.y(), 10)
        point = seg_0.nearest_point(Vector2D(-5, -5))
        self.assertEqual(point.x(), 0)
        self.assertEqual(point.y(), 0)
        point = seg_0.nearest_point(Vector2D(3, 3))
        self.assertEqual(point.x(), 0)
        self.assertEqual(point.y(), 3)

    def test_dist(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.dist(seg_1), 0)
        point_0 = Vector2D(10, -1)
        point_1 = Vector2D(-10, -1)
        seg_1 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.dist(seg_1), 1)
        point_0 = Vector2D(1, 0)
        point_1 = Vector2D(1, 10)
        seg_1 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.dist(seg_1), 1)
        self.assertEqual(seg_0.dist(Vector2D(0, 5)), 0)
        self.assertEqual(seg_0.dist(Vector2D(0, 11)), 1)
        self.assertEqual(seg_0.dist(Vector2D(1, 5)), 1)

    def test_farthest_dist(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertEqual(seg_0.farthest_dist(Vector2D(0, -1)), 11)

    def test_on_segment(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.on_segment(point_0))
        self.assertTrue(seg_0.on_segment(Vector2D(0,5)))
        self.assertFalse(seg_0.on_segment(Vector2D(1,5)))
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        self.assertFalse(seg_0.on_segment(point_0))
        self.assertFalse(seg_0.on_segment(point_1))

    def test_on_segment_weakly(self):
        point_0 = Vector2D(0, 0)
        point_1 = Vector2D(0, 10)
        seg_0 = Segment2D(point_0, point_1)
        self.assertTrue(seg_0.on_segment_weakly(point_0))
        self.assertTrue(seg_0.on_segment_weakly(Vector2D(0.0000001,5.0000001)))
        self.assertFalse(seg_0.on_segment_weakly(Vector2D(0.000001,5.000001)))
        point_0 = Vector2D(10, 1)
        point_1 = Vector2D(-10, 1)
        self.assertFalse(seg_0.on_segment_weakly(point_0))
        self.assertFalse(seg_0.on_segment_weakly(point_1))