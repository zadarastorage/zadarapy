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


from zadarapy.validators import verify_boolean, \
    verify_field, verify_start_limit, verify_volume_id, verify_interval


def get_all_drives(session, start=None, limit=None, return_type=None,
                   **kwargs):
    """
    Retrieves details for all drives attached to the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    parameters = verify_start_limit(start, limit)

    path = '/api/drives.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_free_drives(session, start=None, limit=None, return_type=None,
                    **kwargs):
    """
    Retrieves details for all drives that are available for use (not
    participating in a RAID group).

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    parameters = verify_start_limit(start, limit)

    path = '/api/drives/free.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_drive(session, drive_id, return_type=None, **kwargs):
    """
    Retrieves details for a single drive.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(drive_id)

    path = '/api/drives/{0}.json'.format(drive_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def rename_drive(session, drive_id, display_name, return_type=None, **kwargs):
    """
    Sets the "display_name" drive parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

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
    verify_volume_id(drive_id)
    display_name = verify_field(display_name, "display_name")

    body_values = {'newname': display_name}

    path = '/api/drives/{0}/rename.json'.format(drive_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def remove_drive(session, drive_id, return_type=None, **kwargs):
    """
    Removes a drive from the VPSA.  Only drives that aren't participating in a
    RAID group may be removed.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(drive_id)

    path = '/api/drives/{0}/remove.json'.format(drive_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def replace_drive(session, drive_id, to_drive_id, force='NO',
                  return_type=None, **kwargs):
    """
    Replaces a drive, identified by drive_id parameter, with a new unallocated
    drive, identified by to_drive_id parameter, in a RAID group.  The
    replacement drive must not be currently allocated to a RAID group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive to be replaced.  This is the drive 'name' value
        as returned by get_all_drives.  For example: 'volume-00002a73'.
        Required.

    :type to_drive_id: str
    :param to_drive_id: The replacement drive.  This is the drive 'name' value
        as returned by get_all_drives.  For example: 'volume-00002a76'.
        Required.

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
    verify_volume_id(drive_id)
    verify_volume_id(to_drive_id)
    force = verify_boolean(force, "force")

    body_values = {'toname': to_drive_id, 'force': force}

    path = '/api/drives/{0}/replace.json'.format(drive_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def shred_drive(session, drive_id, force='NO', return_type=None, **kwargs):
    """
    Initializes drive shredding for an individual drive.  Drive must not be
    participating in a RAID group.  CAUTION: This procedure will permanently
    destroy data and is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

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
    verify_volume_id(drive_id)
    force = verify_boolean(force, "force")

    body_values = {'force': force}

    path = '/api/drives/{0}/shred.json'.format(drive_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def cancel_shred_drive(session, drive_id, return_type=None, **kwargs):
    """
    Cancels a drive shred that is currently in process.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(drive_id)

    path = '/api/drives/{0}/cancel_shred.json'.format(drive_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def get_drive_performance(session, drive_id, interval=1, return_type=None,
                          **kwargs):
    """
    Retrieves metering statistics for the drive for the specified interval.
    Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive_id: str
    :param drive_id: The drive 'name' value as returned by get_all_drives.
        For example: 'volume-00002a73'.  Required.

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
    verify_volume_id(drive_id)
    interval = verify_interval(interval)

    path = '/api/drives/{0}/performance.json'.format(drive_id)

    parameters = {'interval': interval}

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)
