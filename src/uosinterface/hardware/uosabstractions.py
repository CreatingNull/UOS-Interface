"""Module defining the base class and static func for interfaces."""
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from functools import lru_cache
from typing import Dict
from typing import List
from typing import Tuple

from uosinterface import UOSUnsupportedError


@dataclass
class COMresult:
    """Containing the data structure used to capture UOS results."""

    status: bool
    exception: str = ""
    ack_packet: List = field(default_factory=list)
    rx_packets: List = field(default_factory=list)
    aux_data: Dict = field(default_factory=dict)


@dataclass
class InstructionArguments:
    """Containing the data structure used to generalise UOS arguments."""

    device_function_lut: Dict = field(default_factory=dict)
    payload: tuple = ()
    expected_rx_packets: int = 1
    check_pin: int = None


@dataclass
class SystemDevice:
    """Structure of the connection string components of a system device."""

    connection: str
    interface: str
    port: str


class UOSInterface(metaclass=ABCMeta):
    """Base class for low level UOS interfaces classes to inherit."""

    @abstractmethod
    def execute_instruction(self, address: int, payload: Tuple[int, ...]) -> COMresult:
        """
        Abstract method for executing instructions on UOSInterfaces.

        :param address: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param payload: A tuple containing the uint8 parameters of the UOS instruction.
        :returns: COM Result object.
        :raises: UOSUnsupportedError if the interface hasn't been built correctly.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.execute_instruction.__name__} prototype."
        )

    @abstractmethod
    def read_response(self, expect_packets: int, timeout_s: float) -> COMresult:
        """
        Abstract method for reading ACK and Data packets from a UOSInterface.

        :param expect_packets: How many packets including ACK to expect
        :param timeout_s: The maximum time this function will wait for data.
        :return: COM Result object.
        :raises: UOSUnsupportedError if the interface hasn't been built correctly.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.read_response.__name__} prototype."
        )

    @abstractmethod
    def hard_reset(self) -> COMresult:
        """
        UOS loop reset functionality should be as hard a reset as possible.

        :return: COM Result object.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.hard_reset.__name__} prototype"
        )

    @abstractmethod
    def open(self) -> bool:
        """
        Abstract method for opening a connection to a UOSInterface.

        :return: Success boolean.
        :raises: UOSUnsupportedError if the interface hasn't been built correctly.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.open.__name__} prototype."
        )

    @abstractmethod
    def close(self) -> bool:
        """
        Abstract method for closing a connection to a UOSInterface.

        :return: Success boolean.
        :raises: UOSUnsupportedError if the interface hasn't been built correctly.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.close.__name__} prototype."
        )

    @staticmethod
    @abstractmethod
    def enumerate_devices() -> [SystemDevice]:
        """
        Static method that should be functional if possible.

        :return: A list of possible SystemDevices on the server.
        :raises: UOSUnsupportedError if the interface hasn't been built correctly.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.enumerate_devices.__name__} prototype."
        )

    @staticmethod
    @lru_cache(maxsize=100)
    def get_npc_packet(to_addr: int, from_addr: int, payload: Tuple[int, ...]) -> bytes:
        """
        Static method to generate a standardised NPC packet.

        :param to_addr: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param from_addr: An 8 bit unsigned integer of the host system, usually 0.
        :param payload: A tuple containing the unsigned 8 bit integers of the command.
        :return: NPC packet as a bytes object. No bytes returned on fault.

        """
        if (
            to_addr < 256 and from_addr < 256 and len(payload) < 256
        ):  # check input is possible to parse
            packet_data = [to_addr, from_addr, len(payload)] + list(payload)
            lrc = UOSInterface.get_npc_checksum(packet_data)
            return bytes(
                [0x3E, packet_data[0], packet_data[1], len(payload)]
                + list(payload)
                + [lrc, 0x3C]
            )
        return bytes([])

    @staticmethod
    def get_npc_checksum(packet_data: [int]) -> int:
        """
        Static method to generate a NPC LRC checksum.

        :param packet_data: List of the uint8 values from an NPC packet.
        :return: NPC checksum as a 8 bit integer.

        """
        lrc = 0
        for byte in packet_data:
            lrc = (lrc + byte) & 0xFF
        return ((lrc ^ 0xFF) + 1) & 0xFF
