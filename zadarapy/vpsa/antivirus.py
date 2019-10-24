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

from zadarapy.validators import verify_boolean, \
    verify_start_limit, verify_interval, verify_controller_id


def get_antivirus_status(session, return_type=None, **kwargs):
    """
    Enables the antivirus engine.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """

    path = '/api/antivirus/engine.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def enable_antivirus(session, pool_id, return_type=None, **kwargs):
    """
    Enables the antivirus engine.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: Pool to create quarantine volume.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """
    body_values = {'pool': pool_id}

    path = '/api/antivirus/engine.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def disable_antivirus(session, return_type=None, **kwargs):
    """
    Disables the antivirus engine.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """

    path = '/api/antivirus/engine.json'

    return session.delete_api(path=path, return_type=return_type, **kwargs)
