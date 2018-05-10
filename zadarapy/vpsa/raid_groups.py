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
from zadarapy.validators import is_valid_raid_id
from zadarapy.validators import is_valid_volume_id


def get_all_raid_groups(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all RAID groups configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    path = '/api/raid_groups.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_free_raid_groups(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all RAID groups configured on the VPSA that are not
    currently participating in a storage pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    path = '/api/raid_groups/free.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_raid_group(session, raid_id, return_type=None):
    """
    Retrieves details for a single RAID group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'GET'
    path = '/api/raid_groups/{0}.json'.format(raid_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_raid_group(session, display_name, protection, disk,
                      stripe_size=64, hot_spare='NO', force='NO',
                      return_type=None):
    """
    Creates a new RAID group from comma separated list of drives in 'drive'
    body parameter.  The drives must not be currently participating in a RAID
    group.  Creation will fail if drives are not of identical capacity - this
    can be overridden with the "force" parameter.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the RAID group.  For
        example: 'rg1', 'rg2', etc.  May not contain a single quote (')
        character.  Required.

    :type protection: str
    :param protection: The type of RAID protection to use as represented by a
        string.  Must be one of: 'RAID1', 'RAID5', or 'RAID6'.  Required.

    :type disk: str
    :param disk: A comma separated string of drives with no spaces around the
        commas.  The value must match drive's 'name' attribute.  For example:
        'volume-00002a73,volume-00002a74'.  Required.

    :type stripe_size: int
    :param stripe_size: The stripe size for a RAID5 or RAID6 group, in KB.
        Must be one of the following sizes: 4, 16, 32, 64, 128, or 256.  It is
        suggested to use the default value of 64KB unless you know what you're
        doing.  Required for RAID5/RAID6, irrelevant for RAID1.

    :type hot_spare: str
    :param hot_spare: If set to 'YES', a hot spare will be assigned to the
        RAID group from the group of drives defined in the 'drive' parameter.
        Optional, set to 'NO' by default.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSA to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :return: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid RAID group ID.'
                         .format(display_name))

    body_values['display_name'] = display_name

    if protection not in ['RAID1', 'RAID5', 'RAID6']:
        raise ValueError('"{0}" is not a valid RAID type.  Allowed values '
                         'are: "RAID1", "RAID5", and "RAID6"'
                         .format(protection))

    body_values['protection'] = protection

    drives = disk.split(',')

    for drive_id in drives:
        if not is_valid_volume_id(drive_id):
            raise ValueError('"{0}" in "{1}" is not a valid drive ID.'
                             .format(drive_id, disk))

    body_values['disk'] = disk

    if stripe_size not in [4, 16, 32, 64, 128, 256]:
        raise ValueError('{0} is not a valid stripe size.  Allowed values '
                         'are: 4, 16, 32, 64, 128, or 256'
                         .format(stripe_size))

    if protection == 'RAID1':
        stripe_size = None

    if stripe_size is not None:
        body_values['stripe_size'] = stripe_size

    hot_spare = hot_spare.upper()

    if hot_spare not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid hot spare setting.  Allowed '
                         'values are: "YES" or "NO"'.format(hot_spare))

    body_values['hot_spare'] = hot_spare

    # Inflect the required protection_width parameter from the count of
    # elements in the 'disk' parameter instead of making the user pass it.
    protection_width = len(drives)

    if protection == 'RAID1':
        if protection_width < 2 or protection_width > 3:
            raise ValueError('A RAID1 group may only have 2 or 3 drives, but '
                             '{0} were supplied.'.format(protection_width))

    if protection == 'RAID5':
        if protection_width < 3 or protection_width > 5:
            raise ValueError('A RAID5 group may only have 3-5 drives, but '
                             '{0} were supplied.'.format(protection_width))

    if protection == 'RAID6':
        if protection_width < 4 or protection_width > 10:
            raise ValueError('A RAID6 group may only have 4-10 drives, but '
                             '{0} were supplied.'.format(protection_width))

    body_values['protection_width'] = protection_width

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/raid_groups.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_raid_group(session, raid_id, return_type=None):
    """
    Deletes a single RAID group.  The RAID group must not be participating in
    a storage pool.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'DELETE'
    path = '/api/raid_groups/{0}.json'.format(raid_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_drives_in_raid_group(session, raid_id, start=None, limit=None,
                             return_type=None):
    """
    Retrieves details for all drives in a RAID group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type start: int
    :param start: The offset to start displaying drives from.  Optional.

    :type: limit: int
    :param limit: The maximum number of drives to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'GET'
    path = '/api/raid_groups/{0}/disks.json'.format(raid_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def rename_raid_group(session, raid_id, display_name, return_type=None):
    """
    Sets the "display_name" RAID group parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The drive 'name' value as returned by get_all_raid_groups.
        For example: 'RaidGroup-1'.  Required.

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
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid RAID group name.'
                         .format(display_name))

    body_values['newname'] = display_name

    method = 'POST'
    path = '/api/raid_groups/{0}/rename.json'.format(raid_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def repair_raid_group(session, raid_id, return_type=None):
    """
    Repairs a degraded RAID group with an available drive.  This function will
    first attempt to detect if there are any available drives, and will only
    proceed if one is found.  This function should be used with caution.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The drive 'name' value as returned by get_all_raid_groups.
        For example: 'RaidGroup-1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'POST'
    path = '/api/raid_groups/{0}/repair.json'.format(raid_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def update_raid_group_resync_speed(session, raid_id, minimum, maximum,
                                   return_type=None):
    """
    Updates the speed at which a RAID group will rebuild using the minimum and
    maximum arguments.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The drive 'name' value as returned by get_all_raid_groups.
        For example: 'RaidGroup-1'.  Required.

    :type minimum: int
    :param minimum: Minimum speed in MB per second. Resync is done at minimum
        speed while there are Server IOs.  Required.

    :type maximum: int
    :param maximum: Maximum speed in MB per second. Resync is done at maximum
        speed when there are no Server IOs.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    body_values = {}

    minimum = int(minimum)
    maximum = int(maximum)

    if minimum < 0 or maximum < 0:
        raise ValueError('Minimum speed ({0}) and maximum speed ({1}) must '
                         'both be a positive integer.'
                         .format(minimum, maximum))

    if minimum > maximum:
        raise ValueError('Minimum speed ({0}) must be less than maximum speed '
                         '({1}).'.format(minimum, maximum))

    body_values['min'] = minimum
    body_values['max'] = maximum

    method = 'POST'
    path = '/api/raid_groups/{0}/resync_speed.json'.format(raid_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def start_raid_group_media_scan(session, raid_id, return_type=None):
    """
    Starts a media scan that will repair any inconsistencies with parity.
    Only valid for RAID5 and RAID6.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'POST'
    path = '/api/raid_groups/{0}/scrub.json'.format(raid_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def pause_raid_group_media_scan(session, raid_id, return_type=None):
    """
    Pauses a currently running RAID group media scan.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'POST'
    path = '/api/raid_groups/{0}/pause_scrub.json'.format(raid_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def add_hot_spare_to_raid_group(session, raid_id, drive_id, force='NO',
                                return_type=None):
    """
    Attaches a drive as a hot spare to an existing RAID group, as identified
    by the drive_id attribute.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSA to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    body_values = {}

    if not is_valid_volume_id(drive_id):
        raise ValueError('{0} is not a valid drive ID.'.format(drive_id))

    body_values['disk'] = drive_id

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/raid_groups/{0}/hot_spares.json'.format(raid_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def remove_hot_spare_from_raid_group(session, raid_id, return_type=None):
    """
    Removes the hot spare drive from an existing RAID group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type raid_id: str
    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    method = 'POST'
    path = '/api/raid_groups/{0}/hot_spares/remove.json'.format(raid_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_raid_group_performance(session, raid_id, interval=1,
                               return_type=None):
    """
    Retrieves metering statistics for the RAID group for the specified
    interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :param raid_id: The RAID group 'name' value as returned by
        get_all_raid_groups.  For example: 'RaidGroup-1'.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.
        Optional (will be set to 1 second by default).

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/raid_groups/{0}/performance.json'.format(raid_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
