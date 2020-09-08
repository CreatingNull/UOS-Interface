from abc import abstractmethod, ABCMeta


# base class inherited by all low level connection objects
class UOSInterface(metaclass=ABCMeta):

    @abstractmethod
    def execute_instruction(self, address: int, payload: [int]) -> (bool, {}):
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.execute_instruction.__name__} prototype."
        )

    @abstractmethod
    def open(self) -> bool:
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.open.__name__} prototype."
        )

    @abstractmethod
    def close(self) -> bool:
        raise NotImplementedError(
            f"UOSInterfaces must over-ride {UOSInterface.close.__name__} prototype."
        )

    # function builds a static bytes object containing all the bytes to be transmitted in sequential order
    # in an npc compliant packet.
    @staticmethod
    def get_npc_packet(to_addr: int, from_addr: int, payload: [int]) -> bytes:
        if to_addr < 256 and from_addr < 256 and len(payload) < 256:  # check input is possible to parse
            packet_data = [to_addr, from_addr, len(payload)] + payload
            lrc = UOSInterface.get_npc_checksum(packet_data)
            return bytes([0x3e, packet_data[0], packet_data[1], len(payload)] + payload + [lrc, 0x3c])
        return bytes([])

    # Computes the LRC checksum based on applicable bytes in a npc formed packet.
    # Addr to, Addr From, Len, Payload should be provided in sequential order.
    @staticmethod
    def get_npc_checksum(packet_data: [int]) -> int:
        lrc = 0
        for byte in packet_data:
            lrc = (lrc + byte) & 0xff
        return ((lrc ^ 0xff) + 1) & 0xff
