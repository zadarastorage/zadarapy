# Copyright 2019 Zadara Storage, Inc.
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
from urllib.parse import quote

install_aliases()

from zadarapy.validators import verify_field, verify_start_limit, \
    verify_email


def get_all_vpsa_users(session, start=None, limit=None, return_type=None,
                       **kwargs):
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
    parameters = verify_start_limit(start, limit)

    path = '/api/users.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def create_vpsa_user(session, username, email, return_type=None, **kwargs):
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
    username = verify_field(username, "username")
    email = verify_email(email)

    body_values = {'username': username, 'email': email}

    path = '/api/users.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_vpsa_user(session, username, return_type=None, **kwargs):
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
    username = verify_field(username, "username")

    username = quote(username)

    path = '/api/users/{0}.json'.format(username)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_vpsa_user_api_key(session, username, password, return_type=None,
                          **kwargs):
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
    username = verify_field(username, "username")
    password = verify_field(password, "password", allow_quote=True)

    body_values = {'user': username, 'password': password}

    path = '/api/users/login.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def reset_vpsa_user_api_key(session, username, password,
                            return_type=None, **kwargs):
    """
    Resets the VPSA user's API/access key to a new value.  Only a VPSA admin
    may perform this action.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required. Note
        that API key MUST be specified for the Session, even though the point
        of this function is to reset the API key. So just provide any string
        as the API key for this session.
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
    username = verify_field(username, "username")
    username_for_path = quote(username)
    password = verify_field(password, 'password', allow_quote=True)

    path = '/api/users/{0}/access_key.json'.format(username_for_path)
    body = {'username': username, 'password' : password}

    return session.post_api(path=path, body=body,
                            return_type=return_type,**kwargs)


def change_vpsa_user_password_by_password(session, username,
                                          existing_password, new_password,
                                          return_type=None, **kwargs):
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
    username = verify_field(username, "username")
    existing_password = verify_field(existing_password, "existing_password",
                                     allow_quote=True)
    new_password = verify_field(new_password, "new_password", allow_quote=True)

    body_values = {'user': username, 'password': existing_password,
                   'new_password': new_password}

    path = '/api/users/password.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def change_vpsa_user_password_by_code(session, username, code, new_password,
                                      return_type=None, **kwargs):
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
    username = verify_field(username, "username")
    username = quote(username)
    new_password = verify_field(new_password, "new_password", allow_quote=True)

    body_values = {'code': code, 'new_password': new_password}

    path = '/api/users/{0}/password_code.json'.format(username)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def generate_vpsa_user_password_reset_code(session, username,
                                           return_type=None, **kwargs):
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
    username = verify_field(username, "username")

    body_values = {'username': username}

    path = '/api/users/reset_password.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def enable_cloud_admin_access(session, confirm, return_type=None, **kwargs):
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

    path = '/api/users/admin_access/enable.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def disable_cloud_admin_access(session, confirm, return_type=None, **kwargs):
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

    path = '/api/users/admin_access/disable.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)
