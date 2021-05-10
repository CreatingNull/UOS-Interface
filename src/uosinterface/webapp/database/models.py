from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import BINARY
from sqlalchemy.types import INTEGER
from sqlalchemy.types import String
from uosinterface.webapp.database import Base
from uosinterface.webapp.database import hash_pass


class User(Base, UserMixin):
    """Model for storing app user info."""

    __tablename__ = "User"
    id = Column(INTEGER, primary_key=True)
    user_name = Column(String, unique=True)
    email_address = Column(String, unique=True)
    pass_hash = Column(BINARY)
    # Defining behaviour for linked tables
    user_privileges = relationship("UserPrivilege", cascade="all, delete-orphan")

    def __init__(self, user_name: str, passwd: str, **kwargs):
        """
        Constructor for a user object.

        :param user_name: String uniquely defining the user.
        :param passwd: String password to be hashed against the user object.
        :param kwargs: Keyword arguments, email_address may be provided.

        """
        self.user_name = user_name
        if "email_address" in kwargs:
            self.email_address = kwargs["email_address"]
        self.pass_hash = hash_pass(passwd)

    def update_hash(self, passwd: str):
        """
        Helper used for setting and updating the user password hashes.

        :param passwd: String password to be hashed against the user object.
        :return: None

        """
        self.pass_hash = hash_pass(passwd)


class Privilege(Base):
    """Model for storing privilege types."""

    __tablename__ = "Privilege"
    id = Column(INTEGER, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


class UserPrivilege(Base):
    """Model for storing links between users and privileges."""

    __tablename__ = "UserPrivilege"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("User.id", ondelete="CASCADE"))
    privilege_id = Column(INTEGER, ForeignKey("Privilege.id", ondelete="CASCADE"))
