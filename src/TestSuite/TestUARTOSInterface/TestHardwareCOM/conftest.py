import pytest
from UARTOSInterface.HardwareCOM import UOSDevice

devices = {"Arduino Nano 3": "/dev/ttyUSB0"}


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_device(request):
    device = UOSDevice(request.param, devices[request.param])
    yield device
    device.close()


@pytest.fixture(scope="session", params=list(devices.keys()))
def uos_identities(request):
    return request.param, devices[request.param]
