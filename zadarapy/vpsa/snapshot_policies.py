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
from zadarapy.validators import is_valid_policy_creation
from zadarapy.validators import is_valid_policy_id


def get_all_snapshot_policies(session, start=None, limit=None,
                              return_type=None):
    """
    Retrieves details for all snapshot policies configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying snapshot policies from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of snapshot policies to return.
        Optional.

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
    path = '/api/snapshot_policies.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_snapshot_policy(session, policy_id, return_type=None):
    """
    Retrieves details for a single snapshot policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    method = 'GET'
    path = '/api/snapshot_policies/{0}.json'.format(policy_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_snapshot_policy(session, display_name, create_policy,
                           local_delete_policy, remote_delete_policy,
                           allow_empty='NO', return_type=None):
    """
    Creates a new snapshot policy.  Can be used in conjunction with local
    volume snapshots, remote mirror jobs, and/or remote object storage backup
    jobs.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the snapshot policy.  For
        example: 'Daily Snapshots at 3 AM'.  May not contain a single quote
        (') character.  Required.

    :type create_policy: str
    :param create_policy: The frequency to take snapshots.  This is defined in
        UNIX cron style format.  For example: '0 3 * * *' would take a
        snapshot at 3 AM every day.  Alternatively, if "manual" is specified,
        an "On Demand" snapshot policy will be created.  Required.

    :type local_delete_policy: int
    :param local_delete_policy: The number of snapshots to retain on the local
        VPSA before removing.  For example, if 10 is specified, when the
        11th snapshot is created, the oldest snapshot will be deleted.
        Required.

    :type remote_delete_policy: int
    :param remote_delete_policy: The number of snapshots to retain on the
        remote VPSA or object storage destination before removing.  For
        example, if 10 is specified, when the 11th snapshot is created, the
        oldest snapshot will be deleted.  Required.

    :type allow_empty: str
    :param allow_empty: If set to 'YES', snapshots will be taken even when no
        data has been changed on the volume (creates empty snapshots).  If set
        to 'NO', snapshots will only be created if data has changed.  Optional
        (will be set to 'NO' by default).

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
        raise ValueError('{0} is not a valid snapshot policy name.'
                         .format(display_name))

    body_values['name'] = display_name

    if not is_valid_policy_creation(create_policy):
        raise ValueError('"{0}" is not a valid snapshot policy creation '
                         'frequency.'.format(create_policy))

    body_values['create_policy'] = create_policy

    if local_delete_policy < 0:
        raise ValueError('The local_delete_policy parameter must not be '
                         'negative ("{0}" was passed).'
                         .format(local_delete_policy))

    body_values['delete_policy'] = 'N' + str(local_delete_policy)

    if remote_delete_policy < 0:
        raise ValueError('The remote_delete_policy parameter must not be '
                         'negative ("{0}" was passed).'
                         .format(remote_delete_policy))

    body_values['destination_policy'] = 'N' + str(remote_delete_policy)

    allow_empty = allow_empty.upper()

    if allow_empty not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid allow_empty parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(allow_empty))

    body_values['empty'] = allow_empty

    method = 'POST'
    path = '/api/snapshot_policies.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_snapshot_policy(session, policy_id, create_policy=None,
                           local_delete_policy=None,
                           remote_delete_policy=None, allow_empty=None,
                           return_type=None):
    """
    Change various settings related to a snapshot policy.  These changes will
    be propagated to any local volume, remote mirror job, or remote object
    storage backup job that uses this policy.  Parameters set to 'None' will
    not have their existing values changed.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type create_policy: str
    :param create_policy: See documentation for create_snapshot_policy.
        Optional.

    :type local_delete_policy: int
    :param local_delete_policy: See documentation for create_snapshot_policy.
        Optional.

    :type remote_delete_policy: int
    :param remote_delete_policy: See documentation for create_snapshot_policy.
        Optional.

    :type allow_empty: str
    :param allow_empty: See documentation for create_snapshot_policy.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values = {}

    if create_policy is not None:
        if not is_valid_policy_creation(create_policy):
            raise ValueError('"{0}" is not a valid snapshot policy creation '
                             'frequency.'.format(create_policy))

        body_values['create_policy'] = create_policy

    if local_delete_policy is not None:
        if local_delete_policy < 0:
            raise ValueError('The local_delete_policy parameter must not be '
                             'negative ("{0}" was passed).'
                             .format(local_delete_policy))

        body_values['delete_policy'] = 'N' + str(local_delete_policy)

    if remote_delete_policy is not None:
        if remote_delete_policy < 0:
            raise ValueError('The remote_delete_policy parameter must not be '
                             'negative ("{0}" was passed).'
                             .format(remote_delete_policy))

        body_values['destination_policy'] = 'N' + str(remote_delete_policy)

    if allow_empty is not None:
        allow_empty = allow_empty.upper()
        
        if allow_empty not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid allow_empty parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(allow_empty))

        body_values['empty'] = allow_empty

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"display_name", "create_policy", '
                         '"local_delete_policy", "remote_delete_policy", '
                         '"allow_empty"')
    method = 'PUT'
    path = '/api/snapshot_policies/{0}.json'.format(policy_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_snapshot_policy(session, policy_id, return_type=None):
    """
    Deletes a snapshot policy.  The policy must not be in use by any local
    volumes, remote mirror jobs, or remote object storage backup jobs.  This
    action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    method = 'DELETE'
    path = '/api/snapshot_policies/{0}.json'.format(policy_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def rename_snapshot_policy(session, policy_id, display_name,
                           return_type=None):
    """
    Sets the "display_name" snapshot policy parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the snapshot policy.  For
        example: 'Daily Snapshots at 3 AM'.  May not contain a single quote
        (') character.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid snapshot policy name.'
                         .format(display_name))

    body_values['new_name'] = display_name

    method = 'POST'
    path = '/api/snapshot_policies/{0}/rename.json'.format(policy_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)
