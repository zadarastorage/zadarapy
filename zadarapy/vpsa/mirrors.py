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
from zadarapy.validators import *


def get_all_mirrors(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all mirror jobs configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying mirror jobs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of mirror jobs to return.  Optional.

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
    path = '/api/mirror_jobs.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def pause_mirror(session, mirror_id, return_type=None):
    """
    Pauses a mirror job.  This should only be initiated from the source VPSA.
    e.g. the mirror job ID should start with "srcjvpsa-".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mirror_id(mirror_id):
        raise ValueError('{0} is not a valid mirror job ID.'
                         .format(mirror_id))

    method = 'POST'
    path = '/api/mirror_jobs/{0}/pause.json'.format(mirror_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def resume_paused_mirror(session, mirror_id, return_type=None):
    """
    Resumes a paused mirror job.  This should only be initiated from the
    source VPSA.  e.g. the mirror job ID should start with "srcjvpsa-".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mirror_id(mirror_id):
        raise ValueError('{0} is not a valid mirror job ID.'
                         .format(mirror_id))

    method = 'POST'
    path = '/api/mirror_jobs/{0}/continue.json'.format(mirror_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def break_mirror(session, mirror_id, return_type=None):
    """
    Breaks a mirror job.  This can be initiated from either the source or
    destination VPSA.  A broken mirror can be reconnected if all appropriate
    snapshots still exist on both systems to resume the relationship - this
    possibility can be ascertained by calling get_suggested_mirrors and
    issuing a resume_broken_mirror using the right information.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001' or
        'dstjvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mirror_id(mirror_id):
        raise ValueError('{0} is not a valid mirror job ID.'
                         .format(mirror_id))

    method = 'POST'
    path = '/api/mirror_jobs/{0}/break.json'.format(mirror_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_all_remote_vpsas(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all remote VPSAs with which this VPSA has a
    relationship.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying remote VPSAs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote VPSAs to return.  Optional.

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
    path = '/api/remote_vpsas.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_remote_vpsa(session, rvpsa_id, return_type=None):
    """
    Retrieves details for a single remote VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA 'name' value as returned by
        get_all_remote_vpsas.  For example: 'rvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_rvpsa_id(rvpsa_id):
        raise ValueError('{0} is not a valid remote VPSA ID.'
                         .format(rvpsa_id))

    method = 'GET'
    path = '/api/remote_vpsas/{0}.json'.format(rvpsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def discover_remote_vpsa(session, ip_address, username, password, public,
                         return_type=None):
    """
    Establishes a relationship with a remote VPSA for the purposes of
    mirroring volume snapshots.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ip_address: str
    :param ip_address: The IP address of the remote VPSA.  Required.

    :type username: str
    :param username: The login username for the administrative user of the
        remote VPSA (same as what's used to log into that VPSA's GUI).
        Required.

    :type password: str
    :param password: The login password for the administrative user of the
        remote VPSA (same as what's used to log into that VPSA's GUI).
        Required.

    :type public: str
    :param public: If set to 'YES', establishing the relationship and future
        mirror jobs will occur over the VPSA's public IP/interface (The VPSA
        must have a valid public IP and setup).  If 'NO', the relationship and
        mirror jobs will occur using the same IP as connecting to the storage
        - in this case the VPSA must be able to route to the remote VPSA in
        question via the VPSA's defined default gateway.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    body_values['ip'] = ip_address

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid VPSA username.'.format(username))

    body_values['user'] = username

    if not is_valid_field(password):
        raise ValueError('{0} is not a valid VPSA password.'.format(password))

    body_values['password'] = password

    public = public.upper()

    if public not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid public parameter.  '
                         'Allowed values are: "YES" or "NO"'.format(public))

    body_values['public'] = public

    method = 'POST'
    path = '/api/remote_vpsas/discover.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def refresh_remote_vpsa(session, rvpsa_id, return_type=None):
    """
    Refreshes information about a remote VPSA - such as discovering new pools
    and updating how much free space remote pools have.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA 'name' value as returned by
        get_all_remote_vpsas.  For example: 'rvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_rvpsa_id(rvpsa_id):
        raise ValueError('{0} is not a valid remote VPSA ID.'
                         .format(rvpsa_id))

    method = 'POST'
    path = '/api/remote_vpsas/{0}/refresh.json'.format(rvpsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def remove_remote_vpsa(session, rvpsa_id, return_type=None):
    """
    Removes a remote VPSA relationship.  There must be no active or paused
    mirror jobs with the specified remote VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA 'name' value as returned by
        get_all_remote_vpsas.  For example: 'rvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_rvpsa_id(rvpsa_id):
        raise ValueError('{0} is not a valid remote VPSA ID.'
                         .format(rvpsa_id))

    method = 'DELETE'
    path = '/api/remote_vpsas/{0}.json'.format(rvpsa_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_remote_vpsa_pools(session, rvpsa_id, start=None, limit=None,
                          return_type=None):
    """
    Retrieves details for all pools on the remote VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA 'name' value as returned by
        get_all_remote_vpsas.  For example: 'rvpsa-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying remote pools from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote pools to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_rvpsa_id(rvpsa_id):
        raise ValueError('{0} is not a valid remote VPSA ID.'
                         .format(rvpsa_id))

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
    path = '/api/remote_vpsas/{0}/pools.json'.format(rvpsa_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_suggested_mirrors(session, rvpsa_id, cg_id, start=None, limit=None,
                          return_type=None):
    """
    Retrieves a list of broken mirror jobs from the remote VPSA and validates
    if one can be re-used for the consistency group ID passed to this
    function.  Re-using a pre-existing mirror can save a lot of transfer time
    for large volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA 'name' value as returned by
        get_all_remote_vpsas.  For example: 'rvpsa-00000001'.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the volume to be mirrored.  For example:
        'cg-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying suggested mirrors from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of suggested mirrors to return.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_rvpsa_id(rvpsa_id):
        raise ValueError('{0} is not a valid remote VPSA ID.'
                         .format(rvpsa_id))

    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

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
    path = '/api/remote_vpsas/{0}/suggested_jobs.json'.format(rvpsa_id)

    parameters = {k: v for k, v in (('cgname', cg_id), ('start', start),
                                    ('limit', limit)) if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def resume_broken_mirror(session, rvpsa_id, display_name, policy_id,
                         local_snapshot_id, remote_snapshot_id,
                         wan_optimization='YES', return_type=None):
    """
    Resumes a previously broken mirror job between VPSAs.  Use in conjunction
    with get_suggested_mirrors to find candidates for resume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA 'name' value as returned by
        get_all_remote_vpsas.  For example: 'rvpsa-00000001'.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the mirror job.  For
        example: 'Daily Mirror to West Region'.  May not contain a single
        quote (') character.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type local_snapshot_id: str
    :param local_snapshot_id: The local snapshot to be used to resume the
        broken mirror.  This corresponds to the "src_snap_name" value returned
        by get_suggested_mirrors.  For example: 'snap-00000001'.  Required.

    :type remote_snapshot_id: str
    :param remote_snapshot_id: The remote snapshot to be used to resume the
        broken mirror.  This corresponds to the "dst_snap_name" value returned
        by get_suggested_mirrors.  For example: 'snap-00000001'.  Required.

    :type wan_optimization: str
    :param wan_optimization: If set to 'YES', the mirror will attempt to
        reduce the amount of data needing to be synchronized to the remote
        side at the expense of more load on the source VPSA.  If set to 'NO',
        more data will be sent by the mirror with less load on the source
        VPSA.  Set to 'YES' by default.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_rvpsa_id(rvpsa_id):
        raise ValueError('{0} is not a valid remote VPSA ID.'
                         .format(rvpsa_id))

    body_values = {}

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid remote mirror name.'
                         .format(display_name))

    body_values['displayname'] = display_name

    if not is_valid_policy_id(policy_id):
        raise ValueError('"{0}" is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values['policy'] = policy_id

    if not is_valid_snapshot_id(local_snapshot_id):
        raise ValueError('"{0}" is not a valid local snapshot ID.'
                         .format(local_snapshot_id))

    body_values['snapname'] = local_snapshot_id

    if not is_valid_snapshot_id(remote_snapshot_id):
        raise ValueError('"{0}" is not a valid remote snapshot ID.'
                         .format(remote_snapshot_id))

    body_values['remote_snapname'] = remote_snapshot_id

    wan_optimization = wan_optimization.upper()

    if wan_optimization not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid wan_optimization parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(wan_optimization))

    body_values['wan_optimization'] = wan_optimization

    method = 'POST'
    path = '/api/remote_vpsas/{0}/resume_mirror_job.json'.format(rvpsa_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def add_mirror_snapshot_policy(session, mirror_id, policy_id,
                               return_type=None):
    """
    Adds an additional snapshot policy to an existing mirror job.  This should
    only be initiated from the source VPSA.  e.g. the mirror job ID should
    start with "srcjvpsa-".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

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
    if not is_valid_mirror_id(mirror_id):
        raise ValueError('{0} is not a valid mirror job ID.'
                         .format(mirror_id))

    body_values = {}

    if not is_valid_policy_id(policy_id):
        raise ValueError('"{0}" is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values['policyname'] = policy_id

    method = 'POST'
    path = '/api/mirror_jobs/{0}/attach_snapshot_policy.json'\
           .format(mirror_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def remove_mirror_snapshot_policy(session, mirror_id, policy_id,
                                  delete_snapshots, return_type=None):
    """
    Removes a snapshot policy from an existing mirror job.  A mirror job must
    always have at least one snapshot policy attached.  This should only be
    initiated from the source VPSA.  e.g. the mirror job ID should start with
    "srcjvpsa-".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type delete_snapshots: str
    :param delete_snapshots: If set to 'YES', all snapshots created by the
        specified policy will be deleted.  If 'NO', they won't.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mirror_id(mirror_id):
        raise ValueError('{0} is not a valid mirror job ID.'
                         .format(mirror_id))

    body_values = {}

    if not is_valid_policy_id(policy_id):
        raise ValueError('"{0}" is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values['policyname'] = policy_id

    delete_snapshots = delete_snapshots.upper()

    if delete_snapshots not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid delete_snapshots parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(delete_snapshots))

    body_values['delete_snapshots'] = delete_snapshots

    method = 'POST'
    path = '/api/mirror_jobs/{0}/detach_snapshot_policy.json'\
           .format(mirror_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_mirror_wan_optimization(session, mirror_id, wan_optimization,
                                   return_type=None):
    """
    Change the WAN optimization setting for a mirror job.  This should only be
    initiated from the source VPSA.  e.g. the mirror job ID should start with
    "srcjvpsa-".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

    :type wan_optimization: str
    :param wan_optimization: If set to 'YES', the mirror will attempt to
        reduce the amount of data needing to be synchronized to the remote
        side at the expense of more load on the source VPSA.  If set to 'NO',
        more data will be sent by the mirror with less load on the source
        VPSA.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mirror_id(mirror_id):
        raise ValueError('{0} is not a valid mirror job ID.'
                         .format(mirror_id))

    body_values = {}

    wan_optimization = wan_optimization.upper()

    if wan_optimization not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid wan_optimization parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(wan_optimization))

    body_values['wan_optimization'] = wan_optimization

    method = 'POST'
    path = '/api/mirror_jobs/{0}/set_wan_optimization.json'.format(mirror_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)
