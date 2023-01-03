""" test_convex_hull.py file
    to test pyrusgeom ConvexHull class
"""
from unittest import TestCase
from pyrusgeom.convex_hull import ConvexHull, MethodType, Polygon2D , \
    list2set, angle_sort_predicate, is_clockwise

from pyrusgeom.vector_2d import Vector2D


class TestConvexHull(TestCase):
    """TestConvexHull class

    Args:
        TestCase (UnitTest): fail if any of tests falis
    """
    input_points_0 = [Vector2D(7, 7), Vector2D(7, -7), Vector2D(-7, -7), Vector2D(-7, 7),
                      Vector2D(9, 0), Vector2D(-9, 0), Vector2D(0, 9), Vector2D(0, -9)]
    input_points_1 = [Vector2D(7, 7), Vector2D(7, -7), Vector2D(-7, -7), Vector2D(-7, 7),
                      Vector2D(9, 0), Vector2D(-9, 0), Vector2D(0, 9), Vector2D(0, -9),
                      Vector2D(1, 2), Vector2D(-2, 1), Vector2D(-1, -1), Vector2D(3, 4),
                      Vector2D(4, 3), Vector2D(-5, 4), Vector2D(6, 5)]
    input_points_2 = [Vector2D(0.02402358131857918, -0.2356728797179394),
                      Vector2D(0.3215348546593775, 0.03629583077160248),
                      Vector2D(0.04590851212470659, -0.4156409924995536),
                      Vector2D(0.3218384001607433, 0.1379850698988746),
                      Vector2D(0.11506479756447, -0.1059521474930943),
                      Vector2D(0.2622539999543261, -0.29702873322836),
                      Vector2D(-0.161920957418085, -0.405533971642641),
                      Vector2D(0.1905378631228002, 0.3698601009043493),
                      Vector2D(0.2387090918968516, -0.01629827079949742),
                      Vector2D(0.07495888748668034, -0.1659825110491202),
                      Vector2D(0.3319341836794598, -0.1821814101954749),
                      Vector2D(0.07703635755650362, -0.2499430638271785),
                      Vector2D(0.2069242999022122, -0.2232970760420869),
                      Vector2D(0.04604079532068295, -0.1923573186549892),
                      Vector2D(0.05054295812784038, 0.4754929463150845),
                      Vector2D(-0.3900589168910486, 0.2797829520700341),
                      Vector2D(0.3120693385713448, -0.0506329867529059),
                      Vector2D(0.01138812723698857, 0.4002504701728471),
                      Vector2D(0.009645149586391732, 0.1060251100976254),
                      Vector2D(-0.03597933197019559, 0.2953639456959105),
                      Vector2D(0.1818290866742182, 0.001454397571696298),
                      Vector2D(0.444056063372694, 0.2502497166863175),
                      Vector2D(-0.05301752458607545, -0.06553921621808712),
                      Vector2D(0.4823896228171788, -0.4776170002088109),
                      Vector2D(-0.3089226845734964, -0.06356112199235814),
                      Vector2D(-0.271780741188471, 0.1810810595574612),
                      Vector2D(0.4293626522918815, 0.2980897964891882),
                      Vector2D(-0.004796652127799228, 0.382663812844701),
                      Vector2D(0.430695573269106, -0.2995073500084759),
                      Vector2D(0.1799668387323309, -0.2973467472915973),
                      Vector2D(0.4932166845474547, 0.4928094162538735),
                      Vector2D(-0.3521487911717489, 0.4352656197131292),
                      Vector2D(-0.4907368011686362, 0.1865826865533206),
                      Vector2D(-0.1047924716070224, -0.247073392148198),
                      Vector2D(0.4374961861758457, -0.001606279519951237),
                      Vector2D(0.003256207800708899, -0.2729194320486108),
                      Vector2D(0.04310378203457577, 0.4452604050238248),
                      Vector2D(0.4916198379282093, -0.345391701297268),
                      Vector2D(0.001675087028811806, 0.1531837672490476),
                      Vector2D(-0.4404289572876217, -0.2894855991839297)]
    convext_hull_points_01 = [Vector2D(-9, 0), Vector2D(-7, -7), Vector2D(0, -9), Vector2D(7, -7),
                              Vector2D(9, 0), Vector2D(7, 7), Vector2D(0, 9), Vector2D(-7, 7)]
    convext_hull_points_2 = [Vector2D(-0.161920957418085, -0.405533971642641),
                             Vector2D(0.05054295812784038, 0.4754929463150845),
                             Vector2D(0.4823896228171788, -0.4776170002088109),
                             Vector2D(0.4932166845474547, 0.4928094162538735),
                             Vector2D(-0.3521487911717489, 0.4352656197131292),
                             Vector2D(-0.4907368011686362, 0.1865826865533206),
                             Vector2D(0.4916198379282093, -0.345391701297268),
                             Vector2D(-0.4404289572876217, -0.2894855991839297)]

    def test_list2set(self):
        list_test = [-1.5, 1, 2, 0, 0, 0, 2]
        set_test = [-1.5, 1, 2, 0]
        self.assertEqual(list2set(list_test), set_test)

    def test_angle_sort_predicate(self):
        alpha_point = Vector2D(20, 10)
        beta_point = Vector2D(-10, 20)
        gamma_point = Vector2D(20, 20)
        self.assertEqual(angle_sort_predicate(alpha_point, beta_point), 1)
        self.assertEqual(angle_sort_predicate(
            alpha_point, beta_point, gamma_point), -1)

    def test_is_clockwise(self):
        alpha_point = Vector2D(20, 10)
        beta_point = Vector2D(-10, 20)
        gamma_point = Vector2D(20, 20)
        self.assertEqual(is_clockwise(
            Vector2D(0, 0), alpha_point, beta_point), False)
        self.assertEqual(is_clockwise(
            alpha_point, beta_point, gamma_point), True)

    def test_convex_hull_wrapping(self):
        convex_hull_test = ConvexHull(self.input_points_0)
        convex_hull_test.compute(MethodType.WRAPPING_METHOD)

        self.assertEqual(convex_hull_test.vertices(),
                              self.convext_hull_points_01)

        convex_hull_test = ConvexHull(self.input_points_1)
        convex_hull_test.compute(MethodType.WRAPPING_METHOD)

        self.assertCountEqual(convex_hull_test.vertices(),
                              self.convext_hull_points_01)

        convex_hull_test = ConvexHull(self.input_points_2)
        convex_hull_test.compute(MethodType.WRAPPING_METHOD)

        self.assertCountEqual(convex_hull_test.vertices(),
                              self.convext_hull_points_2)

    def test_convex_hull_grahan_scan(self):
        convex_hull_test = ConvexHull(self.input_points_0)
        convex_hull_test.compute(MethodType.GRAHAN_SCAN)

        self.assertCountEqual(convex_hull_test.vertices(),
                              self.convext_hull_points_01)

        convex_hull_test = ConvexHull(self.input_points_1)
        convex_hull_test.compute(MethodType.GRAHAN_SCAN)

        self.assertCountEqual(convex_hull_test.vertices(),
                              self.convext_hull_points_01)

        # convex_hull_test = ConvexHull(self.input_points_2)
        # convex_hull_test.compute(MethodType.GRAHAN_SCAN)

        # self.assertCountEqual(convex_hull_test.vertices(),
        #                       self.convext_hull_points_2)

    def test_to_polgon(self):
        convex_hull_test = ConvexHull(self.input_points_0)
        convex_hull_test.compute(MethodType.WRAPPING_METHOD)
        plg_test = Polygon2D(self.convext_hull_points_01)
        plg = convex_hull_test.to_polygon()
        self.assertEqual(plg.vertices(),plg_test.vertices())
            