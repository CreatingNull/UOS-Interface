"""Module defining supported hardware definitions."""
from enum import Enum

from uosinterface.hardware.uosabstractions import Device
from uosinterface.hardware.uosabstractions import Pin


class Interface(Enum):
    """Enumerates interfaces and their reference package names."""

    STUB = "NPCStub"
    USB = "NPCSerialPort"


ARDUINO_NANO_3 = Device(
    name="Arduino Nano 3",
    interfaces=[Interface.USB, Interface.STUB],
    functions_enabled={
        "set_gpio_output": {0: True},
        "get_gpio_input": {0: True},
        "get_adc_input": {0: True},
        "reset_all_io": {0: True},
        "hard_reset": {0: True},
        "get_system_info": {0: True},
        "get_gpio_config": {0: True},
    },
    digital_pins={
        2: Pin(gpio_out=True, gpio_in=True, pull_up=True, pc_int=True, hw_int=True),
        3: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pwm_out=True,
            pc_int=True,
            hw_int=True,
        ),
        4: Pin(gpio_out=True, gpio_in=True, pull_up=True, pc_int=True),
        5: Pin(gpio_out=True, gpio_in=True, pull_up=True, pwm_out=True, pc_int=True),
        6: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pwm_out=True,
            pc_int=True,
            comp={"type": "low", "bus": 0},
        ),
        7: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pc_int=True,
            comp={"type": "high", "bus": 0},
        ),
        8: Pin(gpio_out=True, gpio_in=True, pull_up=True, pc_int=True),
        9: Pin(gpio_out=True, gpio_in=True, pull_up=True, pwm_out=True, pc_int=True),
        10: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pwm_out=True,
            pc_int=True,
            spi={"type": "ss", "bus": 0},
        ),
        11: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pwm_out=True,
            pc_int=True,
            spi={"type": "mosi", "bus": 0},
        ),
        12: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pc_int=True,
            spi={"type": "miso", "bus": 0},
        ),
        13: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pc_int=True,
            i2c={"type": "sck", "bus": 0},
        ),
        14: Pin(
            gpio_out=True, gpio_in=True, pull_up=True, pc_int=True
        ),  # analogue pin 0
        15: Pin(
            gpio_out=True, gpio_in=True, pull_up=True, pc_int=True
        ),  # analogue pin 1
        16: Pin(
            gpio_out=True, gpio_in=True, pull_up=True, pc_int=True
        ),  # analogue pin 2
        17: Pin(
            gpio_out=True, gpio_in=True, pull_up=True, pc_int=True
        ),  # analogue pin 3
        18: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pc_int=True,
            i2c={"type": "sda", "bus": 0},
        ),  # analogue pin 4
        19: Pin(
            gpio_out=True,
            gpio_in=True,
            pull_up=True,
            pc_int=True,
            i2c={"type": "scl", "bus": 0},
        ),  # analogue pin 5
    },
    analogue_pins={
        0: Pin(adc_in=True),
        1: Pin(adc_in=True),
        2: Pin(adc_in=True),
        3: Pin(adc_in=True),
        4: Pin(adc_in=True),
        5: Pin(adc_in=True),
        6: Pin(adc_in=True),
        7: Pin(adc_in=True),
        8: Pin(adc_in=True),
    },
    aux_params={"default_baudrate": 115200},
)


DEVICES = {
    "HWID0": ARDUINO_NANO_3,
    "ARDUINO NANO 3": ARDUINO_NANO_3,
    "ARDUNIO NANO": ARDUINO_NANO_3,
}  # define aliases
