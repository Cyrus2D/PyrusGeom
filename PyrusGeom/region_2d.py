"""
  file region_2d.h
  brief abstract 2D region class File.
"""
from PyrusGeom.vector_2d import Vector2D


class Region2D:
    def __init__(self):
        """
        brief accessible only from derived classes
        """
        pass

    def area(self):
        """
        brief get the area of this region
        return value of the area
        """
        pass

    def contains(self, point: Vector2D):
        """
        brief check if this region contains 'point'.
        param point considered point
        return true or false
        """
        pass
