# Copyright 2020 Zadara Storage, Inc.
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


def get_psdrive(session, return_type=None, **kwargs):
    """
    Return file-system PS Drives

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
    path = '/api/psdrive'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def initialize_disk(session, disk_id, return_type=None, **kwargs):
    """
    Initialize disk on remote windows server

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type disk_id: str
    :param disk_id: Id of the drive - e.g. '1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/initialize_disk'

    body = {"disk_id": disk_id}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def get_volumes(session, return_type=None, **kwargs):
    """
    Get all volumes on remote server

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
    path = '/api/volume'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_volume(session, volume_id, volume_letter, return_type=None, **kwargs):
    """
    Get all volumes on remote server

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: Id of the drive - e.g. '1'.  Required.

    :type volume_letter: str
    :param volume_letter: Drive letter - e.g. 'Q'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/volume'

    body = {"volume_id": volume_id, "volume_letter": volume_letter}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def get_mount_points(session, return_type=None, **kwargs):
    """
    Get net-use points in remote windows server

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
    path = '/api/net_use'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def mount(session, drive, smb_path, return_type=None, **kwargs):
    """
    Set a virtual drive to SMB path on remote windows server

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive: str
    :param drive: Drive letter - e.g. 'Q'.  Required.

    :type smb_path: str
    :param smb_path: SMB path from NFS volume - e.g. '\\\\10.2.12.23\\zat_nas_1JsQ0y'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/net_use'

    body = {"drive": drive, "smb_path": smb_path}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def umount(session, drive, return_type=None, **kwargs):
    """
    Remove a virtual drive from remote windows server

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type drive: str
    :param drive: Drive letter - e.g. 'Q'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/net_use'

    body = {"drive": drive}

    return session.delete_api(path=path, body=body, return_type=return_type, **kwargs)


def rescan_disks(session, return_type=None, **kwargs):
    """
    Set a virtual drive to SMB path on remote windows server

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
    path = '/api/rescan_disks'

    return session.post_api(path=path, return_type=return_type, **kwargs)
