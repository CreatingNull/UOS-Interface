"""Unit tests for the webapp database package."""
import pytest
from sqlalchemy.orm import Session
from tests.testwebapp.test_database.conftest import test_privilege
from tests.testwebapp.test_database.conftest import test_user
from uosinterface import UOSDatabaseError
from uosinterface.webapp.database import hash_pass
from uosinterface.webapp.database import KeyTypes
from uosinterface.webapp.database import verify_pass
from uosinterface.webapp.database.interface import add_user
from uosinterface.webapp.database.interface import get_user
from uosinterface.webapp.database.interface import get_user_privileges
from uosinterface.webapp.database.models import APIPrivilege
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKeys
from uosinterface.webapp.database.models import UserPrivilege


class TestInterface:
    """Contains tests for the high-level interface module."""

    @staticmethod
    def test_get_user(db_session):
        """
        Checks the interface function supports all lookup methods.

        :param db_session: Pytest fixture allocated session.
        :return:

        """
        user = db_session.query(User).filter(User.name == test_user["name"]).first()
        user_key = (
            db_session.query(UserKeys).filter(UserKeys.user_id == user.id).first()
        )
        # lookup via user id
        assert user == get_user(db_session, User.id)
        # lookup via user name
        assert user == get_user(db_session, User.name, user.name)
        # lookup via user api key
        assert user == get_user(db_session, UserKeys.user_id, user_key.user_id)
        # lookup on non-existent user should return None
        assert not get_user(db_session, User.name, "InvalidUser")

    @staticmethod
    def test_add_user(db_session):
        """
        Tests the function executes and fails as designed.

        :param db_session: Pytest fixture allocated session.:
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
            add_user(db_session, test_user["name"], passwd="test")

    @staticmethod
    def test_get_user_privileges(db_session):
        """
        Tests the user privileges can be looked up as both list and object.

        :param db_session: Pytest fixture allocated session.:
        :return:

        """
        privilege = (
            db_session.query(Privilege)
            .filter(Privilege.name == test_privilege["name"])
            .first()
        )
        # Test typical all privilege lookup.
        privileges = get_user_privileges(db_session, test_user["name"], User.name)
        assert isinstance(privileges, list)
        assert len(privileges) > 0
        assert privileges[0] == privilege
        # Test single privilege lookup.
        privileges = get_user_privileges(
            db_session,
            test_user["name"],
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
            db_session, test_user["name"], User.name, "InvalidPrivilege", Privilege.name
        )
        assert not privileges


def test_user_cascades(db_session: Session):
    """
    Checks the test data exists and cascades correctly on removal.

    :param db_session: Pytest fixture allocated session.
    :return:

    """
    user = db_session.query(User).filter(User.name == test_user["name"]).first()
    assert user  # check user populated at start
    user_key = db_session.query(UserKeys).filter(UserKeys.user_id == user.id).first()
    assert user_key  # check api key is populated at start
    assert user_key.key_type == KeyTypes.api
    api_privilege = (
        db_session.query(APIPrivilege)
        .filter(APIPrivilege.key_id == user_key.id)
        .first()
    )
    assert api_privilege  # test api privilege for key is populated at start
    user_privilege = (
        db_session.query(UserPrivilege).filter(UserPrivilege.user_id == user.id).first()
    )
    assert user_privilege
    db_session.delete(user)
    db_session.flush()
    # Check deletion of the user cascades as expected
    user_key = db_session.query(UserKeys).first()
    assert not user_key
    api_privilege = db_session.query(APIPrivilege).first()
    assert not api_privilege
    user_privilege = db_session.query(UserPrivilege).first()
    assert not user_privilege
    # Sanity check that the privilege entry is still present
    privilege = db_session.query(Privilege).first()
    assert privilege


@pytest.mark.parametrize(
    "passwd,saved_hash",
    [
        [
            "abc123",
            b"5b1fa9538d578172d4fd93b8c7b8691fc9c34feb51abe3b06f4c27d052a"
            b"34d27fc42de26a7e267403c5a36c6bd9dee6a430d4cd5f6f62a532d1874"
            b"4242fa8c36019389a8d5088ada41dda29da907165d02e86ecc0a84ec920"
            b"7e73e55147e9e337bd98fc38893c8c2f9234fb318a1d862aa9ca76feda7"
            b"b9c1fe1e896cd2aa2320",
        ]
    ],
)
def test_password_hashing(passwd: str, saved_hash: bytes):
    """
    Tests passwords against a known saved hash and a newly generated hash.

    :param passwd: An example string password.
    :param saved_hash: An example saved hash.
    :return:

    """
    new_hash = hash_pass(passwd)
    assert verify_pass(passwd, new_hash)
    assert verify_pass(passwd, saved_hash)
    assert new_hash != saved_hash  # check sha512 salting is working
