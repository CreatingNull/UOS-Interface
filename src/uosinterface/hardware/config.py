"""Passive configuration file for the UOS Interface Hardware Layer."""
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import Dict
from typing import List

INTERFACE_USB = "USB"
INTERFACE_STUB = "STUB"


@dataclass
class UOSFunction:
    """Defines auxiliary information for UOS commands in the schema."""

    address_lut: Dict
    ack: bool
    rx_packets_expected: List = field(default_factory=list)
    required_arguments: List = None
    pin_requirements: List = None


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
class Pin:
    """Defines supported features of the pin."""

    gpio_out: bool = False
    gpio_in: bool = False
    dac_out: bool = False
    pwm_out: bool = False
    adc_in: bool = False
    pull_up: bool = False
    pull_down: bool = False
    pc_int: bool = False
    hw_int: bool = False
    timer: {} = field(default_factory=dict)
    comp: {} = field(default_factory=dict)
    spi: {} = field(default_factory=dict)
    i2c: {} = field(default_factory=dict)

    def get_dict(self):
        return {attrib.name: getattr(self, attrib.name) for attrib in fields(self)}


@dataclass
class Device:
    """Define an implemented UOS device dictionary."""

    name: str
    interfaces: list
    functions_enabled: Dict
    digital_pins: {int: Pin} = field(default_factory=dict)
    analogue_pins: {int: Pin} = field(default_factory=dict)
    aux_params: Dict = field(default_factory=dict)

    def get_compatible_pins(self, function_name: str) -> []:
        requirements = (
            UOS_SCHEMA[function_name].pin_requirements
            if function_name in UOS_SCHEMA
            else []
        )
        if requirements is None:  # pin is not relevant
            return []
        pin_dict = self.analogue_pins if "adc_in" in requirements else self.digital_pins
        return [
            pin
            for pin in pin_dict
            if all(  # check all pin requirements are met
                [getattr(pin_dict[pin], requirement) for requirement in requirements]
            )
        ]


ARDUINO_NANO_3 = Device(
    name="Arduino Nano 3",
    interfaces=[INTERFACE_USB, INTERFACE_STUB],
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
