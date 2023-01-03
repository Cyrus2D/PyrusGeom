""" region_2d.py file
    Region2D: class name
    Father Class
"""
from pyrusgeom.vector_2d import Vector2D

class Region2D:
    """ handling Regions in SS2D
        father class for other classes
    """
    def __init__(self):
        """accessible only from derived classes
        """

    def area(self) -> float:
        """get the area of this region

        Returns:
            float: value of the area
        """

    def contains(self, point: Vector2D) -> bool:
        """check if this region contains 'point'.

        Args:
            point (Vector2D): considered point

        Returns:
            bool: true or false
        """
