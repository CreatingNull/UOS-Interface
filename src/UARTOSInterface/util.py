"""General utility functions for all packages in UOSInterfaces."""
from configparser import ConfigParser
from logging import FileHandler
from logging import Formatter
from logging import getLogger
from pathlib import Path


def configure_logs(name: str, level: int, base_path: Path):
    """Per-package logs must be manually configured to prefix correctly."""
    logger = getLogger(name)
    logger.setLevel(level)
    # Dont capture to console as custom messages only, root logger captures stderr
    logger.propagate = False
    file_handler = FileHandler(base_path.joinpath(Path("logs/" + name + ".log")))
    file_handler.setFormatter(
        Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    )
    logger.addHandler(file_handler)


def load_config(path: Path):
    """For loading ini files used by the app."""
    getLogger(__name__).debug("Loading config from %s", path)
    parser = ConfigParser()
    parser.read(str(path.resolve()))
    if len(parser.sections()) > 0:  # config was located
        return parser
    return None
