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


import json
from zadarapy.validators import *


def add_proxy_vcs(session, cloud_name, vsa_id, return_type=None):
    """
    Add proxy virtual controller to VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsas.  For
        example: 'vsa-000007de'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_name = cloud_name.strip()

    if not is_valid_field(cloud_name):
        raise ValueError('{0} is not a valid cloud name.'.format(cloud_name))

    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/proxy_vcs.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def add_drives(session, cloud_name, vsa_id, image, when=None,
                         return_type=None):
    """
    Upgrade a VPSA to a new version.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsas.  For
        example: 'vsa-000007de'.  Required.

    :type drive_type: str
    :param drive_type: Drive type internal name.  Required

    :type quantity: int
    :param quantity: Number of drives to add.  Required.

    :type policy_id: str
    :param policy_id: Storage policy id or internal name.  Required

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_name = cloud_name.strip()

    if not is_valid_field(cloud_name):
        raise ValueError('{0} is not a valid cloud name.'.format(cloud_name))

    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    body_values = {}

    drive_type = drive_type.strip()

    if not is_valid_field(drive_type):
        raise ValueError('{0} is not a valid drive type.'.format(drive_type))

    body_values['drive_type'] = drive_type

    if quantity is not None:
        qty = int(quantity)
        if qty < 1:
            raise ValueError('Quantity {0} cannot be less than 1.'.format(qty))

        body_values['quantity'] = qty

    policy_id = policy_id.strip()

    if not is_valid_field(policy_id):
        raise ValueError('{0} is not a valid policy id.'.format(policy_id))

    body_values['policy_id'] = policy_id


    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/drives.json'.format(cloud_name, vsa_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)

