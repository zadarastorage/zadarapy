# Copyright 2020 Zadara Storage, Inc.
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

from zadarapy.validators import verify_id


def get_available_providers(session, return_type=None, **kwargs):
    """
    Retrieves details for all available providers.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
    will return a JSON string.  Otherwise, it will return a Python
    dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    path = '/api/v2/providers.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_provider(session, provider_id, return_type=None, **kwargs):
    """
    Retrieves details for a single provider.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.

    :type provider_id: str|int
    :param provider_id: The provider 'key' value as returned by get_available_providers.  For
        example: 'aws' or 'aws-jp1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
    will return a JSON string.  Otherwise, it will return a Python
    dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    provider_id = verify_id(provider_id)
    path = f'/api/v2/providers/{provider_id}.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_provider_groups(session, return_type=None, **kwargs):
    """
    Retrieves details for all available provider groups.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
    will return a JSON string.  Otherwise, it will return a Python
    dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    path = '/api/v2/provider_groups.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_provider_group(session, provider_group_id, return_type=None, **kwargs):
    """
    Retrieves details for a single provider group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.

    :type provider_group_id: str|int
    :param provider_group_id: The provider 'key' value as returned by get_available_providers.  For
        example: 'aws' or 'aws-jp1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
    will return a JSON string.  Otherwise, it will return a Python
    dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    provider_group_id = verify_id(provider_group_id)
    path = f'/api/v2/provider_groups/{provider_group_id}.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)
