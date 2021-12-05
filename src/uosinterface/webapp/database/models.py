"""Declarative models for webapp's SQLAlchemy database ORM."""
from datetime import datetime
from datetime import timedelta
from secrets import token_urlsafe

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import BINARY
from sqlalchemy.types import DATETIME
from sqlalchemy.types import Enum
from sqlalchemy.types import INTEGER
from sqlalchemy.types import String
from uosinterface.webapp.database import Base
from uosinterface.webapp.database import hash_pass
from uosinterface.webapp.database import KeyTypes

# pylint: disable = too-few-public-methods
# It is normal for SQLAlchemy models to have a low number of methods.


class User(Base, UserMixin):
    """Model for storing app user info."""

    __tablename__ = "User"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(40), unique=True)
    email_address = Column(String(120), unique=True)
    pass_hash = Column(BINARY)
    # Defining behaviour for linked tables
    user_privileges = relationship("UserPrivilege", cascade="all, delete-orphan")
    user_keys = relationship("UserKey", cascade="all, delete-orphan")

    def __init__(self, name: str, passwd: str, **kwargs):
        """Constructor for a user object.

        :param name: String uniquely defining the user.
        :param passwd: String password to be hashed against the user object.
        :param kwargs: Keyword arguments, email_address may be provided.
        """
        self.name = name
        if "email_address" in kwargs and kwargs["email_address"]:
            self.email_address = kwargs["email_address"]
        self.update_hash(passwd)

    def update_hash(self, passwd: str):
        """Helper used for setting and updating the user password hashes.

        :param passwd: String password to be hashed against the user object.
        :return: None
        """
        self.pass_hash = hash_pass(passwd)


class Privilege(Base):
    """Model for storing privilege types."""

    __tablename__ = "Privilege"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(20), unique=True)


class UserPrivilege(Base):
    """Model for storing links between logged in users and privileges."""

    __tablename__ = "UserPrivilege"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("User.id", ondelete="CASCADE"))
    privilege_id = Column(INTEGER, ForeignKey("Privilege.id", ondelete="CASCADE"))


class APIPrivilege(Base):
    """Model for storing links between users and privileges via API key."""

    __tablename__ = "APIPrivilege"
    id = Column(INTEGER, primary_key=True)
    key_id = Column(INTEGER, ForeignKey("UserKey.id"))
    privilege_id = Column(INTEGER, ForeignKey("Privilege.id", ondelete="CASCADE"))


class UserKey(Base):
    """Model for generating secret keys related to a user."""

    __tablename__ = "UserKey"

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("User.id", ondelete="CASCADE"))
    key = Column(String(100), unique=True)
    key_type = Column(Enum(KeyTypes))
    expiry_date = Column(DATETIME)
    # Defining behaviour for linked tables
    api_privileges = relationship("APIPrivilege", cascade="all, delete-orphan")

    def __init__(self, key_length: int = 32, expires: timedelta = None, **kwargs):
        """Constructor for generating a random user key.

        :param key_length: Length of the key to generate in characters.
        :param expires: Timedelta defining when to expire the key, None is never. (default=None)
        :param kwargs: Attributes to populate in the model.
        """
        # Byte resolves to ~1.3 chars
        self.key = token_urlsafe(key_length)[:key_length]
        if expires:
            self.expiry_date = datetime.now() + expires
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])

    def expired(self) -> bool:
        """Check if expired. Expired keys should be removed.

        :return: Boolean describing if the key is active, if true should be removed.
        """
        if not self.expired or self.expiry_date > datetime.now():
            return False
        return True
