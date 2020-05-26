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
from zadarapy.validators import verify_start_limit, verify_vc_index


def get_all_virtual_controllers(session, start=None, limit=None, return_type=None, **kwargs):
    """
    Get details on all VPSAOS virtual controllers.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying accounts from.  Optional.

    :type: limit: int
    :param limit: The maximum number of accounts to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start=start, limit=limit)

    path = "/api/zios/virtual_controllers.json"

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_virtual_controller(session, vc_index, return_type=None, **kwargs):
    """
    Get details on one VPSAOS virtual controller.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vc_index: str
    :param vc_index: Index of the VC. e.g. for VC with ID vc-3, it's index will be 3.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_vc_index(vc_index)

    path = "/api/zios/virtual_controllers/{0}.json".format(vc_index)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_virtual_controller_drives(session, vc_index, return_type=None, **kwargs):
    """
    Get all VPSAOS virtual controller drives.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vc_index: str
    :param vc_index: Index of the VC. e.g. for VC with ID vc-3, it's index will be 3.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_vc_index(vc_index)

    path = "/api/zios/virtual_controllers/{0}/drives.json".format(vc_index)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def delete_proxy_virtual_controller(session, quantity, region_id=None, return_type=None, **kwargs):
    """
    Remove proxy VCs

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type quantity: int
    :param quantity: Number of VCs to remove.  Required.

    :type region_id: int
    :param region_id: Region ID (For Multi Region VPSA object storage)

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """


    path = "/api/zios/virtual_controllers/remove_proxy_vcs.json"

    body_values = {'quantity': quantity}
    if region_id is not None:
        body_values["region_id"] = region_id

    return session.delete_api(path=path, body=body_values, return_type=return_type, **kwargs)
