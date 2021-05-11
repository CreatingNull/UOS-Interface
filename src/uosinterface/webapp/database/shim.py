"""Common high-level database interaction functionality."""
from typing import Union

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from uosinterface.webapp.database.models import User


def get_user(session_maker: sessionmaker, name_id: Union[int, str]) -> User:
    """
    get a user object via username or id.

    :param session_maker:
    :param name_id: integer id of the user or string name of the user.
    :return: User object if found otherwise None.

    """
    with session_maker() as session:
        return session.execute(
            select(User)
            .filter(
                (User.id == name_id)
                if isinstance(name_id, int)
                else (User.name == name_id)
            )
            .one()
        )
