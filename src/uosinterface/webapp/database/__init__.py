"""Package containing SQLite IO for the web-app."""
from binascii import hexlify
from enum import Enum
from hashlib import scrypt
from hashlib import sha512
from os import urandom
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uosinterface import resources_path

# Database base class for associating models.
Base = declarative_base()

engine = create_engine(
    f"sqlite:///{resources_path.joinpath(Path('uosinterface_data.db')).resolve().__str__()}",
    connect_args={"check_same_thread": False},
    future=True,
)
# Session maker to be used for creating distributing db sessions in the webapp.
session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)


class KeyTypes(Enum):
    """Class describing the variation in user keys."""

    API = 0


def hash_pass(passwd: str) -> bytes:
    """Using SHA512 to digest random salt for scrypt."""
    salt = sha512(urandom(64)).hexdigest().encode("ascii")
    hash_result = scrypt(password=passwd.encode("ascii"), salt=salt, n=16384, r=8, p=1)
    return salt + hexlify(hash_result)


def verify_pass(passwd: str, hashed_passwd: bytes) -> bool:
    """Compare hash of entry to saved hash."""
    hashed_passwd = hashed_passwd.decode("ascii")
    salt = hashed_passwd[:128].encode("ascii")  # first 128 chars are salt
    hash_result = scrypt(password=passwd.encode("ascii"), salt=salt, n=16384, r=8, p=1)
    return hexlify(hash_result).decode("ascii") == hashed_passwd[128:]
