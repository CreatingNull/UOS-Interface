"""Configure the general test fixtures for testing the web-app."""
from configparser import ConfigParser
from pathlib import Path

import pytest
from uosinterface.webapp import create_app


@pytest.fixture(scope="package")
def client():
    """Web-app fixture to use for test coverage."""
    parser = ConfigParser()
    parser["Flask Config"] = {
        "TESTING": "True",
        "SECRET_KEY": "Testing",
    }
    base_dir = Path(__file__).resolve().parents[3]
    static_dir = base_dir.joinpath("src/uosinterface/webapp/static/")
    app = create_app(parser, base_dir, static_dir)
    with app.test_client() as client_instance:
        yield client_instance
