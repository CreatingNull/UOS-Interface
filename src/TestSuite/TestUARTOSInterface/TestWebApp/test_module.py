from pathlib import Path
from UARTOSInterface.util import load_config


def test_load_config():
    config_bad = load_config(Path("Non-existent.ini"))
    config_good = load_config(
        Path(__file__)
        .resolve()
        .parents[4]
        .joinpath(Path("resources/UARTOSInterface.ini"))
    )
    assert config_bad is None
    assert config_good is not None
