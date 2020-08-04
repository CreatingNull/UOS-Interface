import serial
from util import log, DEBUG, INFO, WARNING
from serial.tools import list_ports
from serial.serialutil import SerialException


class NPCSerialPort:

    __con = None

    # Constructor also opens the connection, must call close to release resource.
    def __init__(self, device: str):
        port = NPCSerialPort.check_port_exists(device)
        if port is None:
            return
        log(f"{port} located", DEBUG, __name__)
        try:
            self.__con = serial.Serial(device, 115200)
            log(f"{port.device} opened successfully", DEBUG, __name__)
        except SerialException as e:
            log(f"Opening {port.device} threw error {e.strerror}", INFO, __name__)
            if e.errno == 13:  # permission denied another connection open to this device.
                log(f"Cannot open connection, account has insufficient permissions.", WARNING, __name__)
            self.__con = None
            return
        return

    # Checks to see if a connection is open for use
    def check_open(self) -> bool:
        if self.__con is None:
            return False
        return True

    # Closes the serial connection, must be run when finished with the instance.
    def close(self):
        if not self.check_open():
            return True  # already closed
        try:
            self.__con.close()
        except SerialException:
            return False
        return True

    # Takes in a serial port identifier string and checks if the port is available on the system.
    # Returns None type if not found or port object if found.
    @staticmethod
    def check_port_exists(device: str) -> object:
        ports = list_ports.comports()
        for port in ports:
            if device in port.device:
                return port
        return None
