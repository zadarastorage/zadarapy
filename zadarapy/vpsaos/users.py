# Copyright 2018 Zadara Storage, Inc.
# Originally authored by Jeremy Brown - https://github.com/jwbrown77
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.


from future.standard_library import install_aliases

install_aliases()

import json
from zadarapy.validators import is_valid_field


def create_user(session, accountid, username, email, role="member",
                return_type=None):
    """
    Create a VPSAOS user in the given account.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The VPSAOS unique account-id.  Required.

    :type username: str
    :param username: The VPSAOS user's username.  Required.

    :type email: str
    :param email: The VPSAOS user's email address.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    body_values = {}

    if not is_valid_field(accountid):
        raise ValueError('{0} is not a valid account-id.'
                         .format(accountid))

    body_values['account_id'] = accountid
    body_values['username'] = username
    body_values['email'] = email
    body_values['notify_on_events'] = "YES"
    body_values['role'] = role

    method = 'POST'
    path = '/api/zios/users.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def delete_user(session, userid, return_type=None):
    """
    Delete a VPSAOS user.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type userid: str
    :param userid: The VPSAOS unique user-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(userid):
        raise ValueError('{0} is not a valid user-id.'
                         .format(userid))

    method = 'DELETE'
    path = '/api/zios/users/%s.json' % userid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def enable_user(session, userid, return_type=None):
    """
    Enable a VPSAOS user.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type userid: str
    :param user_id: The VPSAOS unique user-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(userid):
        raise ValueError('{0} is not a valid userid.'
                         .format(userid))

    method = 'POST'
    path = '/api/zios/users/%s/enable.json' % userid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def disable_user(session, userid, return_type=None):
    """
    Disable a VPSAOS user.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type userid: str
    :param user_id: The VPSAOS unique user-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(userid):
        raise ValueError('{0} is not a valid user-id.'
                         .format(userid))

    method = 'POST'
    path = '/api/zios/users/%s/disable.json' % userid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def change_user_role(session, userid, role="member", return_type=None):
    """
    Change VPSAOS user role (can be member or admin)
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type userid: str
    :param userid: The VPSAOS user's user-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    body_values = {}

    if not is_valid_field(userid):
        raise ValueError('{0} is not a valid userid.'
                         .format(userid))

    body_values['role'] = role

    method = 'POST'
    path = '/api/zios/users/%s/change_role.json' % userid

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def change_user_password(session, accountname, username, password, newpassword,
                         return_type=None):
    """
    Channge the user default password
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountname: str
    :param accountname: The VPSAOS account name.  Required.

    :type username: str
    :param username: The VPSAOS user's user name.  Required.

    :type password: str
    :param password: The user's password.  Required.

    :type newpassword: str
    :param newpassword: The user's new password.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    body_values = {}

    if not is_valid_field(accountname):
        raise ValueError('{0} is not a valid account name.'
                         .format(accountname))

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid user name.'
                         .format(username))

    body_values['account'] = accountname
    body_values['username'] = username
    body_values['password'] = password
    body_values['new_password'] = newpassword

    method = 'POST'
    path = '/api/users/password.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def get_user(session, userid, return_type=None):
    """
    Get VPSAOS user
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type userid: str
    :param userid: The VPSAOS user's user-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    method = 'GET'
    path = '/api/zios/users/%s.json' % userid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def get_all_users(session, return_type=None):
    """
    Get all VPSAOS users in the VPSA object store
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    method = 'GET'
    path = '/api/zios/users.json'

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def get_auth_token(session, accountname, username, password, return_type=None):
    """
    Get the user auth token for IO
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountname: str
    :param accountname: The VPSAOS account name.  Required.

    :type username: str
    :param username: The VPSAOS user's user name.  Required.

    :type password: str
    :param password: The user's password.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    body_values = {}

    if not is_valid_field(accountname):
        raise ValueError('{0} is not a valid account name.'
                         .format(accountname))

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid user name.'
                         .format(username))

    body_values['account'] = accountname
    body_values['user'] = username
    body_values['password'] = password

    method = 'POST'
    path = '/api/users/authenticate.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)
