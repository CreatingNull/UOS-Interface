"""Configuring fixtures for database testing."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from uosinterface.webapp.database import Base
from uosinterface.webapp.database import KeyTypes
from uosinterface.webapp.database.models import APIPrivilege
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserKeys
from uosinterface.webapp.database.models import UserPrivilege


test_user = {
    "name": "JaneDoe",
    "passwd": "jane.test",
    "email_address": "jane.doe@nulltek.xyz",
}
test_privilege = {"id": 9999, "name": "tester", "description": "Unit-test privilege."}


@pytest.fixture(scope="package")
def database():
    """In memory blank test database from the declarative model."""
    engine = create_engine("sqlite:///:memory:", future=True)
    session_maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True,
    )
    Base.metadata.create_all(engine)  # create our model
    populate_test_data(session_maker())
    yield session_maker
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(database):
    """Creates a session for use against the test database."""
    with database.begin():
        with database() as session:
            yield session
            session.rollback()  # cleanup the state of the test database during teardown


@pytest.fixture(scope="function")
def db_user(db_session):
    """Returns the test user object for reference in tests."""
    yield db_session.query(User).filter(User.name == test_user["name"]).first()


@pytest.fixture(scope="function")
def db_privilege(db_session):
    """Returns the test user object for reference in tests."""
    yield db_session.query(Privilege).filter(
        Privilege.name == test_privilege["name"]
    ).first()


def populate_test_data(db_session: Session):
    """Populates a test dataset across all tables."""
    with db_session as session:
        # Add an test privilege.
        db_session.add(Privilege(**test_privilege))
        # Populate a test user.
        db_session.add(User(**test_user))
        session.flush()
        user_id = session.query(User.id).filter(User.name == test_user["name"])
        privilege_id = session.query(Privilege.id).filter(
            Privilege.name == test_privilege["name"]
        )
        # Populate a relationship between jane and tester.
        db_session.add(UserPrivilege(user_id=user_id, privilege_id=privilege_id))
        # Add an api key for the user.
        db_session.add(UserKeys(key_length=64, user_id=user_id, key_type=KeyTypes.api))
        session.flush()
        # Populate a relationship between jane's API key and tester.
        db_session.add(
            APIPrivilege(
                key_id=session.query(UserKeys.id).filter(UserKeys.user_id == user_id),
                privilege_id=privilege_id,
            )
        )
        session.commit()
