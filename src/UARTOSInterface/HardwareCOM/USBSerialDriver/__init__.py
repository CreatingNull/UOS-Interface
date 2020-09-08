import serial
from serial.tools import list_ports
from logging import getLogger as Log
from serial.serialutil import SerialException
from UARTOSInterface.HardwareCOM.UOSInterface import UOSInterface


class NPCSerialPort(UOSInterface):

    _device = None
    _connection = ""
    _port = None

    # Constructor also opens the connection, must call close to release resource.
    def __init__(self, connection: str):
        self._connection = connection
        self._port = NPCSerialPort.check_port_exists(connection)
        if self._port is None:
            return
        Log(__name__).debug(f"{self._port} located")
        return

    # Opens a connection to the serial port.
    def open(self):
        try:
            self._device = serial.Serial(self._connection, 115200)
            Log(__name__).debug(f"{self._port.device} opened successfully")
            return True
        except SerialException as e:
            Log(__name__).error(f"Opening {self._port.device} threw error {e.strerror}")
            if e.errno == 13:  # permission denied another connection open to this device.
                Log(__name__).error(f"Cannot open connection, account has insufficient permissions.")
            self._device = None
            return False

    # Closes the serial connection, must be run when finished with the instance.
    def close(self):
        if not self.check_open():
            return True  # already closed
        try:
            self._device.close()
        except SerialException:
            self._device = None
            return False
        self._device = None
        return True

    # High level function that executes a UOS instruction.
    # Inherited prototype from abstract class.
    def execute_instruction(self, address, payload) -> (bool, {}):
        # Assemble the packet using the static functions from the abstract class.
        if not self.check_open():
            return False, {}
        packet = self.get_npc_packet(to_addr=address, from_addr=0, payload=payload)
        # Send the packet.
        self._device.write(packet)
        self._device.flush()
        # Do the response shiz later.
        return True, {}  # todo stub

    # Checks to see if a connection is open for use
    def check_open(self) -> bool:
        if self._device is None:
            return False
        return True

    def __repr__(self):
        return f"<NPCSerialPort(_connection='{self._connection}', _port={self._port}, _device={self._device})>"

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
