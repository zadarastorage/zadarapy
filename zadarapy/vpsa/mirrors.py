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


from zadarapy.validators import verify_snapshot_id, verify_boolean, \
    verify_field, verify_start_limit, verify_cg_id, verify_policy_id, \
    verify_volume_id, verify_snaprule_id, verify_remote_vpsa_id, \
    verify_mirror_id


def get_all_mirrors(session, start=None, limit=None, return_type=None,
                    **kwargs):
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
    parameters = verify_start_limit(start, limit)

    path = '/api/mirror_jobs.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_mirror(session, mirror_id, return_type=None, **kwargs):
    """
    Retrieves details for the specified mirror job configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        create_volume_mirror.  For example: 'srcjvpsa-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_mirror_id(mirror_id)

    path = '/api/mirror_jobs/{0}.json'.format(mirror_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def pause_mirror(session, mirror_id, return_type=None, **kwargs):
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
    verify_mirror_id(mirror_id)

    path = '/api/mirror_jobs/{0}/pause.json'.format(mirror_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def resume_paused_mirror(session, mirror_id, return_type=None, **kwargs):
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
    verify_mirror_id(mirror_id)

    path = '/api/mirror_jobs/{0}/continue.json'.format(mirror_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def break_mirror(session, mirror_id, return_type=None, **kwargs):
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
    verify_mirror_id(mirror_id)

    path = '/api/mirror_jobs/{0}/break.json'.format(mirror_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def get_all_remote_vpsas(session, start=None, limit=None, return_type=None,
                         **kwargs):
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
    parameters = verify_start_limit(start, limit)

    path = '/api/remote_vpsas.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_remote_vpsa(session, rvpsa_id, return_type=None, **kwargs):
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
    verify_remote_vpsa_id(rvpsa_id)

    path = '/api/remote_vpsas/{0}.json'.format(rvpsa_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def discover_remote_vpsa(session, ip_address, username, password, public,
                         return_type=None, **kwargs):
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
    username = verify_field(username, "VPSA username")
    password = verify_field(password, "VPSA password")
    public = verify_boolean(public, "public")

    body_values = {'user': username, 'password': password, 'ip': ip_address,
                   'isPublic': public}

    path = '/api/remote_vpsas/discover.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, skip_status_check_range=True, **kwargs)


def refresh_remote_vpsa(session, rvpsa_id, return_type=None, **kwargs):
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
    verify_remote_vpsa_id(rvpsa_id)

    path = '/api/remote_vpsas/{0}/refresh.json'.format(rvpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def remove_remote_vpsa(session, rvpsa_id, return_type=None, **kwargs):
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
    verify_remote_vpsa_id(rvpsa_id)

    path = '/api/remote_vpsas/{0}.json'.format(rvpsa_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_remote_vpsa_pools(session, rvpsa_id, start=None, limit=None,
                          return_type=None, **kwargs):
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
    verify_remote_vpsa_id(rvpsa_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/remote_vpsas/{0}/pools.json'.format(rvpsa_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_suggested_mirrors(session, rvpsa_id, cg_id, start=None, limit=None,
                          return_type=None, **kwargs):
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
    verify_remote_vpsa_id(rvpsa_id)
    verify_cg_id(cg_id)

    parameters = verify_start_limit(start, limit,
                                    list_options=[('cgname', cg_id)])
    path = '/api/remote_vpsas/{0}/suggested_jobs.json'.format(rvpsa_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def resume_broken_mirror(session, rvpsa_id, display_name, policy_id,
                         local_snapshot_id, remote_snapshot_id,
                         wan_optimization='YES', compress=None, dedupe=None,
                         force='NO', return_type=None, **kwargs):
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

    :type compress: str
    :param compress: "YES" for compress. "NO" for not


    :type dedupe: str
    :param dedupe: "YES" for dedupe. "NO" for not


    :type force: str
    :param force: "YES" for force command. "NO" for not

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_remote_vpsa_id(rvpsa_id)
    display_name = verify_field(display_name, "display_name")
    verify_policy_id(policy_id)
    verify_snapshot_id(local_snapshot_id)
    verify_snapshot_id(remote_snapshot_id)
    wan_optimization = verify_boolean(wan_optimization, "wan_optimization")

    body_values = {"displayname": display_name, "policy": policy_id,
                   "snapname": local_snapshot_id,
                   "remote_snapname": remote_snapshot_id,
                   "wanoptimization": wan_optimization, "force": force}

    if compress is not None:
        compress = verify_boolean(compress, "compress")
        body_values["compress"] = compress
    if dedupe is not None:
        dedupe = verify_boolean(dedupe, "dedupe")
        body_values["dedupe"] = dedupe

    path = '/api/remote_vpsas/{0}/resume_mirror_job.json'.format(rvpsa_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def add_mirror_snapshot_policy(session, mirror_id, policy_id,
                               return_type=None, **kwargs):
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
    verify_mirror_id(mirror_id)
    verify_policy_id(policy_id)

    body_values = {'policyname': policy_id}

    path = '/api/mirror_jobs/{0}/attach_snapshot_policy.json'.format(mirror_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def remove_mirror_snapshot_policy(session, mirror_id, policy_id,
                                  delete_snapshots, return_type=None,
                                  **kwargs):
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
    verify_mirror_id(mirror_id)
    verify_policy_id(policy_id)
    delete_snapshots = verify_boolean(delete_snapshots, "delete_snapshots")

    body_values = {'policyname': policy_id,
                   'delete_snapshots': delete_snapshots}

    path = '/api/mirror_jobs/{0}/detach_snapshot_policy.json'.format(mirror_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_mirror_wan_optimization(session, mirror_id, wan_optimization,
                                   return_type=None, **kwargs):
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
    verify_mirror_id(mirror_id)
    wan_optimization = verify_boolean(wan_optimization, "wan_optimization")

    path = '/api/mirror_jobs/{0}/set_wan_optimization.json'.format(mirror_id)

    body_values = {'wan_optimization': wan_optimization}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_snapshots(session, mirror_id, return_type=None, **kwargs):
    """
    Get all snapshots from mirror job

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
    verify_mirror_id(mirror_id)

    path = '/api/mirror_jobs/{0}/snapshots.json'.format(mirror_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def clone_mirror_job(session, mirror_id, snapshot_id, clone_name,
                     return_type=None, **kwargs):
    """
    Clone a mirror job's snapshot into a volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

    :type snapshot_id: str
    :param snapshot_id: A snapshot's id.  Required.

    :type clone_name: str
    :param clone_name: The new cloned volume name.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_mirror_id(mirror_id)
    verify_snapshot_id(snapshot_id)

    body_values = {"snapshot": snapshot_id, 'clone_name': clone_name}

    path = '/api/mirror_jobs/{0}/clone_snapshot.json'.format(mirror_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def detach_snapshot_policy(session, policy_id, mirror_id, snap_rule_id,
                           delete_snapshots="YES", return_type=None, **kwargs):
    """
    Detach a Snapshot Policy from a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type mirror_id: str
    :param mirror_id: The mirror job 'job_name' value as returned by
        get_all_mirrors.  For example: 'srcjvpsa-00000001'.  Required.

    :type snap_rule_id: str
    :param snap_rule_id: A snap rule ID.
    (found in /consistency_groups/{volume_cg_id}/snapshot_policies API).
    For example: 'snaprule-00000001'.  Required.

    :type delete_snapshots: str
    :param delete_snapshots: "YES" iff delete snapshots after detach.
    "NO" otherwise

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_policy_id(policy_id)
    verify_volume_id(mirror_id)
    verify_snaprule_id(snap_rule_id)

    path = "/api/mirror_jobs/{0}/detach_snapshot_policy.json".format(mirror_id)
    body_values = {"id": mirror_id, "snaprule": snap_rule_id,
                   "delete_snapshots": delete_snapshots}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_remote_vpsa_rate_limit(session, remote_vpsa_id, limit,
                                  return_type=None, **kwargs):
    """
    Detach a Snapshot Policy from a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type remote_vpsa_id: str
    :param remote_vpsa_id: Remote VPSA ID

    :type limit: int
    :param limit: New rate limit to set in kb/s

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/remote_vpsas/{0}/rate_limit.json".format(remote_vpsa_id)
    body_values = {"limit": limit}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_mirror_rate_limit(session, remote_vpsa_id, limit, return_type=None,
                             **kwargs):
    """
    Update Mirror rate limit

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type remote_vpsa_id: str
    :param remote_vpsa_id: Remote VPSA ID

    :type limit: int
    :param limit: New rate limit to set in kb/s

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/mirror_jobs/{0}/rate_limit.json".format(remote_vpsa_id)
    body_values = {"limit": limit}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_suggested_mirror_jobs(session, remote_vpsa_id, cg_id,
                              return_type=None, **kwargs):
    """
    Get suggested mirror jobs

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type remote_vpsa_id: str
    :param remote_vpsa_id: Remote VPSA ID.  Required.

    :type cg_id: int
    :param cg_id: Volume CG ID.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/remote_vpsas/{0}/suggested_jobs.json".format(remote_vpsa_id)
    body_values = {"cgname": cg_id}

    return session.get_api(path=path, body=body_values,
                           return_type=return_type, **kwargs)
