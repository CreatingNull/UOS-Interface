"""Test module for the high common function interface for the database."""
import pytest
from sqlalchemy import and_
from sqlalchemy.orm import Session
from uosinterface import UOSDatabaseError
from uosinterface.webapp.auth import PrivilegeNames
from uosinterface.webapp.database.interface import add_user
from uosinterface.webapp.database.interface import add_user_privilege
from uosinterface.webapp.database.interface import get_user
from uosinterface.webapp.database.interface import get_user_privileges
from uosinterface.webapp.database.interface import init_privilege
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKeys
from uosinterface.webapp.database.models import UserPrivilege


def test_get_user(db_session: Session, db_user: User):
    """
    Checks the interface function supports all lookup methods.

    :param db_session: Pytest fixture allocated session.
    :param db_user: Default test user object.
    :return:

    """
    user = db_session.query(User).filter(User.name == db_user.name).first()
    user_key = db_session.query(UserKeys).filter(UserKeys.user_id == user.id).first()
    # lookup via user id
    assert user == get_user(db_session, db_user.id)
    # lookup via user name
    assert user == get_user(db_session, db_user.name, User.name)
    # lookup via user api key
    assert user == get_user(db_session, user_key.user_id, UserKeys.user_id)
    # lookup list of all users
    users = get_user(db_session)
    assert isinstance(users, list)
    assert len(users) > 0 and users[0] == user
    # lookup on non-existent user should return None
    assert not get_user(db_session, "InvalidUser", User.name)


def test_add_user(db_session: Session, db_user: User):
    """
    Tests the function executes and fails as designed.

    :param db_session: Pytest fixture allocated session.
    :param db_user: Default test user object.
    :return:

    """
    # test user add
    confirm_query = db_session.query(User).filter(User.name == "NormalAdd")
    assert not confirm_query.first()  # sanity check
    # Bandit should ignore hardcoded passwords in test contexts
    add_user(db_session, name="NormalAdd", passwd="NormalAdd")  # nosec
    assert confirm_query.first()
    # test a user can be added with an email
    confirm_query = db_session.query(User).filter(User.name == "WithEmailAdd")
    assert not confirm_query.first()  # sanity check
    # Bandit should ignore hardcoded passwords in test contexts
    add_user(
        db_session,
        name="WithEmailAdd",
        passwd="WithEmailAdd",
        email="withemailadd@nulltek.xyz",
    )  # nosec
    assert confirm_query.first()
    # test adding a duplicate user throws error
    with pytest.raises(UOSDatabaseError):
        # Bandit should ignore hardcoded passwords in test contexts
        add_user(db_session, db_user.name, passwd="test")  # nosec


def test_get_user_privileges(
    db_session: Session, db_user: User, db_privilege: Privilege
):
    """
    Tests the user privileges can be looked up as both list and object.

    :param db_session: Pytest fixture allocated session.
    :param db_user: Default test user object.
    :param db_privilege: Default test privilege object.
    :return:

    """
    privilege = (
        db_session.query(Privilege).filter(Privilege.name == db_privilege.name).first()
    )
    # Test typical all privilege lookup.
    privileges = get_user_privileges(db_session, db_user.name, User.name)
    assert isinstance(privileges, list)
    assert len(privileges) > 0
    assert privileges[0] == privilege
    # Test single privilege lookup.
    privileges = get_user_privileges(
        db_session,
        db_user.name,
        User.name,
        privilege.id,
        Privilege.id,
    )
    assert privileges == privilege  # check object returned
    # Test bad user lookup returns empty list.
    privileges = get_user_privileges(db_session, "InvalidName", User.name)
    assert isinstance(privileges, list)
    assert len(privileges) == 0
    # Test bad privilege returns None.
    privileges = get_user_privileges(
        db_session, db_user.name, User.name, "InvalidPrivilege", Privilege.name
    )
    assert not privileges


def test_add_user_privilege(
    db_session: Session, db_user: User, db_privilege: Privilege
):
    """
    Test call methods for adding a user to a group and failure cases.

    :param db_session: Pytest fixture allocated session.
    :param db_user: Default test user object.
    :param db_privilege: Default test privilege object.
    :return:

    """
    db_session.add(Privilege(name="NewPrivilege"))
    db_session.add(Privilege(name="NewerPrivilege"))
    db_session.flush()
    newer_privilege = (
        db_session.query(Privilege).filter(Privilege.name == "NewerPrivilege").first()
    )
    # Test error raised with bad user
    with pytest.raises(UOSDatabaseError) as exception:
        add_user_privilege(
            db_session, "InvalidUser", User.name, "NewPrivilege", Privilege.name
        )
    assert "User must exist" in str(exception.value)
    # Test error raised with bad privilege
    with pytest.raises(UOSDatabaseError) as exception:
        add_user_privilege(
            db_session, db_user.id, User.id, "InvalidPrivilege", Privilege.name
        )
    assert "Privilege must exist" in str(exception.value)
    # Test error raised with duplicate user_privilege.
    with pytest.raises(UOSDatabaseError) as exception:
        add_user_privilege(
            db_session, db_user.name, User.name, db_privilege.name, Privilege.name
        )
    assert "duplicate" in str(exception.value)
    # Tests normal case with lookup via names
    confirm_query = (
        db_session.query(UserPrivilege)
        .join(Privilege)
        .filter(
            and_(
                UserPrivilege.user_id == db_user.id,
                Privilege.name == "NewPrivilege",
            )
        )
    )
    assert not confirm_query.first()  # sanity check
    add_user_privilege(
        db_session, db_user.name, User.name, "NewPrivilege", Privilege.name
    )
    assert confirm_query.first()
    # Tests normal case with lookup via ids
    confirm_query = db_session.query(UserPrivilege).filter(
        and_(
            UserPrivilege.user_id == db_user.id,
            UserPrivilege.privilege_id == newer_privilege.id,
        )
    )
    assert not confirm_query.first()  # sanity check
    add_user_privilege(
        db_session, db_user.id, User.id, newer_privilege.id, Privilege.id
    )
    assert confirm_query.first()


def test_init_privilege(db_session: Session):
    """
    Tests privileges are created and fail cases are triggered correctly.

    :param db_session: Pytest fixture allocated session.:
    :return:

    """
    # Check a normal create works as expected.
    confirm_query = db_session.query(Privilege).filter(
        Privilege.name == PrivilegeNames.ADMIN.name
    )
    assert not confirm_query.first()
    init_privilege(
        db_session,
        PrivilegeNames.ADMIN.value,
        PrivilegeNames.ADMIN.name,
    )
    assert confirm_query.count() == 1
    # Check duplication returns without duplicating
    init_privilege(
        db_session,
        100,  # un-consumed privilege.id
        PrivilegeNames.ADMIN.name,
    )
    assert confirm_query.count() == 1
