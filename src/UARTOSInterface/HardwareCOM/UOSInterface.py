""" Module defining the base class for all UOS device interfaces. """
from abc import abstractmethod, ABCMeta
from functools import lru_cache
from typing import Tuple
from UARTOSInterface.HardwareCOM.util import COMresult


class UOSInterface(metaclass=ABCMeta):
    """ Base class for low level UOS interfaces classes to inherit. """

    @abstractmethod
    def execute_instruction(self, address: int, payload: Tuple[int, ...]) -> COMresult:
        """ Abstract method for executing instructions on UOSInterfaces.
        :param address: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param payload: A tuple containing the unsigned 8 bit integer parameters of the UOS instruction.
        :returns: A tuple containing a success boolean at index 0 and a result-set dict at index 1.
        :raises: NotImplementedError if the interface hasn't been built correctly.
        """
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.execute_instruction.__name__} prototype."
        )

    @abstractmethod
    def read_response(self, expect_packets: int, timeout_s: float) -> COMresult:
        """ Abstract method for reading ACK and Data packets from a UOSInterface.
        :param expect_packets: How many packets including ACK to expect
        :param timeout_s: The maximum time this function will wait for data.
        :return: A tuple containing a success boolean at index 0 and a result-set dict at index 1.
        :raises: NotImplementedError if the interface hasn't been built correctly.
        """
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.read_response.__name__} prototype."
        )

    @abstractmethod
    def hard_reset(self) -> COMresult:
        """ Abstract method for UOS loop reset functionality should be as hard a reset as possible
        :return: A tuple containing a success boolean at index 0 and a result-set dict at index 1.
        """
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.hard_reset.__name__} prototype"
        )

    @abstractmethod
    def open(self) -> bool:
        """ Abstract method for opening a connection to a UOSInterface.
        :return: Success boolean.
        :raises: NotImplementedError if the interface hasn't been built correctly.
        """
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.open.__name__} prototype."
        )

    @abstractmethod
    def close(self) -> bool:
        """ Abstract method for closing a connection to a UOSInterface.
        :return: Success boolean.
        :raises: NotImplementedError if the interface hasn't been built correctly.
        """
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.close.__name__} prototype."
        )

    # function builds a static bytes object containing all the bytes to be transmitted in sequential order
    # in an npc compliant packet.
    @staticmethod
    @lru_cache(maxsize=100)
    def get_npc_packet(to_addr: int, from_addr: int, payload: Tuple[int, ...]) -> bytes:
        """ Static method to generate a standardised NPC packet.
        :param to_addr: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param from_addr: An 8 bit unsigned integer of the host system, usually 0.
        :param payload: A tuple containing the unsigned 8 bit integers of the command.
        :return: NPC packet as a bytes object. No bytes returned on fault.
        """
        if to_addr < 256 and from_addr < 256 and len(payload) < 256:  # check input is possible to parse
            packet_data = [to_addr, from_addr, len(payload)] + list(payload)
            lrc = UOSInterface.get_npc_checksum(packet_data)
            return bytes([0x3e, packet_data[0], packet_data[1], len(payload)] + list(payload) + [lrc, 0x3c])
        return bytes([])

    @staticmethod
    def get_npc_checksum(packet_data: [int]) -> int:
        """ Static method to generate a NPC LRC checksum.
        :param packet_data: List of all the 8-bit integers from an NPC packet that are used to generate a checksum.
        :return: NPC checksum as a 8 bit integer.
        """
        lrc = 0
        for byte in packet_data:
            lrc = (lrc + byte) & 0xff
        return ((lrc ^ 0xff) + 1) & 0xff
