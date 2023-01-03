""" angle_deg.py file
    AngleDeg : class name
    Class attributes : degree
"""
from __future__ import annotations
from typing import Union
import math
from pyrusgeom.math_values import RAD2DEG,EPSILON,DEG2RAD

class AngleDeg:
    """ handling degrees in SS2D
    Attributes:
        degree: a float for angles
    """
    def __init__(self, *args, **kwargs) -> None:
        """This is the class init function and normalizes the input degree.

        Defualt:
            bulid a AngleDeg with value of 0 degree
        Args:
            *args:
                none: for default angle
                one:
                    AngleDeg: create a new AngleDeg with normalized input AngleDeg
                    Degree: create an AngleDeg with normalized degree
        KWArgs:
            af (float): create an AngleDeg with normalized degree
        Raises:
            Exception: Input must be an AngleDeg or a Degree
        """
        if len(args) == 0 and len(kwargs) == 0:
            self._degree = 0
        elif len(args) == 1:
            if isinstance(args[0], AngleDeg):
                self._degree = args[0].degree()
            else:
                self._degree = args[0]
        elif 'af' in kwargs:
            self._degree = kwargs['af']
        else:
            raise Exception('The input should be an AngleDeg or a Degree')
        self.normal()

    def degree(self) -> float:
        """get the degree in a new AngleDeg copy
        # TODO: do we need this?
        Returns:
            float: a new AngleDeg degree with the old AngleDeg's degree
        """
        degree_cp = AngleDeg(self._degree)
        return degree_cp.degree_()

    def degree_(self) -> float:
        """get the orginal degree

        Returns:
            float: AngleDeg's degree
        """
        return self._degree

    def set_degree(self, degree: float) -> None:
        """set a new degree for AngleDeg and normalizes it.

        Args:
            degree (float): new degree to set
        """
        self._degree = degree
        self.normal()

    def set_angle(self, angle: AngleDeg) -> None:
        """set a new degree for AngleDeg from another AngleDeg

        Args:
            angle (AngleDeg): an AngleDeg to copy the degree
        """
        self._degree = angle.degree()

    def normal(self) -> None:
        """normalizing the degree

        if the angle is below -360 degree or above 360 degree,
        it will calculating module of given degree by 360,
        and cap the angle between -180 degree and 180 degree.

        """
        if self._degree < -360.0 or 360.0 < self._degree:
            self._degree = math.fmod(self._degree, 360.0)

        if self._degree < -180.0:
            self._degree += 360.0

        if self._degree > 180.0:
            self._degree -= 360.0

    def is_within(self, left: Union[AngleDeg, float, int],
        right: Union[AngleDeg, float, int]) -> bool:
        """check if this AngleDeg is within [left, right] (turn clockwise)

        Args:
            left (Union[AngleDeg, float, int]): left angle
            right (Union[AngleDeg, float, int]): right angle

        Returns:
            bool: true if this is within [left, right]. else false
        """
        if not isinstance(left, AngleDeg):
            left = AngleDeg(left)
        if not isinstance(right, AngleDeg):
            right = AngleDeg(right)
        if left.is_left_equal_of(right):
            if left.is_left_equal_of(self) and self.is_left_equal_of(right):
                return True
        else:
            if self.is_left_equal_of(right) or left.is_left_equal_of(self):
                return True
        return False

    def abs(self) -> float:
        """get absolute value of this AngleDeg

        Returns:
            float: absolute value of degree()
        """
        return math.fabs(self.degree())

    def radian(self) -> float:
        """get RADIAN value.

        Returns:
            float:  radian value of degree()
        """
        return self.degree() * DEG2RAD

    def copy(self) -> AngleDeg:
        """ copy the AngleDeg

        Returns:
            AngleDeg: a new AngleDeg with same values
        """
        return AngleDeg(self._degree)

    def reverse(self) -> None:
        """reverse this AngleDeg - 180 degrees opposite
        """
        if self._degree >= 0:
            self._degree = -(180 - self._degree)
        else:
            self._degree = 180 + self._degree

    def reverse_angle(self) -> AngleDeg:
        """make a reversed AngleDeg - 180 degrees opposite

        Returns:
            AngleDeg: a new AngleDeg with reverse values
        """
        angle = AngleDeg(self.degree())
        angle.reverse()
        return angle

    def get_normalized(self) -> float:
        """get the Normalized degree betwhen 0 and 1

        Returns:
            float: Normalized degree betwhen 0 and 1
        """
        return (self.degree() + 180) / 360

    def is_left_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        """check if this AngleDeg is left of [angle]

        Args:
            angle (Union[AngleDeg, float, int]): angle to check

        Returns:
            bool: true if this AngleDeg is left of [angle]. else false
        """
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = angle.degree() - self.degree()
        return (0.0 < diff < 180.0) or diff < -180.0

    def is_right_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        """check if this AngleDeg is right of [angle]

        Args:
            angle (Union[AngleDeg, float, int]): angle to check

        Returns:
            bool: true if this AngleDeg is right of [angle]. else false
        """
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = self.degree() - angle.degree()
        return (0.0 < diff < 180.0) or diff < -180.0

    def is_left_equal_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        """check if this AngleDeg is left or equal of [angle]

        Args:
            angle (Union[AngleDeg, float, int]): angle to check

        Returns:
            bool: true if this AngleDeg is left of [angle]. else false
        """
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = angle.degree() - self._degree
        return 0.0 <= diff < 180.0 or diff < -180.0

    def is_right_equal_of(self, angle: Union[AngleDeg, float, int]) -> bool:
        """check if this AngleDeg is right or equal of [angle]

        Args:
            angle (Union[AngleDeg, float, int]): angle to check

        Returns:
            bool: true if this AngleDeg is right of [angle]. else false
        """
        if not isinstance(angle, AngleDeg):
            angle = AngleDeg(angle)
        diff = self.degree() - angle.degree()
        return (0.0 <= diff < 180.0) or diff < -180.0

    def __iadd__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        """operator +=

        Args:
            other (Union[AngleDeg, float, int]): angle added value

        Returns:
            AngleDeg: this AngleDeg
        """
        if isinstance(other, AngleDeg):
            other = other.degree()
        self._degree += other
        self.normal()
        return self

    def __isub__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        """operator -=

        Args:
            other (Union[AngleDeg, float, int]): angle subtract argument

        Returns:
            AngleDeg: this AngleDeg
        """
        if isinstance(other, AngleDeg):
            other = other.degree()
        self._degree -= other
        self.normal()
        return self

    def __imul__(self, other: Union[float, int]) -> AngleDeg:
        """operator *=

        Args:
            other (Union[float, int]): scalar multiply argument

        Returns:
            AngleDeg: this AngleDeg
        """
        self._degree *= other
        self.normal()
        return self

    def __idiv__(self, other: Union[float, int]) -> AngleDeg:
        """operator /=

        Args:
            other (Union[float, int]): scalar division argument

        Returns:
            AngleDeg: this AngleDeg
        """
        self._degree /= other
        self.normal()
        return self

    def __add__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        """operator add for AngleDeg

        Args:
            other (Union[AngleDeg, float, int]): right hand side argument

        Returns:
            AngleDeg: a new Angledeg with value of
            sum of left hand side argument and right hand side argument
        """
        if isinstance(other,AngleDeg):
            new_angle_deg = AngleDeg(self._degree + other.degree())
        else:
            new_angle_deg = AngleDeg(self._degree + other)
        return new_angle_deg

    def __sub__(self, other: Union[AngleDeg, float, int]) -> AngleDeg:
        """operator sub for AngleDeg

        Args:
            other (Union[AngleDeg, float, int]): right hand side argument

        Returns:
            AngleDeg: a new Angledeg with value of
            subtraction of right hand side argument from left hand side argument
        """
        if isinstance(other,AngleDeg):
            return AngleDeg(self._degree - other._degree)
        return AngleDeg(self._degree - other)

    def __mul__(self, other: Union[float, int]) -> AngleDeg:
        """operator mul for AngleDeg

        Args:
            other (Union[float, int]): scalar multiply argument

        Returns:
            AngleDeg: a new AngleDeg with the multiply of this AngleDeg and
            scalar multiply argument
        """
        new_angle_deg = AngleDeg(self._degree * other)
        return new_angle_deg

    def __floordiv__(self, other: Union[float, int]) -> AngleDeg:
        """operator floordiv for AngleDeg

        Args:
            other (Union[float, int]): scalar division argument

        Returns:
            AngleDeg: a new AngleDeg with the floor division of this AngleDeg
            on scalar division argument
        """
        new_angle_deg = AngleDeg(self._degree / other)
        return new_angle_deg

    def __repr__(self) -> str:
        """represent AngleDeg as a string

        Returns:
            str: AngleDeg's Degree as string
        """
        return str(self.degree())

    def __float__(self) -> float:
        """represent AngleDeg as a float

        Returns:
            float: AngleDeg's Degree as float
        """
        return float(self.degree())

    def __neg__(self) -> AngleDeg:
        """ negation operator

        Returns:
            AngleDeg: new AngleDeg with negation
        """
        new_angle_deg = AngleDeg(-self._degree)
        return new_angle_deg

    def __eq__(self, other: Union[AngleDeg, float, int]) -> bool:
        """operator == for AngleDeg

        Args:
            other (Union[AngleDeg,float, int]): right hand side argument
        Returns:
            bool: true if equal or difference is less than EPSILON. else false
        """
        if isinstance(other, AngleDeg):
            other = other.degree()
        return math.fabs(self._degree - other) < EPSILON

    def cos(self) -> float:
        """calculate cosine

        Returns:
            float: cosine value
        """
        return math.cos(self._degree * DEG2RAD)

    def sin(self) -> float:
        """calculate sine

        Returns:
            float: sine value
        """
        return math.sin(self._degree * DEG2RAD)

    def tan(self) -> float:
        """calculate tarngetn

        Returns:
            float: tarngetn value
        """
        return math.tan(self._degree * DEG2RAD)

    @staticmethod
    def rad2deg(rad: float) -> float:
        """static utility. convert radian to degree

        Args:
            rad (float): radian value

        Returns:
            float: degree value
        """
        return rad * RAD2DEG

    @staticmethod
    def deg2rad(deg: float) -> float:
        """static utility. convert degree to radian

        Args:
            deg (float): degree value

        Returns:
            float: radian value
        """
        return deg * DEG2RAD

    @staticmethod
    def cos_deg(deg: float) -> float:
        """static utility. calculate cosine value for degree angle

        Args:
            deg (float): degree value

        Returns:
            float: cosine value
        """
        return math.cos(AngleDeg.deg2rad(deg))

    @staticmethod
    def sin_deg(deg: float) -> float:
        """static utility. calculate sine value for degree angle

        Args:
            deg (float): degree value

        Returns:
            float: sine value
        """
        return math.sin(AngleDeg.deg2rad(deg))

    @staticmethod
    def tan_deg(deg: float) -> float:
        """static utility. calculate tangent value for degree angle

        Args:
            deg (float): degree value

        Returns:
            float: tangent value
        """
        return math.tan(AngleDeg.deg2rad(deg))

    @staticmethod
    def acos_deg(cosine: float) -> float:
        """static utility. calculate arc cosine value

        Args:
            cosine (float): cosine value

        Returns:
            float: arc cosine value, that is degree type.
        """
        if cosine >= 1.0:
            return 0.0
        elif cosine <= -1.0:
            return 180.0
        else:
            return AngleDeg.rad2deg(math.acos(cosine))

    @staticmethod
    def asin_deg(sine: float) -> float:
        """static utility. calculate arc sine value

        Args:
            sine (float): sine value

        Returns:
            float: arc sine value, that is degree type.
        """
        if sine >= 1.0:
            return 90.0
        elif sine <= -1.0:
            return -90.0
        else:
            return AngleDeg.rad2deg(math.asin(sine))

    @staticmethod
    def atan_deg(tangent: float) -> float:
        """static utility. calculate arc tangent value

        Args:
            tangent (float): tangent value

        Returns:
            float: arc tangent value, that is degree.
        """
        return AngleDeg.rad2deg(math.atan(tangent))

    @staticmethod
    def atan2_deg(y_val: float, x_val: float) -> float:
        """static utility. calculate arc tangent value from XY

        Args:
            y_val (float): coordinate Y
            x_val (float): coordinate X

        Returns:
            float: arc tangent value.
        """
        if math.fabs(x_val) < EPSILON and math.fabs(y_val) < EPSILON:
            return 0.0
        else:
            return AngleDeg.rad2deg(math.atan2(y_val, x_val))

    @staticmethod
    def bisect(left: Union[int, float, AngleDeg],
        right: Union[int, float, AngleDeg]) -> Union[AngleDeg, float]:
        """static utility that returns bisect angle of [left, right]
        this method can take obtuse angle

        Args:
            left (Union[int, float, AngleDeg]): left start angle
            right (Union[int, float, AngleDeg]): right end angle

        Returns:
            Union[AngleDeg, float]: bisect angle
        """
        result = AngleDeg(left)
        rel = AngleDeg(AngleDeg(right) - result)
        diff = result.degree() - AngleDeg(right).degree()
        half_deg = rel.degree() * 0.5
        result += half_deg
        if (0.0 < diff < 180.0) or diff < -180.0:
            return result
        return result + 180.0

    @staticmethod
    def normalize_angle(dir: float):
        if dir < -360 or dir > 360:
            dir = dir % 360
        if dir < -180:
            dir += 360
        if dir > 180:
            dir -= 360
        return dir