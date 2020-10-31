"""Passive configuration file for the UOS Interface Hardware Layer."""
from dataclasses import dataclass, field
from typing import List, Dict

INTERFACE_USB = "USB"
INTERFACE_STUB = "STUB"


@dataclass
class Device:
    """Define an implemented UOS device dictionary."""

    interfaces: list
    functions_enabled: Dict
    digital_pins: List = field(default_factory=list)
    analogue_pins: List = field(default_factory=list)
    aux_params: Dict = field(default_factory=dict)


@dataclass
class UOSFunction:
    """Defines auxiliary information for UOS commands in the schema."""

    address_lut: Dict
    ack: bool
    rx_packets_expected: List = field(default_factory=list)


UOS_SCHEMA = {
    "set_gpio_output": UOSFunction(address_lut={0: 64}, ack=True),
    "get_gpio_input": UOSFunction(
        address_lut={0: 64}, ack=True, rx_packets_expected=[1]
    ),
    "get_adc_input": UOSFunction(
        address_lut={0: 85}, ack=True, rx_packets_expected=[2]
    ),
    "reset_all_io": UOSFunction(address_lut={0: 68}, ack=True),
    "hard_reset": UOSFunction(address_lut={0: -1}, ack=False),
    "get_system_info": UOSFunction(
        address_lut={0: 250}, ack=True, rx_packets_expected=[4]
    ),
}


ARDUINO_NANO_3 = Device(
    interfaces=[INTERFACE_USB, INTERFACE_STUB],
    functions_enabled={
        "set_gpio_output": {0: True},
        "get_gpio_input": {0: True},
        "get_adc_input": {0: True},
        "reset_all_io": {0: True},
        "hard_reset": {0: True},
        "get_system_info": {0: True},
    },
    digital_pins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    analogue_pins=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    aux_params={"default_baudrate": 115200},
)

DEVICES = {
    "ARDUINO NANO 3": ARDUINO_NANO_3,
    "ARDUNIO NANO": ARDUINO_NANO_3,
}  # define aliases
