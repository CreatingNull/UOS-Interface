import sys
from ast import literal_eval
from pathlib import Path
from logging import getLogger as Log
from configparser import ConfigParser
from UARTOSInterface.util import configure_logs


SUPER_VOLATILE = 0
VOLATILE = 1
NON_VOLATILE = 2


def register_logs(level, base_path: Path):
    configure_logs(__name__, level=level, base_path=base_path)


# object orientated control of the UOS system.
class UOSDevice:

    identity = ""
    connection = ""
    system_lut = {}

    def __init__(self, identity: str, connection: str = ""):
        self.identity = identity
        self.connection = connection
        self.system_lut = self._locate_device_definition(identity)
        for key in self.system_lut:
            Log(__name__).debug(f"sys lut = {key}: {self.system_lut[key]}")
        if len(self.system_lut) == 0:
            raise NotImplementedError(f"'{self.identity}' does not have a valid look up table")

    def set_gpio_output(self, pin: int, level: int, volatility: int = SUPER_VOLATILE) -> bool:
        self.__check_compatibility(UOSDevice.set_gpio_output.__name__)
        return True

    def get_gpio_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        self.__check_compatibility(UOSDevice.get_gpio_input.__name__)

    def get_adc_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        self.__check_compatibility(UOSDevice.get_adc_input.__name__)

    def reset_all_io(self, volatility: int = NON_VOLATILE):
        self.__check_compatibility(UOSDevice.reset_all_io.__name__)

    def close(self):
        return  # todo stub

    # Raises not implemented error if device does not support action
    def __check_compatibility(self, function_name: str):
        if function_name not in self.system_lut:
            raise NotImplementedError(f"{function_name} has not been implemented for {self.identity}")

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
                output["default_baudrate"] = config[section]["default_baudrate"]
                output["interfaces"] = [interface.strip() for interface in config[section]["interfaces"].split(",")]
                return output
            except (KeyError, SyntaxError, ValueError) as e:
                Log(__name__).error(f"Parsing the hardware ini threw an error {e.__str__()}")
                pass
        return {}
