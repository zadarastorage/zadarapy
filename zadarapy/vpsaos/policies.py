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
from zadarapy.validators import verify_start_limit, verify_field


def get_all_policies(session, start=None, limit=None, return_type=None,
                     **kwargs):
    """
    Retrieves details for all Storage policies in the VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying controllers from.  Optional.

    :type: limit: int
    :param limit: The maximum number of controllers to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)
    path = '/api/zios/policies.json'
    return session.get_api(path=path, parameters=parameters,
                           secure=True, return_type=return_type, **kwargs)


def get_policy(session, policy_name, return_type=None, **kwargs):
    """
    Retrieves details for a single virtual controller for the VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(policy_name, "policy_name")
    path = '/api/zios/policies/{0}.json'.format(policy_name)
    return session.get_api(path=path, secure=True, return_type=return_type,
                           **kwargs)


def set_default_policy(session, policy_name, return_type=None, **kwargs):
    """
    Set the policy as a default policy

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/zios/policies/{0}/set_default.json'.format(policy_name)

    return session.post_api(path=path, secure=True, return_type=return_type,
                            **kwargs)
