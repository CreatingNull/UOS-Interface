"""Module for package test configuration, scope=session."""
import pytest
from uosinterface.hardware import UOSDevice
from uosinterface.hardware.config import Interface

DEVICES = {
    "Arduino Nano 3 LAZY": {
        "identity": "Arduino Nano 3",
        "address": "/dev/ttyUSB0",
        "interface": Interface.STUB,
        "loading": "LAZY",
    },
    "Arduino Nano 3 EAGER": {
        "identity": "Arduino Nano 3",
        "address": "/dev/ttyUSB0",
        "interface": Interface.STUB,
        "loading": "EAGER",
    },
}


@pytest.fixture(scope="session", params=list(DEVICES.keys()))
def uos_device(request):
    """Creates a fixture for testing through the abstraction layer."""
    device = UOSDevice(
        DEVICES[request.param]["identity"],
        DEVICES[request.param]["address"],
        DEVICES[request.param]["interface"],
        loading=DEVICES[request.param]["loading"],
    )
    yield device
    device.close()


@pytest.fixture(scope="session", params=list(DEVICES.keys()))
def uos_errored_device(request):
    """Creates a fixture for testing through the abstraction layer."""
    return UOSDevice(
        DEVICES[request.param]["identity"],
        DEVICES[request.param]["address"],
        DEVICES[request.param]["interface"],
        loading=DEVICES[request.param]["loading"],
        errored=1,
    )


@pytest.fixture(scope="session", params=list(DEVICES.keys()))
def uos_identities(request):
    """Creates the device definition for testing interface config."""
    return DEVICES[request.param]


def pytest_addoption(parser):
    """Adds USB serial connection optional CLI argument."""
    parser.addoption("--usb-serial", action="store", default=None)
