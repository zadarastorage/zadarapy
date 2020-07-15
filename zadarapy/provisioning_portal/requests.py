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

from future.standard_library import install_aliases
install_aliases()


def requests(session, return_type=None, **kwargs):
    """
    Return all the requests in Provisioning Portal

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
    path = '/api/v2/vpsa_requests.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def request(session, request_id, return_type=None, **kwargs):
    """
    Return all the requests in Provisioning Portal

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type request_id: int
    :param request_id: Request ID.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/v2/vpsa_requests/{0}.json'.format(request_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def approve(session, request_id, request_name="pg2", return_type=None, **kwargs):
    """
    Approve a Provisioning portal request

    :type request_id: int
    :param request_id: Request ID.  Required.
    
    :type request_name: str
    :param request_name: Request name.  Optional.

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
    path = '/api/v2/vpsa_requests/{0}/approve.json'.format(request_id)

    body = {"name": request_name}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def deny(session, request_id, reason, return_type=None, **kwargs):
    """
    Deny a Provisioning portal request

    :type reason: str
    :param reason: Reason for request deny.  Required.

    :type request_id: int
    :param request_id: Request ID.  Required.

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
    path = '/api/v2/vpsa_requests/{0}/deny.json'.format(request_id)

    body = {"reason": reason}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)
