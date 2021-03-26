# Purpose: contain different kinds of serial packets.
import struct
from enum import Enum
from typing import Dict

from CustomTypes import LimitedSignedPercentage


class SerialPacketType(Enum):
    """
    Holds different packet types.
    """

    MOTORS = 0x1
    SENSORS = 0x2

    # This packet type informs the receiver that the next packet is related to the previous one.
    CONT = 0xFE

    # This packet type informs the receive that the next packet is the last related packet to the previous one.
    LAST = 0xFF


# TODO: add motor packet, sensor packet, etc.

class BasicSerialPacket:
    """
    Models a basic serial packet.
    Packets are made out of a type and raw data.
    """

    STRUCT_FORMAT = "Bs"
    """
    *struct*-compatible format for parsing serial packet data.
    """

    def __init__(self, packet_type: SerialPacketType, data: bytes = ()):
        """
        Initialize a new serial packet.
        :param packet_type: 8-bit unsigned integer describing the type of the packet sent.
        :param data: data to write to the serial bus.
        """

        if packet_type not in SerialPacketType.__dict__.values():
            raise ValueError("The provided packet type (%d) is not supported." % packet_type)

        if not isinstance(data, bytes):
            raise TypeError("Data must be in form of a byte array.")

        self._packet_type = packet_type
        self._data = data

    def __str__(self, encoding="utf8"):
        """
        Retrieve the string representation of the packet.
        :param encoding: the encoding used to parse the packet data as.
        """

        return self._data.decode(encoding)

    def set(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError("Data must be in form of a byte array.")

        self._data = data

    @property
    def bytes(self):
        # B: unsigned char.
        # s: char[].
        return struct.pack(self.STRUCT_FORMAT, self._packet_type, self._data)


class MotorSpeedSerialPacket(BasicSerialPacket):
    def __init__(self, motor_speeds: Dict[int: LimitedSignedPercentage]):
        """
        TODO
        :param motor_speeds: dictionary of motor indexes and their speeds (as a percentage of the voltage they
        may receive. Negative values represent reverse rotation direction).
        """

        super(BasicSerialPacket, self).__init__(SerialPacketType.MOTORS)
        raise NotImplementedError
