"""Testing the authentication functionality of the web-app."""
from flask_login import AnonymousUserMixin
from uosinterface.webapp.auth import check_privileges
from uosinterface.webapp.auth import PrivilegeNames
from uosinterface.webapp.database.models import Privilege
from uosinterface.webapp.database.models import User
from uosinterface.webapp.database.models import UserPrivilege


def test_check_privileges(db_session, db_user: User, db_privilege: Privilege):
    """
    Checks the low level authentication checking responds as designed.

    :param db_session: Pytest fixture allocated session.:
    :param db_user: Default test user object.
    :param db_privilege: Default test privilege object.
    :return:

    """
    # Test logged in user can access with empty privilege list.
    assert check_privileges([], db_session, db_user)
    # Test logged in user can access if named in privilege list.
    assert check_privileges([db_privilege.name], db_session, db_user)
    # Test admin can access all views without explicitly defined.
    admin_privilege = Privilege(id=999, name=PrivilegeNames.ADMIN.name)
    db_session.add(admin_privilege)
    db_session.add(UserPrivilege(user_id=db_user.id, privilege_id=admin_privilege.id))
    db_session.flush()
    assert check_privileges(["InvalidPrivilege"], db_session, db_user)
    db_session.rollback()  # get rid of that admin stuff
    # Test not logged in user is denied with empty privilege list.
    assert not check_privileges([], db_session, AnonymousUserMixin())
    # Test logged in user blocked if not named in privilege list.
    assert not check_privileges([PrivilegeNames.READ], db_session, db_user)
