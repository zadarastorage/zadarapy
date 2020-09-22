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
from zadarapy.validators import verify_boolean, verify_encryption_state, \
    get_parameters_options, verify_percentage


def get_settings_config(session, return_type=None, **kwargs):
    """
    Get VPSAOS setting configuration

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
    path = "/api/settings_config.json"
    return session.get_api(path=path, return_type=return_type, **kwargs)


def ssl_termination(session, is_terminate, return_type=None, **kwargs):
    """
    VPSAOS SSL termination

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type is_terminate: bool
    :param is_terminate: True iff terminate SSL. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    is_terminate = verify_boolean(is_terminate, is_terminate)
    path = "/api/zios/settings/ssl_termination.json"
    body_values = {"ssltermination": "on" if is_terminate else "off"}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_gradual_policy_expansion_percentage(session, expansion_percent, return_type=None, **kwargs):
    """
    Set gradual policy expansion percentage

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type expansion_percent: int
    :param expansion_percent: Expansion percentage (0-100). Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_percentage(expansion_percent)
    body_values = {"expansion_percent": expansion_percent}

    path = "/api/zios/settings/set_gradual_policy_expansion_percentage.json"
    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def set_encryption(session, encryption_pwd, return_type=None, **kwargs):
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
    parameters = get_parameters_options([('encryption_pwd', encryption_pwd)])
    return session.post_api(path=path, parameters=parameters,
                            return_type=return_type, **kwargs)


def set_encryption_state(session, state, return_type=None, **kwargs):
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
    verify_encryption_state(state)

    path = '/api/zios/settings/change_encryption.json'
    parameters = get_parameters_options([('state', state)])

    return session.post_api(path=path, parameters=parameters,
                            return_type=return_type, **kwargs)


def restore_encryption(session, encryption_pwd, return_type=None, **kwargs):
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
    parameters = get_parameters_options([('encryption_pwd', encryption_pwd)])
    return session.post_api(path=path, parameters=parameters,
                            return_type=return_type, **kwargs)
