""" file matrix_2d.py
    Matrix2D: class name
"""

from __future__ import annotations
from typing import Union
import math
from pyrusgeom.math_values import EPSILON

from pyrusgeom.vector_2d import Vector2D
from pyrusgeom.angle_deg import AngleDeg


class Matrix2D:
    """ 2D transform matrix class File.

        ( m11, m12, dxtf )
        ( m21, m22, dytf )
        (   0,   0,  1 )

    Attributes:
        self.11 element (1,1): the horizontal scaling factor.
        self.12 element (1,2): the vertical shearing factor.
        self.21 element (2,1): the horizontal shearing factor.
        self.22 element (2,2): the vertical scaling factor.
        self.dxtf dxtf: the horizontal translation factor.
        self.dytf dytf: the vertical translation factor.

    """
    _m11:float
    _m12:float
    _dx:float
    _m21:float
    _m22:float
    _dy:float


    def __init__(self, __11=1.0, __12=0.0, __21=0.0, __22=1.0, __x=0.0, __y=0.0):
        """This is the class init function and creates a matrix2d

        Defualt:
            create a matrix with all the given elements
        OR
            create an identity matrix
        Args:
            __11 (float, optional): the horizontal scaling factor. Defaults to 1.0.
            __12 (float, optional): the vertical shearing factor. Defaults to 0.0.
            __21 (float, optional): the horizontal shearing factor. Defaults to 0.0.
            __22 (float, optional): the vertical scaling factor. Defaults to 1.0.
            __x (float, optional): the horizontal translation factor. Defaults to 0.0.
            __y (float, optional): the vertical translation factor. Defaults to 0.0.
        """
        self._m11 = __11
        self._m12 = __12
        self._m21 = __21
        self._m22 = __22
        self._dx = __x
        self._dy = __y
        self.is_valid = True

    def reset(self):
        """ reset this matrix to the identity matrix
        """
        self._m11 = self._m22 = 1.0
        self._m12 = self._m21 = self._dx = self._dy = 0.0

    def assign(self, __11: float, __12: float, __21: float, __22: float, __x: float, __y: float):
        """set this matrix elements with the given specified values.

        Args:
            __11 (float): the horizontal scaling factor.
            __12 (float): the vertical shearing factor.
            __21 (float): the horizontal shearing factor.
            __22 (float): the vertical scaling factor.
            __x (float): the horizontal translation factor.
            __y (float): the vertical translation factor.
        """
        self._m11 = __11
        self._m12 = __12
        self._m21 = __21
        self._m22 = __22
        self._dx = __x
        self._dy = __y

    def m11(self) -> float:
        """get the horizontal scaling factor.

        Returns:
            float: the horizontal scaling factor value.
        """
        return self._m11

    def m12(self) -> float:
        """get the vertical shearing factor.

        Returns:
            float: return the vertical shearing factor value.
        """
        return self._m12

    def m21(self) -> float:
        """get the horizontal shearing factor.

        Returns:
            float: the horizontal shearing factor value.
        """
        return self._m21

    def m22(self) -> float:
        """get the vertical scaling factor.

        Returns:
            float: the vertical scaling factor value.
        """
        return self._m22

    def dxtf(self) -> float:
        """get the horizontal translation factor.

        Returns:
            float: the horizontal translation factor value.
        """
        return self._dx

    def dytf(self) -> float:
        """get the vertical translation factor.

        Returns:
            float: the vertical translation factor value.
        """
        return self._dy

    # def __members(self):
    #     """get the matrix members

    #     Returns:
    #         object: (m11,m12,dx,m21,m22,dy)
    #     """
    #     return (self.m11(),self.m12(),self.dxtf(),self.m21(),self.m22(),self.dytf)

    def det(self) -> float:
        """get the matrix's determinant

        Returns:
            float: the determinant value.
        """
        return self._m11 * self._m22 - self._m12 * self._m21

    def invertible(self) -> bool:
        """check if this matrix is invertible (is not insular).

        Returns:
            bool: true if this matrix is invertible.else false.
        """
        return math.fabs(self.det()) > EPSILON

    def inverted(self) -> Matrix2D:
        """get the inverted matrix.

        if the matrix isn't invertible return the defualt Matrix

        Returns:
            Matrix2D: if invertible return the inverted matrix object.
        """
        determinant = self.det()
        if determinant == 0.0:  # not invertible
            return Matrix2D()  # default matrix

        dinv = 1.0 / determinant
        return Matrix2D(self._m22 * dinv, -self._m12 * dinv,
                        -self._m21 * dinv, self._m11 * dinv,
                        (self._m12 * self._dy - self._dx * self._m22) * dinv,
                        (self._dx * self._m21 - self._m11 * self._dy) * dinv)

    def translate(self, dxtf: float, dytf: float):
        """moves the coordinate as the other matrix.

        SameAs:
            self = Matrix2D.make_translation(dxtf,dytf) * self

        Args:
            dxtf (float): move factor for the x axis.
            dytf (float): move factor for the y axis.
        """
        self._dx += dxtf
        self._dy += dytf

    def scale(self, scale_x: float, scale_y: float):
        """scales the coordinate.

        SameAs:
            self = Matrix2D.make_scaling(scale_x,scale_y) * self

        Args:
            scale_x (float): scaling factor for the x axis.
            scale_y (float): scaling factor for the y axis.
        """
        self._m11 *= scale_x
        self._m12 *= scale_x
        self._dx *= scale_x
        self._m21 *= scale_y
        self._m22 *= scale_y
        self._dy *= scale_y

    def rotate(self, angle: AngleDeg):
        """rotates the coordinate system

        SameAs:
            self = Matrix2D.make_rotation(angle) * self

        Args:
            angle (AngleDeg): rotation angle
        """
        ang_sin = angle.sin()
        ang_cos = angle.cos()
        tm11 = self._m11 * ang_cos - self._m21 * ang_sin
        tm12 = self._m12 * ang_cos - self._m22 * ang_sin
        tm21 = self._m11 * ang_sin + self._m21 * ang_cos
        tm22 = self._m12 * ang_sin + self._m22 * ang_cos
        tdx = self._dx * ang_cos - self._dy * ang_sin
        tdy = self._dx * ang_sin + self._dy * ang_cos

        self._m11 = tm11
        self._m12 = tm12
        self._dx = tdx
        self._m21 = tm21
        self._m22 = tm22
        self._dy = tdy

    def transform(self, *args) -> Vector2D:
        """create transformed vector from input

        Args:
            One:
                vector (Vector2D): input vector
            Two:
                x (float): input x-coordinates value
                y (folat): input y-coordinates value
        Raises:
            Exception: Need one Vector2D or Two floats
                to pervent raise

        Returns:
            Vector2D : mapped vector object
        """
        if len(args) == 1:
            vector:Vector2D = args[0]
            return Vector2D(self._m11 * vector.x() + self._m12 * vector.y() + self._dx,
                            self._m21 * vector.x() + self._m22 * vector.y() + self._dy)
        if len(args) == 2:
            return Vector2D(self._m11 * args[0] + self._m12 * args[1] + self._dx,
                            self._m21 * args[0] + self._m22 * args[1] + self._dy)

        raise Exception(
            'The input should must inclue a Vector2D or two float for xy')

    def transform_vec(self, vector: Vector2D) -> Vector2D:
        """transform input vector with this matrix

        Args:
            vector (Vector2D): input vector

        Returns:
            Vector2D: trasformed vector
        """
        t_x = self._m11 * vector.x() + self._m12 * vector.y() + self._dx
        t_y = self._m21 * vector.x() + self._m22 * vector.y() + self._dy
        vector.assign(t_x, t_y)
        return vector

    @staticmethod
    def make_translation(dxtf: float, dytf: float) -> Matrix2D:
        """create the translation matrix.

        Args:
            dxtf (float): the horizontal translation factor.
            dytf (float): the vertical translation factor.

        Returns:
            Matrix2D: new matrix object
        """
        return Matrix2D(1.0, 0.0, 0.0, 1.0, dxtf, dytf)

    @staticmethod
    def make_scaling(scale_x: float, scale_y: float) -> Matrix2D:
        """create the scaling matrix.

        Args:
            scale_x (float): the horizontal scaling factor.
            scale_y (float): the vertical scaling factor.

        Returns:
            Matrix2D: new matrix object
        """
        return Matrix2D(scale_x, 0.0, 0.0, scale_y, 0.0, 0.0)

    @staticmethod
    def make_rotation(angle: AngleDeg) -> Matrix2D:
        """create the rotation matrix.

        Args:
            angle (AngleDeg): angle the rotation angle

        Returns:
            Matrix2D: new matrix object
        """
        ang_cos = angle.cos()
        ang_sin = angle.sin()
        return Matrix2D(ang_cos, -ang_sin, ang_sin, ang_cos, 0.0, 0.0)

    def __imul__(self, other: Matrix2D):
        """multiplied by other matrix

        Args:
            other ([Matrix2D]): left hand side matrix
        """
        tm11 = self._m11 * other.m11() + self._m12 * other.m21()
        tm12 = self._m11 * other.m12() + self._m12 * other.m22()
        tm21 = self._m21 * other.m11() + self._m22 * other.m21()
        tm22 = self._m21 * other.m12() + self._m22 * other.m22()
        tdx = self._m11 * other.dxtf() + self._m12 * other.dytf() + self._dx
        tdy = self._m21 * other.dxtf() + self._m22 * other.dytf() + self._dy

        self._m11 = tm11
        self._m12 = tm12
        self._m21 = tm21
        self._m22 = tm22
        self._dx = tdx
        self._dy = tdy

        return self

    def __mul__(self, other: Union[Matrix2D, Vector2D]) -> Union[Matrix2D, Vector2D]:
        """multiplication operator of Matrix * Matrix OR
        multiplication(transformation) operator of Matrix x Vector.

        Args:
            other (Union[Matrix2D, Vector2D]): right hand side matrix OR vector

        Returns:
            Union[Matrix2D, Vector2D]: result matrix object or vector opject
        """
        if isinstance(other, Vector2D):
            return self.transform(other)
        if isinstance(other, Matrix2D):
            mat_tmp = self
            return mat_tmp.__imul__(other)
        return self

    # def __hash__(self):
    #     return hash(self.__members())

    def __eq__(self, other: Matrix2D) -> bool:
        """__eq__ operator

        Args:
            other (Matrix2D): other matrix to compare

        Returns:
            bool: true if eq. else false
        """

        return self._m11 == other.m11() and self._m12 == other.m12() and\
            self._m21 == other.m21() and self._m22 == other.m22() and\
            self._dx == other.dytf() and self._dy == other.dytf()


    def __repr__(self):
        """represent the Matrix2D as a logical string

        Returns:
            str: contains Matrix2D index
        """
        return f"{[self._m11, self._m12, self._m21, self._m22, self._dx, self._dy]}"
