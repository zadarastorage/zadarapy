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
# License for the specific language governing permissions and per_pageations
# under the License.


from zadarapy.validators import verify_vpsa_id, \
    verify_cloud_name, verify_field, verify_capacity, verify_positive_argument, is_valid_volume_id


def add_drives(session, cloud_name, vsa_id, drive_type, drive_quantity,
               policy_id, return_type=None, **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)
    policy_id = verify_field(policy_id, 'policy_id')
    drive_type = verify_field(drive_type, 'drive_type')

    body_values = {'drive_type': drive_type, 'policy_id': policy_id}

    if drive_quantity is not None:
        drive_quantity = verify_capacity(drive_quantity, 'drive_quantity')
        body_values['quantity'] = drive_quantity

    path = '/api/clouds/{0}/zioses/{1}/drives.json'.format(cloud_name, vsa_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def add_proxy_vcs(session, cloud_name, vsa_id, return_type=None, **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}/proxy_vcs.json' \
        .format(cloud_name, vsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def add_storage_policy(session, cloud_name, vsa_id, policy_name, policy_desc,
                       drive_type, drive_quantity, policy_type_id,
                       return_type=None, **kwargs):
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
    :param policy_type_id: Policy type id as returned by
     vpsa_zone_group_storage_policy_type.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)
    policy_name = verify_field(policy_name, 'policy_name')
    drive_type = verify_field(drive_type, 'drive_type')

    body_values = {'name': policy_name, 'drive_type': drive_type}

    if policy_desc is not None:
        policy_desc = verify_field(policy_desc, 'policy_desc')
        body_values['policy_desc'] = policy_desc

    if drive_quantity is not None:
        drive_quantity = verify_capacity(drive_quantity, 'drive_quantity')
        body_values['drive_quantity'] = drive_quantity

    if policy_type_id is not None:
        policy_type_id = int(policy_type_id)
        if policy_type_id < 0:
            raise ValueError('policy_type_id {0} cannot be negative.'.format(
                policy_type_id))

        body_values['policy_type_id'] = policy_type_id

    path = '/api/clouds/{0}/zioses/{1}/policy.json'.format(cloud_name, vsa_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def assign_publicip(session, cloud_name, vsa_id, return_type=None, **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}/public_ip/assign.json' \
        .format(cloud_name, vsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def create_zsnap(session, cloud_name, vsa_id, prefix, return_type=None,
                 **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)
    prefix = verify_field(prefix, 'prefix')

    body_values = {'prefix': prefix}

    path = '/api/clouds/{0}/zioses/{1}/zsnap.json'.format(cloud_name, vsa_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_all_vpsaoss(session, cloud_name, page=None, per_page=None,
                    return_type=None, **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)

    page = verify_positive_argument(page, 'page')
    per_page = verify_positive_argument(per_page, 'per_page')
    parameters = {'page': page, 'per_page': per_page}

    path = '/api/clouds/{0}/zioses.json'.format(cloud_name)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_one_vpsaos(session, cloud_name, vsa_id, return_type=None, **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}.json'.format(cloud_name, vsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsaos_accounts(session, cloud_name, vsa_id, return_type=None,
                        **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}/accounts.json' \
        .format(cloud_name, vsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsaos_comments(session, cloud_name, vsa_id, return_type=None,
                        **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)
    path = '/api/clouds/{0}/zioses/{1}/comments.json' \
        .format(cloud_name, vsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsaos_drives(session, return_type=None, **kwargs):
    """
    Retrieves the list of a VPSAOS drives.

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

    path = '/api/zios/drives.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsaos_drive(session, drive_id, return_type=None, **kwargs):
    """
    Retrieves the list of a VPSAOS drives.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: ZIOS drive ID.  e.g.: 'volume-00000ca8'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    is_valid_volume_id(drive_id)

    path = '/api/zios/drives/{0}.json'.format(drive_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsaos_sps(session, cloud_name, vsa_id, return_type=None, **kwargs):
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
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}/storage_policies.json' \
        .format(cloud_name, vsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsaos_vcs(session, cloud_name, vsa_id, return_type=None, **kwargs):
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
    verify_cloud_name(cloud_name)
    verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}/virtual_controllers.json'.format(
        cloud_name, vsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def unassign_publicip(session, cloud_name, vsa_id, return_type=None, **kwargs):
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
    verify_cloud_name(cloud_name)
    verify_vpsa_id(vsa_id)

    path = '/api/clouds/{0}/zioses/{1}/public_ip/unassign.json' \
        .format(cloud_name, vsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def upgrade_vpsaos_image(session, cloud_name, vsa_id, image, return_type=None,
                         **kwargs):
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
    verify_cloud_name(cloud_name)
    verify_vpsa_id(vsa_id)
    verify_field(image, "image")

    body_values = {'image': image}

    path = '/api/clouds/{0}/zioses/{1}/upgrade.json'.format(cloud_name, vsa_id)
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
