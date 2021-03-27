# Purpose: provide an interface to all physical aspects of the droid (movement).

from typing import List

from Consts import MovementConstants, seconds_to_milliseconds, percentage_to_float, Types
from Limits import Limits
from Serial.SerialPackets import MotorSpeedSerialPacket, BasicSerialPacket, CoreSleepSerialPacket


def _stop_motor(motor_id: MovementConstants.MotorId) -> MotorSpeedSerialPacket:
    """
    Stop the specified motor.

    :param motor_id: ID of the motor to stop.
    :return: a serial packet to send to the external unit to perform the required task(s).
    """

    return MotorSpeedSerialPacket(motor_id, Types.Percentage(0))


class MovementController:
    """
    Control the droid's movement by generating serial packets.
    """

    @classmethod
    def start_moving(cls, direction: MovementConstants.MovementDirection = MovementConstants.MovementDirection.FORWARD,
                     speed: Types.Percentage = 100) -> List[MotorSpeedSerialPacket]:
        """
        Start droid movement in the specified direction at the specified speed.

        :param direction: direction of movement - whether to rotate the wheels forwards or backwards.
        :param speed: speed as a percentage of the maximum motor voltage.
            Valid values are ranged between 0 and 100.
        :return: serial packets to send to the external unit to perform the required task(s).
        """

        Limits.SIGNED_PERCENTAGE.assert_value(speed)

        target_speed = speed

        # If moving backwards, speed should be negative.
        if direction == MovementConstants.MovementDirection.BACKWARD:
            target_speed *= -1

        return [MotorSpeedSerialPacket(MovementConstants.MotorId.WHEEL_LEFT, target_speed),
                MotorSpeedSerialPacket(MovementConstants.MotorId.WHEEL_RIGHT, target_speed)]

    @classmethod
    def stop_moving(cls) -> List[MotorSpeedSerialPacket]:
        """
        Stop the rover from moving. This method is based on ``start_moving`` with a zeroed-speed.

        :return: serial packets to send to the external unit to perform the required task(s).
        """

        return [_stop_motor(MovementConstants.MotorId.WHEEL_LEFT),
                _stop_motor(MovementConstants.MotorId.WHEEL_RIGHT)]

    @classmethod
    def turn(cls, angle: Types.Degrees,
             direction: MovementConstants.RotationDirection = MovementConstants.RotationDirection.RIGHT,
             speed: Types.Percentage = 100) -> List[BasicSerialPacket]:
        """
        Turn the droid.

        :param angle: angle in which the droid should rotate, in degrees. Setting a negative value will cause
            rotation to the left. The angle is added to the droid's current bearing. For example, 180 degrees will not
            rotate the droid to the south but backwards. Negative values are the same as flipping the
            direction parameter.
        :param direction: the direction in which the angle is relative to. For example, RIGHT and 90 degrees
            will cause the droid to turn right. LEFT and 90 degrees will cause the droid to turn left.
        :param speed: speed as a percentage of the maximum motor voltage.
            Valid values are ranged between 0 and 100.
        :return: serial packets to send to the external unit to perform the required task(s).
        """

        Limits.TURN_ANGLE.assert_value(angle)
        Limits.UNSIGNED_PERCENTAGE.assert_value(speed)

        # Considering there are two ways to control rotation direction, we will use the direction to determine
        # the sign of the angle to rotate to.

        # If the angle is negative and relative to the left, it's the same as a positive value relative to the
        # right.
        if angle < 0 and direction == MovementConstants.RotationDirection.LEFT:
            target_angle = -angle
        else:
            target_angle = angle

        target_speed = speed.real

        # angle > 0 is the same as turning right. In that case, the left wheel drives forward (positive speed) and the
        # right wheel the opposite direction. If we're turning to the left,
        if target_angle < 0:
            target_speed *= -1

        # Wait for the droid's turning.
        time_to_sleep_ms = seconds_to_milliseconds(MovementConstants.TURNING_RATE * percentage_to_float(speed) * angle)

        return [MotorSpeedSerialPacket(MovementConstants.MotorId.WHEEL_LEFT, Types.Percentage(target_speed)),
                MotorSpeedSerialPacket(MovementConstants.MotorId.WHEEL_RIGHT, Types.Percentage(-target_speed)),
                CoreSleepSerialPacket(Types.Milliseconds(time_to_sleep_ms)),
                cls.stop_moving()]


class DomeController:
    """
    Control the droid's dome rotation and gizmos.
    """

    @classmethod
    def turn(cls, angle: Types.Degrees,
             direction: MovementConstants.RotationDirection = MovementConstants.RotationDirection.RIGHT,
             speed: Types.Percentage = 100) -> List[BasicSerialPacket]:
        """
        Turn the droid's dome. See :func:`~MovementController.turn` method for information on the parameters
        supplied to this method.
        """

        Limits.TURN_ANGLE.assert_value(angle)
        Limits.UNSIGNED_PERCENTAGE.assert_value(speed)

        if angle < 0 and direction == MovementConstants.RotationDirection.LEFT:
            target_angle = -angle
        else:
            target_angle = angle

        target_speed = speed

        if target_angle < 0:
            target_speed *= -1

        return [MotorSpeedSerialPacket(MovementConstants.MotorId.DOME, target_speed),
                CoreSleepSerialPacket(
                    Types.Milliseconds(seconds_to_milliseconds(MovementConstants.TURNING_RATE * angle))),
                _stop_motor(MovementConstants.MotorId.DOME)]
