import sys
from logging import getLogger, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, basicConfig, StreamHandler

DEBUG = DEBUG
INFO = INFO
WARNING = WARNING
ERROR = ERROR

LOGGING_LEVEL = WARNING  # default program logging level


# per package manually inserted logs
def configure_logs(name: str, level: int):
    logger = getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Dont capture to console as custom messages only, root logger captures stderr
    file_handler = FileHandler("logs/"+name+".log")
    file_handler.setFormatter(Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
    logger.addHandler(file_handler)


# system base logger tagged to stderr stream
def configure_root_stream(level: int):
    basicConfig(format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', filename="logs/Error.log", level=level)
    logger = getLogger()  # base system logger
    logger.addHandler(StreamHandler(sys.stderr))


# per module log entry wrapper function
def log(info: str, level: int, name: str):
    logger = configure_logs(name, LOGGING_LEVEL) if getLogger(name) is None else getLogger(name)
    if level == DEBUG:
        logger.debug(info)
    elif level == INFO:
        logger.info(info)
    elif level == WARNING:
        logger.warning(info)
    elif level == ERROR:
        logger.error(info)
