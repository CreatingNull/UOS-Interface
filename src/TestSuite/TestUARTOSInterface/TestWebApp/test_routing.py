"""Module for testing the routing of the web-app excluding API."""
from UARTOSInterface.WebApp import create_app
from configparser import ConfigParser
from pathlib import Path
import pytest


@pytest.fixture()
def client():
    parser = ConfigParser()
    parser["Flask Config"] = {
        "TESTING": "True",
        "SECRET_KEY": "Testing",
    }
    base_dir = Path(__file__).resolve().parents[4]
    app = create_app(parser, base_dir)
    with app.test_client() as client:
        yield client


# Basic test of the backend routing configuration for the index route
def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
