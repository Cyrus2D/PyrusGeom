"""
  file soccer_math
  brief math utility depending on RCSSServer2D
"""
from __future__ import annotations
from typing import Union
from PyrusGeom.vector_2d import Vector2D
import math


EPS = 1.0e-8


def kick_rate(dist: float, dir_diff: float, kick_rate_power: float,
              ball_size: float, player_size: float, kickable_margin: float) -> float:
    """
    brief calculate kick rate
    @param dist distance from player to ball
    @param dir_diff angle difference from player's body to ball
    @param kick_rate_power player's kick power rate parameter
    @param ball_size ball radius
    @param player_size player radius
    @param kickable_margin player's kickable area margin
    @return rate of the kick power effect
    """
    return kick_rate_power * (1.0 - 0.25 * math.fabs(dir_diff)
                              / 180.0 - 0.25 * (dist - ball_size - player_size) / kickable_margin)


def dir_rate(rel_dash_dir: float, back_dash_rate: float, side_dash_rate: float) -> float:
    """
    brief calculate effective dash power rate according to the input dash direction
    @param rel_dash_dir relative dash direction
    @param back_dash_rate server parameter
    @param side_dash_rate server parameter
    @return effective dash power rate
    """
    if math.fabs(rel_dash_dir) > 90.0:
        return back_dash_rate - ((back_dash_rate - side_dash_rate) * (1.0 - (math.fabs(rel_dash_dir) - 90.0) / 90.0))
    return side_dash_rate + ((1.0 - side_dash_rate) * (1.0 - math.fabs(rel_dash_dir) / 90.0))


def effective_turn(turn_moment: float, speed: float, inertia_moment: float) -> float:
    """
    brief calculate effective turn moment.
    it may be useful to redefine self algorithm in movement action module
    @param turn_moment value used by turn command
    @param speed player's current speed
    @param inertia_moment player's inertia moment parameter
    @return calculated actual turn angle
    """
    return turn_moment / (1.0 + inertia_moment * speed)


def final_speed(dash_power: float, player_dash_power_rate: float, effort: float, decay: float) -> float:
    """
    brief calculate converged max speed, using "dash_power"
    NOTE: returned value should be compared with player_speed_max parameter
    @param dash_power value used by dash command
    @param player_dash_power_rate player's dash power rate parameter
    @param effort player's effort parameter
    @param decay player's decay parameter
    @return achieved final speed
    """
    return (math.fabs(dash_power) * player_dash_power_rate * effort) / (1.0 - decay)


def can_over_speed_max(dash_power: float, dash_power_rate: float, effort: float,
                       decay: float, speed_max: float) -> float:
    """
    brief check if player's potential max speed is over player_speed_max parameter.
    @param dash_power value used by dash command
    @param dash_power_rate player's dash power rate parameter
    @param effort player's effort parameter
    @param speed_max player's limited speed parameter
    @param decay player's decay parameter
    @return True, player can over player_speed_max
    """
    return math.fabs(dash_power) * dash_power_rate * effort > speed_max * (1.0 - decay)


def inertia_n_step_travel(initial_vel: Vector2D, n_step: int, decay: float) -> Vector2D:
    """
    brief estimate future travel after n steps only by inertia.
    No additional acceleration.
    @param initial_vel object's first velocity
    @param n_step number of total steps
    @param decay object's decay parameter
    @return vector of total travel
    """
    tmp = Vector2D(initial_vel.x(), initial_vel.y())
    tmp *= ((1.0 - math.pow(decay, n_step)) / (1.0 - decay))
    return tmp


def inertia_n_step_point(initial_pos: Vector2D, initial_vel: Vector2D, n_step: int, decay: float) -> Vector2D:
    """
    brief estimate future point after n steps only by inertia.
    No additional acceleration
    @param initial_pos object's first position
    @param initial_vel object's first velocity
    @param n_step number of total steps
    @param decay object's decay parameter
    @return coordinate of the reached point
    """
    tmp = Vector2D(initial_pos.x(), initial_pos.y())
    tmp += inertia_n_step_travel(initial_vel, n_step, decay)
    return tmp


def inertia_n_step_distance(initial_speed: float, n_step: int, decay: float) -> float:
    """
    brief estimate travel distance only by inertia.
    No additional acceleration
    @param initial_speed object's first speed
    @param n_step number of total steps
    @param decay object's decay parameter
    @return total travel distance
    """
    if type(n_step) == int:
        return initial_speed * (1.0 - math.pow(decay, n_step)) / (1.0 - decay)
    else:
        return initial_speed * (1.0 - math.pow(decay, n_step)) / (1.0 - decay)


def inertia_final_travel(initial_vel: Vector2D, decay: float) -> Vector2D:
    """
    brief calculate total travel only by inertia movement.
    @param initial_vel object's first velocity
    @param decay object's decay parameter
    @return final travel vector
    """
    tmp = Vector2D(initial_vel.x(), initial_vel.y())
    tmp /= (1.0 - decay)
    return tmp


def inertia_final_point(initial_pos: Vector2D, initial_vel: Vector2D, decay: float) -> Vector2D:
    """
    brief calculate final reach point only by inertia.
    @param initial_pos object's first position
    @param initial_vel object's first velocity
    @param decay object's decay parameter
    @return coordinate of the reached point
    """
    tmp = Vector2D(initial_pos.x(), initial_pos.y())
    tmp += inertia_final_travel(initial_vel, decay)
    return tmp


def inertia_final_distance(initial_speed: float, decay: float) -> float:
    """
    brief calculate total travel distance only by inertia.
    @param initial_speed object's first speed
    @param decay object's decay parameter
    @return distance value that the object reaches
    """
    return initial_speed / (1.0 - decay)


def r_int(f: float):
    """
    brief Rounds the floating-point argument f to an integer value (in floating-point format),
    using the current rounding mode.
    @param f floating point value
    @return If no errors occur, the nearest integer value to f, according to the current
    rounding mode, is returned.a
    """
    fi = int(f)
    fi_diff = math.fabs(fi - f)
    fi_left = fi - 1
    fi_left_diff = math.fabs(fi_left - f)
    fi_right = fi + 1
    fi_right_diff = math.fabs(fi_right - f)
    if fi_diff < fi_left_diff and fi_diff < fi_right_diff:
        return fi
    elif fi_left_diff < fi_right_diff:
        return fi_left
    else:
        return fi_right


def calc_first_term_geom_series(sums: float, r: float, length: int) -> float:
    return sums * (1.0 - r) / (1.0 - math.pow(r, length))


def bound(a: float, b: float, c: float) -> float:
    return min(max(a, b), c)


def min_max(low: float, x: float, high: float) -> float:
    return min(max(low, x), high)


def f_range(start: float, stop: Union[None, float] = None, step: Union[None, float] = None):
    """
    brief  Use float number in range() function
    @param start the start number
    @param stop the end number
    @param step start += step until end
    @return float number
    """
    # if stop and step argument is null set start=0.0 and step = 1.0
    if stop is None:
        stop = start + 0.0
        start = 0.0
    if step is None:
        step = 1.0
    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield start
        start = start + step


SERVER_EPS = 1.0e-10

# localization


def quantize(value: float, qstep: float):
    """
    brief quantize a floating point number
    @param value value to be rounded
    @param qstep round precision
    @return rounded value
    same as define Quantize(v,q) ((rint((v)/(q)))*(q))
    """
    return r_int(value / qstep) * qstep


def quantize_dist(unq_dist: float, qstep: float) -> float:
    """
    brief calculate quantized distance value about dist quantization
    @param unq_dist actual distance
    @param qstep server parameter
    @return quantized distance
    """
    return quantize(math.exp(quantize(math.log(unq_dist + SERVER_EPS), qstep)), 0.1)


def unquantize_min(dist: float, qstep: float):
    """
    brief calculate minimal value by inverse quantize function
    @param dist quantized distance
    @param qstep server parameter
    @return minimal distance within un quantized distance range
    """
    return (r_int(dist / qstep) - 0.5) * qstep


def unquantize_max(dist: float, qstep: float) -> float:
    """
    brief calculate maximal value by inverse quantize function
    @param dist quantized distance
    @param qstep server parameter
    @return maximal distance within un quantized distance range
    """
    return (r_int(dist / qstep) + 0.5) * qstep


"""add in servers"""


def wind_effect(speed: float,
                weight: float,
                wind_force: float,
                wind_dir: float,
                wind_weight: float,
                wind_rand: float,
                wind_error: Vector2D):
    """
    brief calculate wind effect
    @param speed current object's speed
    @param weight object's speed
    @param wind_force server parameter
    @param wind_dir server parameter
    @param wind_weight server parameter
    @param wind_rand server parameter
    @param wind_error error value that is calculated by self method
    @return wind effect acceleration
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


def unquantize_error(see_dist: float, qstep: float):
    """
    brief calculate min max error range by inverse quantize function
    @param see_dist seen(quantized) distance
    @param qstep server parameter
    @return error value of inverse un quantized distance
    """
    min_dist = (math.exp(unquantize_min(math.log(unquantize_min(see_dist, 0.1)), qstep)) - SERVER_EPS)
    max_dist = (math.exp(unquantize_max(math.log(unquantize_max(see_dist, 0.1)), qstep)) - SERVER_EPS)
    return math.fabs(max_dist - min_dist)


def calc_length_geom_series(first_term: float, sum_all: float, r: float) -> float:
    """
    brief caluculate the length of a geometric series
    @param first_term value of the first term
    @param r multiplication ratio
    @param sum_all sum of a geometric series
    @return a round number of the length of geometric series
    """
    if first_term <= SERVER_EPS or sum_all < 0.0 or r <= SERVER_EPS:
        return -1.0
    if sum_all <= SERVER_EPS:
        return 0.0
    tmp = 1.0 + sum_all * (r - 1.0) / first_term
    if tmp <= SERVER_EPS:
        return -1.0
    return math.log(tmp) / math.log(r)
