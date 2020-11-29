"""Module is used to initialise pytest fixtures for the hardware com tests."""
import pytest
from uosinterface.hardware import UOSDevice

DEVICES = {
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


@pytest.fixture(scope="package", params=list(DEVICES.keys()))
def uos_device(request):
    """Creates a fixture for testing through the abstraction layer."""
    device = UOSDevice(
        DEVICES[request.param]["identity"],
        DEVICES[request.param]["connection"],
        loading=DEVICES[request.param]["loading"],
    )
    yield device
    device.close()


@pytest.fixture(scope="package", params=list(DEVICES.keys()))
def uos_identities(request):
    """Creates the device definition from the for testing interface config."""
    return DEVICES[request.param]["identity"], DEVICES[request.param]["connection"]
