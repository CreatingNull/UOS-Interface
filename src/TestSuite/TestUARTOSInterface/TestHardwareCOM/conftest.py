import pytest
from pathlib import Path
from UARTOSInterface.HardwareCOM import UOSDevice
from UARTOSInterface.util import load_config

devices = {"Arduino Nano 3": "USB|/dev/ttyUSB0"}


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_device(request):
    device = UOSDevice(request.param, devices[request.param])
    yield device
    device.close()


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_identities(request):
    return request.param, devices[request.param]


@pytest.fixture(scope="session")
def hardware_config():
    base_dir = Path(__file__).resolve().parents[4]
    return load_config(base_dir.joinpath(Path("resources/HardwareCOM.ini")))
