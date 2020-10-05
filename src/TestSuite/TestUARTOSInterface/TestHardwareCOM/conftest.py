"""Module is used to initialise pytest fixtures for the hardware com tests."""
import pytest
from pathlib import Path
from UARTOSInterface.HardwareCOM import UOSDevice
from UARTOSInterface.util import load_config

devices = {
    "Arduino Nano 3 LAZY": {
        "identity": "Arduino Nano 3",
        "connection": "USB|/dev/ttyUSB0",
        "loading": "LAZY",
    },
    "Arduino Nano 3 EAGER": {
        "identity": "Arduino Nano 3",
        "connection": "USB|/dev/ttyUSB0",
        "loading": "EAGER",
    },
}


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_device(request):
    device = UOSDevice(
        devices[request.param]["identity"],
        devices[request.param]["connection"],
        loading=devices[request.param]["loading"],
    )
    yield device
    device.close()


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_identities(request):
    return devices[request.param]["identity"], devices[request.param]["connection"]


@pytest.fixture(scope="session")
def hardware_config():
    base_dir = Path(__file__).resolve().parents[4]
    return load_config(base_dir.joinpath(Path("resources/HardwareCOM.ini")))
