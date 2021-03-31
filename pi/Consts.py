# Purpose: contain application constants.

import math
import os
from enum import IntEnum, Enum
from typing import NewType


class ConfigConstants:
    """
    Constants relevant to configuration, such as configuration file path etc.
    """

    CONFIG_PATH: str = os.path.abspath("config.json")
    """
    Path to the application configuration file.
    ``os.path.abspath`` is used so that files using this path will get it correctly no matter where they are,
    as long as this file is at the same relative path as the configuration file.
    E.g., if ``CONFIG_PATH`` is ``"config.json"``, then this file must be in the same directory as ``"config.json"``.
    """


class ComponentConstants:
    """
    Constants relevant to external components such as the Arduino microcontroller, a camera etc..
    """

    ANALOG_INPUT_BITS = 10
    """
    Bit depth of the analog input.
    """

    ANALOG_MAX_VALUE = 2 ** ANALOG_INPUT_BITS - 1
    """
    Maximum value that the analog input can produce. 
    Arduino Uno operates on 10 bit inputs, so the maximum value is 2 ^ 10 - 1.
    """

    PWM_BITS = 8
    """
    Bit depth of the PWM output.
    """

    PWM_MIN_VALUE = 0
    """
    Minimum output the PWM output can produce.
    """

    PWM_MAX_VALUE = 2 ** PWM_BITS - 1
    """
    Maximum value that the PWM output can produce.
    Arduino Uno operates on 8 bit PWM outputs, so the maximum value is 2 ^ 8 = 255.
    """

    PWM_MIDDLE_VALUE = math.floor(PWM_MAX_VALUE / 2)
    """
    The middle value in the PWM range.
    For example, on 8-bit outputs, 127 is the middle value, equivalent to 0 in a -127 - 127 range.
    """


class MovementConstants:
    """
    Constants relevant to droid movement such as the turning rate, wheel radius etc.
    """

    TURNING_RATE: float = 0
    """
    Turning rate in degrees per second.
    """

    class MotorId(IntEnum):
        """
        The different motors built into the droid.
        """

        WHEEL_LEFT = 0
        """
        Left wheel of the droid. Turning this wheel forwards will cause the droid to turn right.
        """

        WHEEL_RIGHT = 1
        """
        Right wheel of the droid. Turning this wheel forwards will cause the droid to turn left.
        """

        DOME = 2
        """
        The dome of the droid. Turning the dome right will cause it to turn clock-wise. 
        """

        DOME_GIZMOS = 3
        """
        Doors and flaps in the droid's dome.
        """

        FRONT_GIZMOS = 4
        """
        Doors and flaps in the front of the droid.
        """

        SENSOR = 5
        """
        Moving sensor in the dome of the droid.
        """

    class MovementDirection(Enum):
        """
        The directions in which the droid can move.
        *Note* that movement (translation) is not the same as rotation.
        """

        FORWARD = 0
        BACKWARD = 1

    class RotationDirection(Enum):
        """
        The direction in which the droid can rotate.
        *Note* that rotation is not the same as translation (or movement).
        """

        LEFT = 0
        RIGHT = 1


class SerialConstants:
    """
    Constants relevant to serial communication according to the droid serial protocol.
    """

    STRUCT_FORMAT = "BBs"
    """
    *struct*-compatible format for parsing serial packet data.

    - ``B`` - unsigned char - packet type.
    - ``B`` - unsigned char - packet sub-type.
    - ``s`` - char array.
    """

    class SerialPacketType(IntEnum):
        """
        Holds different packet types.
        """

        CORE = 0x0
        MOTORS = 0x1
        SENSORS = 0x2

        CONT = 0xFE
        """
        This packet type informs the receiver that the next packet is related to the previous one.
        """

        LAST = 0xFF
        """
        This packet type informs the receive that the next packet is the last related packet to the previous one.
        """

    class CoreSerialPacketType(IntEnum):
        """
        Holds packet types relevant to the core functionality of the droid.
        """

        SLEEP = 0x1

    class MotorSerialPacketType(IntEnum):
        """
        Holds packet types relevant to movements aspects of the droid.
        """

        SPEED = 0x1
        DRIVE = 0x2
        TURN = 0x3


class Types:
    """
    Types help clarify the units of measurement of certain fields.
    """

    Centimeters = NewType("Centimeters", int)
    """
    Type used to describe distance measurements in centimeters.
    """

    Degrees = NewType("Degrees", int)
    """
    Type used to describe distance measurements in degrees.
    """

    Percentage = NewType("Percentage", int)
    """
    Type used to describe a percentage as a number between 0 and 100, inclusive.
    """

    Milliseconds = NewType("Milliseconds", int)
    """
    Type used to describe thousandths of seconds.
    """


def seconds_to_milliseconds(secs: float) -> int:
    """
    Convert seconds to a whole number of milliseconds.

    :param secs: number of seconds to convert to milliseconds.
    :return: a whole number of milliseconds.
    """

    return abs(int(secs * 1000))


def percentage_to_float(percentage: float) -> float:
    """
    Convert a percentage to a decimal number.
    :param percentage: a percentage to convert (i.e. 95 (%)).
    :return: a decimal number (i.e. 0.95).
    """

    return percentage / 100.0


def remap(value, max_input, min_input, max_output, min_output):
    """
    Convert a value in one range to a value in another range, maintaining the ratio.

    :return: value in same relative position to ``min_output`` - ``max_output`` as it was with its original range.
    """

    value = max_input if value > max_input else value
    value = min_input if value < min_input else value

    input_span = max_input - min_input
    output_span = max_output - min_output

    scaled_thrust = float(value - min_input) / float(input_span)

    return min_output + (scaled_thrust * output_span)
