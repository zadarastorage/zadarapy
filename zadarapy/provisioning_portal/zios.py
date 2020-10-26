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

from zadarapy.validators import is_valid_field, verify_positive_argument


def create_zios(session, name, provider, drives, vpsa_zone_group_storage_policy_type_id, custom_network_id,
                description=None, allocation_zone=None, return_type=None, **kwargs):
    """
    Submits a request to create a new ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: A text label to assign to the ZIOS.  For example:
        'aws_east_master_zios'.  May only contain alphanumeric and underscore
        characters.  Required.

    :type provider: str
    :param provider: The storage cloud (provider) 'key' value as returned by
        get_all_clouds.  For example: 'zadaraqa10' or 'zadaraqa17'.  The ZIOS will be
        created on this storage cloud.  Required.

    :type drives: List[Dict]
    :param drives: A Python list of Python dictionaries that defines what type
        and how many of each type of drive to attach to the ZIOS.  Each list
        item should contain a dictionary that defines a 'drive_type' key and
        'quantity' key.  The 'drive_type' key is the 'key' value as returned
        by the 'drive_types' list for the cloud_id from get_cloud.  For
        example: 'SATA_2793GB_5940RPM'.  The 'quantity' key is the number of
        drives to add for this type.  Every ZIOS must have at least two drives.
        For example, to add two SATA 3TB drives and two 600GB SAS drives, use
        the following: [{'drive_type':'SATA_2793GB_5940RPM','quantity':2},
                        {'drive_type':'SAS_557GB_10500RPM','quantity':2}]
        Please note that the example is not a string, rather a representation
        of what the "pprint" function might return.  Required.

    :type vpsa_zone_group_storage_policy_type_id: int
    :param vpsa_zone_group_storage_policy_type_id: Storage policy id. See `get_clouds` and under 'clouds.py'
            and the corresponding cloud will have a 'vpsa_zone_group_storage_policy_types' property.
            For example: '1'.  Required.

    :type custom_network_id: int
    :param custom_network_id: Custom network id. For example: '1'.  Required.

    :type description: str
    :param description: A text description for the ZIOS.  For example:
        'Primary ZIOS for AWS East'.  May not contain a single quote
        (') character.  Optional.

    :type allocation_zone: str
    :param allocation_zone: For multi-zone environments, this parameter
        specifies that either the ZIOS should run in multi-zone mode, or in a
        specific zone.  If set to None, for multi-zone environments, multi-zone
        will be used; for single zone, the only available zone will be used.
        If set to a string, that zone will be used.  Zone names are listed in
        the 'allocation_zones' list as returned by get_cloud for cloud_id.
        For example: 'zone_0'.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body = {}

    name = name.strip()

    if not is_valid_field(name):
        raise ValueError('{0} is not a valid ZIOS name.'.format(name))

    body['name'] = name

    provider = provider.strip()

    if not is_valid_field(provider):
        raise ValueError('{0} is not a valid storage cloud key.'.format(provider))

    body['provider'] = provider

    if type(drives) is not list:
        raise ValueError('The passed "drives" parameter is not a Python list.')

    drives_to_add = {}
    for v in drives:
        if type(v) is not dict:
            raise ValueError('Each item in the "drives" list must be a Python dictionary.')

        if 'drive_type' not in v:
            raise ValueError('The required "drive_type" key was not found in '
                             'the drive dictionary.')

        if 'quantity' not in v:
            raise ValueError('The required "quantity" key was not found in '
                             'the drive dictionary.')
        drives_to_add[v["drive_type"]] = str(v["quantity"])

    body["drives"] = drives_to_add

    body['vpsa_zone_group_storage_policy_type_id'] = vpsa_zone_group_storage_policy_type_id

    body['custom_network_id'] = custom_network_id

    body['kind'] = "object_storage"

    if description is not None:
        description = description.strip()

        if not is_valid_field(description):
            raise ValueError('{0} is not a valid ZIOS description.'
                             .format(description))

        body['description'] = description

    if allocation_zone is not None:
        body['allocation_zone'] = allocation_zone

    path = '/api/v2/vpsas.json'

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def add_storage_policy(session, zios_id, name, storage_policy_type, drives, return_type=None, **kwargs):
    """
    Add a storage policy to a VPSA object storage.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_zioses.  For
        example: '2653'.  Required.

    :type name: str
    :param name: Storage Policy Name.  Required.

    :type storage_policy_type: int
    :param storage_policy_type: Storage Policy Type Id.  Example - 2-Way is '1'.  Required.

    :type drives: List[Dict]
    :param drives: A Python list of Python dictionaries that defines what type
        and how many of each type of drive to attach to the ZIOS.  Each list
        item should contain a dictionary that defines a 'drive_type' key and
        'quantity' key.  The 'drive_type' key is the 'key' value as returned
        by the 'drive_types' list for the cloud_id from get_cloud.  For
        example: 'SATA_2793GB_5940RPM'.  The 'quantity' key is the number of
        drives to add for this type.  Every ZIOS must have at least two drives.
        For example, to add two SATA 3TB drives and two 600GB SAS drives, use
        the following: [{'drive_type':'SATA_2793GB_5940RPM','quantity':2},
                        {'drive_type':'SAS_557GB_10500RPM','quantity':2}]
        Please note that the example is not a string, rather a representation
        of what the "pprint" function might return.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(zios_id, 'zios_id')
    body = {'name': name, 'storage_policy_type': storage_policy_type}

    drives_to_add = {}
    for v in drives:
        if type(v) is not dict:
            raise ValueError('Each item in the "drives" list must be a Python dictionary.')

        if 'drive_type' not in v:
            raise ValueError('The required "drive_type" key was not found in '
                             'the drive dictionary.')

        if 'quantity' not in v:
            raise ValueError('The required "quantity" key was not found in '
                             'the drive dictionary.')
        drives_to_add[v["drive_type"]] = int(v["quantity"])

    body["drives"] = drives_to_add

    path = '/api/v2/vpsas/{0}/storage_policy.json'.format(zios_id)

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def add_proxy_vc(session, zios_id, allocation_zone_id, return_type=None, **kwargs):
    """
    Submits a request to add proxy VC to ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_zioses.  For
        example: '2653'.  Required.

    :type allocation_zone_id: int
    :param allocation_zone_id: Allocation Zone ID.  For example: '1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(zios_id, 'zios_id')

    body = {"allocation_zone_id": allocation_zone_id}
    path = '/api/v2/vpsas/{0}/proxy_vcs/add.json'.format(zios_id)

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)
