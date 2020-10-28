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


from zadarapy.validators import verify_vpsa_id, verify_boolean


def get_cloud(session, cloud_name, return_type=None, **kwargs):
    """
    Retrieves details for a given cloud name

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_all_clouds(session, return_type=None, **kwargs):
    """
    Retrieves details for all clouds on the Cloud.

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_user(session, email, first_name, last_name, admin, role_ids, return_type=None, **kwargs):
    """
    Creates a user of CC.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type email: str
    :param email: The email of the user used for login
        example: 'qa@zadarastorage.com'.  Required.

    :type first_name: str
    :param first_name: The first name of the user

    :type last_name: str
    :param last_name: The first name of the user

    :type admin: bool
    :param admin: True if the user should be admin

    :type role_ids: array
    :param role_ids: Array of roles, i.e. ["1","3"]

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/users.json'
    body_values = {"user":{'email': email, 'firstname': first_name, 'lastname': last_name, 'admin':admin, 'role_ids': role_ids}}
    return session.post_api(path=path, body=body_values, secure=False,
                            return_type=return_type, **kwargs)


def update_user(session, email, first_name, last_name, admin, role_ids,
                password, new_password, id, return_type=None, **kwargs):
    """
    Updates a user of CC.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type email: str
    :param email: The email of the user used for login
        example: 'qa@zadarastorage.com'.  Required.

    :type first_name: str
    :param first_name: The first name of the user

    :type last_name: str
    :param last_name: The first name of the user

    :type admin: bool
    :param admin: True if the user should be admin

    :type role_ids: array
    :param role_ids: Array of roles, i.e. ["1","3"]

    :type password: str
    :param password: the current password.   Required.

    :type new_password: str
    :param new_password: a new password for the user.   Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/users/{0}.json'.format(id)
    body_values = {"user":{'email': email, 'firstname': first_name, 'lastname': last_name, 'admin':admin,
                           'role_ids': role_ids, 'current_password': password, 'password': new_password}}
    return session.put_api(path=path, body=body_values, secure=False,
                            return_type=return_type, **kwargs)


def regenerate_user_api_token(session, email, password, return_type=None, **kwargs):
    """
    Regenerates the user's API token.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type email: str
    :param email: The email of the user used for login
        example: 'qa@zadarastorage.com'.  Required.

    :type password: str
    :param password: the current password.   Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/users/regenerate_token.json'
    body_values = {'email': email, 'password': password}
    return session.post_api(path=path, body=body_values, secure=False, return_type=return_type, **kwargs)


def delete_user(session, id, return_type=None, **kwargs):
    """
    Deletes a user of CC.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type id: int

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/users/{0}.json'.format(id)
    return session.delete_api(path=path, secure=False, return_type=return_type, **kwargs)


def get_all_users(session, return_type, **kwargs):
    """
    Deletes a user of CC.

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
    path = '/api/users.json'
    return session.get_api(path=path, secure=False, return_type=return_type, **kwargs)


def get_user_token(session, email, password, return_type=None, **kwargs):
    """
    Retrieves API token for the Cloud.

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
    return session.post_api(path=path, body=body_values, secure=False,
                            return_type=return_type, **kwargs)


def get_vpsa_from_cloud(session, cloud_name, vpsa_id, return_type=None,
                        **kwargs):
    """
    Returns VPSA info from Cloud

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_zios_from_cloud(session, cloud_name, zios_id, return_type=None,
                        **kwargs):
    """
    Returns ZIOS info from Cloud

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_all_drives(session, cloud_name, per_page=30, page=1,  return_type=None, **kwargs):
    """
    Get all Cloud Drives

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type per_page: int
    :param per_page: The number of drives to be returned in one page: 30

    :type page: int
    :param page: Page number to be queried: i.e: 2

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/drives.json?per_page={1}&page={2}".format(cloud_name, per_page, page)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_drive(session, cloud_name, drive_id, return_type=None, **kwargs):
    """
    Get all Cloud Drives

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type drive_id: str
    :param drive_id: The id of drive to be returned e.g. 113

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/drives/{1}.json".format(cloud_name, drive_id)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vlans(session, cloud_name, return_type=None, **kwargs):
    """
    Get all Cloud VLANs

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

    return session.get_api(path=path, return_type=return_type, **kwargs)


def delete_vlans(session, cloud_name, vlan_id, return_type=None, **kwargs):
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
    return session.delete_api(path=path, return_type=return_type, **kwargs)


def populate_vrid_in_vlan(session, cloud_name, vlan_id, range_start, range_end, return_type=None, **kwargs):
    """
    Populate vrid in a Vlan

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type vlan_id: str
    :param vlan_id: VLAN ID

    :type range_start: int
    :param range_start: VRID start range

    :type range_end: int
    :param range_end: VRID end range

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    path = "/api/clouds/{0}/vlans/{1}/add_vrids.json".format(cloud_name, vlan_id)

    body = {"range_start": range_start, "range_end": range_end, "vlan": vlan_id}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def get_tenants(session, cloud_name, return_type=None, **kwargs):
    """
    Get all Cloud Tennants

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_tenant(session, cloud_name, cloud_user, return_type=None, **kwargs):
    """
    Get all Cloud Tennants

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_all_storage_nodes(session, cloud_name, return_type=None, **kwargs):
    """
    Get all Storage Nodes

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
    path = "/api/clouds/{0}/nodes.json".format(cloud_name)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_storage_node(session, cloud_name, sn_id, return_type=None, **kwargs):
    """
    Get Storage Nodes found in Cloud

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_fault_domains(session, cloud_name, return_type=None, **kwargs):
    """
    Get all fault domains

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
    path = "/api/clouds/{0}/fault_domains.json".format(cloud_name)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_storage_node_drives(session, cloud_name, sn_id, return_type=None,
                            **kwargs):
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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def reboot_storage_node(session, cloud_name, sn_id, return_type=None,
                        **kwargs):
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
    return session.post_api(path=path, return_type=return_type, **kwargs)


def shutdown_storage_node(session, cloud_name, sn_id, return_type=None,
                          **kwargs):
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
    return session.post_api(path=path, return_type=return_type, **kwargs)


def zsnap_storage_node(session, cloud_name, sn_id, return_type=None, **kwargs):
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
    return session.post_api(path=path, return_type=return_type, **kwargs)


def license_storage_node(session, cloud_name, sn_id, return_type=None,
                         **kwargs):
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
    return session.post_api(path=path, return_type=return_type, **kwargs)


def set_default_image(session, cloud_name, image_id, return_type=None,
                      **kwargs):
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
    return session.post_api(path=path, return_type=return_type, **kwargs)


def delete_tenant(session, cloud_name, cloud_user, return_type=None, **kwargs):
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
    return session.delete_api(path=path, return_type=return_type, **kwargs)


def allocate_vlan(session, cloud_name, cloud_user, vlan_id, force="NO",
                  return_type=None, **kwargs):
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
                            return_type=return_type, **kwargs)


def deallocate_vlan(session, cloud_name, cloud_user, vlan_id, force="NO",
                    return_type=None, **kwargs):
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
                            return_type=return_type, **kwargs)


def get_vpsa_settings(session, cloud_name, vpsa_id, section=None,
                      return_type=None, **kwargs):
    """
    Returns VPSA info from Cloud

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
                           return_type=return_type, **kwargs)


def get_all_images(session, cloud_name, page, per_page, return_type=None,
                   **kwargs):
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
                           return_type=return_type, **kwargs)


def get_image(session, cloud_name, image_id, return_type=None, **kwargs):
    """
    Get Image

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
    return session.get_api(path=path, return_type=return_type, **kwargs)


def set_automatic_drive_replacement(session, cloud_name, time, return_type=None, **kwargs):
    """
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type time: int
    :param time: Time in minutes from drive failed state detection. (0 - disable automatic drive replacement)

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/settings/automatic_drive_replacement.json" \
        .format(cloud_name)

    body_values = {"time": time}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_redundancy_level_policies(session, cloud_name, return_type=None, **kwargs):
    """
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
    path = "/api/clouds/{0}/vpsa_zone_group_storage_policy_types.json".format(cloud_name)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_inventory(session, cloud_name, id="1", return_type=None, **kwargs):
    """
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: Cloud Name: i.e: zadaraqa9

    :type id: str
    :param id: VPSA ID. i.e: 126

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/vpsa_zone_groups/{1}/inventory.json".format(cloud_name, id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def enable_pool_migration(session, cloud_name, vpsa_id, return_type=None, **kwargs):
    path = "/api/clouds/{0}/vpsas/{1}/enable_pool_migration".format(cloud_name, vpsa_id)
    return session.post_api(path=path, return_type=return_type, **kwargs)
