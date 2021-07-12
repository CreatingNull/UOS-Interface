"""Unit tests for the HardwareCOM package."""
import pytest
from uosinterface import UOSCommunicationError
from uosinterface import UOSConfigurationError
from uosinterface import UOSUnsupportedError
from uosinterface.hardware import uosabstractions
from uosinterface.hardware import UOSDevice
from uosinterface.hardware.config import Interface
from uosinterface.hardware.config import UOS_SCHEMA


class TestHardwareCOMInterface:
    """Tests for the object orientated abstraction layer."""

    @staticmethod
    def test_implemented_devices(uos_identities: {}):
        """Checks devices in config can init without error."""
        assert (
            UOSDevice(
                identity=uos_identities["identity"],
                address=uos_identities["address"],
                interface=uos_identities["interface"],
            )
            is not None
        )

    @staticmethod
    def test_unimplemented_devices():
        """Checks an un-implemented device throws the correct error."""
        with pytest.raises(UOSUnsupportedError):
            UOSDevice(identity="Not Implemented", address="", interface=Interface.STUB)

    @staticmethod
    @pytest.mark.parametrize("interface", Interface)  # checks all interfaces
    def test_bad_connection(uos_identities: {}, interface: Interface):
        """Checks that bad connections fail sensibly."""
        with pytest.raises(UOSCommunicationError):
            device = UOSDevice(
                uos_identities["identity"],
                "",
                interface=interface,
                loading=uos_identities["loading"],
            )
            if device.is_lazy():  # lazy connection so manually open
                device.open()

    @staticmethod
    @pytest.mark.parametrize("function_name", UOS_SCHEMA.keys())
    def test_device_function(uos_device, function_name):
        """Checks the UOS functions respond correctly."""
        for volatility in [0, 1, 2]:
            pins = uos_device.device.get_compatible_pins(function_name)
            if pins is None or len(pins) == 0:
                pins = [0]  # insert a dummy pin for non-pinned functions.
            for pin in pins:
                if volatility in uos_device.device.functions_enabled[function_name]:
                    result = getattr(uos_device, function_name)(
                        pin=pin, level=1, volatility=volatility
                    )
                    assert result.status
                    assert len(result.rx_packets) == len(
                        UOS_SCHEMA[function_name].rx_packets_expected
                    )
                    for i, rx_packet in enumerate(result.rx_packets):
                        assert (  # packet length validation
                            len(rx_packet)
                            == 6 + UOS_SCHEMA[function_name].rx_packets_expected[i]
                        )
                        assert (  # payload length validation
                            rx_packet[3]
                            == UOS_SCHEMA[function_name].rx_packets_expected[i]
                        )
                else:  # not implemented check error raised correctly
                    with pytest.raises(UOSUnsupportedError):
                        getattr(uos_device, function_name)(
                            pin=pin, level=1, volatility=volatility
                        )

    @staticmethod
    def test_invalid_pin(uos_device):
        """Checks a pin based instruction with an invalid pin throws error."""
        with pytest.raises(UOSUnsupportedError):
            uos_device.set_gpio_output(-1, 1)

    @staticmethod
    def test_close_error(uos_errored_device):
        """Checks error is thrown correctly on close."""
        with pytest.raises(UOSCommunicationError):
            uos_errored_device.close()


class TestHardwareCOMAbstractions:
    """Test for the UOSInterface abstraction layer and helper functions."""

    TEST_PACKETS = [
        {
            "addr_to": 0,
            "addr_from": 1,
            "payload": tuple([1]),
            "checksum": 253,
            "binary": b">\x00\x01\x01\x01\xfd<",
        },
        {
            "addr_to": 64,
            "addr_from": 0,
            "payload": (13, 0, 1, 12, 1, 0),
            "checksum": 159,
            "binary": b">\x40\x00\x06\x0d\x00\x01\x0c\x01\x00\x9f<",
        },
        {  # Bad packet
            "addr_to": 256,
            "addr_from": 256,
            "payload": tuple(),
            "checksum": 0,
            "binary": b"",
        },
    ]

    @staticmethod
    def test_execute_instruction():
        """Using the base class directly should throw an error."""
        with pytest.raises(UOSUnsupportedError):
            # noinspection PyTypeChecker
            uosabstractions.UOSInterface.execute_instruction(
                self=None, address=10, payload=()
            )

    @staticmethod
    def test_read_response():
        """Using the base class directly should throw an error."""
        with pytest.raises(UOSUnsupportedError):
            # noinspection PyTypeChecker
            uosabstractions.UOSInterface.read_response(
                self=None, expect_packets=1, timeout_s=2
            )

    @staticmethod
    def test_hard_reset():
        """Using the base class directly should throw an error."""
        with pytest.raises(UOSUnsupportedError):
            # noinspection PyTypeChecker
            uosabstractions.UOSInterface.hard_reset(self=None)

    @staticmethod
    def test_open():
        """Using the base class directly should throw an error."""
        with pytest.raises(UOSUnsupportedError):
            # noinspection PyTypeChecker
            uosabstractions.UOSInterface.open(self=None)

    @staticmethod
    def test_close():
        """Using the base class directly should throw an error."""
        with pytest.raises(UOSUnsupportedError):
            # noinspection PyTypeChecker
            uosabstractions.UOSInterface.close(self=None)

    @staticmethod
    @pytest.mark.parametrize(
        "test_packet_data, expected_lrc",
        [
            [[255], 1],  # overflow case
            [[0], 0],  # base case
            [
                (  # simple NPC packet case
                    [
                        TEST_PACKETS[0]["addr_to"],
                        TEST_PACKETS[0]["addr_from"],
                        len(TEST_PACKETS[0]["payload"]),
                    ]
                    + list(TEST_PACKETS[0]["payload"])
                ),
                TEST_PACKETS[0]["checksum"],
            ],
            [
                (  # simple NPC packet case
                    [
                        TEST_PACKETS[1]["addr_to"],
                        TEST_PACKETS[1]["addr_from"],
                        len(TEST_PACKETS[1]["payload"]),
                    ]
                    + list(TEST_PACKETS[1]["payload"])
                ),
                TEST_PACKETS[1]["checksum"],
            ],
            [
                (  # simple NPC packet case
                    [
                        TEST_PACKETS[2]["addr_to"],
                        TEST_PACKETS[2]["addr_from"],
                        len(TEST_PACKETS[2]["payload"]),
                    ]
                    + list(TEST_PACKETS[2]["payload"])
                ),
                TEST_PACKETS[2]["checksum"],
            ],
        ],
    )
    def test_get_npc_checksum(test_packet_data: [], expected_lrc: int):
        """Checks the computation of LRC checksums for some known packets."""
        print(f"\n -> packet: {test_packet_data}, lrc:{expected_lrc}")
        assert (
            uosabstractions.UOSInterface.get_npc_checksum(test_packet_data)
            == expected_lrc
        )

    @staticmethod
    @pytest.mark.parametrize(
        "test_packet", [TEST_PACKETS[0], TEST_PACKETS[1], TEST_PACKETS[2]]
    )
    def test_get_npc_packet(test_packet: {}):
        """Checks packets are formed correctly from some known data."""
        print(
            f"\n -> addr_to: {test_packet['addr_to']}, addr_from: {test_packet['addr_from']}, "
            f"payload: {test_packet['payload']}, packet: {test_packet['binary']}"
        )
        assert (
            uosabstractions.UOSInterface.get_npc_packet(
                test_packet["addr_to"],
                test_packet["addr_from"],
                test_packet["payload"],
            )
            == test_packet["binary"]
        )
