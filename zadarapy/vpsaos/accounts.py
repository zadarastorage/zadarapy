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
from zadarapy.validators import verify_account_id, verify_start_limit, \
    verify_field, verify_boolean


def get_all_accounts(session, start=None, limit=None, return_type=None,
                     **kwargs):
    """
    Get details on all VPSAOS accounts.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying accounts from.  Optional.

    :type: limit: int
    :param limit: The maximum number of accounts to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start=start, limit=limit)

    path = "/api/zios/accounts.json"
    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_account(session, account_id, return_type=None, **kwargs):
    """
    Get details of a single account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}.json".format(account_id)
    return session.get_api(path=path, secure=True, return_type=return_type,
                           **kwargs)


def create_account(session, account_name, return_type=None, **kwargs):
    """
    Create a VPSAOS account.  An object storage account is a collection of
    containers. Typically an account is associated with a tenant.  Access
    rights can be granted for users per account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_name: str
    :param account_name: A text label assigned to the VPSAOS account name.
        For example, 'accounting' or 'sales'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(account_name, "account_name")
    path = "/api/zios/accounts.json"
    body_values = {'name': account_name}
    return session.post_api(path=path, body=body_values, secure=True,
                            return_type=return_type, **kwargs)


def delete_account(session, account_id, force='NO', return_type=None,
                   **kwargs):
    """
    Delete a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type account_id: str
    :param account_id: The VPSAOS account 'id' value as returned by
        get_all_accounts.  For example: '91ea5bd5cdc04adb9f5e3c00a346c463'.
        Required.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSAOS to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(account_id=account_id)
    verify_boolean(force, 'force')

    path = "/api/zios/accounts/{0}.json".format(account_id)
    body_values = {'force': force}
    return session.delete_api(path=path, body=body_values, secure=True,
                              return_type=return_type, **kwargs)


def cleanup_account(session, account_id, return_type=None, **kwargs):
    """
    Cleanup a VPSAOS account's details.  This will remove billing information
    after an account was deleted.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}/cleanup.json".format(account_id)
    return session.delete_api(path=path, secure=True, return_type=return_type,
                              **kwargs)


def disable_account(session, account_id, return_type=None, **kwargs):
    """
    Disable a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}/disable.json".format(account_id)
    return session.post_api(path=path, secure=True, return_type=return_type,
                            **kwargs)


def get_all_users_in_account(session, account_id, return_type=None, **kwargs):
    """
    Get details for all users in a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    path = '/api/zios/accounts/{0}/users.json'.format(account_id)
    return session.get_api(path=path, secure=True, return_type=return_type,
                           **kwargs)


def enable_account(session, account_id, return_type=None, **kwargs):
    """
    Enable a VPSAOS account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}/enable.json".format(account_id)
    return session.post_api(path=path, secure=True, return_type=return_type,
                            **kwargs)
