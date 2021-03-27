# Purpose: map packet type and sub-type to BasicSerialPacket subclasses.

from Serial.SerialPackets import SerialConstants, CoreSleepSerialPacket, MotorSpeedSerialPacket, DriveSerialPacket, \
    TurnSerialPacket

PACKET_MAPPING = {
    (SerialConstants.SerialPacketType.CORE, SerialConstants.CoreSerialPacketType.SLEEP): CoreSleepSerialPacket,
    (SerialConstants.SerialPacketType.MOTORS, SerialConstants.MotorSerialPacketType.SPEED): MotorSpeedSerialPacket,
    (SerialConstants.SerialPacketType.MOTORS, SerialConstants.MotorSerialPacketType.DRIVE): DriveSerialPacket,
    (SerialConstants.SerialPacketType.MOTORS, SerialConstants.MotorSerialPacketType.TURN): TurnSerialPacket,
}
"""
Mapping of packets' type and sub-type to classes.
"""
