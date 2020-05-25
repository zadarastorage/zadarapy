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


from zadarapy.validators import verify_start_limit, verify_vc_index, \
    verify_capacity, get_parameters_options


def get_all_controllers(session, start=None, limit=None, return_type=None,
                        **kwargs):
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
    parameters = verify_start_limit(start, limit)
    path = '/api/zios/virtual_controllers.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_virtual_controller(session, vc_index, return_type=None, **kwargs):
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
    verify_vc_index(vc_index)

    path = '/api/zios/virtual_controllers/{0}.json'.format(vc_index)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_virtual_controller_drives(session, vc_index, return_type=None,
                                  **kwargs):
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
    verify_vc_index(vc_index)

    path = '/api/zios/virtual_controllers/{0}/drives.json'.format(vc_index)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def remove_proxy_vcs(session, quantity, return_type=None, **kwargs):
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
    verify_capacity(quantity, "quantity")
    path = '/api/zios/virtual_controllers/remove_proxy_vcs.json'
    parameters = get_parameters_options([('quantity', quantity)])

    # should filter out the bad statuses
    return session.delete_api(path=path, parameters=parameters,
                              return_type=return_type, skip_status_check_range=False, **kwargs)
