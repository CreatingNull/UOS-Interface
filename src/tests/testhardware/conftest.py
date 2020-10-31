"""Module is used to initialise pytest fixtures for the hardware com tests."""
import pytest
from uosinterface.hardware import UOSDevice

devices = {
    "Arduino Nano 3 LAZY": {
        "identity": "Arduino Nano 3",
        "connection": "STUB|/dev/ttyUSB0",
        "loading": "LAZY",
    },
    "Arduino Nano 3 EAGER": {
        "identity": "Arduino Nano 3",
        "connection": "STUB|/dev/ttyUSB0",
        "loading": "EAGER",
    },
}


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_device(request):
    """Creates a fixture for testing through the abstraction layer."""
    device = UOSDevice(
        devices[request.param]["identity"],
        devices[request.param]["connection"],
        loading=devices[request.param]["loading"],
    )
    yield device
    device.close()


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_identities(request):
    """Creates the device definition from the for testing interface config."""
    return devices[request.param]["identity"], devices[request.param]["connection"]
