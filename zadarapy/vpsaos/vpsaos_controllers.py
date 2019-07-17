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


from zadarapy.validators import is_valid_vc_index


def get_all_controllers(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all virtual controllers for the VPSAOS.

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
    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/zios/virtual_controllers.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_virtual_controller(session, vc_index, return_type=None):
    """
    Retrieves details for a single virtual controller for the VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vc_index: str
    :param vc_index: The virtual controller 'index' value as returned by
        get_all_controllers.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vc_index(vc_index):
        raise ValueError('{0} is not a valid vc index.'
                         .format(vc_index))
    method = 'GET'
    path = '/api/zios/virtual_controllers/{0}.json'.format(vc_index)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_virtual_controller_drives(session, vc_index, return_type=None):
    """
    Retrieves drives for a virtual controller.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vc_index: str
    :param vc_index: The virtual controller 'index' value as returned by
        get_all_controllers.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_vc_index(vc_index):
        raise ValueError('{0} is not a valid vc index.'
                         .format(vc_index))
    method = 'GET'
    path = '/api/zios/virtual_controllers/{0}/drives.json'.format(vc_index)

    return session.call_api(method=method, path=path, return_type=return_type)


def remove_proxy_vcs(session, quantity, return_type=None):
    """
    Removes proxy vcs.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type quantity: int
    :param quantity: The number of vcs to be removed.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if quantity is None:
        raise ValueError('quantity param is missing.')

    qty = int(quantity)
    if qty < 1:
        raise ValueError('Supplied quantity ("{0}") cannot be less than 1.'
                         .format(quantity))

    method = 'DELETE'
    path = '/api/zios/virtual_controllers/remove_proxy_vcs.json'

    parameters = {k: v for k, v in (('quantity', qty),)
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
