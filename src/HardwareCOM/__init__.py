import sys
from pathlib import Path
from util import configure_logs, log, DEBUG


SUPER_VOLATILE = 0
VOLATILE = 1
NON_VOLATILE = 2


def init_logs(level: int):
    configure_logs(__name__, level)


# object orientated control of the UOS system.
class UOSDevice:

    identity = ""
    connection = ""
    system_lut = {}

    def __init__(self, identity: str, connection: str=""):
        self.identity = identity
        self.connection = connection
        self.system_lut = self._locate_device_definition(identity)

    def set_gpio_output(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        return  # todo stub

    def get_gpio_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        return  # todo stub

    def get_adc_input(self, pin: int, level: int, volatility: int = SUPER_VOLATILE):
        return  # todo stub

    def reset_all_io(self, volatility: int = NON_VOLATILE):
        return  # todo stub

    def close(self):
        return  # todo stub

    @staticmethod
    def _locate_device_definition(identity: str):
        if getattr(sys, 'frozen', False):  # running as packaged
            config_path = Path(sys.executable).resolve().parent
            config_path = config_path.joinpath('HardwareCOM.ini')
        else:  # running from source
            config_path = Path(__file__).resolve().parent.parent.parent
            config_path = config_path.joinpath('resources/HardwareCOM.ini')
        log(f"Hardware config path resolved to {config_path}", level=DEBUG, name=__name__)
        return {}  # todo stub
