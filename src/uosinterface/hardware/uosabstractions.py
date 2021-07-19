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
class UOSFunction:
    """Defines auxiliary information for UOS commands in the schema."""

    address_lut: dict
    ack: bool
    rx_packets_expected: list = field(default_factory=list)
    required_arguments: list = None
    pin_requirements: list = None


UOS_SCHEMA = {
    "set_gpio_output": UOSFunction(
        address_lut={0: 64},
        ack=True,
        required_arguments=[None, 0, None],  # pin index, io type, level.
        pin_requirements=["gpio_out"],
    ),
    "get_gpio_input": UOSFunction(
        address_lut={0: 64},
        ack=True,
        rx_packets_expected=[1],
        required_arguments=[None, 1, None],  # pin index, io type, level.
        pin_requirements=["gpio_in"],
    ),
    "get_adc_input": UOSFunction(
        address_lut={0: 85},
        ack=True,
        rx_packets_expected=[2],
        pin_requirements=["adc_in"],
    ),
    "reset_all_io": UOSFunction(address_lut={0: 68}, ack=True),
    "hard_reset": UOSFunction(address_lut={0: -1}, ack=False),
    "get_system_info": UOSFunction(
        address_lut={0: 250}, ack=True, rx_packets_expected=[6]
    ),
    "get_gpio_config": UOSFunction(
        address_lut={0: 251},
        ack=True,
        rx_packets_expected=[2],
        pin_requirements=[],
    ),
}


@dataclass
class ComResult:
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


class UOSInterface(metaclass=ABCMeta):
    """Base class for low level UOS interfaces classes to inherit."""

    @abstractmethod
    def execute_instruction(self, address: int, payload: Tuple[int, ...]) -> ComResult:
        """
        Abstract method for executing instructions on UOSInterfaces.

        :param address: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param payload: A tuple containing the uint8 parameters of the UOS instruction.
        :returns: ComResult object.
        :raises: UOSUnsupportedError if the interface hasn't been built correctly.

        """
        raise UOSUnsupportedError(
            f"UOSInterfaces must over-ride {UOSInterface.execute_instruction.__name__} prototype."
        )

    @abstractmethod
    def read_response(self, expect_packets: int, timeout_s: float) -> ComResult:
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
    def hard_reset(self) -> ComResult:
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
    def enumerate_devices() -> []:
        """
        Static method that should be functional if possible.

        :return: A list of possible UOSInterfaces on the server.
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
    def get_npc_checksum(packet_data: list[int]) -> int:
        """
        Static method to generate a NPC LRC checksum.

        :param packet_data: List of the uint8 values from an NPC packet.
        :return: NPC checksum as a 8 bit integer.

        """
        lrc = 0
        for byte in packet_data:
            lrc = (lrc + byte) & 0xFF
        return ((lrc ^ 0xFF) + 1) & 0xFF


@dataclass
class Pin:
    """Defines supported features of the pin."""

    # pylint: disable=too-many-instance-attributes
    # Due to the nature of embedded pin complexity.

    gpio_out: bool = False
    gpio_in: bool = False
    dac_out: bool = False
    pwm_out: bool = False
    adc_in: bool = False
    pull_up: bool = False
    pull_down: bool = False
    pc_int: bool = False
    hw_int: bool = False
    timer: dict = field(default_factory=dict)
    comp: dict = field(default_factory=dict)
    spi: dict = field(default_factory=dict)
    i2c: dict = field(default_factory=dict)


@dataclass
class Device:
    """Define an implemented UOS device dictionary."""

    name: str
    interfaces: list
    functions_enabled: dict
    digital_pins: dict = field(default_factory=dict)
    analogue_pins: dict = field(default_factory=dict)
    aux_params: dict = field(default_factory=dict)

    def get_compatible_pins(self, function_name: str) -> {}:
        """
        Returns a dict of pin objects that are suitable for a function.

        :param function_name: the string name of the UOS Schema function.
        :return: Dict of pin objects, keyed on pin index.

        """
        if function_name not in UOS_SCHEMA:
            raise UOSUnsupportedError(f"UOS function {function_name} doesn't exist.")
        requirements = UOS_SCHEMA[function_name].pin_requirements
        if requirements is None:  # pins are not relevant to this function
            return {}
        pin_dict = self.analogue_pins if "adc_in" in requirements else self.digital_pins
        return {
            pin: pin_dict[pin]
            for pin in pin_dict
            if all(hasattr(pin_dict[pin], requirement) for requirement in requirements)
        }
