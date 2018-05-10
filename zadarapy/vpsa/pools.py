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
from zadarapy.validators import is_valid_field
from zadarapy.validators import is_valid_pool_id
from zadarapy.validators import is_valid_raid_id


def get_all_pools(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all storage pools configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying pools from.  Optional.

    :type: limit: int
    :param limit: The maximum number of pools to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/pools.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_pool(session, pool_id, return_type=None):
    """
    Retrieves details for all single storage pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    method = 'GET'
    path = '/api/pools/{0}.json'.format(pool_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_pool(session, display_name, raid_groups, capacity, pooltype,
                cache='NO', cowcache='YES', mode='stripe', return_type=None):
    """
    Creates a new storage pool.  A storage pool is an abstraction over RAID
    groups.  Multiple RAID groups can, and often do, participate in a single
    storage pool.  Volumes are then created on the storage pool, rather than
    on the individual RAID groups.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the pool.  For example:
        'pool1', 'pool2', etc.  May not contain a single quote (') character.
        Required.

    :type raid_groups: str
    :param raid_groups: A comma separated string of RAID groups with no spaces
        around the commas.  The value must match RAID groups's 'name'
        attribute.  For example: 'RaidGroup-1,RaidGroup-2'.  Required.

    :type capacity: int
    :param capacity: The total capacity in GB that will be created for the
        storage pool.  May not exceed the capacity of the combined underlying
        RAID groups.  Required.

    :type pooltype: str
    :param pooltype: Whether the pool should be set to Transactional,
        Repository, or Archival type.  Transactional is useful for more space
        efficient writes on snapshots, but requires 4x as much memory,
        therefore is limited to 20TB maximum space.  Repository is a good
        general purpose option that suits all workloads up to 100TB.  Archival
        can be used when >100TB pools are mandatory, but comes with
        restrictions such as minimum 1 hour snapshot interval (instead of 1
        minute).  Please see the VSPA User Guide "Pools" section for a more
        descriptive definition of these types.  Must be the string
        'Transactional', 'Repository', or 'Archival'.  Required.

    :type cache: str
    :param cache: If set to 'YES', SSD caching will be enabled for this pool.
        Optional, set to 'NO' by default.

    :type cowcache: str
    :param cowcache: If set to 'YES', the pool's copy on write (CoW)
        operations will occur on SSD for elevated performance instead of
        directly on the underlying drives.  In certain extreme scenarios, this
        may be detrimental.  It is suggested to leave 'YES' unless instructed
        by a Zadara Storage representative.  Optional, set to 'YES' by
        default.

    :type mode: str
    :param mode: If set to 'stripe', use striping to distribute data across
        all participating RAID sets in the pool - this should always be used
        for pools with more than one RAID group, unless you know what you're
        doing.  If set to 'simple', data will fill up one RAID group before
        moving to the next (worse for performance than stripe).  Single RAID
        group pools will be set to 'simple' below automatically.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid pool name.'.format(display_name))

    body_values['display_name'] = display_name

    capacity = int(capacity)

    if capacity < 1:
        raise ValueError('Storage pool must be >= 1 GB ("{0}" was given)'
                         .format(capacity))

    body_values['capacity'] = '{0}G'.format(capacity)

    rg = raid_groups.split(',')

    for raid_group in rg:
        if not is_valid_raid_id(raid_group):
            raise ValueError('"{0}" in "{1}" is not a valid RAID group ID.'
                             .format(raid_group, raid_groups))

    body_values['raid_groups'] = raid_groups

    if pooltype not in ['Transactional', 'Repository', 'Archival']:
        raise ValueError('"{0}" is not a valid pool type.  Allowed values '
                         'are: "Transactional", "Repository", or "Archival"'
                         .format(pooltype))

    if pooltype == 'Transactional':
        pooltype = 'Transactional Workloads'
    else:
        pooltype = '{0} Storage'.format(pooltype)

    body_values['pooltype'] = pooltype

    cache = cache.upper()

    if cache not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid cache setting.  Allowed '
                         'values are: "YES" or "NO"'.format(cache))

    body_values['cache'] = cache

    cowcache = cowcache.upper()

    if cowcache not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid cowcache setting.  Allowed '
                         'values are: "YES" or "NO"'.format(cowcache))

    body_values['cowcache'] = cowcache

    if mode not in ['stripe', 'simple']:
        raise ValueError('"{0}" is not a valid pool mode.  Allowed values '
                         'are: "stripe" or "simple"'.format(mode))

    # If only one RAID group will be participating in this pool, force the
    # mode to simple.
    if len(rg) == 1:
        mode = 'simple'

    body_values['mode'] = mode

    method = 'POST'
    path = '/api/pools.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_pool(session, pool_id, return_type=None):
    """
    Deletes a storage pool.  The storage pool must not contain any volumes,
    including in the pool's recycle bin.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    method = 'DELETE'
    path = '/api/pools/{0}.json'.format(pool_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def rename_pool(session, pool_id, display_name, return_type=None):
    """
    Sets the "display_name" pool parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type display_name: str
    :param display_name: The new "display_name" to set.  May not contain a
        single quote (') character.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid pool name.'
                         .format(display_name))

    body_values['new_name'] = display_name

    method = 'POST'
    path = '/api/pools/{0}/rename.json'.format(pool_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_raid_groups_in_pool(session, pool_id, start=None, limit=None,
                            return_type=None):
    """
    Retrieves a list of RAID groups that are participating in the given pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying RAID groups from.  Optional.

    :type: limit: int
    :param limit: The maximum number of RAID groups to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/pools/{0}/raid_groups.json'.format(pool_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_volumes_in_pool(session, pool_id, start=None, limit=None,
                        return_type=None):
    """
    Retrieves a list of volumes stored on the given pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying volumes from.  Optional.

    :type: limit: int
    :param limit: The maximum number of volumes to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/pools/{0}/volumes.json'.format(pool_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def add_raid_groups_to_pool(session, pool_id, raid_groups, capacity,
                            return_type=None):
    """
    Adds RAID groups to a storage pool.  RAID groups need to be of the same
    type as the RAID groups already participating in the pool.  RAID groups
    also must not be allocated to another pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type raid_groups: str
    :param raid_groups: A comma separated string of RAID groups with no spaces
        around the commas.  The value must match RAID groups's 'name'
        attribute.  For example: 'RaidGroup-3,RaidGroup-4'.  Required.

    :type capacity: int
    :param capacity: The total capacity in GB that will be added for the
        storage pool.  May not exceed the capacity of the combined added
        RAID groups.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {}

    for raid_group in raid_groups.split(','):
        if not is_valid_raid_id(raid_group):
            raise ValueError('"{0}" in "{1}" is not a valid RAID group ID.'
                             .format(raid_group, raid_groups))

    body_values['raid_groups'] = raid_groups

    capacity = int(capacity)

    if capacity < 1:
        raise ValueError('Storage pool must be expanded by >= 1 GB ("{0}" '
                         'was given)'.format(capacity))

    body_values['capacity'] = '{0}G'.format(capacity)

    method = 'POST'
    path = '/api/pools/{0}/expand.json'.format(pool_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_pool_capacity_alerts(session, pool_id, capacityhistory=None,
                                alertmode=None, protectedmode=None,
                                emergencymode=None, return_type=None):
    """
    Update the pool alerting thresholds.  Alerts are used both to notify
    administrators of pending pool space exhaustion, as well as deleting
    the oldest snapshots in an attempt to free space.  Parameters set to
    'None' will not have their existing values changed.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type capacityhistory: int
    :param capacityhistory: The number of minutes used to calculate pool
        exhaustion.  This value is used in conjunction with "alertmode".  For
        example, if "capacityhistory" is 60 minutes, the VPSA will use the
        amount of data written in the last 60 minutes to calculate the write
        rate for the "alertmode" value.  Optional.

    :type alertmode: int
    :param alertmode: The number of minutes before the storage pool is
        predicted to reach space exhaustion.  Works in conjunction with the
        "capacityhistory" value.  If the VPSA predicts the pool will run out
        of space in less than or equal to the amount of minutes defined here,
        an alert will be sent to the VPSA administrator.  Optional.

    :type protectedmode: int
    :param protectedmode: If the number of minutes before the pool is
        predicted to reach space exhaustion is less than this value, the VPSA
        will not allow the creation of new volumes, shares, or snapshots.
        Optional.

    :type emergencymode: int
    :param emergencymode: If the number of GB free on the pool is less than
        this value, the VPSA will start deleting old snapshots in an attempt
        to prevent space exhaustion.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {}

    if capacityhistory is not None:
        capacityhistory = int(capacityhistory)
        if capacityhistory < 1:
            raise ValueError('Supplied capacityhistory interval ("{0}") must '
                             'be at least one minute.'
                             .format(capacityhistory))

        body_values['capacityhistory'] = capacityhistory

    if alertmode is not None:
        alertmode = int(alertmode)
        if alertmode < 1:
            raise ValueError('Supplied alertmode interval ("{0}") must be at '
                             'least one minute.'.format(alertmode))

        body_values['alertmode'] = alertmode

    if protectedmode is not None:
        protectedmode = int(protectedmode)
        if protectedmode < 1:
            raise ValueError('Supplied protectedmode interval ("{0}") must '
                             'be at least one minute.'
                             .format(protectedmode))

        body_values['protectedmode'] = protectedmode

    if emergencymode is not None:
        emergencymode = int(emergencymode)
        if emergencymode < 1:
            raise ValueError('Supplied emergencymode value ("{0}") must be '
                             'at least one gigabyte.'.format(emergencymode))

        body_values['emergencymode'] = emergencymode

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"capacityhistory", "alertmode", "protectedmode", '
                         '"emergencymode"')

    method = 'POST'
    path = '/api/pools/{0}/update_protection.json'.format(pool_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_pool_mirror_destination_volumes(session, pool_id, start=None,
                                        limit=None, return_type=None):
    """
    Retrieves all mirror destination volumes that reside in this pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying volumes from.  Optional.

    :type: limit: int
    :param limit: The maximum number of volumes to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/pools/{0}/destination_volumes.json'.format(pool_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def set_pool_cache(session, pool_id, cache, return_type=None):
    """
    Toggle the SSD caching for a pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type cache: str
    :param cache: Set to 'YES' to turn SSD caching on for this pool, or
        'NO' to turn it off.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {}

    cache = cache.upper()

    if cache not in ['YES', 'NO']:
        raise ValueError('cache parameter must be set to either "YES" or '
                         '"NO" ("{0}" was given).')

    if cache == 'YES':
        body_values['command'] = 'Enable'
    else:
        body_values['command'] = 'Disable'

    method = 'POST'
    path = '/api/pools/{0}/toggle_cache.json'.format(pool_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def set_pool_cowcache(session, pool_id, cowcache, return_type=None):
    """
    Toggle the CoW caching for a pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type cowcache: str
    :param cowcache: If set to 'YES', the pool's copy on write (CoW)
        operations will occur on SSD for elevated performance instead of
        directly on the underlying drives.  In certain extreme scenarios, this
        may be detrimental.  It is suggested to leave 'YES' unless instructed
        by a Zadara Storage representative.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {}

    cowcache = cowcache.upper()

    if cowcache not in ['YES', 'NO']:
        raise ValueError('cowcache parameter must be set to either "YES" or '
                         '"NO" ("{0}" was given).')

    if cowcache == 'YES':
        body_values['cowcache'] = 'true'
    else:
        body_values['cowcache'] = 'false'

    method = 'POST'
    path = '/api/pools/{0}/cow_cache.json'.format(pool_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_volumes_in_pool_recycle_bin(session, pool_id, start=None, limit=None,
                                    return_type=None):
    """
    Retrieves a list of volumes in the pool's recycle bin.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying volumes from.  Optional.

    :type: limit: int
    :param limit: The maximum number of volumes to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/pools/{0}/volumes_in_recycle_bin.json'.format(pool_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_pool_performance(session, pool_id, interval=1, return_type=None):
    """
    Retrieves metering statistics for the pool for the specified interval.
    Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/pools/{0}/performance.json'.format(pool_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
