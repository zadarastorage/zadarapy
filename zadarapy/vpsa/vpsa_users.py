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
from urllib.parse import quote
from zadarapy.validators import is_valid_email
from zadarapy.validators import is_valid_field


def get_all_vpsa_users(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all configured VPSA users.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying VPSA users from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of VPSA users to return.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/users.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def create_vpsa_user(session, username, email, return_type=None):
    """
    Creates a VPSA user.  User will receive a temporary password at the
    provided email address and will be forced to change it on first login.
    Only a VPSA admin may perform this action.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type email: str
    :param email: The VPSA user's email address.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    body_values['username'] = username

    if not is_valid_email(email):
        raise ValueError('{0} is not a valid email address.'
                         .format(email))

    body_values['email'] = email

    method = 'POST'
    path = '/api/users.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_vpsa_user(session, username, return_type=None):
    """
    Deletes a VPSA user.  Only a VPSA admin may perform this action.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    username = quote(username)

    method = 'DELETE'
    path = '/api/users/{0}.json'.format(username)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_vpsa_user_api_key(session, username, password, return_type=None):
    """
    Retrieves a VPSA user's API key by their username and password.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type password: str
    :param password: The VPSA user's password.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    body_values['user'] = username

    if not is_valid_field(password, allow_quote=True):
        raise ValueError('A valid VPSA password was not given.')

    body_values['password'] = password

    method = 'POST'
    path = '/api/users/login.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def reset_vpsa_user_api_key(session, username, return_type=None):
    """
    Resets the VPSA user's API/access key to a new value.  Only a VPSA admin
    may perform this action.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    username = quote(username)

    method = 'POST'
    path = '/api/users/{0}/access_key.json'.format(username)

    return session.call_api(method=method, path=path, return_type=return_type)


def change_vpsa_user_password_by_password(session, username,
                                          existing_password, new_password,
                                          return_type=None):
    """
    Changes a VPSA user's password.  The user needs their existing password to
    use this method.  If the password was forgotten, use the
    change_vpsa_user_password_by_code method.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type existing_password: str
    :param existing_password: The VPSA user's existing password.  Required.

    :type new_password: str
    :param new_password: The new password for the VPSA user.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    body_values['user'] = username

    if not is_valid_field(existing_password, allow_quote=True):
        raise ValueError('A valid VPSA password was not given.')

    body_values['password'] = existing_password

    if not is_valid_field(new_password, allow_quote=True):
        raise ValueError('A valid VPSA password was not given.')

    body_values['new_password'] = new_password

    method = 'POST'
    path = '/api/users/password.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def change_vpsa_user_password_by_code(session, username, code, new_password,
                                      return_type=None):
    """
    Changes a VPSA user's password with a password reset code.  If the user
    knows their existing password, use change_vpsa_user_password_by_password
    instead.  Use generate_vpsa_user_password_reset_code to send a reset code
    to the user via e-mail.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type code: str
    :param code: The password reset code e-mailed to the user.  Required.

    :type new_password: str
    :param new_password: The new password for the VPSA user.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    username = quote(username)

    body_values['code'] = code

    if not is_valid_field(new_password, allow_quote=True):
        raise ValueError('A valid VPSA password was not given.')

    body_values['new_password'] = new_password

    method = 'POST'
    path = '/api/users/{0}/password_code.json'.format(username)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def generate_vpsa_user_password_reset_code(session, username,
                                           return_type=None):
    """
    Initiates a password reset for a VPSA user and e-mails the user a code
    that can be used with change_vpsa_user_password_by_code.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The VPSA user's username.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'
                         .format(username))

    body_values['username'] = username

    method = 'POST'
    path = '/api/users/reset_password.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def enable_cloud_admin_access(session, confirm, return_type=None):
    """
    Enables the ability of a storage cloud administrator to access the VPSA
    GUI of this VPSA to assist in troubleshooting.  This does not grant access
    to any volume data.  Enabled by default.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type confirm: bool
    :param confirm: If True, cloud admin access will be enabled.  This is a
        safeguard for this function since it requires no other arguments.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not confirm:
        raise ValueError('The confirm parameter is not set to True - '
                         'cloud admin access will not be enabled.')

    method = 'POST'
    path = '/api/users/admin_access/enable.json'

    return session.call_api(method=method, path=path, return_type=return_type)


def disable_cloud_admin_access(session, confirm, return_type=None):
    """
    Disables the ability of a storage cloud administrator to access the VPSA
    GUI of this VPSA to assist in troubleshooting.  This does not grant access
    to any volume data.  Enabled by default.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type confirm: bool
    :param confirm: If True, cloud admin access will be disabled.  This is a
        safeguard for this function since it requires no other arguments.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not confirm:
        raise ValueError('The confirm parameter is not set to True - '
                         'cloud admin access will not be disabled.')

    method = 'POST'
    path = '/api/users/admin_access/disable.json'

    return session.call_api(method=method, path=path, return_type=return_type)
