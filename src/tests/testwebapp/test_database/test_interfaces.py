import pytest
from sqlalchemy import and_
from sqlalchemy.orm import Session
from uosinterface import UOSDatabaseError
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
    assert user == get_user(db_session, User.id)
    # lookup via user name
    assert user == get_user(db_session, User.name, user.name)
    # lookup via user api key
    assert user == get_user(db_session, UserKeys.user_id, user_key.user_id)
    # lookup on non-existent user should return None
    assert not get_user(db_session, User.name, "InvalidUser")


def test_add_user(db_session: Session, db_user: User):
    """
    Tests the function executes and fails as designed.

    :param db_session: Pytest fixture allocated session.
    :param db_user: Default test user object.
    :return:

    """
    # test user add
    add_user(db_session, name="NormalAdd", passwd="NormalAdd")
    assert get_user(db_session, "NormalAdd", User.name)
    # test a user can be added with an email
    add_user(
        db_session,
        name="WithEmailAdd",
        passwd="WithEmailAdd",
        email="withemailadd@nulltek.xyz",
    )
    assert get_user(db_session, "WithEmailAdd", User.name)
    # test adding a duplicate user throws error
    with pytest.raises(UOSDatabaseError):
        add_user(db_session, db_user.name, passwd="test")


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
    db_session.add(Privilege(name="NewPrivilege", description="A test privilege"))
    db_session.add(Privilege(name="NewerPrivilege", description="A test privilege"))
    db_session.flush()
    newer_privilege = (
        db_session.query(Privilege).filter(Privilege.name == "NewerPrivilege").first()
    )
    # Test error raised with bad user
    with pytest.raises(UOSDatabaseError) as exception:
        add_user_privilege(db_session, "InvalidUser", "NewPrivilege")
        assert "User" in exception.value
    # Test error raised with bad privilege
    with pytest.raises(UOSDatabaseError) as exception:
        add_user_privilege(db_session, "InvalidUser", "InvalidPrivilege")
        assert "Privilege" in exception
    # Test error raised with duplicate user_privilege.
    with pytest.raises(UOSDatabaseError) as exception:
        add_user_privilege(db_session, db_user.name, db_privilege.name)
        assert "duplicate" in exception
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
    add_user_privilege(db_session, db_user.name, "NewPrivilege")
    assert confirm_query.first()
    # Tests normal case with lookup via ids
    confirm_query = db_session.query(UserPrivilege).filter(
        and_(
            UserPrivilege.user_id == db_user.id,
            UserPrivilege.privilege_id == newer_privilege.id,
        )
    )
    assert not confirm_query.first()  # sanity check
    add_user_privilege(db_session, db_user.id, newer_privilege.id)
    assert confirm_query.first()


def test_init_privilege(db_session: Session, db_user: User, db_privilege: Privilege):
    """
    Tests privileges are created and fail cases are triggered correctly.

    :param db_session: Pytest fixture allocated session.:
    :param db_user: Default test user object.
    :param db_privilege: Default test privilege object.
    :return:

    """
    # Check a normal create works as expected.
    init_privilege(db_session, "NewPrivilege", "A test privilege.")
    assert db_session.query(Privilege).filter(Privilege.name == "NewPrivilege").first()
    # Check duplication of privilege raises error correctly
    with pytest.raises(UOSDatabaseError):
        init_privilege(db_session, Privilege.name, Privilege.description)
