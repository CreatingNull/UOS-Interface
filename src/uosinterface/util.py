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
    log_dir = Path(base_path.joinpath(Path("logs/")))
    if not log_dir.exists():
        log_dir.mkdir()
    file_handler = FileHandler(log_dir.joinpath(Path(name + ".log")))
    file_handler.setFormatter(
        Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    )
    logger.addHandler(file_handler)
