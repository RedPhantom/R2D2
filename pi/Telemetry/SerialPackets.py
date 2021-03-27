# Purpose: contain different kinds of serial packets.
import struct
from enum import IntEnum

from Limits import Limits, LimitNames


class SerialPacketType(IntEnum):
    """
    Holds different packet types.
    """

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


class MotorSerialPacketType(IntEnum):
    SPEED = 0x1


class BasicSerialPacket:
    """
    Models a basic serial packet.
    Packets are made out of a type, sub-type (determined by the packet itself) and raw data (as a byte array).
    """

    STRUCT_FORMAT = "Bs"
    """
    *struct*-compatible format for parsing serial packet data.
    
    - ``B`` - unsigned char.
    - ``s`` - char array.
    """

    def __init__(self, packet_type: SerialPacketType, data: bytes):
        """
        Initialize a new serial packet.
        For every packet inheriting this Base Serial Packet, the ``super()`` call should be at the end of
        the inheriting class' ``__init__(self)`` method.

        :param packet_type: 8-bit unsigned integer describing the type of the packet sent.
        :param data: data to write to the serial bus.
        """

        if packet_type not in SerialPacketType.__dict__.values():
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


class MotorSpeedSerialPacket(BasicSerialPacket):
    """
    A packet that orders a motor to be provided a voltage relative to its maximum voltage.
    Call the constructor with the required motor ID and speed, and then access the ``bytes`` property
    to receive the byte sequence to send via the serial bus.
    """

    def __init__(self, motor_id: int, speed: int):
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

        Limits.assert_limit(LimitNames.SIGNED_PERCENTAGE, speed)
        self._fields = [MotorSerialPacketType.SPEED.value, motor_id, speed.__int__()]
        super().__init__(SerialPacketType.MOTORS, bytes(self._fields))
