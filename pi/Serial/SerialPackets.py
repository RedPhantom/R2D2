# Purpose: provide different kinds of serial packets.

import struct

import Consts
from Consts import MovementConstants, SerialConstants, Types
from Limits import Limits


class BasicSerialPacket:
    """
    Models a basic serial packet.
    Packets are made out of a type, sub-type (determined by the packet itself) and raw data (as a byte array).
    """

    def __init__(self, packet_type: SerialConstants.SerialPacketType, data: bytes):
        """
        Initialize a new serial packet.
        For every packet inheriting this Base Serial Packet, the ``super()`` call should be at the end of
        the inheriting class' ``__init__(self)`` method.

        :param packet_type: 8-bit unsigned integer describing the type of the packet sent.
        :param data: data to write to the serial bus.
        """

        if packet_type not in SerialConstants.SerialPacketType.__dict__.values():
            raise ValueError("The provided packet type (%d) is not supported." % packet_type)

        if not isinstance(data, bytes):
            raise TypeError("Data must be in form of a byte array.")

        self._packet_type = packet_type
        self._data = data
        self._bytes = bytes([self._packet_type]) + self._data

    def __str__(self, encoding="utf8"):
        """
        Retrieve the string representation of the packet.

        :param encoding: encoding used to parse the packet data as.
        """

        return self._data.decode(encoding)

    def set(self, data: bytes):
        """
        Directly set the packet's bytes. Not recommended.

        :param data: byte array to set this packet's data to.
        """

        if not isinstance(data, bytes):
            raise TypeError("Data must be in form of a byte array.")

        self._data = data

    @property
    def bytes(self) -> bytes:
        """
        Retrieve the packet's representation as bytes.

        :return: bytes representation of this (or any inheriting) packet.
        """

        return self._bytes

    @staticmethod
    def from_bytes(byte_array: bytes):
        """
        Create a new packet object from the bytes received over the serial bus.

        :param byte_array: bytes received over the serial bus, excluding packet type and sub-type.
        :return: a prepared instance of the packet object.
        """

        raise NotImplementedError("Must be implemented in a child class.")


#
# Core Packets
#
class CoreSleepSerialPacket(BasicSerialPacket):
    """
    A packet that orders the external component to stop software execution for a specified period of time.
    """

    def __init__(self, sleep_period: Types.Milliseconds):
        """
        Initialize a packet that halts software execution for a period of time according to the following bytes:
            0. ``CORE`` serial packet type.
            1. ``SLEEP`` serial packet sub-type.
            2. ``sleep_period`` most significant byte.
            3. ``sleep_period`` least significant byte.

        :param sleep_period: period of time, in milliseconds, in which software should halt execution.
        """

        Limits.POSITIVE_INT.assert_value(sleep_period)
        self._sleep_period = sleep_period

        self._fields = [SerialConstants.CoreSerialPacketType.SLEEP.value, sleep_period]
        super().__init__(SerialConstants.SerialPacketType.CORE, bytes(self._fields))

    @property
    def sleep_period(self):
        return self._sleep_period

    @staticmethod
    def from_bytes(byte_array: bytes):
        sleep_period, _ = struct.unpack(">H", byte_array)
        return CoreSleepSerialPacket(Types.Milliseconds(sleep_period))


#
# Movement Packets
#
class MotorSpeedSerialPacket(BasicSerialPacket):
    """
    A packet that orders a motor to be provided a voltage relative to its maximum voltage.
    Call the constructor with the required motor ID and speed, and then access the ``bytes`` property
    to receive the byte sequence to send via the serial bus.
    """

    def __init__(self, motor_id: int, speed: Types.Percentage):
        """
        Initialize a packet that configures the motor speeds according to the following bytes:

            0. ``MOTORS`` serial packet type.
            1. ``SPEED`` serial packet sub-type.
            2. Motor ID.
            3. Motor speed.

        :param motor_id: identifier of the motor to control.
        :param speed: motor speed to set, as a percentage of the voltage the motor may receive.
            Negative values represent reverse rotation direction.
        """

        Limits.SIGNED_PERCENTAGE.assert_value(speed)
        self._motor_id = motor_id
        self._speed = speed

        self._fields = [SerialConstants.MotorSerialPacketType.SPEED.value, motor_id, speed.__int__()]
        super().__init__(SerialConstants.SerialPacketType.MOTORS, bytes(self._fields))

    @staticmethod
    def from_bytes(byte_array: bytes):
        motor_id, motor_speed, _ = struct.unpack(">BB", byte_array)
        return MotorSpeedSerialPacket(motor_id, motor_speed)

    @property
    def motor_id(self):
        return self._motor_id

    @property
    def speed(self):
        return self._speed


class DriveSerialPacket(BasicSerialPacket):
    """
    A packet that instructs the droid to drive a specified distance.
    """

    def __init__(self, direction: MovementConstants.MovementDirection, distance: Types.Centimeters,
                 speed: Types.Percentage):
        """
        Initialize a packet that instructs the droid to drive forwards or backwards a specified distance, according
        to the following bytes:

            0. ``MOTORS`` serial packet type.
            1. ``DRIVE`` serial packet sub-type.
            2. ``direction`` in which driving should occur.
            3. ``distance`` most significant byte.
            4. ``distance`` least significant byte.
            5. ``speed`` in which driving should occur.

        :param direction: direction in which the droid should drive.
        :param distance: distance the droid should drive, in centimeters.
        :param speed: speed in which driving should occur.
        """

        Limits.TWO_BYTE_UINT.assert_value(distance)
        Limits.SIGNED_PERCENTAGE.assert_value(speed)
        self._direction = direction
        self._distance = distance
        self._speed = speed

        assert direction in MovementConstants.MovementDirection, "ERROR: direction not in MovementDirection."

        distance_msb = (distance >> 8) & 0xFF
        distance_lsb = distance & 0xFF

        # Since motors have their direction as well as speed controlled via the PWM output,
        # PWM values that are smaller than 127 (not inclusive) will cause the motor to turn in reverse.
        # This is the reason for using the SIGNED_PERCENTAGE instead of the UNSIGNED one.

        percentage_limit = Limits.UNSIGNED_PERCENTAGE
        adjusted_speed = Consts.remap(speed, percentage_limit.max, percentage_limit.min,
                                      Consts.ComponentConstants.PWM_MAX_VALUE, Consts.ComponentConstants.PWM_MIN_VALUE)
        self._fields = [SerialConstants.MotorSerialPacketType.DRIVE.value, direction.value, distance_msb, distance_lsb,
                        adjusted_speed]
        super().__init__(SerialConstants.SerialPacketType.MOTORS, bytes(self._fields))

    @staticmethod
    def from_bytes(byte_array: bytes):
        direction, distance, speed, _ = struct.unpack(">BHB", byte_array)

        speed_limit = Limits.SIGNED_PERCENTAGE
        speed = Consts.remap(speed, Consts.ComponentConstants.PWM_MAX_VALUE, Consts.ComponentConstants.PWM_MIN_VALUE,
                             speed_limit.max, speed_limit.min)

        return DriveSerialPacket(direction, distance, speed)

    @property
    def direction(self):
        return self._direction

    @property
    def distance(self):
        return self._distance

    @property
    def speed(self):
        return self._speed


class TurnSerialPacket(BasicSerialPacket):
    """
    A packet that instructs the droid to turn a specified angle.
    """

    def __init__(self, angle: Types.Degrees, speed: Types.Percentage):
        """
        Initialize a packet that instructs the droid to turn a specified angle, according to the following bytes:

            0. ``MOTORS`` serial packet type.
            1. ``TURN`` serial packet sub-type.
            2. ``angle`` the droid should turn.
            3. ``speed`` the droid should turn at.

        :param angle: angle the droid should turn clock-wise. Negative values signify counter-clock-wise rotation.
        :param speed: speed in which the rotation should occur.
        """

        angle_limit = Limits.SIGNED_PERCENTAGE
        percentage_limit = Limits.UNSIGNED_PERCENTAGE
        self._angle = angle
        self._speed = speed

        adjusted_angle = Consts.remap(angle, angle_limit.max, angle_limit.min, Consts.ComponentConstants.PWM_MAX_VALUE,
                                      Consts.ComponentConstants.PWM_MIN_VALUE)
        adjusted_speed = Consts.remap(speed, percentage_limit.max, percentage_limit.min,
                                      Consts.ComponentConstants.PWM_MAX_VALUE, Consts.ComponentConstants.PWM_MIN_VALUE)

        self._fields = [SerialConstants.MotorSerialPacketType.TURN.value, adjusted_angle, adjusted_speed]
        super().__init__(SerialConstants.SerialPacketType.MOTORS, bytes(self._fields))

    @staticmethod
    def from_bytes(byte_array: bytes):
        angle, speed, _ = struct.unpack(">BB", byte_array)

        angle_limit = Limits.TURN_ANGLE
        speed_limit = Limits.UNSIGNED_PERCENTAGE

        angle = Consts.remap(angle, Consts.ComponentConstants.PWM_MAX_VALUE, Consts.ComponentConstants.PWM_MIN_VALUE,
                             angle_limit.max, angle_limit.min)
        speed = Consts.remap(speed, Consts.ComponentConstants.PWM_MAX_VALUE, Consts.ComponentConstants.PWM_MIN_VALUE,
                             speed_limit.max, speed_limit.min)

        return TurnSerialPacket(angle, speed)

    @property
    def angle(self):
        return self._angle

    @property
    def speed(self):
        return self._speed
