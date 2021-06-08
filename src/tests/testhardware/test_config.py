"""Tests for the hardware configuration module."""
import pytest
from uosinterface import UOSUnsupportedError
from uosinterface.hardware import UOSDevice
from uosinterface.hardware.config import Pin


def test_get_compatible_pins(uos_device: UOSDevice):
    """
    Checks the device function for returning lists of compatible pins.

    :param uos_device:
    :return:

    """
    # Check lookup of digital pins works.
    if "set_gpio_output" in uos_device.system_lut.functions_enabled:
        pins = uos_device.system_lut.get_compatible_pins("set_gpio_output")
        assert len(pins) > 0
        assert isinstance(pins[next(iter(pins))], Pin)
        assert all(pins[pin].gpio_out for pin in pins)
    # Check lookup of analogue pins works.
    if "get_adc_input" in uos_device.system_lut.functions_enabled:
        pins = uos_device.system_lut.get_compatible_pins("get_adc_input")
        assert len(pins) > 0
        assert isinstance(pins[next(iter(pins))], Pin)
        assert all(pins[pin].adc_in for pin in pins)
    # Check lookup of function without pins returns empty list.
    pins = uos_device.system_lut.get_compatible_pins("hard_reset")
    assert isinstance(pins, dict)
    assert len(pins) == 0
    # Check bad function throws unsupported error
    with pytest.raises(UOSUnsupportedError):
        uos_device.system_lut.get_compatible_pins("not_a_uos_function")
