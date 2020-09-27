from dataclasses import dataclass, field
from typing import List


@dataclass
class COMresult:
    status: bool
    exception: str = ""
    ack_packet: List = field(default_factory=list)
    rx_packets: List = field(default_factory=list)


test = COMresult(status=False)
print(test)
