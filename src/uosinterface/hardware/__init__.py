"""The high level interface for communicating with UOS devices."""
import sys
from logging import getLogger as Log
from pathlib import Path
from typing import Union

from uosinterface import UOSCommunicationError
from uosinterface import UOSConfigurationError
from uosinterface import UOSUnsupportedError
from uosinterface.hardware.config import Device
from uosinterface.hardware.config import DEVICES
from uosinterface.hardware.config import Interface
from uosinterface.hardware.config import UOS_SCHEMA
from uosinterface.hardware.stub import NPCStub
from uosinterface.hardware.uosabstractions import ComResult
from uosinterface.hardware.uosabstractions import InstructionArguments
from uosinterface.hardware.usbserial import NPCSerialPort
from uosinterface.util import configure_logs

SUPER_VOLATILE = 0
VOLATILE = 1
NON_VOLATILE = 2


def register_logs(level, base_path: Path):
    """
    Configures the log files for the hardware COM package.

    :param level: Set the logger level, debug ect. Use the constants from logging lib.
    :param base_path: Set the logging directory.

    """
    configure_logs(__name__, level=level, base_path=base_path)


def get_device_definition(identity: str) -> Device:
    """
    Looks up the system config dictionary for the defined device mappings.

    :param identity: String containing the lookup key of the device in the dictionary.
    :return: Device Object or None if not found

    """
    if identity is not None and identity.upper() in DEVICES:
        device = DEVICES[identity.upper()]
        for function_enabled in device.functions_enabled:
            device.functions_enabled[function_enabled] = {
                vol: UOS_SCHEMA[function_enabled].address_lut[vol]
                for vol in device.functions_enabled[function_enabled]
            }
    else:
        device = None
    return device


def enumerate_system_devices(interface_filter: Interface = None) -> []:
    """
    Iterates through all interfaces and locates available devices.

    :param interface_filter: Interface enum to limit the search to a single interface type.
    :return: A list of uosinterface objects.

    """
    devices = []
    for interface in Interface:  # enum object
        if not interface_filter or interface_filter == interface:
            devices.extend(
                getattr(sys.modules[__name__], interface.value).enumerate_devices()
            )
        if interface_filter is not None:
            break
    return devices


class UOSDevice:
    """
    Class for high level object-orientated control of UOS devices.

    :ivar identity: The type of device, this is must have a valid device in the config.
    :ivar connection: Compliant connection string for identifying the device and interface.
    :ivar device: Device definitions as parsed from a compatible ini.
    :ivar __kwargs: Connection specific / optional parameters.
    :ivar __device_interface: Lower level communication protocol layer.

    """

    identity = ""
    address = ""
    device = Device
    __kwargs = {}
    __device_interface = None

    def __init__(
        self, identity: Union[str, Device], address: str, interface: Interface, **kwargs
    ):
        """
        Instantiate a UOS device instance for communication.

        :param identity: Specify the type of device, this must exist in the device dictionary.
        :param address: Compliant connection string for identifying the device and interface.
        :param interface: Set the type of interface to use for communication.
        :param kwargs: Additional optional connection parameters as defined in documentation.

        """
        self.identity = identity
        self.address = address
        if isinstance(identity, str):
            self.device = get_device_definition(identity)
        else:
            self.device = identity
        self.__kwargs = kwargs
        if self.device is None:
            raise UOSUnsupportedError(
                f"'{self.identity}' does not have a valid look up table"
            )
        if interface == Interface.USB and Interface.USB in self.device.interfaces:
            self.__device_interface = NPCSerialPort(
                address,
                baudrate=self.device.aux_params["default_baudrate"],
            )
        elif interface == Interface.STUB and Interface.STUB in self.device.interfaces:
            self.__device_interface = NPCStub(
                connection=address,
                errored=(kwargs["errored"] if "errored" in kwargs else False),
            )
        else:
            raise UOSCommunicationError(
                f"Could not correctly open a connection to {self.identity} - {self.address}"
            )
        if not self.is_lazy():  # eager connections open when they are created
            self.open()
        Log(__name__).debug("Created device %s", self.__device_interface.__repr__())

    def set_gpio_output(
        self, pin: int, level: int, volatility: int = SUPER_VOLATILE
    ) -> ComResult:
        """
        Sets a pin to digital output mode and sets a level on that pin.

        :param pin: The numeric number of the pin as defined in the dictionary for that device.
        :param level: The output level, 0 - low, 1 - High.
        :param volatility: How volatile should the command be, use constants from HardwareCOM.
        :return: ComResult object.

        """
        return self.__execute_instruction(
            UOSDevice.set_gpio_output.__name__,
            volatility,
            InstructionArguments(
                device_function_lut=self.device.functions_enabled,
                payload=(pin, 0, level),
                check_pin=pin,
            ),
        )

    def get_gpio_input(
        self, pin: int, level: int, volatility: int = SUPER_VOLATILE
    ) -> ComResult:
        """
        Reads a GPIO pins level from device and returns the value.

        :param pin: The numeric number of the pin as defined in the dictionary for that device.
        :param level: Not used currently, future will define pull-up state.
        :param volatility: How volatile should the command be, use constants from HardwareCOM.
        :return: ComResult object.

        """
        return self.__execute_instruction(
            UOSDevice.get_gpio_input.__name__,
            volatility,
            InstructionArguments(
                device_function_lut=self.device.functions_enabled,
                payload=(pin, 1, level),
                expected_rx_packets=2,
                check_pin=pin,
            ),
        )

    def get_adc_input(
        self,
        pin: int,
        level: int,
        volatility: int = SUPER_VOLATILE,
    ) -> ComResult:
        """
        Reads the current 10 bit ADC value.

        :param pin: The index of the analogue pin to read
        :param level: Reserved for future use.
        :param volatility: How volatile should the command be, use constants from HardwareCOM.
        :return: ComResult object containing the ADC readings.

        """
        return self.__execute_instruction(
            UOSDevice.get_adc_input.__name__,
            volatility,
            InstructionArguments(
                device_function_lut=self.device.functions_enabled,
                payload=tuple([pin]),
                expected_rx_packets=2,
                check_pin=pin,
            ),
        )

    def get_system_info(self, **kwargs) -> ComResult:
        """
        Reads the UOS version and device type.

        :param kwargs: Control arguments, accepts volatility.
        :return: ComResult object containing the system information.

        """
        return self.__execute_instruction(
            UOSDevice.get_system_info.__name__,
            kwargs["volatility"] if "volatility" in kwargs else SUPER_VOLATILE,
            InstructionArguments(
                device_function_lut=self.device.functions_enabled,
                expected_rx_packets=2,
            ),
        )

    def get_gpio_config(self, pin: int, **kwargs) -> ComResult:
        """
        Reads the configuration for a digital pin on the device.

        :param pin: Defines the pin for config querying.
        :param kwargs: Control arguments accepts volatility.
        :return: ComResult object containing the system information.

        """
        return self.__execute_instruction(
            UOSDevice.get_gpio_config.__name__,
            kwargs["volatility"] if "volatility" in kwargs else SUPER_VOLATILE,
            InstructionArguments(
                device_function_lut=self.device.functions_enabled,
                payload=tuple([pin]),
                expected_rx_packets=2,
                check_pin=pin,
            ),
        )

    def reset_all_io(self, **kwargs) -> ComResult:
        """Executes the reset IO at the defined volatility level."""
        return self.__execute_instruction(
            UOSDevice.reset_all_io.__name__,
            kwargs["volatility"] if "volatility" in kwargs else SUPER_VOLATILE,
            InstructionArguments(device_function_lut=self.device.functions_enabled),
        )

    def hard_reset(self, **kwargs) -> ComResult:
        """Hard reset functionality for the UOS Device."""
        return self.__execute_instruction(
            UOSDevice.hard_reset.__name__,
            kwargs["volatility"] if "volatility" in kwargs else SUPER_VOLATILE,
            InstructionArguments(device_function_lut=self.device.functions_enabled),
        )

    def open(self):
        """
        Connects to the device, explict calls are normally not required.

        :raises: UOSCommunicationError - Problem opening a connection.

        """
        if not self.__device_interface.open():
            raise UOSCommunicationError(
                "There was an error opening a connection to the device."
            )

    def close(self):
        """
        Releases connection, must be called explicitly if loading is eager.

        :raises: UOSCommunicationError - Problem closing the connection to an active device.

        """
        if not self.__device_interface.close():
            raise UOSCommunicationError(
                "There was an error closing a connection to the device"
            )

    def __execute_instruction(
        self,
        function_name: str,
        volatility,
        instruction_data: InstructionArguments,
        retry: bool = True,
    ) -> ComResult:
        """
        Common functionality for execution of all UOS instructions.

        :param function_name: The name of the function in the OOL.
        :param volatility: How volatile should the command be, use constants in HardwareCOM.
        :param instruction_data: device_functions from the LUT, payload ect.
        :param retry: Allows the instruction to retry execution when fails.
        :return: ComResult object
        :raises: UOSUnsupportedError if function is not possible on the loaded device.

        """
        if (
            function_name not in self.device.functions_enabled
            or volatility not in self.device.functions_enabled[function_name]
            or (
                instruction_data.check_pin is not None
                and instruction_data.check_pin
                not in self.device.get_compatible_pins(function_name)
            )
        ):
            Log(__name__).debug(
                "Known functions %s", self.device.functions_enabled.keys().__str__()
            )
            raise UOSUnsupportedError(
                f"{function_name}({volatility}) has not been implemented for {self.identity}"
            )
        rx_response = ComResult(False)
        if self.is_lazy():  # Lazy loaded
            self.open()
        if (
            instruction_data.device_function_lut[function_name][volatility] >= 0
        ):  # a normal instruction
            tx_response = self.__device_interface.execute_instruction(
                instruction_data.device_function_lut[function_name][volatility],
                instruction_data.payload,
            )
            if tx_response.status:
                rx_response = self.__device_interface.read_response(
                    instruction_data.expected_rx_packets, 2
                )
                if rx_response.status:
                    # validate checksums on all packets
                    for count in range(len(rx_response.rx_packets) + 1):
                        current_packet = (
                            rx_response.ack_packet
                            if count == 0
                            else rx_response.rx_packets[count - 1]
                        )
                        computed_checksum = self.__device_interface.get_npc_checksum(
                            current_packet[1:-2]
                        )
                        Log(__name__).debug(
                            "Calculated checksum %s must match rx %s",
                            computed_checksum,
                            current_packet[-2],
                        )
                        rx_response.status = rx_response.status & (
                            computed_checksum == current_packet[-2]
                        )
        else:  # run a special action
            rx_response = getattr(self.__device_interface, function_name)()
        if self.is_lazy():  # Lazy loaded
            self.close()
        if (
            not rx_response.status and retry
        ):  # allow one retry per instruction due to DTR resets
            return self.__execute_instruction(
                function_name, volatility, instruction_data, False
            )
        return rx_response

    def is_lazy(self) -> bool:
        """
        Checks the loading type of the device lazy or eager.

        :return: Boolean, true is lazy.

        """
        if "loading" not in self.__kwargs or self.__kwargs["loading"].upper() == "LAZY":
            return True
        return False

    def __repr__(self):
        """
        Over-rides the built in repr with something useful.

        :return: String containing connection and identity of the device

        """
        return (
            f"<UOSDevice(address='{self.address}', identity='{self.identity}', "
            f"device={self.device}, __device_interface='{self.__device_interface}', "
            f"__kwargs={self.__kwargs})>"
        )
