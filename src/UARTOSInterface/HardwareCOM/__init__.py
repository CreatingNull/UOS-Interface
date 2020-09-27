""" Module containing the high level hardware interface for communicating with UOS devices. """
import sys
from ast import literal_eval
from pathlib import Path
from logging import getLogger as Log
from configparser import ConfigParser
from UARTOSInterface.util import configure_logs
from UARTOSInterface.HardwareCOM.USBSerialDriver import NPCSerialPort
from UARTOSInterface.HardwareCOM.util import COMresult

SUPER_VOLATILE = 0
VOLATILE = 1
NON_VOLATILE = 2


def register_logs(level, base_path: Path):
    """ Configures the log files for the hardware COM package
    :param level: Set the logger level, debug ect. Use the constants from logging lib.
    :param base_path: Set the logging directory.
    """
    configure_logs(__name__, level=level, base_path=base_path)


class UOSDevice:
    """ Class for high level object-orientated control of UOS devices.
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
        """ Instantiate a UOS device instance for communication.
        :param identity: Specify the type of device, this must exist in the device dictionary.
        :param connection: Compliant connection string for isleepdentifying the device and interface.
        :param kwargs: Additional optional connection parameters as defined in documentation.
        """
        self.identity = identity
        self.connection = connection
        self.system_lut = self._locate_device_definition(identity)
        self.__kwargs = kwargs
        for key in self.system_lut:
            Log(__name__).debug(f"sys lut = {key}: {self.system_lut[key]}")
            # Select the low level backend-interface based on interface key
        if len(self.system_lut) == 0:
            raise NotImplementedError(f"'{self.identity}' does not have a valid look up table")
        connection_params = self.connection.split('|')
        if len(connection_params) != 2:
            raise ValueError(f"NPC connection string was incorrectly formatted, length={len(connection_params)}")
        if connection_params[0].upper() == "USB":
            self.__device_interface = NPCSerialPort(connection_params[1], baudrate=self.system_lut["default_baudrate"])
        else:
            raise AttributeError(f"Could not correctly open a connection to {self.identity} - {self.connection}")
        if "loading" in self.__kwargs and self.__kwargs["loading"].upper() == "EAGER":
            self.open()
        Log(__name__).debug(f"Created device {self.__device_interface.__repr__()}")

    def set_gpio_output(self, pin: int, level: int, volatility: int = SUPER_VOLATILE) -> COMresult:
        """ Sets a pin to digital output mode and sets a level on that pin.
        :param pin: The numeric number of the pin as defined in the dictionary for that device.
        :param level: The output level, 0 - low, 1 - High.
        :param volatility: How volatile should the command be, use constant values from HardwareCOM package.
        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.
        """
        response = self.__execute_instruction(
            UOSDevice.set_gpio_output.__name__,
            volatility,
            {
                "device_functions": self.system_lut["functions"],
                "payload": (pin, 0, level),
                "expected_packets": 1
            },
        )
        return response

    def get_gpio_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE) -> COMresult:
        """ Reads a GPIO pins level from device and returns the value
        :param pin: The numeric number of the pin as defined in the dictionary for that device.
        :param level: Not used currently, future will define pull-up state
        :param volatility: How volatile should the command be, use constant values from HardwareCOM package.
        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.
        """
        response = self.__execute_instruction(
            UOSDevice.get_gpio_input.__name__,
            volatility,
            {
                "device_functions": self.system_lut["functions"],
                "payload": (pin, 1, level),
                "expected_packets": 2
            }
        )
        return response

    def get_adc_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        self.__execute_instruction(UOSDevice.get_adc_input.__name__, volatility)

    def reset_all_io(self, volatility: int = NON_VOLATILE):
        self.__execute_instruction(UOSDevice.reset_all_io.__name__, volatility)

    def hard_reset(self) -> bool:
        response = self.__execute_instruction(
            UOSDevice.hard_reset.__name__,
            0,
            {"device_functions": self.system_lut["functions"]},
        )
        return response[0]

    def open(self):
        """ Opens a connection to the low level device, explict calls are normally not required.
        :raises: RuntimeError - If there was an issue opening a connection.
        :raises: Attribute Error - if bad configuration of the UOSDevice object.
        """
        if self.__device_interface is not None:
            if not self.__device_interface.open():
                raise RuntimeError("There was an error opening a connection to the device.")
        else:
            raise AttributeError("You can't open a connection on a empty device.")

    def close(self):
        """ Closes a connection to the low level device, must be called explicitly if loading is eager.
        :raises: RuntimeError - If there was a problem closing the connection to an active device.
        """
        if self.__device_interface is not None:
            if not self.__device_interface.close():
                raise RuntimeError("There was an error closing a connection to the device")

    def __execute_instruction(self, function_name: str, volatility, instruction_data: {}) -> COMresult:
        """ Helper function used to combine common functionality of the object orientated layer.
        :param function_name: The name of the function in the OOL.
        :param volatility: How volatile should the command be, use constant values from HardwareCOM package.
        :param instruction_data: device_functions from the LUT, payload ect.
        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.
        :raises: NotImplementedError if function is not possible on the loaded device.
        """
        if function_name not in self.system_lut["functions"] or volatility not in \
                self.system_lut["functions"][function_name]:
            raise NotImplementedError(
                f"{function_name} at volatility:{volatility} has not been implemented for {self.identity}"
            )
        rx_response = COMresult(False)
        if self.check_lazy():  # Lazy loaded
            self.open()
        if instruction_data["device_functions"][function_name][volatility] >= 0:  # a normal instruction
            tx_response = self.__device_interface.execute_instruction(
                instruction_data["device_functions"][function_name][volatility],
                instruction_data["payload"],
            )
            if tx_response.status:
                rx_response = self.__device_interface.read_response(instruction_data["expected_packets"], 2)
                if rx_response.status:
                    # validate checksums on all packets
                    # todo need to find a new way to do this with the data objects
                    for count in range(len(rx_response.rx_packets) + 1):
                        current_packet = rx_response.ack_packet if count == 0 else rx_response.rx_packets[count-1]
                        computed_checksum = self.__device_interface.get_npc_checksum(current_packet)
                        Log(__name__).debug(
                            f"Calculated checksum {computed_checksum} must match rx {current_packet[-2]}"
                        )
                        rx_response.status = rx_response.status & (computed_checksum == current_packet[-2])
        else:  # run a special action
            rx_response = getattr(self.__device_interface, function_name)()
        if self.check_lazy():  # Lazy loaded
            self.close()
        return rx_response

    def check_lazy(self) -> bool:
        """ Checks the loading type of the device lazy or eager.
        :return: Boolean, true is lazy.
        """
        if "loading" not in self.__kwargs or self.__kwargs["loading"].upper() == "LAZY":
            return True
        return False

    def __repr__(self):
        return f"<UOSDevice(connection='{self.connection}', identity='{self.identity}', " \
               f"system_lut={self.system_lut}, __device_interface='{self.__device_interface}', " \
               f"__kwargs={self.__kwargs})>"

    @staticmethod
    def _locate_device_definition(identity: str):
        """ Looks up the system dictionary ini for the defined device mappings
        :param identity: String containing the lookup key of the device in the dictionary
        :return: Dictionary of the device lookup table. Empty if no device located.
        """
        if getattr(sys, "frozen", False):  # running as packaged
            config_path = Path(sys.executable).resolve().parent
            config_path = config_path.joinpath("HardwareCOM.ini")
        else:  # running from source
            config_path = Path(__file__).resolve().parents[3]
            config_path = config_path.joinpath("resources/HardwareCOM.ini")
        Log(__name__).debug(f"Hardware config path resolved to {config_path}")
        if config_path.is_file():
            config = ConfigParser()
            config.read(config_path)
            try:
                output = {"functions": {}}
                section = f"DEVICE - {identity.upper()}"
                for key_name in ("digital_pins", "analogue_pins"):
                    output[key_name] = [int(pin.strip()) for pin in config[section][key_name].split(",")]
                for function_name in (
                        "set_gpio_output",
                        "get_gpio_input",
                        "get_adc_input",
                        "reset_all_io",
                        "hard_reset"
                ):
                    if f"function - {function_name}" in config[section]:  # just exclude undefined functions
                        output["functions"][function_name] = literal_eval(
                            config[section][f"function - {function_name}"]
                        )
                        output["functions"][function_name] = {  # populate as address lookup using the schema
                            volatility: literal_eval(config["UOS SCHEMA"][function_name])[volatility] for
                            volatility in output["functions"][function_name] if
                            output["functions"][function_name][volatility] is True
                        }
                output["default_baudrate"] = config[section]["default_baudrate"]
                output["interfaces"] = [interface.strip() for interface in config[section]["interfaces"].split(",")]
                return output
            except (KeyError, SyntaxError, ValueError) as e:
                Log(__name__).error(f"Parsing the hardware ini threw an error {e.__str__()}")
        return {}
