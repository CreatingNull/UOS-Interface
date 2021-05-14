"""Common high-level database interaction functionality."""
from typing import Union

from sqlalchemy.orm import sessionmaker
from uosinterface.webapp.database.models import User


def get_user(
    session_maker: sessionmaker, identifier: Union[int, str], user_field=User.id
) -> User:
    """
    get a user object via username or id.

    :param session_maker: The session_maker object to obtain a session from.
    :param identifier: Identifying parameter for looking up the user.
    :param user_field: The field on which to compare to the identifying parameter (default id).
    :return: User object if found otherwise None.

    """
    with session_maker() as session:
        return session.query(User).filter(user_field == identifier).first()
