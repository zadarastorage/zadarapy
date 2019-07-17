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

from zadarapy.validators import verify_vpsa_id, verify_boolean


def get_cloud(session, cloud_name, return_type=None):
    """
    Retrieves details for current cloud

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9


    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/clouds/{0}.json'.format(cloud_name)
    return session.get_api(path=path, return_type=return_type)


def get_all_clouds(session, return_type=None):
    """
    Retrieves details for all clouds on the Command Center.

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
    path = '/api/clouds.json'
    return session.get_api(path=path, return_type=return_type)


def get_user_token(session, email, password, return_type=None):
    """
    Retrieves API token for the Command Center.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type email: str
    :param email: The email of the user used for login
        example: 'qa@zadarastorage.com'.  Required.

    :type password: str
    :param password: The password of the user.  Required

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/users/token.json'
    body_values = {'email': email, 'password': password}

    return session.post_api(path=path, body=json.dumps(body_values),
                            secure=False,
                            return_type=return_type)


def get_vpsa_from_cloud(session, cloud_name, vpsa_id, return_type=None):
    """
    Returns VPSA info from Command Center

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type vpsa_id: str
    :param vpsa_id: VPSA ID. i.e: 126

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}.json".format(cloud_name, vpsa_id)
    return session.get_api(path=path, return_type=return_type)


def get_zios_from_cloud(session, cloud_name, zios_id, return_type=None):
    """
    Returns ZIOS info from Command Center

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type zios_id: str
    :param zios_id: ZIOS ID. i.e: 126

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/zioses/{1}.json".format(cloud_name, zios_id)
    return session.get_api(path=path, return_type=return_type)


def get_all_drives(session, cloud_name, return_type=None):
    """
    Get all command Center Drives

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/drives.json".format(cloud_name)
    return session.get_api(path=path, return_type=return_type)


def get_vlans(session, cloud_name, return_type=None):
    """
    Get all command Center VLANs

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/vlans.json".format(cloud_name)

    return session.get_api(path=path, return_type=return_type)


def delete_vlans(session, cloud_name, vlan_id, return_type=None):
    """
    Delete VLan

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type vlan_id: str
    :param vlan_id: VLAN ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/vlans/{1}.json".format(cloud_name, vlan_id)
    return session.delete_api(path=path, return_type=return_type)


def get_tenants(session, cloud_name, return_type=None):
    """
    Get all command Center Tennants

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/cloud_users.json".format(cloud_name)
    return session.get_api(path=path, return_type=return_type)


def get_tenant(session, cloud_name, cloud_user, return_type=None):
    """
    Get all command Center Tennants

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type cloud_user: str
    :param cloud_user: Cloud User

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/cloud_users/{1}.json" \
        .format(cloud_name, cloud_user)
    return session.get_api(path=path, return_type=return_type)


def get_storage_node(session, cloud_name, sn_id, return_type=None):
    """
    Get all command Center Tennants

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type sn_id: str
    :param sn_id: Storage Node ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/nodes/{1}.json".format(cloud_name, sn_id)
    return session.get_api(path=path, return_type=return_type)


def get_storage_node_drives(session, cloud_name, sn_id, return_type=None):
    """
    Get all Storage Node drives

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type sn_id: str
    :param sn_id: Storage Node ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/nodes/{1}/drives.json".format(cloud_name, sn_id)
    return session.get_api(path=path, return_type=return_type)


def reboot_storage_node(session, cloud_name, sn_id, return_type=None):
    """
    Reboot Storage Node

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type sn_id: str
    :param sn_id: Storage Node ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/nodes/{1}/reboot.json".format(cloud_name, sn_id)
    return session.post_api(path=path, return_type=return_type)


def shutdown_storage_node(session, cloud_name, sn_id, return_type=None):
    """
    Shutdown Storage Node

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type sn_id: str
    :param sn_id: Storage Node ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/nodes/{1}/shutdown.json".format(cloud_name, sn_id)
    return session.post_api(path=path, return_type=return_type)


def zsnap_storage_node(session, cloud_name, sn_id, return_type=None):
    """
    Create Storage Node ZSnap

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type sn_id: str
    :param sn_id: Storage Node ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/nodes/{1}/zsnap.json".format(cloud_name, sn_id)
    return session.post_api(path=path, return_type=return_type)


def license_storage_node(session, cloud_name, sn_id, return_type=None):
    """
    Storage Node license

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type sn_id: str
    :param sn_id: Storage Node ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/nodes/{1}/license.json".format(cloud_name, sn_id)
    return session.post_api(path=path, return_type=return_type)


def set_default_image(session, cloud_name, image_id, return_type=None):
    """
    Set default Image

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type image_id: str
    :param image_id: Image ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/images/{1}/set_default.json" \
        .format(cloud_name, image_id)
    return session.post_api(path=path, return_type=return_type)


def delete_tenant(session, cloud_name, cloud_user, return_type=None):
    """
    Delete tenant

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type cloud_user: str
    :param cloud_user: Cloud User ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/cloud_users/{1}/deallocate_vlan_id.json" \
        .format(cloud_name, cloud_user)
    return session.delete_api(path=path, return_type=return_type)


def allocate_vlan(session, cloud_name, cloud_user, vlan_id, force="NO",
                  return_type=None):
    """
    Allocate VLAN from cloud user

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type cloud_user: str
    :param cloud_user: Cloud User ID

    :type vlan_id: str
    :param vlan_id: VLAN ID

    :type force: str
    :param force: "YES", "NO"

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    force = verify_boolean(force, "force")

    path = "/api/clouds/{0}/cloud_users/{1}/allocate_vlan_id.json" \
        .format(cloud_name, cloud_user)

    body_values = {"vlan_id": vlan_id, "force": force}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def deallocate_vlan(session, cloud_name, cloud_user, vlan_id, force="NO",
                    return_type=None):
    """
    Allocate VLAN from cloud user

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type cloud_user: str
    :param cloud_user: Cloud User ID

    :type vlan_id: str
    :param vlan_id: VLAN ID

    :type force: str
    :param force: "YES", "NO"

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    force = verify_boolean(force, "force")

    path = "/api/clouds/{0}/cloud_users/{1}/deallocate_vlan_id.json" \
        .format(cloud_name, cloud_user)

    body_values = {"vlan_id": vlan_id, "force": force}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def get_vpsa_settings(session, cloud_name, vpsa_id, section=None,
                      return_type=None):
    """
    Returns VPSA info from Command Center

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type vpsa_id: str
    :param vpsa_id: VPSA ID. i.e: 126

    :type section: str
    :param section: VPSA Settings section.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/settings".format(cloud_name, vpsa_id)
    parameters = {}
    if section is not None:
        parameters = {"section": section}

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type)


def get_all_images(session, cloud_name, page, per_page, return_type=None):
    """
    Returns all build images found in cloud

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type page: int
    :param page: The page number to start from.

    :type per_page: int
    :param per_page: The total number of records to return.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    path = "/api/clouds/{cloud_name}/images".format(cloud_name=cloud_name)
    parameters = {'page': page, 'per_page': per_page}
    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type)


def get_image(session, cloud_name, image_id, return_type=None):
    """
    Set default Image

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type image_id: str
    :param image_id: Image ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{cloud_name}/images/{id}" \
        .format(cloud_name=cloud_name, id=image_id)
    return session.get_api(path=path, return_type=return_type)
