"""Module for testing the dashboard to HAL shim."""
from uosinterface.webapp.dashboard.shim import get_system_info


def test_get_system_info(uos_identities: ()):
    """Test the shim behaviour for getting uos system info."""
    if "LAZY" in uos_identities["loading"]:
        # EAGER usage not supported through web app.
        response = get_system_info(
            device_identity=uos_identities["identity"],
            device_address=uos_identities["address"],
            interface=uos_identities["interface"],
        )
        assert len(response) == 3
        assert "version" in response and "address" in response and "type" in response
        assert response["version"].count(".") == 2
        assert response["address"] == uos_identities["address"]
        assert "unknown" not in response["type"].lower() and len(response["type"]) > 0
