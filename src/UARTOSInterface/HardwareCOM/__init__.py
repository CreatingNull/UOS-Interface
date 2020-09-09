import sys
from ast import literal_eval
from pathlib import Path
from logging import getLogger as Log
from configparser import ConfigParser
from UARTOSInterface.util import configure_logs
from UARTOSInterface.HardwareCOM.USBSerialDriver import NPCSerialPort


SUPER_VOLATILE = 0
VOLATILE = 1
NON_VOLATILE = 2


def register_logs(level, base_path: Path):
    configure_logs(__name__, level=level, base_path=base_path)


# object orientated control of the UOS system.
class UOSDevice:

    identity = ""  # The type of device, this is must have a valid section in the system_lut
    connection = ""  # Compliant connection string for identifying the device
    system_lut = {}  # Device definitions as parsed from a compatible ini
    __kwargs = {}  # Connection specific / optional parameters
    __device_interface = None  # Lower level communication protocol layer

    def __init__(self, identity: str, connection: str = "", **kwargs):
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
            self.__device_interface = NPCSerialPort(connection_params[1])
        else:
            raise AttributeError(f"Could not correctly open a connection to {self.identity} - {self.connection}")
        if "loading" in self.__kwargs and self.__kwargs["loading"].upper() == "EAGER":
            self.open()

    def set_gpio_output(self, pin: int, level: int, volatility: int = SUPER_VOLATILE) -> bool:
        response = self.__execute_instruction(
            UOSDevice.set_gpio_output.__name__,
            volatility,
            {
                "device_functions": self.system_lut["functions"],
                "payload": [pin, 0, level],
            },
        )
        return response[0]

    def get_gpio_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        self.__execute_instruction(UOSDevice.get_gpio_input.__name__, volatility)

    def get_adc_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        self.__execute_instruction(UOSDevice.get_adc_input.__name__, volatility)

    def reset_all_io(self, volatility: int = NON_VOLATILE):
        self.__execute_instruction(UOSDevice.reset_all_io.__name__, volatility)

    def open(self):
        if self.__device_interface is not None:
            if not self.__device_interface.open():
                raise RuntimeError("There was an error opening a connection to the device.")
        else:
            raise AttributeError("You can't open a connection on a empty device.")

    def close(self):
        if self.__device_interface is not None:
            if not self.__device_interface.close():
                raise RuntimeError("There was an error closing a connection to the device")

    # Raises not implemented error if device does not support action
    # If lazy loaded will open connection
    def __execute_instruction(self, function_name: str, volatility, instruction_data: {}) -> (bool, {}):
        if function_name not in self.system_lut["functions"] or volatility not in \
                self.system_lut["functions"][function_name]:
            raise NotImplementedError(
                f"{function_name} at volatility:{volatility} has not been implemented for {self.identity}"
            )
        if self.check_lazy():  # Lazy loaded
            self.open()
        return_data = self.__device_interface.execute_instruction(
            instruction_data["device_functions"][function_name][volatility],
            instruction_data["payload"],
        )
        if self.check_lazy():  # Lazy loaded
            self.close()
        return return_data

    def check_lazy(self) -> bool:
        if "loading" not in self.__kwargs or self.__kwargs["loading"].upper() == "LAZY":
            return True
        return False

    def __repr__(self):
        return f"<UOSDevice(connection='{self.connection}', identity='{self.identity}', " \
               f"system_lut={self.system_lut}, __device_interface='{self.__device_interface}', " \
               f"__kwargs={self.__kwargs})>"

    @staticmethod
    def _locate_device_definition(identity: str):
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
                for function_name in ("set_gpio_output", "set_gpio_input", "get_adc_input", "reset_all_io"):
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
