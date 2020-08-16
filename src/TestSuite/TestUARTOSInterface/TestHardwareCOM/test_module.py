import pytest
from UARTOSInterface.HardwareCOM import UOSDevice


# Checks to ensure all defined devices can init correctly on the UOSDevice class, makes sure no error is thrown
def test_implemented_devices(uos_identities: ()):
    assert UOSDevice(uos_identities[0], uos_identities[1]) is not None


# Checks to ensure a not implemented error is thrown when a non-existent device is entered
def test_unimplemented_devices():
    with pytest.raises(NotImplementedError):
        UOSDevice("Not Implemented", "")


