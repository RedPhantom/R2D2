# Purpose: contain unit tests for serial capabilities.
import unittest

from CustomTypes import LimitedSignedPercentage
from Telemetry.SerialPackets import MotorSpeedSerialPacket, SerialPacketType, MotorSerialPacketType


class BasicSanity(unittest.TestCase):
    def test_build_packets(self):
        """
        Ensure serial packets are build correctly.
        """

        # MotorSpeedSerialPacket
        motor_index = 5
        motor_speed = LimitedSignedPercentage(95)
        mssp = MotorSpeedSerialPacket(motor_index, motor_speed)
        mssp_bytes = bytes(
            [SerialPacketType.MOTORS, MotorSerialPacketType.SPEED, motor_index, motor_speed.__int__()])
        self.assertEqual(mssp_bytes, mssp.bytes,
                         "Expected specific byte sequence for MotorSpeedSerialPacket, got another.")
