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


def get_antivirus_status(session, return_type=None, **kwargs):
    """
    Enables the antivirus engine.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """

    path = '/api/antivirus/engine.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_policies(session, return_type=None, **kwargs):
    """
    Returns all antivirus policies.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """

    path = '/api/antivirus/default_policy.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def enable_antivirus(session, pool_id, return_type=None, **kwargs):
    """
    Enables the antivirus engine.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: Pool to create quarantine volume.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """
    body_values = {'pool': pool_id}

    path = '/api/antivirus/engine.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def disable_antivirus(session, return_type=None, **kwargs):
    """
    Disables the antivirus engine.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """

    path = '/api/antivirus/engine.json'

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def update_on_demand_policy(session, run_policy, include_file_types=None, exclude_file_types=None,
                            scan_subfolders=False, scan_archives=False, primary_action=None,
                            secondary_action=None, return_type=None, **kwargs):
    """
    Updates on demand policy settings

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type run_policy: str
    :param run_policy: cron expression that sets scan schedule. For example: "5 0 * * *"

    :type include_file_types: list, str
    :param include_file_types: scan only specific file types. Can't be used together with exclude_file_types param.

    :type exclude_file_types: list, str
    :param exclude_file_types: scan all file types, except those provided in this list.
        Can't be used together with include_file_types param.

    :type scan_subfolders: bool
    :param scan_subfolders: Includes subfolders on scan. Default is False

    :type scan_archives: bool
    :param scan_archives: Includes archives on scan. Default is False

    :type primary_action: str
    :param primary_action: one of the following values: delete, clean, continue

    :param secondary_action: str
    :param primary_action: one of the following values: delete, continue

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :param kwargs:
    :return:
    """

    path = '/api/antivirus/update_ods_defaults.json'
    file_types_to_scan = 'all'

    if include_file_types is not None and exclude_file_types is not None:
        raise ValueError("Include_file_types and exclude_file_types can't be used together")

    if include_file_types is not None:
        file_types_to_scan = 'onlyspecified'
        if type(include_file_types) is list:
            include_file_types = ','.join(list)

    if type(exclude_file_types) is list:
        exclude_file_types = ','.join(list)

    __validate_primary_action(primary_action)
    __validate_secondary_action(secondary_action)

    body_values = {'runpolicy': run_policy, 'filetypestoscan': file_types_to_scan,
                   'includefiletypes': include_file_types, 'excludefiletypes':exclude_file_types,
                   'scansubfolders': scan_subfolders, 'scanarchives': scan_archives,
                   'primaryaction': primary_action, 'secondaryaction': secondary_action}

    return session.post_api(path=path, body=body_values,  return_type=return_type, **kwargs)


def show_quarantined_files(session, return_type=None, **kwargs):
    """
    Shows quarantined files

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    """

    path = '/api/antivirus/quarantined_files.json'
    return session.get_api(path=path, return_type=return_type, **kwargs)


def restore_quarantined_file(session, file_id, return_type=None, **kwargs):
    """
    Restores a quarantined file

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type file_id: str
    :param file_id: File to be deleted

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :param kwargs:
    :return:
    """

    path = "/api/antivirus/restore_file/%s" % file_id
    return session.post_api(path=path, return_type=return_type, **kwargs)


def delete_quarantined_file(session, file_id, return_type=None, **kwargs):
    """
    Deletes a quarantined file

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type file_id: str
    :param file_id: File to be deleted

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :param kwargs:
    :return:
    """

    path = "/api/antivirus/delete_file/%s" % file_id
    return session.post_api(path=path, return_type=return_type, **kwargs)


def download_volume_log(session, volume_id, return_type='raw', **kwargs):
    """
    Downloads antivirus log

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: Volume ID. Required.

    :type return_type: str
    :param return_type: This returns a raw binary stream.
        Output should be redirected to a file with a .zip extension.

    :rtype: str
    :returns: Raw zip file data.
    """
    path = '/api/antivirus/log_files/%s' % volume_id

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_vpsa_time(session, **kwargs):
    """
    Get a json which contain the timezone of the VPSA

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :rtype: str
    :returns: Raw zip file data.
    """
    path = '/api/accounts/checklogin.json'

    return session.post_api(path=path, **kwargs)


def __validate_primary_action(primary_action):
    if primary_action is not None and primary_action not in ['delete', 'clean', 'continue']:
        raise ValueError("Invalid value for primary_action. Valid values are: delete, clean and continue")


def __validate_secondary_action(secondary_action):
    if secondary_action is not None and secondary_action not in ['delete', 'continue']:
        raise ValueError("Invalid value for secondary_action. Valid values are: delete and continue")
