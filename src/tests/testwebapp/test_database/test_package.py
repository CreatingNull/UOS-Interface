"""Unit tests for the webapp database package."""
import pytest
from sqlalchemy.orm import Session
from uosinterface.webapp.database import hash_pass
from uosinterface.webapp.database import KeyTypes
from uosinterface.webapp.database import verify_pass
from uosinterface.webapp.database.models import APIPrivilege
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKey
from uosinterface.webapp.database.models import UserPrivilege


def test_user_cascades(db_session: Session, db_user: User):
    """
    Checks the test data exists and cascades correctly on removal.

    :param db_session: Pytest fixture allocated session.
    :param db_user: Default test user object.
    :return:

    """
    user = db_session.query(User).filter(User.id == db_user.id).first()
    assert user  # check user populated at start
    user_key = db_session.query(UserKey).filter(UserKey.user_id == user.id).first()
    assert user_key  # check api key is populated at start
    assert user_key.key_type == KeyTypes.API
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
    user_key = db_session.query(UserKey).first()
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
