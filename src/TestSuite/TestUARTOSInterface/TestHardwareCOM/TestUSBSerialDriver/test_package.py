import pytest
from time import sleep
from UARTOSInterface.HardwareCOM.USBSerialDriver import NPCSerialPort

connection = "/dev/ttyUSB0"  # populate with the connection str / COM for relevant device.


@pytest.mark.skipif(False, reason="You need the relevant NPC Serial Hardware to test these low level functions")
class TestNPCSerialPort:

    @pytest.fixture
    def npc_serial_port(self):
        serial_port = NPCSerialPort(connection, baudrate=115200)
        yield serial_port
        serial_port.close()

    @pytest.fixture
    def invalid_serial_port(self):
        serial_port = NPCSerialPort("not_a_valid_connection")
        return serial_port

    def test_basic_functions(self, npc_serial_port):
        assert npc_serial_port.open()
        assert npc_serial_port.check_open()
        sleep(2)  # Allow the system time to boot
        assert npc_serial_port.execute_instruction(64, (13, 0, 1))[0]
        response = npc_serial_port.read_response(expect_packets=1, timeout_s=2)
        assert response[0]
        assert npc_serial_port.hard_reset()
        assert npc_serial_port.close()
        assert npc_serial_port.close()  # should be safe to close an already closed connection
        assert not npc_serial_port.check_open()
        assert type(npc_serial_port.enumerate_ports()) == list

    def test_basic_fault_cases(self, invalid_serial_port, npc_serial_port):
        assert not invalid_serial_port.check_open()
        assert not invalid_serial_port.open()
        assert invalid_serial_port.close()
        assert not invalid_serial_port.execute_instruction(64, (13, 0, 1))[0]
        assert not invalid_serial_port.read_response(expect_packets=1, timeout_s=2)[0]
