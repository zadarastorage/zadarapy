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


from zadarapy.validators import verify_start_limit, verify_field, \
    verify_capacity, verify_raid_groups, \
    verify_pool_type, verify_boolean, verify_pool_id, verify_mode, \
    verify_drives, verify_positive_argument, verify_multiplier

__all__ = ["get_all_pools", "get_pool", "create_pool", "create_raid10_pool",
           "delete_pool", "rename_pool",
           "get_raid_groups_in_pool", "get_volumes_in_pool",
           "add_raid_groups_to_pool", "update_pool_capacity_alerts",
           "get_pool_mirror_destination_volumes", "set_pool_cache",
           "enable_cache", "disable_cache", "set_pool_cowcache", "expand_pool",
           "get_volumes_in_pool_recycle_bin", "get_pool_performance",
           "pool_shrink", "cancel_pool_shrink", "cooloff"]


def get_all_pools(session, start=None, limit=None, return_type=None, **kwargs):
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
    parameters = verify_start_limit(start, limit)

    path = '/api/pools.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_pool(session, pool_id, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)

    path = '/api/pools/{0}.json'.format(pool_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_pool(session, display_name, raid_groups, capacity, pooltype,
                cache='NO', cowcache='YES', mode='stripe', return_type=None,
                **kwargs):
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
        descriptive definition of these types.
        For VPSAs of gen 2: Must be the string 'Transactional', 'Repository', or 'Archival'.
        For VPSAs of gen 3: Must be the string 'Iops-Optimized', 'Balanced' or 'Throughput-Optimized'.
        Required.

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
    display_name = verify_field(display_name, "display_name")
    capacity = verify_capacity(capacity, "Storage Pool")
    verify_raid_groups(raid_groups)
    verify_pool_type(pooltype)
    cache = verify_boolean(cache, "cache")
    mode = verify_mode(mode)

    # If only one RAID group will be participating in this pool, force the
    # mode to simple.
    if len(raid_groups.split(',')) == 1:
        mode = 'simple'

    body_values = {'display_name': display_name,
                   'capacity': '{0}G'.format(capacity),
                   'raid_groups': raid_groups,
                   'cache': cache, 'mode': mode}

    if pooltype == 'Transactional':
        pooltype = 'Transactional Workloads'
    elif pooltype == 'Archival' or pooltype == 'Repository':
        pooltype = '{0} Storage'.format(pooltype)
    elif pooltype == 'Iops-Optimized':
        pooltype = 'IOPs-Optimized'

    body_values['pooltype'] = pooltype

    # CoW cache can only be enabled or disabled for pools where primary cache
    # is enabled.
    if cache == 'YES':
        cowcache = verify_boolean(cowcache, "cowcache")
        body_values['cowcache'] = str(cowcache == 'YES').lower()

    path = '/api/pools.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def create_raid10_pool(session, display_name, drives, pooltype,
                       cache='NO', cowcache='YES', return_type=None, **kwargs):
    """
    Creates a new RAID10 storage pool.  This is similar to the "create_pool"
    API, except the the caller passes a list of drives, and not a list of RAID
    groups. The VPSA will create the needed RAID groups.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: See documentation for create_pool.  Required.

    :type drives: str
    :param drives: A comma separated string of drives with no spaces
        around the commas. Note that drives are named as 'volume-00000001'
        etc.  For example: 'volume-00000012','volume-00000013'.  Required.

    :type pooltype: str
    :param pooltype: See documentation for create_pool.  Required.

    :type cache: str
    :param cache: See documentation for create_pool.  Optional, set to 'NO'
        by default.

    :type cowcache: str
    :param cowcache: See documentation for create_pool.  Optional, set to
        'YES' by default.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    display_name = verify_field(display_name, "display_name")
    verify_drives(drives)
    verify_pool_type(pooltype)
    pooltype = fix_pooltype(pooltype)
    cache = verify_boolean(cache, "cache")

    body_values = {'display_name': display_name, 'disks': drives,
                   'pooltype': pooltype, 'cache': cache}

    # CoW cache can only be enabled or disabled for pools where primary cache
    # is enabled.
    if cache == 'YES':
        cowcache = verify_boolean(cowcache, "cowcache")
        body_values['cowcache'] = str(cowcache == 'YES').lower()

    path = '/api/pools.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_pool(session, pool_id, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)

    path = '/api/pools/{0}.json'.format(pool_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def rename_pool(session, pool_id, display_name, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    display_name = verify_field(display_name, "display_name")

    body_values = {'new_name': display_name}

    path = '/api/pools/{0}/rename.json'.format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_raid_groups_in_pool(session, pool_id, start=None, limit=None,
                            return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/pools/{0}/raid_groups.json'.format(pool_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_volumes_in_pool(session, pool_id, start=None, limit=None,
                        return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/pools/{0}/volumes.json'.format(pool_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def add_raid_groups_to_pool(session, pool_id, raid_groups, capacity,
                            return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    verify_raid_groups(raid_groups)
    capacity = verify_capacity(capacity, "Storage pool")

    body_values = {'raid_groups': raid_groups,
                   'capacity': '{0}G'.format(capacity)}

    path = '/api/pools/{0}/expand.json'.format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_pool_capacity_alerts(session, pool_id, capacityhistory=None,
                                alertmode=None, protectedmode=None,
                                emergencymode=None, return_type=None,
                                **kwargs):
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
    verify_pool_id(pool_id)
    capacityhistory = verify_positive_argument(capacityhistory,
                                               "capacityhistory")
    alertmode = verify_positive_argument(alertmode, "alertmode")
    protectedmode = verify_positive_argument(protectedmode, "protectedmode")
    emergencymode = verify_positive_argument(emergencymode, "emergencymode")
    body_values = {}

    if capacityhistory is not None:
        body_values['capacityhistory'] = capacityhistory

    if alertmode is not None:
        body_values['alertmode'] = alertmode

    if protectedmode is not None:
        body_values['protectedmode'] = protectedmode

    if emergencymode is not None:
        body_values['emergencymode'] = emergencymode

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"capacityhistory", "alertmode", "protectedmode", '
                         '"emergencymode"')

    path = '/api/pools/{0}/update_protection.json'.format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_pool_mirror_destination_volumes(session, pool_id, start=None,
                                        limit=None, return_type=None,
                                        **kwargs):
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
    verify_pool_id(pool_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/pools/{0}/destination_volumes.json'.format(pool_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def set_pool_cache(session, pool_id, cache, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    cache = verify_boolean(cache, "cache")

    body_values = {'command': 'Enable' if cache == 'YES' else 'Disable'}

    path = '/api/pools/{0}/toggle_cache.json'.format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def enable_cache(session, pool_id, cowcache, return_type=None, **kwargs):
    verify_pool_id(pool_id)
    cowcache = verify_boolean(cowcache, "cowcache")
    cowcache = str(cowcache == 'YES').lower()
    path = '/api/pools/{0}'.format(pool_id)
    body_values = {'command': 'enable', 'cowcache': cowcache}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def disable_cache(session, pool_id, return_type=None, **kwargs):
    verify_pool_id(pool_id)
    path = '/api/pools/{0}'.format(pool_id)
    body_values = {'command': 'enable'}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_pool_cowcache(session, pool_id, cowcache, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    cowcache = verify_boolean(cowcache, "cowcache")

    body_values = {'cowcache': str(cowcache == 'YES').lower()}

    path = '/api/pools/{0}/cow_cache.json'.format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_volumes_in_pool_recycle_bin(session, pool_id, start=None, limit=None,
                                    return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/pools/{0}/volumes_in_recycle_bin.json'.format(pool_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_pool_performance(session, pool_id, interval=1, return_type=None,
                         **kwargs):
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
    verify_pool_id(pool_id)
    interval = verify_positive_argument(interval, "interval")

    path = '/api/pools/{0}/performance.json'.format(pool_id)

    parameters = {'interval': interval}

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


"""
Private functions
"""


def fix_pooltype(pooltype):
    """
    :type: str
    :param pooltype: Pool type to fix

    :rtype: str
    :return: Fixed pool type
    """

    if pooltype == 'Transactional':
        pooltype = 'Transactional Workloads'
    else:
        pooltype = '{0} Storage'.format(pooltype)

    return pooltype


def update_protection(session, pool_id, alertmode=None,
                      effectivecapacityhistory=None, capacityhistory=None,
                      protectedmode=None, effectiveprotectedmode=None,
                      emergencymode=None, effectiveemergencymode=None,
                      return_type=None, **kwargs):
    """
    Update free capacity alert notification settings for a Pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type capacityhistory: str
    :param capacityhistory: Window size in minutes which is used to calculate
    the rate of which free Pool capacity  is consumed. This rate is used to
    calculate the estimated time until a Pool is full.

    :type effectivecapacityhistory: str
    :param effectivecapacityhistory: Window size in minutes which is used to
     calculate the rate of which free Pool effective capacity is consumed.
     This rate is used to calculate the estimated time until a Pool is full.

    :type effectiveprotectedmode: str
    :param effectiveprotectedmode: Block Volume/Share/Pool creation when it's
    estimated that the Pool effective capacity will be full in this many
    minutes.

    :type effectiveemergencymode: str
    :param effectiveemergencymode: Delete snapshots, starting with the oldest,
    when the Pool effective capacity has less than this number of GB left.

    :type alertmode: int
    :param alertmode: Send an alert when it is estimated that the Pool will be
     at full capacity in this many minutes.

    :type emergencymode: int
    :param emergencymode: Delete snapshots, starting with the oldest, when the
     Volume has less than this number of GB left.

    :type capacityhistory: int
    :param capacityhistory: Window size in minutes which is used to calculate
    the rate of which free Volume capacity is consumed. This rate is used to
     calculate the estimated time until a Volume is full

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_pool_id(pool_id)

    body = {}

    if alertmode is not None:
        body["alertmode"] = alertmode
    if emergencymode is not None:
        body['emergencymode'] = emergencymode
    if effectiveemergencymode is not None:
        body['effectiveemergencymode'] = effectiveemergencymode
    if protectedmode is not None:
        body['protectedmode'] = protectedmode
    if effectiveprotectedmode is not None:
        body['effectiveprotectedmode'] = effectiveprotectedmode
    if capacityhistory is not None:
        body['capacityhistory'] = capacityhistory
    if effectivecapacityhistory is not None:
        body['effectivecapacityhistory'] = effectivecapacityhistory

    if not body:
        raise ValueError('At least one of the following must be set: '
                         '"alertmode", "emergencymode", '
                         '"effectiveemergencymode", '
                         '"protectedmode", "effectiveprotectedmode", '
                         '"capacityhistory", "effectivecapacityhistory"')

    path = "/api/pools/{0}/update_protection.json".format(pool_id)

    return session.post_api(path=path, body=body, return_type=return_type,
                            **kwargs)


def pool_shrink(session, pool_id, raid_group_id=None, obs_shrink_size=None, return_type=None, **kwargs):
    """
    Shrink a pool

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type raid_group_id: str
    :param raid_group_id: RAID Group ID

    :type obs_shrink_size: int
    :param obs_shrink_size: OBS size to shrink (multiple of 20)

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_pool_id(pool_id=pool_id)
    body_values = {}

    if raid_group_id is not None:
        verify_raid_groups(raid_groups=raid_group_id)
        body_values['raid_group'] = raid_group_id

    if obs_shrink_size is not None:
        verify_multiplier(num=obs_shrink_size, multiplier=20)
        body_values['obsshrinksize'] = obs_shrink_size

    path = "/api/pools/{0}/shrink.json".format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def cancel_pool_shrink(session, pool_id, return_type=None, **kwargs):
    """
    Cancel a pool shrink

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type raid_group_id: str
    :param raid_group_id: RAID Group ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_pool_id(pool_id=pool_id)
    path = "/api/pools/{0}/cancel_shrink.json".format(pool_id)
    return session.post_api(path=path, return_type=return_type, **kwargs)


def expand_pool(session, pool_id, raid_groups_ids=None, capacity=None,
                obsdestname=None, cloud_size=None, sse=None,
                return_type=None, **kwargs):
    """
    Add additional RAID Groups to a Pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type raid_groups_ids: str
    :param raid_groups_ids: RAID Group IDs separated by comma , (Cannot be used with `obsdestname`)

    :type capacity: int
    :param capacity: Capacity in GB.

    :type obsdestname: str
    :param obsdestname: Object storage destination name. Cannot be used with `raid_groups`

    :type cloud_size: str
    :param cloud_size: Object storage size (multiple of 20)

    :type sse: str
    :param sse: Encryption type

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_pool_id(pool_id=pool_id)

    if raid_groups_ids is not None and capacity is not None:
        verify_raid_groups(raid_groups=raid_groups_ids)
        body_values = {"capacity": "{}G".format(capacity),
                       "raid_groups": raid_groups_ids}
    else:
        verify_multiplier(cloud_size, 20)
        body_values = {"obsdestname": obsdestname,
                       "cloud_size": cloud_size}
        if sse is not None:
            body_values["sse"] = sse

    path = "/api/pools/{0}/expand.json".format(pool_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def cooloff(session, pool_id, cool_off_hours, return_type=None, **kwargs):
    """
    Add additional RAID Groups to a Pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type cool_off_hours: int
    :param cool_off_hours: Cool off hours time.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_pool_id(pool_id=pool_id)

    path = "/api/pools/{0}/update_ssd_cool_off.json".format(pool_id)
    body_values = {"cool_off_hours": cool_off_hours}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
