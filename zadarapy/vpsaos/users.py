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

from zadarapy.validators import verify_start_limit, verify_account_id, \
    verify_boolean, verify_email, verify_field


def get_user(session, user_id, return_type=None, **kwargs):
    """
    Get VPSAOS User information

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/zios/users/{0}.json".format(user_id)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_all_users(session, account_id, start=None, limit=None,
                  return_type=None, **kwargs):
    """
    Get all VPSAOS Users information

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type start: int
    :param start: The offset to start displaying NAS users from.  Optional.

    :type: limit: int
    :param limit: The maximum number of NAS users to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id=account_id)
    parameters = verify_start_limit(start, limit)
    path = "/api/zios/accounts/{0}/users.json".format(account_id)
    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def add_new_user(session, account_id, username, email, role,
                 notify_on_events="NO", return_type=None, **kwargs):
    """
    Add new user

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type username: str
    :param username: Username. Required.

    :type email: str
    :param email: User Email. Required.

    :type: role: str
    :param role: Role. Required.

    :type: notify_on_events: str
    :param notify_on_events: "Yes" if notify on events, else "No"

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id)
    verify_boolean(notify_on_events, "notify_on_events")
    verify_field(username, "username")
    verify_email(email)
    verify_field(role, "role")

    path = "/api/zios/users.json"
    body_values = {'account_id': account_id, 'username': username,
                   'email': email, 'role': role,
                   'notify_on_events': notify_on_events}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_user(session, user_id, return_type=None, **kwargs):
    """
    Delete user

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(user_id, "user_id")
    path = "/api/zios/users/{0}.json".format(user_id)
    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_auth_token(session, account_id, username, password, return_type=None,
                   **kwargs):
    """
    Get user authentication token

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type username: str
    :param username: Username. Required.

    :type password: str
    :param password: User password. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/users/authenticate.json"
    body_values = {'account': account_id, 'user': username,
                   'password': password}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def disable_user(session, user_id, return_type=None, **kwargs):
    """
    Disable User

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(user_id, 'user_id')
    path = "/api/zios/users/{0}/disable.json".format(user_id)
    return session.post_api(path=path, return_type=return_type, **kwargs)


def enable_user(session, user_id, return_type=None, **kwargs):
    """
    Enable User

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(user_id, 'user_id')
    path = "/api/zios/users/{0}/enable.json".format(user_id)
    return session.post_api(path=path, return_type=return_type, **kwargs)


def disable_admin_access(session, return_type=None, **kwargs):
    """
    Disable Admin acccess

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
    path = "/api/users/admin_access/disable.json"
    return session.post_api(path=path, return_type=return_type, **kwargs)


def reset_token(session, account_id, user_id, password, return_type=None,
                **kwargs):
    """
    Enable User

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type password: str
    :param password: User password. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id)
    verify_field(user_id, 'user_id')
    verify_field(password, 'password')

    path = "/api/users/reset_token.json"
    body_values = {'account': account_id, 'user': user_id,
                   'password': password}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def change_password(session, account_id, user_id, password, new_password,
                    return_type=None, **kwargs):
    """
    Change user password

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type password: str
    :param password: User password. Required.

    :type new_password: str
    :param new_password: New password to change to. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id)
    verify_field(user_id, 'user_id')
    verify_field(password, 'password')
    verify_field(new_password, 'new_password')

    path = "/api/users/password.json"
    body_values = {'account': account_id, 'user': user_id,
                   'password': password, 'new_password': new_password}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def reset_password(session, account_id, user_id, return_type=None, **kwargs):
    """
    Reset user password

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id)
    verify_field(user_id, "user_id")
    path = '/api/zios/users/reset_password.json'
    body_values = {'account': account_id, 'username': user_id}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def reset_using_temporary_password(session, code, new_password, user_id,
                                   account_id, return_type=None, **kwargs):
    """
    Reset using temp password

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type code: str
    :param code: Required.

    :type new_password: str
    :param new_password: New user password ID. Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id)
    verify_field(user_id, "user_id")
    verify_field(new_password, 'new_password')
    verify_field(code, 'code')
    path = '/api/users/{0}/password_code'.format(user_id)
    body_values = {'code': code, 'new_password': new_password,
                   'account': account_id}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def change_user_role(session, user_id, role, return_type=None, **kwargs):
    """
    Change user role

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type: role: str
    :param role: Role. Required.

    :type user_id: str
    :param user_id: User ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(user_id, "user_id")
    verify_field(role, "role")
    path = '/api/zios/users/{0}/change_rol.json'.format(user_id)
    body_values = {'role': role}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
