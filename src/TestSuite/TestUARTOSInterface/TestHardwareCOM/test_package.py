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

    # Checks instruction correctly behaves on hardware interface.
    # Note to run this configured hardware must be present on the system.
    @pytest.mark.skipif(False, reason="You must have low level hardware to test low level interfaces")
    def test_set_gpio_output(self, uos_device):
        for volatility in [0, 1, 2]:
            if volatility in uos_device.system_lut["functions"]["set_gpio_output"]:
                assert uos_device.set_gpio_output(pin=1, level=1, volatility=volatility).status
            else:  # not implemented check error raised correctly
                with pytest.raises(NotImplementedError):
                    uos_device.set_gpio_output(pin=1, level=1, volatility=volatility)


class TestHardwareCOMAbstractions:
    TEST_PACKETS = [
        {"addr_to": 0,
         "addr_from": 1,
         "payload": tuple([1]),
         "checksum": 253,
         "binary": b">\x00\x01\x01\x01\xfd<"
         },
        {"addr_to": 64,
         "addr_from": 0,
         "payload": (13, 0, 1, 12, 1, 0),
         "checksum": 159,
         "binary": b">\x40\x00\x06\x0d\x00\x01\x0c\x01\x00\x9f<"
         },
        # Bad packet
        {"addr_to": 256,
         "addr_from": 256,
         "payload": tuple(),
         "checksum": 0,
         "binary": b""}
    ]

    # Checks the base class correctly triggers an exception when the abstract method is called directly
    # This indicates the abstract class is correctly configured to warn inherited classes.
    def test_execute_instruction(self):
        with pytest.raises(NotImplementedError):
            # noinspection PyTypeChecker
            UOSInterface.UOSInterface.execute_instruction(self=None, address=10, payload=())

    def test_read_response(self):
        with pytest.raises(NotImplementedError):
            # noinspection PyTypeChecker
            UOSInterface.UOSInterface.read_response(self=None, expect_packets=1, timeout_s=2)

    def test_hard_reset(self):
        with pytest.raises(NotImplementedError):
            # noinspection PyTypeChecker
            UOSInterface.UOSInterface.hard_reset(self=None)

    def test_open(self):
        with pytest.raises(NotImplementedError):
            # noinspection PyTypeChecker
            UOSInterface.UOSInterface.open(self=None)

    def test_close(self):
        with pytest.raises(NotImplementedError):
            # noinspection PyTypeChecker
            UOSInterface.UOSInterface.close(self=None)

    # Checks the static function correctly computes the LRC checksums for some known packets.
    @pytest.mark.parametrize(
        "test_packet_data, expected_lrc",
        [
            [[255], 1],  # overflow case
            [[0], 0],  # base case
            [(  # simple NPC packet case
                [TEST_PACKETS[0]["addr_to"], TEST_PACKETS[0]["addr_from"],
                 len(TEST_PACKETS[0]["payload"])] + list(TEST_PACKETS[0]["payload"])
            ), TEST_PACKETS[0]["checksum"]],
            [(  # simple NPC packet case
                [TEST_PACKETS[1]["addr_to"], TEST_PACKETS[1]["addr_from"],
                 len(TEST_PACKETS[1]["payload"])] + list(TEST_PACKETS[1]["payload"])
            ), TEST_PACKETS[1]["checksum"]],
            [(  # simple NPC packet case
                    [TEST_PACKETS[2]["addr_to"], TEST_PACKETS[2]["addr_from"],
                     len(TEST_PACKETS[2]["payload"])] + list(TEST_PACKETS[2]["payload"])
            ), TEST_PACKETS[2]["checksum"]],
        ]
    )
    def test_get_npc_checksum(self, test_packet_data: [], expected_lrc: int):
        print(f"\n -> packet: {test_packet_data}, lrc:{expected_lrc}")
        assert UOSInterface.UOSInterface.get_npc_checksum(test_packet_data) == expected_lrc

    # Checks the static function correctly forms packets using some known examples
    @pytest.mark.parametrize("test_packet", [TEST_PACKETS[0], TEST_PACKETS[1], TEST_PACKETS[2]])
    def test_get_npc_packet(self, test_packet: {}):
        print(
            f"\n -> addr_to: {test_packet['addr_to']}, addr_from: {test_packet['addr_from']}, "
            f"payload: {test_packet['payload']}, packet: {test_packet['binary']}"
        )
        assert UOSInterface.UOSInterface.get_npc_packet(
            test_packet["addr_to"],
            test_packet["addr_from"],
            test_packet["payload"],
        ) == test_packet["binary"]
