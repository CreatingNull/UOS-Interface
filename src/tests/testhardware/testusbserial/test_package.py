"""Module for testing the the USB serial package hardware interface."""
from time import sleep

import pytest
from uosinterface.hardware.usbserial import NPCSerialPort


class TestNPCSerialPort:
    """Test suite for the low level serial backend."""

    @staticmethod
    @pytest.fixture(scope='class')
    def npc_serial_port(usb_serial_argument):
        """Fixture to connect to a physical UOS device for testing."""
        serial_port = NPCSerialPort(usb_serial_argument, baudrate=115200)
        yield serial_port
        serial_port.close()

    @staticmethod
    @pytest.fixture(scope='class')
    def invalid_serial_port():
        """Fixture to attempt a connection to an invalid device."""
        serial_port = NPCSerialPort("not_a_valid_connection")
        return serial_port

    @staticmethod
    def test_basic_functions(npc_serial_port):
        """Checks some low level execution on a NPCSerialPort fixture."""
        assert npc_serial_port.open()
        assert npc_serial_port.check_open()
        sleep(2)  # Allow the system time to boot
        assert npc_serial_port.execute_instruction(64, (13, 0, 1)).status
        response = npc_serial_port.read_response(expect_packets=1, timeout_s=2)
        assert response.status
        assert npc_serial_port.hard_reset()
        assert npc_serial_port.close()
        assert (
            npc_serial_port.close()
        )  # should be safe to close an already closed connection
        assert not npc_serial_port.check_open()
        assert isinstance(npc_serial_port.enumerate_devices(), list)

    @staticmethod
    def test_basic_fault_cases(invalid_serial_port):
        """Checks the invalid fixture fails correctly."""
        assert not invalid_serial_port.check_open()
        assert not invalid_serial_port.open()
        assert invalid_serial_port.close()
        assert not invalid_serial_port.execute_instruction(64, (13, 0, 1)).status
        assert not invalid_serial_port.read_response(
            expect_packets=1, timeout_s=1
        ).status
