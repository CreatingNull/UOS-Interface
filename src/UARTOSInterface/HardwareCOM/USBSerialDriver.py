import serial
from serial.tools import list_ports
from logging import getLogger as Log
from serial.serialutil import SerialException
from UARTOSInterface.HardwareCOM.UOSInterface import UOSInterface


class NPCSerialPort(UOSInterface):

    _con = None
    _port = ""

    # Constructor also opens the connection, must call close to release resource.
    def __init__(self, device: str):
        self._port = device
        port = NPCSerialPort.check_port_exists(device)
        if port is None:
            return
        Log(__name__).debug(f"{port} located")
        try:
            self._con = serial.Serial(device, 115200)
            Log(__name__).debug(f"{port.device} opened successfully")
        except SerialException as e:
            Log(__name__).error(f"Opening {port.device} threw error {e.strerror}")
            if e.errno == 13:  # permission denied another connection open to this device.
                Log(__name__).error(f"Cannot open connection, account has insufficient permissions.")
            self._con = None
            return
        return

    # Checks to see if a connection is open for use
    def check_open(self) -> bool:
        if self._con is None:
            return False
        return True

    # High level function that executes a UOS instruction, inherited prototype from abstract class
    def execute_instruction(self, address, payload) -> (bool, {}):
        return False, {}  # todo stub

    # Closes the serial connection, must be run when finished with the instance.
    def close(self):
        if not self.check_open():
            return True  # already closed
        try:
            self._con.close()
        except SerialException:
            return False
        return True

    # Takes in a serial port identifier string and checks if the port is available on the system.
    # Returns None type if not found or port object if found.
    @staticmethod
    def check_port_exists(device: str):
        ports = list_ports.comports()
        for port in ports:
            if device in port.device:
                return port
        return None

    @staticmethod
    def enumerate_ports() -> ():
        return list_ports.comports()
