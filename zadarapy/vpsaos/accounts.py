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


def create_account(session, accountname, return_type=None):
    """
    Creates a VPSAOS account.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountname: str
    :param accountname: The VPSAOS account name.  Required.

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
        raise ValueError('{0} is not a valid VPSA Object store account name.'
                         .format(accountname))

    body_values['name'] = accountname

    method = 'POST'
    path = '/api/zios/accounts.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def delete_account(session, accountid, return_type=None):
    """
    Delete a VPSAOS account.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The VPSAOS unique account_id for the
         account name to be deleted.  Required.

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

    body_values['force'] = "YES"

    method = 'DELETE'
    path = '/api/zios/accounts/%s.json' %accountid

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body, secure=True,
                            return_type=return_type)


def cleanup_account(session, accountid, return_type=None):
    """
    Cleanup a VPSAOS account details (billing inforamtion).
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The VPSAOS unique account-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(accountid):
        raise ValueError('{0} is not a valid accountid.'
                         .format(accountid))

    method = 'DELETE'
    path = '/api/zios/accounts/%s/cleanup.json'%accountid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def disable_account(session, accountid, return_type=None):
    """
    Disable a VPSAOS account.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The VPSAOS unique account-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(accountid):
        raise ValueError('{0} is not a valid account-id.'
                         .format(accountid))

    method = 'POST'
    path = '/api/zios/accounts/%s/disable.json' %accountid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def enable_account(session, accountid, return_type=None):
    """
    Enable a VPSAOS account.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The vpsaos unique account-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(accountid):
        raise ValueError('{0} is not a valid account-id.'
                         .format(accountid))

    method = 'POST'
    path = '/api/zios/accounts/%s/enable.json'%accountid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def get_account(session, accountid, return_type=None):
    """
    Get the details of the account
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The VPSAOS accounts's account-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if not is_valid_field(accountid):
        raise ValueError('{0} is not a valid VPSA Object store account-id.'
                         .format(accountid))

    method = 'GET'
    path = '/api/zios/accounts/%s.json' %accountid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def get_all_accounts(session, return_type=None):
    """
    Get all VPSAOS accounts in VPSA object storage
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
    path = '/api/zios/accounts.json'

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)


def get_all_users_in_account(session, accountid, return_type=None):
    """
    Get all users in the VPSAOS account
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type accountid: str
    :param accountid: The VPSAOS accounts's account-id.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    method = 'GET'
    path = '/api/zios/accounts/%s/users.json' %accountid

    return session.call_api(method=method, path=path, secure=True,
                            return_type=return_type)

