from logging import getLogger, FileHandler, Formatter
from configparser import ConfigParser
from pathlib import Path


# per package manually inserted logs
def configure_logs(name: str, level: int, base_path: Path):
    logger = getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Dont capture to console as custom messages only, root logger captures stderr
    file_handler = FileHandler(base_path.joinpath(Path("logs/" + name + ".log")))
    file_handler.setFormatter(
        Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    )
    logger.addHandler(file_handler)


def load_config(path: Path):
    getLogger(__name__).debug(f"Loading config from {path}")
    parser = ConfigParser()
    parser.read(str(path.resolve()))
    if len(parser.sections()) > 0:  # config was located
        return parser
    return None
