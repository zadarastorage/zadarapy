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

from zadarapy.validators import is_valid_field, verify_positive_argument, \
    verify_io_engine_id, verify_zcs_engine_id, verify_cache_argument
from future.standard_library import install_aliases
install_aliases()


def get_all_vpsas(session, return_type=None, **kwargs):
    """
    Retrieves details for all VPSAs of the connecting user.

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
    path = '/api/v2/vpsas.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsa(session, vpsa_id, return_type=None, **kwargs):
    """
    Retrieves details for a single VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if type(vpsa_id) is int:
        vpsa_id = str(vpsa_id)

    if not vpsa_id.isdigit():
        raise ValueError('The VPSA ID should be a positive integer.')

    path = '/api/v2/vpsas/{0}.json'.format(vpsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_vpsa(session, display_name, cloud_id, io_engine_id, drives,
                description=None, allocation_zone=None, custom_network_id=None, app_engine=None,
                flash_cache_capacity=None, return_type=None, **kwargs):
    """
    Submits a request to create a new VPSA.  This must be approved by a
    storage cloud administrator before the VPSA creation starts.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the VPSA.  For example:
        'aws_east_master_vpsa'.  May only contain alphanumeric and underscore
        characters.  Required.

    :type cloud_id: str
    :param cloud_id: The storage cloud (provider) 'key' value as returned by
        get_all_clouds.  For example: 'zadaraqa10' or 'zadaraqa17'.  The VPSA will be
        created on this storage cloud.  Required.

    :type io_engine_id: str
    :param io_engine_id: The IO engine 'key' value as returned by the
        'engine_types' list for cloud_id from get_cloud.  For example:
        'vsa.V2.baby.vf'.  Required.

    :type app_engine: str
    :param app_engine: The ZCS engine 'key' value as returned by the
        'app_engine_types' list for cloud_id from get_cloud.  For example:
        'tiny'.  Can also be the string 'None', which will disable the ZCS
        engine for this VPSA.

    :type drives: list
    :param drives: A Python list of Python dictionaries that defines what type
        and how many of each type of drive to attach to the VPSA.  Each list
        item should contain a dictionary that defines a 'drive_type' key and
        'quantity' key.  The 'drive_type' key is the 'key' value as returned
        by the 'drive_types' list for the cloud_id from get_cloud.  For
        example: 'SATA_2793GB_5940RPM'.  The 'quantity' key is the number of
        drives to add for this type.  Every VPSA must have at least two
        drives.

        For example, to add two SATA 3TB drives and two 600GB SAS drives, use
        the following:

        [{'drive_type':'SATA_2793GB_5940RPM','quantity':2},
         {'drive_type':'SAS_557GB_10500RPM','quantity':2}]

        Please note that the example is not a string, rather a representation
        of what the "pprint" function might return.  Required.

    :type flash_cache_capacity: int
    :param flash_cache_capacity: The amount of extended Flash Cache you would
        like your VPSA to be created with, if your Cloud supports extended Flash
        Cache. Cannot exceed the maximum extended Flash Cache value for your
        VPSA's Engine Type, and must be in increments of `increment_gb`, as
        specified by the Cloud's `flash_cache` properties.

    :type description: str
    :param description: A text description for the VPSA.  For example:
        'Primary VPSA for AWS East'.  May not contain a single quote
        (') character.  Optional.

    :type allocation_zone: str
    :param allocation_zone: For multizone environments, this parameter
        specifies that either the VPSA should run in multizone mode, or in a
        specific zone.  If set to None, for multizone environments, multizone
        will be used; for single zone, the only available zone will be used.
        If set to a string, that zone will be used.  Zone names are listed in
        the 'allocation_zones' list as returned by get_cloud for cloud_id.
        For example: 'zone_0'.  Optional.

    :type custom_network_id: int
    :param custom_network_id: Custom network id. For example: '1'. If custom network is not needed, enter None.
         Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid VPSA name.'.format(display_name))

    body['name'] = display_name

    cloud_id = cloud_id.strip()

    if not is_valid_field(cloud_id):
        raise ValueError('{0} is not a valid storage cloud key.'.format(cloud_id))

    body['provider'] = cloud_id

    if 'vsa.' not in io_engine_id:
        raise ValueError('{0} is not a valid IO engine type.'.format(io_engine_id))

    body['engine'] = io_engine_id

    if app_engine is not None:
        if app_engine not in ['None', 'tiny', 'small', 'medium', 'large', 'xlarge']:
            raise ValueError('{0} is not a valid ZCS engine type.'.format(app_engine))

        body['app_engine'] = app_engine

    if type(drives) is not list:
        raise ValueError('The passed "drives" parameter is not a Python list.')

    for v in drives:
        if type(v) is not dict:
            raise ValueError('Each item in the "drives" list must be a Python dictionary.')

        if 'drive_type' not in v:
            raise ValueError('The required "drive_type" key was not found in '
                             'the drive dictionary.')

        if 'quantity' not in v:
            raise ValueError('The required "quantity" key was not found in '
                             'the drive dictionary.')

        body[v['drive_type'] + '_drives'] = int(v['quantity'])

    if description is not None:
        description = description.strip()

        if not is_valid_field(description):
            raise ValueError('{0} is not a valid VPSA description.'
                             .format(description))

        body['description'] = description

    if allocation_zone is not None:
        body['allocation_zone'] = allocation_zone

    body['custom_network_id'] = custom_network_id

    if flash_cache_capacity is not None:
        body['flash_cache_capacity'] = flash_cache_capacity

    # Enterprise suite should always be enabled.
    body['enterprise_suite'] = 'YES'

    path = '/api/v2/vpsas.json'

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def delete_vpsa(session, vpsa_id, return_type=None, **kwargs):
    """
    Submits a request to delete a VPSA.  This must be approved by a storage
    cloud administrator before the VPSA is deleted.  Once approved by the
    storage cloud administrator, this action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA/ZIOS 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    path = '/api/v2/vpsas/{0}.json'.format(vpsa_id)
    return session.delete_api(path=path, return_type=return_type, **kwargs)


def add_drives(session, vpsa_id, drives, storage_policy, return_type=None, **kwargs):
    """
    Submits a request to add drives to a VPSA.  This must be approved by a
    storage cloud administrator before the drives are added.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type drives: list
    :param drives: A Python list of Python dictionaries that defines what type
        and how many of each type of drive to attach to the VPSA.  Each list
        item should contain a dictionary that defines a 'drive_type' key and
        'quantity' key.  The 'drive_type' key is the 'key' value as returned
        by the 'drive_types' list for the cloud_id from get_cloud.  For
        example: 'SATA_2793GB_5940RPM'.  The 'quantity' key is the number of
        drives to add for this type.  Every VPSA must have at least two
        drives.

        For example, to add two SATA 3TB drives and two 600GB SAS drives, use
        the following:

        [{'drive_type':'SATA_2793GB_5940RPM','quantity':2},
         {'drive_type':'SAS_557GB_10500RPM','quantity':2}]

        Please note that the example is not a string, rather a representation
        of what the "pprint" function might return.  Required.

    :type storage_policy: str
    :param storage_policy: Storage Policy Name.
        Example - "storage-policy-00000001". (Only for VPSA Object Storage).  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, "vpsa_id")
    body = {}

    if type(drives) is not list:
        raise ValueError('The passed "drives" parameter is not a Python '
                         'list.')

    drives_to_add = {}
    for v in drives:
        if type(v) is not dict:
            raise ValueError('Each item in the "drives" list must be a '
                             'Python dictionary.')

        if 'drive_type' not in v:
            raise ValueError('The required "drive_type" key was not found in '
                             'the drive dictionary.')

        if 'quantity' not in v:
            raise ValueError('The required "quantity" key was not found in '
                             'the drive dictionary.')
        drives_to_add[v["drive_type"]] = v["quantity"]

    body["drives"] = drives_to_add

    if storage_policy is not None:
        body['storage_policy'] = storage_policy

    path = '/api/v2/vpsas/{0}/drives.json'.format(vpsa_id)

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def change_vpsa_engines(session, vpsa_id, io_engine_id, zcs_engine_id,
                        return_type=None, **kwargs):
    """
    Submits a request to create a new VPSA.  This must be approved by a
    storage cloud administrator before the VPSA creation starts.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type io_engine_id: str
    :param io_engine_id: The IO engine 'key' value as returned by the
        'engine_types' list for cloud_id from get_cloud.  For example:
        'vsa.V2.baby.vf'.  This can be the same value as the existing IO
        engine.  Required.

    :type zcs_engine_id: str
    :param zcs_engine_id: The ZCS engine 'key' value as returned by the
        'app_engine_types' list for cloud_id from get_cloud.  For example:
        'tiny'.  Can also be the string 'None', which will disable the ZCS
        engine for this VPSA.  This can be the same value as the existing ZCS
        engine.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    verify_io_engine_id(io_engine_id)
    verify_zcs_engine_id(zcs_engine_id)
    body = {'engine': io_engine_id, 'app_engine': zcs_engine_id}
    path = '/api/v2/vpsas/{0}/engine.json'.format(vpsa_id)

    return session.post_api(path=path, body=body, return_type=return_type,
                            **kwargs)


def change_vpsa_cache(session, vpsa_id, quantity, return_type=None, **kwargs):
    """
    Sets the quantity of additional cache groups for a VPSA.  The quantity of
    cache groups that comes with the base engine is not included in this
    calculation.  For example, if the engine comes with 2 cache groups,
    passing a quantity of 0 will result in 2 total groups, a quantity of 1
    will result in 3 total groups, and so on.  Conversely, in the same
    example, to go from 4 to 2 cache groups, a quantity of 0 would be needed.
    This must be approved by a storage cloud administrator before the cache
    groups are modified.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type quantity: int
    :param quantity: As described above, the total number of additional cache
        groups needed in addition to the groups that come with the engine.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    verify_cache_argument(quantity, 'quantity')

    path = '/api/v2/vpsas/{0}/cache.json'.format(vpsa_id)
    body = {'flash_cache_capacity': '{}'.format(quantity)}

    return session.post_api(path=path, body=body, return_type=return_type,
                            **kwargs)


def assign_vpsa_public_ip(session, vpsa_id, return_type=None, **kwargs):
    """
    Submits a request to assign a public IP to the VPSA.  Public IPs are
    optionally used to replicate data between VPSAs or from a VPSA to an
    object storage destination.  Only valid for storage clouds where public
    IPs are available.  This must be approved by a storage cloud administrator
    before the public IP is assigned.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    path = '/api/v2/vpsas/{0}/public_ip.json'.format(vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def remove_vpsa_public_ip(session, vpsa_id, return_type=None, **kwargs):
    """
    Submits a request to remove a public IP from a VPSA.  This must be
    approved by a storage cloud administrator before the public IP is
    assigned.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    path = '/api/v2/vpsas/{0}/public_ip.json'.format(vpsa_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def hibernate_vpsa(session, vpsa_id, return_type=None, **kwargs):
    """
    Hibernates a VPSA.  A hibernated VPSA will have all IO and ZCS engines
    shutdown, during which time there is no hourly cost incurred for those
    engines (costs still apply for all attached drives).  This action is
    immediate and does not require a storage cloud administrator's approval.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    path = '/api/v2/vpsas/{0}/hibernate.json'.format(vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def resume_vpsa(session, vpsa_id, return_type=None, **kwargs):
    """
    Resumes a hibernated VPSA.  This action is immediate and does not require
    a storage cloud administrator's approval.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    path = '/api/v2/vpsas/{0}/restore.json'.format(vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def add_virtual_network_vpsa(session, vpsa_id, virtual_network_id, return_type=None, **kwargs):
    """
    Add a virtual network to VPSA

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type virtual_network_id: int
    :param virtual_network_id: The virtual network 'id' value as returned by get_virtual_networks.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')
    verify_positive_argument(virtual_network_id, 'virtual_network_id')
    path = '/api/v2/vpsas/{0}/add_vni.json'.format(vpsa_id)
    body = {'virtual_network_id': '{}'.format(virtual_network_id)}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def rename(session, vpsa_id, new_name, description, return_type=None, **kwargs):
    """
    Rename VPSA/ZIOS

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type new_name: str
    :param new_name: New VPSA/ZIOS name.  Required.

    :type description: str
    :param description: New VPSA/ZIOS description.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_positive_argument(vpsa_id, 'vpsa_id')

    path = '/api/v2/vpsas/{0}.json'.format(vpsa_id)
    body = {'display_name': new_name, 'display_description': description}

    return session.put_api(path=path, body=body, return_type=return_type, **kwargs)
