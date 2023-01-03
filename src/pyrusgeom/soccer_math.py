"""soccer_math file
   math utility depending on RCSSServer2D
   TODO: use math_values
"""
from __future__ import annotations
# from typing import Union
import math

from pyrusgeom.vector_2d import Vector2D

EPS = 1.0e-8
SERVER_EPS = 1.0e-10


def kick_rate(dist: float, dir_diff: float, kick_rate_power: float,
              ball_size: float, player_size: float, kickable_margin: float) -> float:
    """calculate kick rate

    Args:
        dist (float): distance from player to ball
        dir_diff (float): angle difference from player's body to ball
        kick_rate_power (float): player's kick power rate parameter
        ball_size (float): ball radius
        player_size (float): player radius
        kickable_margin (float): player's kickable area margin

    Returns:
        float: rate of the kick power effect
    """
    return kick_rate_power * (1.0 - 0.25 * math.fabs(dir_diff)
                              / 180.0 - 0.25 * (dist - ball_size - player_size) / kickable_margin)


def dir_rate(rel_dash_dir: float, back_dash_rate: float, side_dash_rate: float) -> float:
    """calculate effective dash power rate according to the input dash direction

    Args:
        rel_dash_dir (float): relative dash direction
        back_dash_rate (float): server parameter
        side_dash_rate (float): server parameter

    Returns:
        float: dash power rate
    """
    if math.fabs(rel_dash_dir) > 90.0:
        return back_dash_rate - ((back_dash_rate - side_dash_rate) * (
            1.0 - (math.fabs(rel_dash_dir) - 90.0) / 90.0))
    return side_dash_rate + ((1.0 - side_dash_rate) * (1.0 - math.fabs(rel_dash_dir) / 90.0))


def effective_turn(turn_moment: float, speed: float, inertia_moment: float) -> float:
    """calculate effective turn moment.

    it may be useful to redefine self algorithm in movement action module

    Args:
        turn_moment (float): value used by turn command
        speed (float): player's current speed
        inertia_moment (float): player's inertia moment parameter

    Returns:
        float: calculated actual turn angle
    """
    return turn_moment / (1.0 + inertia_moment * speed)


def final_speed(dash_power: float, player_dash_power_rate: float,
                effort: float, decay: float) -> float:
    """calculate converged max speed, using "dash_power"

    NOTE: returned value should be compared with player_speed_max parameter

    Args:
        dash_power (float): value used by dash command
        player_dash_power_rate (float): player's dash power rate parameter
        effort (float): player's effort parameter
        decay (float): player's decay parameter

    Returns:
        float: final speed
    """
    return (math.fabs(dash_power) * player_dash_power_rate * effort) / (1.0 - decay)


def can_over_speed_max(dash_power: float, dash_power_rate: float, effort: float,
                       decay: float, speed_max: float) -> bool:
    """check if player's potential max speed is over player_speed_max parameter.

    Args:
        dash_power (float): value used by dash command
        dash_power_rate (float): player's dash power rate parameter
        effort (float): player's effort parameter
        decay (float): decay parameter
        speed_max (float): player's limited speed parameter

    Returns:
        bool: True if player can over player_speed_max. else False.
    """
    return math.fabs(dash_power) * dash_power_rate * effort > speed_max * (1.0 - decay)


def inertia_n_step_travel(initial_vel: Vector2D, n_step: int, decay: float) -> Vector2D:
    """estimate future travel after n steps only by inertia.

    No additional acceleration.

    Args:
        initial_vel (Vector2D): object's first velocity
        n_step (int): number of total steps
        decay (float): object's decay parameter

    Returns:
        Vector2D: vector of total travel
    """
    return (Vector2D(initial_vel.x(), initial_vel.y()) *
           ((1.0 - math.pow(decay, n_step)) / (1.0 - decay)))


def inertia_n_step_point(initial_pos: Vector2D,
                         initial_vel: Vector2D, n_step: int, decay: float) -> Vector2D:
    """estimate future point after n steps only by inertia.

    No additional acceleration.

    Args:
        initial_pos (Vector2D): object's first position
        initial_vel (Vector2D): object's first velocity
        n_step (int): number of total steps
        decay (float): object's decay parameter

    Returns:
        Vector2D: coordinate of the reached point
    """
    return (Vector2D(initial_pos.x(), initial_pos.y()) +
            inertia_n_step_travel(initial_vel, n_step, decay))


def inertia_n_step_distance(initial_speed: float, n_step: int, decay: float) -> float:
    """estimate travel distance only by inertia.

    No additional acceleration.

    Args:
        initial_speed (float): object's first speed
        n_step (int): number of total steps
        decay (float): decay object's decay parameter

    Returns:
        float: total travel distance
    """
    return initial_speed * (1.0 - math.pow(decay, n_step)) / (1.0 - decay)

def inertia_final_travel(initial_vel: Vector2D, decay: float) -> Vector2D:
    """calculate total travel only by inertia movement.

    Args:
        initial_vel (Vector2D): initial_vel object's first velocity
        decay (float): object's decay parameter

    Returns:
        Vector2D: final travel vector
    """
    return  Vector2D(initial_vel.x(), initial_vel.y()) / (1.0 - decay)


def inertia_final_point(initial_pos: Vector2D, initial_vel: Vector2D, decay: float) -> Vector2D:
    """calculate final reach point only by inertia.

    Args:
        initial_pos (Vector2D): object's first position
        initial_vel (Vector2D): object's first velocity
        decay (float): decay parameter

    Returns:
        Vector2D: coordinate of the reached point
    """
    return Vector2D(initial_pos.x(), initial_pos.y()) + inertia_final_travel(initial_vel, decay)


def inertia_final_distance(initial_speed: float, decay: float) -> float:
    """calculate total travel distance only by inertia.

    Args:
        initial_speed (float): object's first speed
        decay (float): object's decay parameter

    Returns:
        float: distance value that the object reaches
    """
    return initial_speed / (1.0 - decay)


def r_int(floating_point: float) -> int:
    """Rounds the floating-point argument f to an integer value (in floating-point format),
    using the current rounding mode.

    Args:
        floating_point (float): floating point value

    Returns:
        int: If no errors occur, the nearest integer value to f, according to the current
    rounding mode, is returned.
    """

    fi_og = int(floating_point)
    fi_diff = math.fabs(fi_og - floating_point)
    fi_left = fi_og - 1
    fi_left_diff = math.fabs(fi_left - floating_point)
    fi_right = fi_og + 1
    fi_right_diff = math.fabs(fi_right - floating_point)
    if fi_diff < fi_left_diff and fi_diff < fi_right_diff:
        return fi_og
    if fi_left_diff < fi_right_diff:
        return fi_left
    return fi_right


def calc_length_geom_series(first_term: float, sum_all: float, ratio: float) -> float:
    """caluculate the length of a geometric series

    Args:
        first_term (float): value of the first term
        sum_all (float): sum of a geometric series
        ratio (float): multiplication ratio

    Returns:
        float: a round number of the length of geometric series
    """
    if first_term <= SERVER_EPS or sum_all < 0.0 or ratio <= SERVER_EPS:
        return -1.0
    if sum_all <= SERVER_EPS:
        return 0.0
    tmp = 1.0 + sum_all * (ratio - 1.0) / first_term
    if tmp <= SERVER_EPS:
        return -1.0
    return math.log(tmp) / math.log(ratio)

def calc_first_term_geom_series(sums: float, ratio: float, length: int) -> float:
    """calculate the frist term of geometric series

    Args:
        sums (float): sum of a geometric series
        ratio (float): ratio of series
        length (int): length of a geometric series

    Returns:
        float: frist term of geometric series
    """
    return sums * (1.0 - ratio) / (1.0 - math.pow(ratio, length))


def bound(num_0: float, num_1: float, num_2: float) -> float:
    """calc the bound between three input float

    Args:
        num_0 (float): 1st number
        num_1 (float): 2nd number
        num_2 (float): 3rd number

    Returns:
        float: bounded number
    """
    return min(max(num_0, num_1), num_2)

def min_max(low: float, number: float, high: float) -> float:
    """min max the input number

    Args:
        low (float): lower bound
        number (float): input number
        high (float): higher bound

    Returns:
        float: bounded number
    """
    return min(max(low, number), high)


def f_range(start: float, stop: float = None, step: float = None) -> float:
    """Use float number in range() function

    if stop and step argument is null set start=0.0 and step = 1.0

    Args:
        start (float): the start number
        stop (float, optional): the end number. Defaults to None.
        step (float, optional): start += step until end. Defaults to None.


    Args:
        start (float): [description]
        stop (float, optional): [description]. Defaults to None.
        step (float, optional): [description]. Defaults to None.

    Returns:
        float: number

    Yields:
        Iterator[float]: [description]
    """
    if stop is None:
        stop = start + 0.0
        start = 0.0
    if step is None:
        step = 1.0
    while True:
        if step > 0 and start >= stop:
            break
        if step < 0 and start <= stop:
            break
        yield start
        start = start + step

# localization

def quantize(value: float, qstep: float) -> float:
    """quantize a floating point number
    same as define Quantize(v,q) ((rint((v)/(q)))*(q))

    Args:
        value (float):  value to be rounded
        qstep (float): round precision

    Returns:
        float: rounded value
    """
    return r_int(value / qstep) * qstep


def quantize_dist(unq_dist: float, qstep: float) -> float:
    """calculate quantized distance value about dist quantization

    Args:
        unq_dist (float): actual distance
        qstep (float): server parameter

    Returns:
        float: quantized distance
    """
    return quantize(math.exp(quantize(math.log(unq_dist + SERVER_EPS), qstep)), 0.1)


def unquantize_min(dist: float, qstep: float) -> float:
    """calculate minimal value by inverse quantize function

    Args:
        dist (float): quantized distance
        qstep (float): server parameter

    Returns:
        float: minimal distance within un quantized distance range
    """
    return (r_int(dist / qstep) - 0.5) * qstep


def unquantize_max(dist: float, qstep: float) -> float:
    """calculate maximal value by inverse quantize function

    Args:
        dist (float): dist quantized distance
        qstep (float): server parameter

    Returns:
        float: maximal distance within un quantized distance range
    """
    return (r_int(dist / qstep) + 0.5) * qstep


def wind_effect(speed: float, weight: float,
                wind_force: float, wind_dir: float,
                wind_weight: float, wind_rand: float,
                wind_error: Vector2D) -> Vector2D:
    """calculate wind effect

    Args:
        speed (float): current object's speed
        weight (float): object's speed weight
        wind_force (float): server parameter
        wind_dir (float): server parameter
        wind_weight (float): server parameter
        wind_rand (float): server parameter
        wind_error (Vector2D): error value that is calculated by this method

    Returns:
        Vector2D: wind effect acceleration
    """
    wind_vec = Vector2D()
    wind_vec.polar2vector(wind_force, wind_dir)

    if wind_error:
        wind_error.assign(speed * wind_vec.x() * wind_rand
                          / (weight * wind_weight),
                          speed * wind_vec.y() * wind_rand
                          / (weight * wind_weight))

    return Vector2D(speed * wind_vec.x() / (weight * wind_weight),
                    speed * wind_vec.y() / (weight * wind_weight))


def unquantize_error(see_dist: float, qstep: float) -> float:
    """calculate min max error range by inverse quantize function

    Args:
        see_dist (float): seen(quantized) distance
        qstep (float): server parameter

    Returns:
        float: error value of inverse un quantized distance
    """
    min_dist = (math.exp(unquantize_min(
        math.log(unquantize_min(see_dist, 0.1)), qstep)) - SERVER_EPS)
    max_dist = (math.exp(unquantize_max(
        math.log(unquantize_max(see_dist, 0.1)), qstep)) - SERVER_EPS)
    return math.fabs(max_dist - min_dist)
