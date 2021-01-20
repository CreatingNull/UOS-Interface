"""Module for testing the routing of the web-app excluding API."""


def test_index_route(client):
    """Basic test of the backend routing config for the index route."""
    response = client.get("/")
    assert response.status_code == 200
