import pytest
from UARTOSInterface.HardwareCOM import USBSerialDriver


@pytest.mark.skipif(True, reason="Skip if system doesn't have the hardware to test the low level interface")
class TestNPCSerialPort:

    @pytest.mark.parametrize("device", ["/dev/ttyUSB0"])
    def test_init(self, device: str):
        usb_device = USBSerialDriver.NPCSerialPort(device)
        assert usb_device._con is not None
