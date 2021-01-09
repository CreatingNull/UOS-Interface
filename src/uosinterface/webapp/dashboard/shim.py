"""Module contains general device functions used within the dashboard."""
from logging import getLogger

from uosinterface.hardware import UOSDevice
from uosinterface.hardware.config import DEVICES


def get_system_info(device_identity, device_connection: str) -> {}:
    """Gets the 'version', 'type' and 'connection' and formats into dict."""
    uos_data = {}
    try:
        device = UOSDevice(
            identity=device_identity,
            connection=device_connection,
        )
        result = device.get_system_info()
        device.close()
        if result.status:
            uos_data["version"] = (
                f"V{result.rx_packets[0][4]}.{result.rx_packets[0][5]}."
                f"{result.rx_packets[0][6]}"
            )
            uos_data["connection"] = device.connection
            if f"HWID{result.rx_packets[0][7]}" in DEVICES:
                uos_data["type"] = f"{DEVICES[f'HWID{result.rx_packets[0][7]}'].name}"
    except (AttributeError, ValueError, NotImplementedError) as exception:
        getLogger(__name__).warning(
            "Cannot open connection to '%s', error: %s",
            device_connection,
            exception.__str__(),
        )
    return uos_data
