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


def set_encryption(session, encryption_pwd, return_type=None):
    """
    Set encryption.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type encryption_pwd: string
    :param encryption_pwd: The encryption_pwd.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/zios/settings/encryption.json'

    parameters = {k: v for k, v in (('encryption_pwd', encryption_pwd),)
                  if v is not None}

    return session.post_api(path=path, parameters=parameters,
                            return_type=return_type)


def set_encryption_state(session, state, return_type=None):
    """
    Set encryption state.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type state: string
    :param state: state enable/disable.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if state not in ('enable', 'disable'):
        raise ValueError('{0} is not a valid state.'.format(state))

    path = '/api/zios/settings/change_encryption.json'

    parameters = {k: v for k, v in (('state', state),)
                  if v is not None}

    return session.post_api(path=path, parameters=parameters,
                            return_type=return_type)


def restore_encryption(session, encryption_pwd, return_type=None):
    """
    Restore encryption.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type encryption_pwd: string
    :param encryption_pwd: The encryption_pwd.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/zios/settings/restore_encryption.json'

    parameters = {k: v for k, v in (('encryption_pwd', encryption_pwd),)
                  if v is not None}

    return session.post_api(path=path, parameters=parameters,
                            return_type=return_type)
