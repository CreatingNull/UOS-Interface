""" Module defining the low level UOSImplementation for serial port devices. """
import serial
from serial.tools import list_ports
from logging import getLogger as Log
from serial.serialutil import SerialException
from UARTOSInterface.HardwareCOM.UOSInterface import UOSInterface


class NPCSerialPort(UOSInterface):
    """ Low level pyserial class that handles reading / writing to the serial port.
        :ivar _device: Holds the pyserial device once opened. None if not opened.
        :ivar _connection: Holds the standard connection string 'Interface'|'OS Connection String.
        :ivar _port: Holds the port class, containing OS level info on the device. None if device not instantiated.
    """

    _device = None
    _connection = ""
    _port = None

    def __init__(self, connection: str):
        """ Constructor for a NPCSerialPort device.
        :param connection: OS connection string for the serial port.
        """
        self._connection = connection
        self._port = NPCSerialPort.check_port_exists(connection)
        if self._port is None:
            return
        Log(__name__).debug(f"{self._port} located")

    def open(self):
        """ Opens a connection to the the defined port and creates the device object.
        :return: Success boolean.
        """
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

    def close(self):
        """ Closes the serial connection and clears the device.
        :return: Success boolean.
        """
        if not self.check_open():
            return True  # already closed
        try:
            self._device.close()
        except SerialException:
            self._device = None
            return False
        self._device = None
        return True

    def execute_instruction(self, address, payload) -> (bool, {}):
        """ Builds and executes a new packet.
        :param address: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param payload: A tuple containing the unsigned 8 bit integer parameters of the UOS instruction.
        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.
        """
        if not self.check_open():
            return False, {"exception": "Connection must be open first."}
        packet = self.get_npc_packet(to_addr=address, from_addr=0, payload=payload)
        Log(__name__).debug(f"packet formed {packet}")
        try:  # Send the packet.
            self._device.write(packet)
            self._device.flush()
        except serial.SerialException as e:
            return False, {"exception": str(e)}
        return True, {}

    def read_response(self, timeout_s: int) -> (bool, {}):
        """ Reads ACK and response packets from the serial device.
        :param timeout_s: The maximum time this function will wait for data.
        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.
        """
        pass

    def check_open(self) -> bool:
        """ Tests if the connection is open by validating an open device.
        :return: Boolean, true if open.
        """
        if self._device is None:
            return False
        return True

    def __repr__(self):
        return f"<NPCSerialPort(_connection='{self._connection}', _port={self._port}, _device={self._device})>"

    # Takes in a serial port identifier string and checks if the port is available on the system.
    # Returns None type if not found or port object if found.
    @staticmethod
    def check_port_exists(device: str):
        """ Takes in a serial port connection string and checks if the port is available on the system.
        :param device: OS connection string for the serial port.
        :return: The port device class if it exists, else None.
        """
        ports = list_ports.comports()
        for port in ports:
            if device in port.device:
                return port
        return None

    @staticmethod
    def enumerate_ports() -> ():
        """ Get the available ports on the system.
        :return: Tuple of ports visible to the OS as port objects.
        """
        return list_ports.comports()
