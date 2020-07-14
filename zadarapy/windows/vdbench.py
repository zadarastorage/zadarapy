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


def vdbench(session, cmd, cmd_parameters, return_type=None, **kwargs):
    """
    Run vdbench on remote windows server

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cmd: str
    :param cmd: vdbench command.  Required.

    :type cmd_parameters: str
    :param cmd_parameters: vdbench command parameters.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/vdbench'

    body = {"cmd": cmd, "cmd_parameters": cmd_parameters}

    return session.post_api(path=path, body=body, secure=False, return_type=return_type, **kwargs)


def get_vdbench_process_list(session, return_type=None, **kwargs):
    """
    Get all vdbench process on remote windows server

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
    path = '/api/vdbench_process_list'

    return session.get_api(path=path, secure=False, return_type=return_type, **kwargs)
