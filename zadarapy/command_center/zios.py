# Copyright 2019 Zadara Storage, Inc.
# Originally authored by Nir Hayun
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

from zadarapy.validators import verify_cloud_name, verify_positive_argument, verify_zios_id, \
    verify_field, verify_capacity


def get_all_zios_objects(session, cloud_name, per_page=30, page=1, return_type=None, **kwargs):
    """
    Retrieves details for all ZIOSs in the cloud.

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

    path = "/api/clouds/{0}/zioses.json?per_page={1}&page={2}".format(cloud_name, per_page, page)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def hibernate_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Hibernate ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/hibernate.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def restore_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Restore ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/restore.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def enable_elastic_load_balancer_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Enable Elastic Load Balancer in ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/enable_external_load_balancer.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def disable_elastic_load_balancer_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Disable Elastic Load Balancer in ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/disable_external_load_balancer.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def get_load_balancer(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Get a list of Load Balancers.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/load_balancer.json".format(cloud_name, zios_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def add_drives_to_zios(session, cloud_name, zios_id, drive_type, drive_quantity, policy_id, return_type=None, **kwargs):
    """
    Add drives to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type drive_type: str
    :param drive_type: Drive type internal name.  Required

    :type drive_quantity: int
    :param drive_quantity: Number of drives to add.  Required.

    :type policy_id: int
    :param policy_id: Storage policy id or internal name.  Required

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)
    policy_id = verify_field(policy_id, 'policy_id')
    drive_type = verify_field(drive_type, 'drive_type')
    drive_quantity = verify_capacity(drive_quantity, 'drive_quantity')

    body_values = {'drive_type': drive_type, 'quantity': drive_quantity, 'policy_id': policy_id}

    path = "/api/clouds/{0}/zioses/{1}/drives.json".format(cloud_name, zios_id)

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def create_storage_policy_zios(session, cloud_name, zios_id, policy_name, drive_type, drive_quantity,
                               policy_type_id, description=None, return_type=None, **kwargs):
    """
    Creates a new policy to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type policy_name: str
    :param policy_name: Policy name.  Required

    :type drive_type: str
    :param drive_type: Drive type internal name.  Required

    :type drive_quantity: int
    :param drive_quantity: Number of drives to add.  Required.

    :type policy_type_id: int
    :param policy_type_id: Storage policy type id.  Required.

    :type description: str
    :param description: Policy description

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)
    drive_type = verify_field(drive_type, 'drive_type')
    drive_quantity = verify_capacity(drive_quantity, 'drive_quantity')
    policy_type_id = verify_capacity(policy_type_id, 'policy_type_id')

    body_values = {"name":policy_name, "drive_type":drive_type,
                   "drive_quantity":drive_quantity, "policy_type_id":policy_type_id}

    if description is not None:
        body_values["description"] = description

    path = "/api/clouds/{0}/zioses/{1}/policy.json".format(cloud_name, zios_id)

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def pause_policy_rebalance_zios(session, cloud_name, zios_id, policy_name, return_type=None, **kwargs):
    """
    Pause policy rebalance in ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type policy_name: str
    :param policy_name: Policy name.  Required

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    body_values = {"policy_name":policy_name}

    path = "/api/clouds/{0}/zioses/{1}/policy_pause_rebalance.json".format(cloud_name, zios_id)

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def continue_policy_rebalance_zios(session, cloud_name, zios_id, policy_name, return_type=None, **kwargs):
    """
    Continue policy rebalance in ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type policy_name: str
    :param policy_name: Policy name.  Required

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    body_values = {"policy_name":policy_name}

    path = "/api/clouds/{0}/zioses/{1}/policy_continue_rebalance.json".format(cloud_name, zios_id)

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def add_proxy_virtual_controller_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Add proxy virtual controller to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/proxy_vcs.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def change_engine_type_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Changes ZIOS engine from ZIOS_MINI to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/change_engine_type.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def upgrade_zios(session, cloud_name, zios_id, image, return_type=None, **kwargs):
    """
    Upgrade a ZIOS software to a specified image.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

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
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)
    image = verify_field(image, "image")

    body_values = {'image': image}

    path = "/api/clouds/{0}/zioses/{1}/upgrade.json".format(cloud_name, zios_id)
    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def assign_public_ip_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Assign public ip to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/public_ip/assign.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def unassign_public_ip_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Unassign public ip to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/public_ip/unassign.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def create_zsnap_zios(session, cloud_name, zios_id, prefix, return_type=None, **kwargs):
    """
    Create a ZIOS Zsnap.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

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
    zios_id = verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)
    prefix = verify_field(prefix, 'prefix')

    body_values = {'prefix': prefix}

    path = "/api/clouds/{0}/zioses/{1}/zsnap.json".format(cloud_name, zios_id)
    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)
