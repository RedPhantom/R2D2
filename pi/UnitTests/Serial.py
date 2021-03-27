# Purpose: contain unit tests for serial capabilities.

import unittest

from Consts import SerialConstants, Types
from Serial.SerialPackets import MotorSpeedSerialPacket


class BasicSanity(unittest.TestCase):
    def test_build_packets(self):
        """
        Ensure serial packets are build correctly.
        """

        # MotorSpeedSerialPacket
        motor_index = 5
        motor_speed = Types.Percentage(95)
        mssp = MotorSpeedSerialPacket(motor_index, motor_speed)
        fields = [SerialConstants.SerialPacketType.MOTORS,
                  SerialConstants.MotorSerialPacketType.SPEED,
                  motor_index,
                  motor_speed.__int__()]
        mssp_bytes = bytes(fields)
        self.assertEqual(mssp_bytes, mssp.bytes,
                         "Expected specific byte sequence for MotorSpeedSerialPacket, got another.")
