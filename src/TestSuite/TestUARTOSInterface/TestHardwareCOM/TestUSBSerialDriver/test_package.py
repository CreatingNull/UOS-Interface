import pytest
from UARTOSInterface.HardwareCOM.USBSerialDriver import NPCSerialPort

connection = "/dev/ttyUSB0"  # populate with the connection str / COM for relevant device.

@pytest.mark.skipif(False, reason="You need the relevant NPC Serial Hardware to test these low level functions")
class TestNPCSerialPort:

    @pytest.fixture
    def npc_serial_port(self):
        serial_port = NPCSerialPort(connection)
        yield serial_port
        serial_port.close()

    def test_basic_functions(self, npc_serial_port):
        assert npc_serial_port.open()
        assert npc_serial_port.check_open()
        assert npc_serial_port.close()
        assert not npc_serial_port.check_open()
