"""The high level interface for communicating with UOS devices."""
from logging import getLogger as Log
from pathlib import Path

from UARTOSInterface.HardwareCOM.config import Device
from UARTOSInterface.HardwareCOM.config import DEVICES
from UARTOSInterface.HardwareCOM.config import INTERFACE_STUB
from UARTOSInterface.HardwareCOM.config import INTERFACE_USB
from UARTOSInterface.HardwareCOM.config import UOS_SCHEMA
from UARTOSInterface.HardwareCOM.LowLevelStub import NPCStub
from UARTOSInterface.HardwareCOM.UOSInterface import COMresult
from UARTOSInterface.HardwareCOM.UOSInterface import InstructionArguments
from UARTOSInterface.HardwareCOM.USBSerialDriver import NPCSerialPort
from UARTOSInterface.util import configure_logs

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


def _locate_device_definition(identity: str) -> Device:
    """
    Looks up the system config dictionary for the defined device mappings.

    :param identity: String containing the lookup key of the device in the dictionary.
    :return: Device Object or None if not found

    """
    if identity.upper() in DEVICES:
        device = DEVICES[identity.upper()]
        for function_enabled in device.functions_enabled:
            device.functions_enabled[function_enabled] = {
                vol: UOS_SCHEMA[function_enabled].address_lut[vol]
                for vol in device.functions_enabled[function_enabled]
            }
    else:
        device = None
    return device


def enumerate_devices() -> []:
    """Returns a list of all devices from all implemented interfaces."""
    output = []
    for interface in (
        NPCSerialPort,
        NPCStub,
    ):  # todo generalise interface clustering
        output.extend(interface.enumerate_devices())
    return output


class UOSDevice:
    """
    Class for high level object-orientated control of UOS devices.

    :ivar identity: The type of device, this is must have a valid section in the system_lut.
    :ivar connection: Compliant connection string for identifying the device and interface.
    :ivar system_lut: Device definitions as parsed from a compatible ini.
    :ivar __kwargs: Connection specific / optional parameters.
    :ivar __device_interface: Lower level communication protocol layer.

    """

    identity = ""
    connection = ""
    system_lut = {}
    __kwargs = {}
    __device_interface = None

    def __init__(self, identity: str, connection: str = "", **kwargs):
        """
        Instantiate a UOS device instance for communication.

        :param identity: Specify the type of device, this must exist in the device dictionary.
        :param connection: Compliant connection string for identifying the device and interface.
        :param kwargs: Additional optional connection parameters as defined in documentation.

        """
        self.identity = identity
        self.connection = connection
        self.system_lut = _locate_device_definition(identity)
        self.__kwargs = kwargs
        if self.system_lut is None:
            raise NotImplementedError(
                f"'{self.identity}' does not have a valid look up table"
            )
        connection_params = self.connection.split("|")
        if len(connection_params) != 2:
            raise ValueError(
                f"NPC connection string was incorrectly formatted, length={len(connection_params)}"
            )
        if (
            connection_params[0].upper() == INTERFACE_USB
            and INTERFACE_USB in self.system_lut.interfaces
        ):
            self.__device_interface = NPCSerialPort(
                connection_params[1],
                baudrate=self.system_lut.aux_params["default_baudrate"],
            )
        elif (
            connection_params[0].upper() == INTERFACE_STUB
            and INTERFACE_STUB in self.system_lut.interfaces
        ):
            self.__device_interface = NPCStub()
        else:
            raise AttributeError(
                f"Could not correctly open a connection to {self.identity} - {self.connection}"
            )
        if "loading" in self.__kwargs and self.__kwargs["loading"].upper() == "EAGER":
            self.open()
        Log(__name__).debug("Created device %s", self.__device_interface.__repr__())

    def set_gpio_output(
        self, pin: int, level: int, volatility: int = SUPER_VOLATILE
    ) -> COMresult:
        """
        Sets a pin to digital output mode and sets a level on that pin.

        :param pin: The numeric number of the pin as defined in the dictionary for that device.
        :param level: The output level, 0 - low, 1 - High.
        :param volatility: How volatile should the command be, use constants from HardwareCOM.
        :return: COMresult object.

        """
        response = self.__execute_instruction(
            UOSDevice.set_gpio_output.__name__,
            volatility,
            InstructionArguments(
                device_function_lut=self.system_lut.functions_enabled,
                payload=(pin, 0, level),
            ),
        )
        return response

    def get_gpio_input(
        self, pin: int, level: int, volatility: int = SUPER_VOLATILE
    ) -> COMresult:
        """
        Reads a GPIO pins level from device and returns the value.

        :param pin: The numeric number of the pin as defined in the dictionary for that device.
        :param level: Not used currently, future will define pull-up state.
        :param volatility: How volatile should the command be, use constants from HardwareCOM.
        :return: COMresult object.

        """
        response = self.__execute_instruction(
            UOSDevice.get_gpio_input.__name__,
            volatility,
            InstructionArguments(
                device_function_lut=self.system_lut.functions_enabled,
                payload=(pin, 1, level),
                expected_rx_packets=2,
            ),
        )
        return response

    def get_adc_input(
        self,
        pin: int,
        level: int,
        volatility: int = SUPER_VOLATILE,
    ) -> COMresult:
        """
        Reads the current 10 bit ADC value.

        :param pin: The index of the analogue pin to read
        :param level: Reserved for future use.
        :param volatility: How volatile should the command be, use constants from HardwareCOM.
        :return: COMresult object containing the ADC readings.

        """
        response = self.__execute_instruction(
            UOSDevice.get_adc_input.__name__,
            volatility,
            InstructionArguments(
                device_function_lut=self.system_lut.functions_enabled,
                payload=tuple([pin]),
                expected_rx_packets=2,
            ),
        )
        return response

    def get_system_info(self, **kwargs) -> COMresult:
        """
        Reads the UOS version and device type.

        :return: COMResult object containing the system information

        """
        response = self.__execute_instruction(
            UOSDevice.get_system_info.__name__,
            SUPER_VOLATILE,
            InstructionArguments(
                device_function_lut=self.system_lut.functions_enabled,
                expected_rx_packets=2,
            ),
        )
        return response

    def reset_all_io(self, volatility: int = NON_VOLATILE):
        """Executes the reset IO at the defined volatility level."""
        self.__execute_instruction(
            UOSDevice.reset_all_io.__name__,
            volatility,
            InstructionArguments(device_function_lut=self.system_lut.functions_enabled),
        )

    def hard_reset(self) -> COMresult:
        """Hard reset functionality for the UOS Device."""
        response = self.__execute_instruction(
            UOSDevice.hard_reset.__name__,
            0,
            InstructionArguments(device_function_lut=self.system_lut.functions_enabled),
        )
        return response

    def open(self):
        """
        Connects to the device, explict calls are normally not required.

        :raises: RuntimeError - If there was an issue opening a connection.
        :raises: Attribute Error - if bad configuration of the UOSDevice object.

        """
        if self.__device_interface is not None:
            if not self.__device_interface.open():
                raise RuntimeError(
                    "There was an error opening a connection to the device."
                )
        else:
            raise AttributeError("You can't open a connection on a empty device.")

    def close(self):
        """
        Releases connection, must be called explicitly if loading is eager.

        :raises: RuntimeError - If there was a problem closing the connection to an active device.

        """
        if self.__device_interface is not None:
            if not self.__device_interface.close():
                raise RuntimeError(
                    "There was an error closing a connection to the device"
                )

    def __execute_instruction(
        self, function_name: str, volatility, instruction_data: InstructionArguments
    ) -> COMresult:
        """
        Common functionality for execution of all UOS instructions.

        :param function_name: The name of the function in the OOL.
        :param volatility: How volatile should the command be, use constants in HardwareCOM.
        :param instruction_data: device_functions from the LUT, payload ect.
        :return: COMresult object
        :raises: NotImplementedError if function is not possible on the loaded device.

        """
        if (
            function_name not in self.system_lut.functions_enabled
            or volatility not in self.system_lut.functions_enabled[function_name]
        ):
            Log(__name__).debug(
                "Known functions %s", self.system_lut.functions_enabled.keys().__str__()
            )
            raise NotImplementedError(
                f"{function_name}({volatility}) has not been implemented for {self.identity}"
            )
        rx_response = COMresult(False)
        if self.check_lazy():  # Lazy loaded
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
        if self.check_lazy():  # Lazy loaded
            self.close()
        return rx_response

    def check_lazy(self) -> bool:
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
            f"<UOSDevice(connection='{self.connection}', identity='{self.identity}', "
            f"system_lut={self.system_lut}, __device_interface='{self.__device_interface}', "
            f"__kwargs={self.__kwargs})>"
        )
