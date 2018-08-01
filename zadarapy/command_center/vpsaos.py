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
# License for the specific language governing permissions and per_pageations
# under the License.


import json
from zadarapy.validators import *


def add_drives(session, cloud_name, vsa_id, drive_type, drive_quantity, policy_id,
                         return_type=None):
    """
    Add drives to a VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
        example: 'vsa-000007de'.  Required.

    :type drive_type: str
    :param drive_type: Drive type internal name.  Required

    :type drive_quantity: int
    :param drive_quantity: Number of drives to add.  Required.

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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    body_values = {}

    drive_type = drive_type.strip()

    if not is_valid_field(drive_type):
        raise ValueError('{0} is not a valid drive type.'.format(drive_type))

    body_values['drive_type'] = drive_type

    if drive_quantity is not None:
        qty = int(drive_quantity)
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

def add_proxy_vcs(session, cloud_name, vsa_id, return_type=None):
    """
    Add proxy virtual controller to VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/proxy_vcs.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def add_storage_policy(session, cloud_name, vsa_id, policy_name, policy_desc,
                                drive_type, drive_quantity, policy_type_id,
                                return_type=None):
    """
    Create a new storage policy in VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
        example: 'vsa-000007de'.  Required.

    :type policy_name: str
    :param policy_name: Storage policy name.  Required

    :type policy_desc: str
    :param policy_desc: Storage policy description.  Optional

    :type drive_type: str
    :param drive_type: Drive type internal name.  Required

    :type drive_quantity: int
    :param drive_quantity: Number of drives to add.  Required.

    :type policy_type_id: int
    :param policy_type_id: Policy type id as returned by vpsa_zone_group_storage_policy_type.  Required.

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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    body_values = {}

    policy_name = policy_name.strip()

    if not is_valid_field(policy_name):
        raise ValueError('{0} is not a valid storage policy name.'.format(policy_name))

    body_values['policy_name'] = policy_name

    if policy_desc is not None:
        policy_desc = policy_desc.strip()

    if not is_valid_field(policy_desc):
        raise ValueError('{0} is not a valid storage policy description.'.format(policy_desc))

    body_values['policy_desc'] = policy_desc

    drive_type = drive_type.strip()

    if not is_valid_field(drive_type):
        raise ValueError('{0} is not a valid drive type.'.format(drive_type))

    body_values['drive_type'] = drive_type

    if drive_quantity is not None:
        qty = int(drive_quantity)
        if qty < 1:
            raise ValueError('Quantity {0} cannot be less than 1.'.format(qty))

        body_values['drive_quantity'] = qty

    if policy_type_id is not None:
        policy_type_id = int(policy_type_id)
        if policy_type_id < 0:
            raise ValueError('policy_type_id {0} cannot be negative.'.format(policy_type_id))

        body_values['policy_type_id'] = policy_type_id

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/policy.json'.format(cloud_name, vsa_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)

def assign_publicip(session, cloud_name, vsa_id, return_type=None):
    """
    Assign public IP to VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/public_ip/assign.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def create_zsnap(session, cloud_name, vsa_id, prefix, return_type=None):
    """
    Create a zsnap.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
        example: 'vsa-000007de'.  Required.

    :type prefix: str
    :param prefix: Required.

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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    prefix = prefix.strip()

    if not is_valid_field(prefix):
        raise ValueError('{0} is not a valid prefix.'.format(prefix))

    body_values = {}

    body_values['prefix'] = prefix

    body = json.dumps(body_values)

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/zsnap.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)

def get_all_vpsaoss(session, cloud_name, page=None, per_page=None, return_type=None):
    """
    Retrieves details for all VPSAOSs in the cloud.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type page: int
    :param page: The page number to page from.  Optional.

    :type: per_page: int
    :param per_page: The total number of records to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if page is not None:
        page = int(page)
        if page < 0:
            raise ValueError('Supplied page ("{0}") cannot be negative.'
                             .format(page))

    if per_page is not None:
        per_page = int(per_page)
        if per_page < 0:
            raise ValueError('Supplied per_page ("{0}") cannot be negative.'
                             .format(per_page))

    method = 'GET'
    path = '/api/clouds/{0}/zioses.json'.format(cloud_name)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_one_vpsaos(session, cloud_name, vsa_id, return_type=None):
    """
    Retrieves details for a single VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'GET'
    path = '/api/clouds/{0}/zioses/{1}.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def get_vpsaos_accounts(session, cloud_name, vsa_id, return_type=None):
    """
    Retrieves the list of a VPSAOS accounts.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'GET'
    path = '/api/clouds/{0}/zioses/{1}/accounts.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def get_vpsaos_comments(session, cloud_name, vsa_id, return_type=None):
    """
    Retrieves the list of a VPSAOS comments.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'GET'
    path = '/api/clouds/{0}/zioses/{1}/comments.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def get_vpsaos_drives(session, cloud_name, vsa_id, return_type=None):
    """
    Retrieves the list of a VPSAOS drives.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'GET'
    path = '/api/clouds/{0}/zioses/{1}/drives.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def get_vpsaos_sps(session, cloud_name, vsa_id, return_type=None):
    """
    Retrieves the list of a VPSAOS storage policies.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'GET'
    path = '/api/clouds/{0}/zioses/{1}/storage_policies.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def get_vpsaos_vcs(session, cloud_name, vsa_id, return_type=None):
    """
    Retrieves the list of a VPSAOS virtual controllers.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'GET'
    path = '/api/clouds/{0}/zioses/{1}/virtual_controllers.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def unassign_publicip(session, cloud_name, vsa_id, return_type=None):
    """
    Unassign public IP from VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/public_ip/unassign.json'.format(cloud_name, vsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)

def upgrade_vpsaos_image(session, cloud_name, vsa_id, image, return_type=None):
    """
    Upgrade a VPSAOS to a specified image.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
        example: 'vsa-000007de'.  Required.

    :type image: str
    :param image: The image 'name' value as returned by get_images.  For
        example: 'zios-00.00-1389.img'.  Required.

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

    vsa_id = vsa_id.strip()
    if not is_valid_field(vsa_id):
        raise ValueError('{0} is not a valid vsa_id.'.format(vsa_id))

    image = image.strip()

    if not is_valid_field(image):
        raise ValueError('{0} is not a valid image name.'.format(image))

    body_values = {}

    body_values['image'] = image

    body = json.dumps(body_values)

    method = 'POST'
    path = '/api/clouds/{0}/zioses/{1}/upgrade.json'.format(cloud_name, vsa_id)
    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)

