import pytest
from UARTOSInterface.HardwareCOM import UOSDevice
from UARTOSInterface.HardwareCOM import UOSInterface


class TestHardwareCOMInterface:
    # Checks to ensure all defined devices can init correctly on the UOSDevice class, makes sure no error is thrown
    def test_implemented_devices(self, uos_identities: ()):
        assert UOSDevice(identity=uos_identities[0], connection=uos_identities[1]) is not None

    # Checks to ensure a not implemented error is thrown when a non-existent device is entered
    def test_unimplemented_devices(self):
        with pytest.raises(NotImplementedError):
            UOSDevice(identity="Not Implemented", connection="")


class TestHardwareCOMAbstractions:

    # Checks the static function correctly computes the LRC checksums for some known packets.
    @pytest.mark.parametrize("test_packet_data, expected_lrc", [
                                [[255], 1],  # overflow case
                                [[0], 0],  # base case
                                [[0, 1, 1, 1], 253],  # simple NPC packet case
                                [[254, 0, 3, 255, 0, 13], 243]  # typical NPC packet case
                             ])
    def test_get_npc_checksum(self, test_packet_data: [], expected_lrc: int):
        assert UOSInterface.UOSInterface.get_npc_checksum(test_packet_data) == expected_lrc
