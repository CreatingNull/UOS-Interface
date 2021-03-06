"""Module for testing the dashboard to HAL shim."""
from uosinterface.webapp.dashboard.shim import get_system_info


def test_get_system_info(uos_identities: ()):
    if "LAZY" in uos_identities[2]:  # EAGER usage not supported through web app.
        response = get_system_info(
            device_identity=uos_identities[0], device_connection=uos_identities[1]
        )
        assert len(response) == 3
        assert "version" in response and "connection" in response and "type" in response
        assert response["version"].count(".") == 2
        assert response["connection"] == uos_identities[1]
        assert "unknown" not in response["type"].lower() and len(response["type"]) > 0
