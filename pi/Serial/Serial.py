# Purpose: provide serial bus communication capabilities.

import serial
import struct

from Consts import SerialConstants
from Serial import PacketMapping
from Serial.SerialPackets import BasicSerialPacket
from Telemetry.Exceptions import AppExceptions


class SerialCommunicator:
    """
    Communicates via the serial bus.
    """

    PACKET_TERMINATOR = b"\n"
    """
    Character describing the end of the packet. Parties will continue to read from the buffer
    until this character is reached.
    """

    def __init__(self, serial_device: str, baud_rate: int):
        """
        Initialize a new serial communication bus.

        :param serial_device: name of the serial device to connect via.
        :param baud_rate: communication rate (baud).
        """

        if baud_rate <= 0:
            raise ValueError("Argument 'baud_rate' must be > 0.")

        if serial_device is None or len(serial_device) == 0:
            raise ValueError("Argument 'serial_device' is invalid.")

        self._serial_device = serial_device
        self._baud_rate = baud_rate

        try:
            self._serial_port = serial.Serial(self._serial_device, self._baud_rate, timeout=2)
        except serial.SerialException as e:
            raise AppExceptions.SerialException(e)

    def __del__(self):
        self._serial_port.close()

    def send(self, packet: BasicSerialPacket):
        """
        Send the provided packet over the serial bus.
        """

        if not self._serial_port.is_open:
            raise AppExceptions.SerialException("Called send when serial port is closed.")

        try:
            self._serial_port.write(packet.bytes + self.PACKET_TERMINATOR)
        except serial.SerialException as e:
            raise AppExceptions.SerialException(e)

    def receive(self) -> BasicSerialPacket:
        """
        Read from the buffer the next serial packet.

        :return: a serial packet read from the serial bus.
        """

        if not self._serial_port.is_open:
            raise AppExceptions.SerialException("Called read when serial port is closed.")

        raw_data = self._serial_port.readline().rstrip(self.PACKET_TERMINATOR)
        packet_type, packet_subtype, packet_data = struct.unpack(SerialConstants.STRUCT_FORMAT, raw_data)

        if packet_type not in SerialConstants.SerialPacketType.__dict__.values():
            raise AppExceptions.SerialException("Received an invalid packet type.")

        packet_class = PacketMapping.PACKET_MAPPING[(packet_type, packet_subtype)]
        return packet_class(packet_data)

    @property
    def device_name(self):
        return self._serial_device

    @property
    def baud_rate(self):
        return self._baud_rate
