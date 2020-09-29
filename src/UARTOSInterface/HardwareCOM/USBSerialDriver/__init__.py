"""Module defining the low level UOSImplementation for serial port devices."""
import serial
import platform
from serial.tools import list_ports
from logging import getLogger as Log
from serial.serialutil import SerialException
from time import time_ns, sleep
from UARTOSInterface.HardwareCOM.UOSInterface import UOSInterface, COMresult


class NPCSerialPort(UOSInterface):
    """
    Low level pyserial class that handles reading / writing to the serial port.

    :ivar _device: Holds the pyserial device once opened. None if not opened.
    :ivar _connection: Holds the standard connection string 'Interface'|'OS Connection String.
    :ivar _port: Holds the port class, containing OS level info on the device. None if device not instantiated.
    :ivar _kwargs: Additional keyword arguments as defined in the documentation.

    """

    _device = None

    _connection = ""
    _port = None
    _kwargs = {}

    def __init__(self, connection: str, **kwargs):
        """
        Constructor for a NPCSerialPort device.

        :param connection: OS connection string for the serial port.

        """
        self._connection = connection
        self._port = NPCSerialPort.check_port_exists(connection)
        self._kwargs = kwargs
        if self._port is None:
            return
        Log(__name__).debug(f"{self._port} located")

    def open(self):
        """
        Opens a connection to the the defined port and creates the device
        object.

        :return: Success boolean.

        """
        try:
            self._device = serial.Serial()
            self._device.port = self._connection
            if "baudrate" in self._kwargs:
                self._device.baudrate = self._kwargs["baudrate"]
            if platform.system() == "Linux":
                Log(__name__).debug("Linux platform found so using DTR workaround")
                import termios

                with open(self._connection) as p:  # DTR transient workaround for Unix
                    attrs = termios.tcgetattr(p)
                    attrs[2] = attrs[2] & ~termios.HUPCL
                    termios.tcsetattr(p, termios.TCSAFLUSH, attrs)
            self._device.dtr = True
            self._device.open()
            Log(__name__).debug(f"{self._port.device} opened successfully")
            return True
        except (SerialException, FileNotFoundError) as e:
            Log(__name__).error(
                f"Opening {self._port.device if self._port is not None else 'None'} threw error {e.__str__()}"
            )
            if (
                e.errno == 13
            ):  # permission denied another connection open to this device.
                Log(__name__).error(
                    "Cannot open connection, account has insufficient permissions."
                )
            self._device = None
            return False

    def close(self):
        """
        Closes the serial connection and clears the device.

        :return: Success boolean.

        """
        if not self.check_open():
            return True  # already closed
        try:
            self._device.close()
        except SerialException as e:
            Log(__name__).debug(f"Closing the connection threw error {e.__str__()}")
            self._device = None
            return False
        Log(__name__).debug("Connection closed successfully")
        self._device = None
        return True

    def execute_instruction(self, address, payload):
        """
        Builds and executes a new packet.

        :param address: An 8 bit unsigned integer of the UOS subsystem targeted by the instruction.
        :param payload: A tuple containing the unsigned 8 bit integer parameters of the UOS instruction.
        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.

        """
        if not self.check_open():
            return COMresult(False, exception="Connection must be opened first.")
        packet = self.get_npc_packet(to_addr=address, from_addr=0, payload=payload)
        Log(__name__).debug(f"packet formed {packet}")
        try:  # Send the packet.
            num_bytes = self._device.write(packet)
            self._device.flush()
            Log(__name__).debug(f"Sent {num_bytes} bytes of data")
        except serial.SerialException as e:
            return COMresult(False, exception=str(e))
        finally:
            self._device.reset_output_buffer()
        return COMresult(num_bytes == len(packet))

    def read_response(self, expect_packets: int, timeout_s: float):
        """
        Reads ACK and response packets from the serial device.

        :param expect_packets: How many packets including ACK to expect.
        :param timeout_s: The maximum time this function will wait for data.
        :return: COMresult object.

        """
        response_object = COMresult(False)
        if not self.check_open():
            return response_object
        start_ns = time_ns()
        packet = []
        payload_len = 0  # tracks the current packet's payload length
        byte_index = -1  # tracks the byte position index of the current packet
        packet_index = 0  # tracks the packet number being received 0 = ACK
        try:
            while (
                timeout_s * 1000000000
            ) > time_ns() - start_ns and byte_index > -2:  # read until packet or timeout
                num_bytes = self._device.in_waiting
                if num_bytes > 0:
                    for index in range(num_bytes):
                        byte_in = self._device.read(1)
                        if byte_index == -1:  # start symbol
                            if byte_in == b">":
                                byte_index += 1
                        if byte_index >= 0:
                            Log(__name__).debug(f"read {byte_in} index = {byte_index}")
                            if byte_index == 3:  # payload len
                                payload_len = int.from_bytes(
                                    byte_in, byteorder="little"
                                )
                            elif byte_index == 3 + payload_len + 2:  # End packet symbol
                                if byte_in == b"<":
                                    byte_index = -2  # packet complete
                                    Log(__name__).debug("Found end packet symbol")
                                else:  # Errored data
                                    byte_index = -1
                                    payload_len = 0
                                    packet = []
                            packet.append(int.from_bytes(byte_in, byteorder="little"))
                            if byte_index == -2:
                                if packet_index == 0:
                                    response_object.ack_packet = packet
                                else:
                                    response_object.rx_packets.append(packet)
                                packet_index += 1
                                if expect_packets == packet_index:
                                    break
                                byte_index = -1
                                packet = []
                                payload_len = 0
                            byte_index += 1
                sleep(0.05)  # Don't churn CPU cycles waiting for data
            Log(__name__).debug(f"Packet received {packet}")
            if expect_packets != packet_index or len(packet) < 6 or byte_index != -2:
                response_object.rx_packets.append(packet)
                response_object.exception = "did not receive all the expected data"
                return response_object
            response_object.status = True
            return response_object
        except serial.SerialException as e:
            response_object.exception = str(e)
            return response_object

    def hard_reset(self):
        """
        Manually drives the DTR line low to reset the device.

        :return: Tuple containing a status boolean and index 0 and a result-set dict at index 1.

        """
        if not self.check_open():
            return COMresult(False, exception="Connection must be open first.")
        Log(__name__).debug("Resetting the device using the DTR line")
        self._device.dtr = not self._device.dtr
        sleep(0.2)
        self._device.dtr = not self._device.dtr
        return COMresult(True)

    def check_open(self) -> bool:
        """
        Tests if the connection is open by validating an open device.

        :return: Boolean, true if open.

        """
        if self._device is None:
            return False
        return True

    def __repr__(self):
        """
        Over-rides the built in repr with something useful.

        :return: String containing connection, port and device.

        """
        return f"<NPCSerialPort(_connection='{self._connection}', _port={self._port}, _device={self._device})>"

    @staticmethod
    def check_port_exists(device: str):
        """
        Takes in a serial port connection string and checks if the port is
        available on the system.

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
        """
        Get the available ports on the system.

        :return: Tuple of ports visible to the OS as port objects.

        """
        return list_ports.comports()
