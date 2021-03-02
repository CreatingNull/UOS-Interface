"""Module contains general device functions used within the dashboard."""
from logging import getLogger

from flask import flash
from uosinterface.hardware import UOSDevice
from uosinterface.hardware.config import DEVICES


def get_system_info(device_identity, device_connection: str) -> {}:
    """
    Gets the 'version', 'type' and 'connection' and formats into dict.

    :param device_identity: Class of device being connected to.
    :param device_connection: Connection string to the device.
    :return: Dictionary containing 'version', 'connection', and 'type', empty if fails.

    """
    uos_data = {}
    try:
        device = UOSDevice(
            identity=device_identity,
            connection=device_connection,
        )
        result = device.get_system_info()
        getLogger(__name__).debug("Shim queried device info %s", str(result))
        device.close()
        if result.status:
            uos_data["version"] = (
                f"V{result.rx_packets[0][4]}.{result.rx_packets[0][5]}."
                f"{result.rx_packets[0][6]}"
            )
            uos_data["connection"] = device.connection
            if f"HWID{result.rx_packets[0][7]}" in DEVICES:
                uos_data["type"] = f"{DEVICES[f'HWID{result.rx_packets[0][7]}'].name}"
            else:
                uos_data["type"] = "Unknown"
    except (AttributeError, ValueError, NotImplementedError, RuntimeError) as exception:
        message = f"Cannot open connection to '{device_connection}', info: {exception.__str__()}"
        flash(message, "error")
        getLogger(__name__).error(message)
    return uos_data


def execute_digital_instruction(
    device_identity: str, device_connection: str, set_output: bool, set_level: bool
) -> {}:
    """Configs the pin from form data and formats response into dict."""
    uos_data = {}
    return uos_data
