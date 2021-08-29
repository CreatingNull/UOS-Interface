"""Module contains general device functions used within the dashboard."""
from logging import getLogger

from flask import flash
from uosinterface.hardware import UOSDevice
from uosinterface.hardware.devices import DEVICES


def get_system_info(device_identity, device_address: str, **kwargs) -> {}:
    """
    Gets the 'version', 'type' and 'connection' and formats into dict.

    :param device_identity: Class of device being connected to.
    :param device_address: Connection string to the device.
    :param kwargs: Additional arguments that can be supplied to the UOS device.
    :return: Dictionary containing system data.

    """
    sys_data = {}
    try:
        device = UOSDevice(identity=device_identity, address=device_address, **kwargs)
        result = device.get_system_info()
        getLogger(__name__).debug("Shim queried device info %s", str(result))
        device.close()
        if result.status:
            sys_data["version"] = (
                f"V{result.rx_packets[0][4]}.{result.rx_packets[0][5]}."
                f"{result.rx_packets[0][6]}"
            )
            sys_data["address"] = device.address
            if f"hwid{result.rx_packets[0][7]}" in DEVICES:
                sys_data["type"] = f"{DEVICES[f'hwid{result.rx_packets[0][7]}'].name}"
            else:
                sys_data["type"] = "Unknown"
    except (AttributeError, ValueError, NotImplementedError, RuntimeError) as exception:
        message = (
            f"Cannot open connection to '{device_address}', info: {exception.__str__()}"
        )
        flash(message, "error")
        getLogger(__name__).error(message)
    return sys_data


def get_system_config(device_identity: str, device_address):
    """
    Gets the mode and level of all gpio configured on the device.

    :param device_identity: Class of device being connected to.
    :param device_address: Connection string to the device.
    :return: Dictionary containing 'gpioX' with 'mode'/'level' for each pin index X.

    """
    uos_data = {}
    try:
        device = UOSDevice(
            identity=device_identity,
            address=device_address,
        )
        for digital_pin in device.device.digital_pins:
            pin_config = device.get_gpio_config(digital_pin)
            getLogger(__name__).debug("Shim queried device info %s", str(pin_config))
            if pin_config.status:
                uos_data[digital_pin] = {
                    "current_mode": pin_config.rx_packets[0][4],
                    "current_level": pin_config.rx_packets[0][5],
                    "ram_mode": pin_config.rx_packets[0][6],
                    "ram_level": pin_config.rx_packets[0][7],
                    "eeprom_mode": pin_config.rx_packets[0][8],
                    "eeprom_level": pin_config.rx_packets[0][9],
                }
    except (AttributeError, ValueError, NotImplementedError, RuntimeError) as exception:
        message = (
            f"Cannot open connection to '{device_address}', info: {exception.__str__()}"
        )
        flash(message, "error")
        getLogger(__name__).error(message)
    return uos_data


def execute_digital_instruction(
    device_identity: str, device_address: str, set_output: bool, set_level: bool
) -> {}:
    """Configs the pin from form data and formats response into dict."""
    uos_data = {}
    try:
        device = UOSDevice(
            identity=device_identity,
            address=device_address,
        )
        # result = device.set_gpio_output()
        device.close()
    except (AttributeError, ValueError, NotImplementedError, RuntimeError) as exception:
        message = (
            f"Cannot open connection to '{device_address}', info: {exception.__str__()}"
        )
        flash(message, "error")
        getLogger(__name__).error(message)
    return uos_data
