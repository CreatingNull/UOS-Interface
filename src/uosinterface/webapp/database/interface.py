"""Common high-level database interaction functionality."""
from datetime import timedelta
from typing import Union

from sqlalchemy import and_
from sqlalchemy.orm import Session
from uosinterface import UOSDatabaseError
from uosinterface.webapp.database import KeyTypes
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKey
from uosinterface.webapp.database.models import UserPrivilege


def get_user(
    session: Session, user_value: Union[int, str] = None, user_field=User.id
) -> Union[User, list]:
    """
    Get a user object via username or id.

    :param session: The session_maker object to obtain a session from.
    :param user_value: Identifier for looking up the user, all if None. (default None).
    :param user_field: The field to compare to the value parameter (default id).
    :return: User object if found otherwise None, list of users if user_value None.

    """
    if user_value is None:  # return a list of all users
        return session.query(User).all()
    if user_field == UserKey.user_id:  # Lookup user via api key.
        return (
            session.query(User).join(UserKey).filter(user_field == user_value).first()
        )
    # Lookup via user table parameters.
    return session.query(User).filter(user_field == user_value).first()


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


def get_user_privileges(
    session: Session,
    user_value: Union[str, int],
    user_field=User.id,
    privilege_value: Union[str, int] = None,
    privilege_field=None,
) -> Union[list, Privilege]:
    """
    Get user privileges can limit search to object if privilege arguments set.

    :param session: The session_maker object to obtain a session from.
    :param user_value: Identifying parameter for looking up the user.
    :param user_field: The field to compare to the value parameter (default id).
    :param privilege_value: Identifying parameter for looking up the privilege (default None).
    :param privilege_field: The field to compare to the value parameter (default None).
    :return: A tuple of privileges or a single privilege object depending on input.

    """
    user_privileges = (
        session.query(Privilege)
        .join(UserPrivilege)
        .join(User)
        .filter(user_field == user_value)
    )
    if privilege_field and privilege_value:
        # Looking for a specific privilege.
        user_privileges = user_privileges.filter(privilege_field == privilege_value)
        return user_privileges.first()
    return user_privileges.all()


def add_user_privilege(
    session: Session,
    user_value: Union[int, str],
    user_field,
    privilege: Union[int, str],
    privilege_field,
):
    """
    Function for linking a user to a privilege.

    :param session: The session_maker object to obtain a session from.
    :param user_value: The name or id of the user add the privilege to.
    :param user_field: The field to compare to the value parameter.
    :param privilege: The name or id of the privilege.

    :param privilege_field: The field to compare to the value parameter (default None).
    :return:

    """
    linked_user = get_user(session, user_value, user_field)
    if not linked_user:
        raise UOSDatabaseError("User must exist for privileges to be added.")
    linked_privilege = (
        session.query(Privilege).filter(privilege_field == privilege).first()
    )
    if not linked_privilege:
        raise UOSDatabaseError("Privilege must exist to be added to user.")
    if (
        session.query(UserPrivilege)
        .filter(
            and_(
                UserPrivilege.user_id == linked_user.id,
                UserPrivilege.privilege_id == linked_privilege.id,
            )
        )
        .first()
    ):
        raise UOSDatabaseError("Privilege is a duplicate.")
    user_privilege = UserPrivilege(
        user_id=linked_user.id, privilege_id=linked_privilege.id
    )
    session.add(user_privilege)
    session.flush()


def add_api_key(
    session: Session, user_value: Union[int, str], user_field, expires: timedelta = None
) -> str:
    """
    Generate a new API key and link it to a user.

    :param session: The session_maker object to obtain a session from.
    :param user_value: The name or id of the user add the privilege to.
    :param user_field: The field to compare to the value parameter.
    :param expires: Timedelta defining when to expire the key, None is never. (default=None)
    :return: The generated API key string.

    """
    linked_user = get_user(session, user_value, user_field)
    if not linked_user:
        raise UOSDatabaseError("User must exist for API key to be added.")
    api_key = UserKey(user_id=linked_user.id, key_type=KeyTypes.API, expires=expires)
    session.add(api_key)
    session.flush()
    return api_key.key


def init_privilege(session: Session, id_: int, name: str):
    """
    Function for adding privilege types available in the program.

    :param session: The session_maker object to obtain a session from.
    :param id_: Primary key from the enum index for the privilege.
    :param name: The privilege name used for lookup, cannot already exist in db.
    :return:

    """
    # Check privilege doesn't already exist.
    if session.query(Privilege).filter(Privilege.name == name).first():
        return
    new_privilege = Privilege(id=id_, name=name)
    session.add(new_privilege)
    session.flush()
