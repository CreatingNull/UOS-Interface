"""Common high-level database interaction functionality."""
from typing import Union

from sqlalchemy import and_
from sqlalchemy.orm import Session
from uosinterface import UOSDatabaseError
from uosinterface.webapp.database.models import APIPrivilege
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKeys
from uosinterface.webapp.database.models import UserPrivilege


def get_user(session: Session, identifier: Union[int, str], user_field=User.id) -> User:
    """
    get a user object via username or id.

    :param session: The session_maker object to obtain a session from.
    :param identifier: Identifying parameter for looking up the user.
    :param user_field: The field on which to compare to the identifying parameter (default id).
    :return: User object if found otherwise None.

    """
    return session.query(User).filter(user_field == identifier).first()


def add_user(session: Session, name: str, passwd: str, **kwargs):
    """
    Function for adding a new user into the database.

    :param session: The session_maker object to obtain a session from.
    :param name: The username for the user, cannot already exist in db..
    :param passwd: The password to be hashed for the user.
    :param kwargs: Additional optional arguments, email_address.
    :return:

    """
    # Check name is not taken.
    if session.query(User).filter(User.name == name).first():
        raise UOSDatabaseError("Username is already in use.")
    new_user = User(
        name=name,
        passwd=passwd,
        email_address=kwargs["email_address"] if "email_address" in kwargs else None,
    )
    session.add(new_user)
    session.flush()


def add_user_privilege(session: Session, user: [int, str], privilege: Union[int, str]):
    """
    Function for linking a user to a privilege.

    :param session: The session_maker object to obtain a session from.
    :param user: The name or id of the user add the privilege to.
    :param privilege: The name or id of the privilege.
    :return:

    """
    linked_user = get_user(
        session=session,
        identifier=user,
        user_field=User.id if isinstance(user, int) else User.name,
    )
    if not linked_user:
        raise UOSDatabaseError("User must exist for privileges to be added.")
    linked_privilege = (
        session.query(Privilege)
        .filter(
            Privilege.id if isinstance(privilege, int) else Privilege.name == privilege
        )
        .first()
    )
    if not linked_privilege:
        raise UOSDatabaseError("Tried to add non-existent privilege to user.")
    user_privilege = UserPrivilege(
        user_id=linked_user.id, privilege_id=linked_privilege.id
    )
    if (
        session.query(user_privilege)
        .filter(
            and_(
                UserPrivilege.user_id == user_privilege.user_id,
                privilege_id=user_privilege.privilege_id,
            )
        )
        .first()
    ):
        raise UOSDatabaseError("Privilege is a duplicate.")
    session.add(user_privilege)
    session.flush()


def init_privilege(session: Session, name: str, description: str):
    """
    Function for adding privilege types available in the program.

    :param session: The session_maker object to obtain a session from.
    :param name: The privilege name used for lookup, cannot already exist in db.
    :param description: A brief description of the privilege's use.
    :return:

    """
    # Check privilege doesn't already exist.
    if session.query(Privilege).filter(Privilege.name == name).first():
        raise UOSDatabaseError("Privilege %s already exists in the database.", name)
    new_privilege = Privilege(name=name, description=description)
    session.add(new_privilege)
    session.flush()
