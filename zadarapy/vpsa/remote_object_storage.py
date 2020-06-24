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
    verify_field, verify_start_limit, verify_policy_id, \
    verify_ros_backup_job_id, verify_volume_id, verify_pool_id, \
    verify_interval, verify_port, verify_ros_destination_id, \
    verify_ros_restore_job_id, verify_restore_mode, verify_restore_job_mode


def get_all_ros_destinations(session, start=None, limit=None,
                             return_type=None, **kwargs):
    """
    Retrieves details for all remote object storage destinations configured on
    the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying remote object storage
        destinations from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote object storage destinations to
        return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)

    path = '/api/object_storage_destinations.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_ros_destination(session, ros_destination_id, return_type=None,
                        **kwargs):
    """
    Retrieves details for a single remote object storage destination.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations.  For example:
        'obsdst-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_destination_id(ros_destination_id)

    path = '/api/object_storage_destinations/{0}.json' \
        .format(ros_destination_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_ros_destination(session, display_name, bucket, endpoint, username,
                           password, public, use_proxy, ros_type,
                           allow_lifecycle_policies=None, proxy_host=None,
                           proxy_port=None, proxy_username=None,
                           proxy_password=None, return_type=None, **kwargs):
    """
    Creates a remote object storage destination.  The VPSA can either connect
    directly to the object storage endpoint, or through an HTTP/HTTPS proxy
    server.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the remote object storage
        destination.  For example: 'zadarabackup-bucket in AWS East'.  May not
        contain a single quote (') character.  Required.

    :type bucket: str
    :param bucket: The globally unique destination bucket identifier.  For
        example: 'zadarabackup-bucket'.  May not contain a single quote (')
        character.  Required.

    :type endpoint: str
    :param endpoint: The hostname for the object storage endpoint.  For
        example, for S3 US East: 's3.amazonaws.com'.  Required.

    :type username: str
    :param username: The username or access key ID for the object storage
        endpoint.  Required.

    :type password: str
    :param password: The password or secret access key for the object storage
        endpoint.  Required.

    :type public: str
    :param public: If set to 'YES', establishing the remote object storage
        destination and all future remote object storage jobs occur over the
        VPSA's public IP/interface (The VPSA must have a valid public IP and
        setup).  If 'NO', the relationship and remote object storage jobs will
        occur using the same IP as connecting to the storage - in this case
        the VPSA must be able to route to the remote object storage
        destination in question via the VPSA's defined default gateway.
        Required.

    :type allow_lifecycle_policies: str
    :param allow_lifecycle_policies: If set to 'YES', the VPSA will allow
    bucket to have lifecycle policies. (Valid Only for AWS)

    :type use_proxy: str
    :param use_proxy: If set to 'YES', the VPSA will connect via an HTTP/HTTPS
        proxy when addressing the object storage destination.  If 'NO', a
        direct connection will be used.  Required.

    :type proxy_host: str
    :param proxy_host: When use_proxy is set to 'YES', this defines the DNS
        hostname or IP of the HTTP/HTTPS proxy server to use.  Optional.

    :type proxy_port: str
    :param proxy_port: When use_proxy is set to 'YES', this defines the port
        number of the HTTP/HTTPS proxy server to use.  Optional.

    :type proxy_username: str
    :param proxy_username: When use_proxy is set to 'YES', this defines the
        proxy server username if proxy authentication is required.  Optional.

    :type proxy_password: str
    :param proxy_username: When use_proxy is set to 'YES', this defines the
        proxy server password if proxy authentication is required.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    display_name = verify_field(display_name, "display_name")
    bucket = verify_field(bucket, "bucket")
    username = verify_field(username, "username")
    password = verify_field(password, "password")
    public = verify_boolean(public, "public")
    use_proxy = verify_boolean(use_proxy, "use_proxy")
    allow_lifecycle_policies = verify_boolean(allow_lifecycle_policies,
                                              "allow_lifecycle_policies")

    body_values = {'name': display_name, 'bucket': bucket,
                   'endpoint': endpoint, 'username': username,
                   'type': ros_type, 'password': password,
                   'connectVia': 'public' if public == 'YES' else 'fe',
                   'allow_lifecycle_policies': allow_lifecycle_policies}

    if use_proxy == 'YES':
        body_values['proxyhost'] = proxy_host
        body_values['proxyport'] = verify_port(proxy_port)

        if proxy_username is not None:
            body_values['proxyuser'] = verify_field(proxy_username,
                                                    "proxy_username")

        if proxy_password is not None:
            body_values['proxypassword'] = verify_field(proxy_password,
                                                        "proxy_password")

    path = '/api/object_storage_destinations.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_ros_destination(session, ros_destination_id, bucket=None,
                           endpoint=None, username=None, password=None,
                           public=None, use_proxy=None, proxy_host=None,
                           proxy_port=None, proxy_username=None,
                           proxy_password=None, return_type=None, **kwargs):
    """
    Updates options for an existing remote object storage destination.
    Parameters set to 'None' will not have their existing values changed.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations.  For example:
        'obsdst-00000001'.  Required.

    :type bucket: str
    :param bucket: See documentation for create_ros_destination.  Optional.

    :type endpoint: str
    :param endpoint: See documentation for create_ros_destination.  Optional.

    :type username: str
    :param username: See documentation for create_ros_destination.  Optional.

    :type password: str
    :param password: See documentation for create_ros_destination.  Optional.

    :type public: str
    :param public: See documentation for create_ros_destination.  Optional.

    :type use_proxy: str
    :param use_proxy: See documentation for create_ros_destination.  Optional.

    :type proxy_host: str
    :param proxy_host: See documentation for create_ros_destination.
        Optional.

    :type proxy_port: str
    :param proxy_port: See documentation for create_ros_destination.
        Optional.

    :type proxy_username: str
    :param proxy_username: See documentation for create_ros_destination.
        Optional.

    :type proxy_password: str
    :param proxy_username: See documentation for create_ros_destination.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_destination_id(ros_destination_id)

    body_values = {}

    if bucket is not None:
        body_values['bucket'] = verify_field(bucket, "bucket")

    if endpoint is not None:
        body_values['endpoint'] = endpoint

    if username is not None:
        body_values['username'] = verify_field(username, "username")

    if password is not None:
        body_values['password'] = verify_field(password, "password")

    if public is not None:
        public = verify_boolean(public, "public")
        body_values['connectVia'] = 'public' if public == 'YES' else 'fe'

    if use_proxy is not None:
        use_proxy = verify_boolean(use_proxy, "use_proxy")
        body_values['use_proxy'] = str(use_proxy == 'YES').lower()

    if proxy_host is not None or use_proxy == 'YES':
        body_values['proxyhost'] = proxy_host

    if proxy_port is not None or use_proxy == 'YES':
        body_values['proxyport'] = verify_port(proxy_port)

    if proxy_username is not None:
        body_values['proxyuser'] = verify_field(proxy_username,
                                                "proxy_username")

    if proxy_password is not None:
        body_values['proxypassword'] = verify_field(proxy_password,
                                                    "proxy_password")

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"bucket", "endpoint", "username", "password", '
                         '"public", "use_proxy", "proxy_host", "proxy_port", '
                         '"proxy_username", "proxy_password"')

    path = '/api/object_storage_destinations/{0}.json' \
        .format(ros_destination_id)

    return session.put_api(path=path, body=body_values,
                           return_type=return_type, **kwargs)


def remove_ros_destination(session, ros_destination_id, return_type=None,
                           **kwargs):
    """
    Removes a remote object storage destination.  There must not be any remote
    object storage backup jobs associated with this destination.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations.  For example:
        'obsdst-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_destination_id(ros_destination_id)

    path = '/api/object_storage_destinations/{0}.json' \
        .format(ros_destination_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_all_ros_destination_backup_jobs(session, ros_destination_id,
                                        start=None, limit=None,
                                        return_type=None, **kwargs):
    """
    Retrieves details for all remote object storage backup jobs for the
    specified remote object storage destination.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations.  For example:
        'obsdst-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying remote object storage
        backup jobs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote object storage backup jobs to
        return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_destination_id(ros_destination_id)

    path = '/api/object_storage_destinations/{0}/backup_jobs.json' \
        .format(ros_destination_id)

    parameters = verify_start_limit(start, limit)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_all_ros_destination_restore_jobs(session, ros_destination_id,
                                         start=None, limit=None,
                                         return_type=None, **kwargs):
    """
    Retrieves details for all remote object storage restore jobs for the
    specified remote object storage destination.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations.  For example:
        'obsdst-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying remote object storage
        restore jobs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote object storage restore jobs to
        return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/object_storage_destinations/{0}/restore_jobs.json' \
        .format(ros_destination_id)

    parameters = verify_start_limit(start, limit)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_all_ros_backup_jobs(session, start=None, limit=None,
                            return_type=None, **kwargs):
    """
    Retrieves details for all remote object storage backup jobs configured on
    the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying remote object storage
        backup jobs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote object storage backup jobs to
        return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/object_storage_backup_jobs.json'

    parameters = verify_start_limit(start, limit)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_ros_backup_job(session, ros_backup_job_id, return_type=None, **kwargs):
    """
    Retrieves details a single remote object storage backup job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_backup_job_id(ros_backup_job_id)

    path = '/api/object_storage_backup_jobs/{0}.json' \
        .format(ros_backup_job_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_ros_backup_job(session, display_name, ros_destination_id, sse,
                          volume_id, policy_id, compression='YES',
                          return_type=None, **kwargs):
    """
    Creates a new remote object storage backup job.  Backups are based on
    snapshots taken by the specified snapshot policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the remote object storage
        backup job.  For example: 'Daily S3 Backup'.  May not contain a single
        quote (') character.  Required.

    :type sse: str
    :param sse: The remote object storage destination SSE:
     'NO', 'AES256', 'KMS', 'KMSKEYID  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations.  For example:
        'obsdst-00000001'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes
        for the volume to be backed up.  For example: 'volume-00000001'.
        Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  This
        policy will determine the frequency and retention of backups for this
        job.  Required.

    :type compression: str
    :param compression: If set to 'YES', backup data will be compressed in
        flight.  If 'NO', backup data will not be compressed.  Set to 'YES' by
        default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    display_name = verify_field(display_name, "display_name")
    verify_ros_destination_id(ros_destination_id)
    verify_volume_id(volume_id)
    verify_policy_id(policy_id)

    body_values = {'name': display_name, 'destination': ros_destination_id,
                   'volume': volume_id, 'policy': policy_id,
                   'sse': sse,
                   'compression': verify_boolean(compression, "compression")}

    path = '/api/object_storage_backup_jobs.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def pause_ros_backup_job(session, ros_backup_job_id, return_type=None,
                         **kwargs):
    """
    Pauses a remote object storage backup job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_destination_id(ros_backup_job_id)

    path = '/api/object_storage_backup_jobs/{0}/pause.json' \
        .format(ros_backup_job_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def resume_ros_backup_job(session, ros_backup_job_id, return_type=None,
                          **kwargs):
    """
    Resumes a paused remote object storage backup job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_backup_job_id(ros_backup_job_id)

    path = '/api/object_storage_backup_jobs/{0}/continue.json' \
        .format(ros_backup_job_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def break_ros_backup_job(session, ros_backup_job_id, purge_data,
                         delete_snapshots, return_type=None, **kwargs):
    """
    Breaks a remote object storage backup job.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type purge_data: str
    :param purge_data: If set to 'YES', all data related to this backup job
        will be deleted on the remote object storage destination endpoint.  If
        'NO', the data will remain on the endpoint.  Required.

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
    verify_ros_backup_job_id(ros_backup_job_id)

    body_values = {'purge_data': verify_boolean(purge_data, "purge_data"),
                   "delete_snapshots": verify_boolean(delete_snapshots,
                                                      "delete_snapshots")}

    path = '/api/object_storage_backup_jobs/{0}/break.json' \
        .format(ros_backup_job_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_ros_backup_job_compression(session, ros_backup_job_id, compression,
                                      return_type=None, **kwargs):
    """
    Updates the compression setting for a remote object storage backup job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type compression: str
    :param compression: If set to 'YES', backup data will be compressed in
        flight.  If 'NO', backup data will not be compressed.  Set to 'YES' by
        default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_backup_job_id(ros_backup_job_id)

    body_values = {'compression': verify_boolean(compression, 'compression')}

    path = '/api/object_storage_backup_jobs/{0}/compression.json' \
        .format(ros_backup_job_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def replace_ros_backup_job_snapshot_policy(session, ros_backup_job_id,
                                           policy_id, return_type=None,
                                           **kwargs):
    """
    Replaces the existing snapshot policy used for a remote object storage
    backup job with the specified policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  This
        policy will determine the frequency and retention of backups for this
        job.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_backup_job_id(ros_backup_job_id)
    verify_policy_id(policy_id)

    body_values = {'policyname': policy_id}

    path = '/api/object_storage_backup_jobs/{0}/replace_snapshot_policy.json' \
        .format(ros_backup_job_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_all_ros_restore_jobs(session, start=None, limit=None,
                             return_type=None, **kwargs):
    """
    Retrieves details for all remote object storage restore jobs running on
    the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying remote object storage
        restore jobs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote object storage restore jobs to
        return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)

    path = '/api/object_storage_restore_jobs.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_ros_restore_job(session, ros_restore_job_id, return_type=None,
                        **kwargs):
    """
    Retrieves details a single remote object storage restore job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job 'name'
        value as returned by get_all_ros_restore_jobs.  For example:
        'rstjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_restore_job_id(ros_restore_job_id)

    path = '/api/object_storage_restore_jobs/{0}.json' \
        .format(ros_restore_job_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_ros_restore_job(session, display_name, ros_destination_id, pool_id,
                           restore_mode, volume_name, local_snapshot_id,
                           object_store_key, crypt, dedupe='NO', compress='NO',
                           return_type=None, **kwargs):
    """
    Creates a new remote object storage backup job.  Backups are based on
    snapshots taken by the specified snapshot policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the remote object storage
        restore job.  For example: 'PDF archive restore'.  May not contain a
        single quote (') character.  Required.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination 'name'
        value as returned by get_all_ros_destinations for the destination
        where the snapshot is stored.  For example: 'obsdst-00000001'.
        Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools where
        the snapshot will be restored.  For example: 'pool-00000001'.  The
        volume will be created on this pool.  Required.

    :type restore_mode: str
    :param restore_mode: This parameter expects one of three values:
        'restore', 'clone', or 'import_seed'.  When set to 'restore', the
        volume can be immediately attached to servers; data is retrieved from
        object storage on demand and in a background process; and all data
        will eventually be restored.  When set to 'clone', the volume can be
        immediately attached to servers; and starting with zero capacity, data
        is retrieved from object storage only on-demand when accessed by the
        attached servers.  When set to 'import_seed', a full capacity clone is
        created, including snapshot time-stamping; The volume can be attached
        to servers only after the volume's data was fully retrieved from
        object storage; use this mode to import initial data seed for remote
        mirroring.  Required.

    :type volume_name: str
    :param volume_name: A text label to assign to the restored volume.  For
        example: 'pdf-files'.  May not contain a single quote (') character.
        Required.

    :type local_snapshot_id: str
    :param local_snapshot_id: Either this or object_store_key is required.
        If using local_snapshot_id, the desired snapshot 'name' is passed as
        returned by get_all_snapshots (with the ros_backup_job_id specified).
        For example: 'snap-00000001'.  Optional.

    :type object_store_key: str
    :param object_store_key: Either this or local_snapshot_id is required.  If
        using object_store_key, this is the full object storage key for the
        "path" to the individual snapshot to be restored.  For example:
        "cloud1.C97E9A00ADE7489BB08A9AB3B0B6484F/myvpsa.vsa-00000169/
        myvol.volume-00000011/2015-07-01T09:26:01+0000_snap-0000003e/".  This
        is useful when there is no local_snapshot_id to reference; for
        example, if the snapshot is being restored to a different VPSA than
        the original source.  Optional.

    :type crypt: str
    :param crypt: If set to 'YES', the resulting volume of the restoration
        will be encrypted with the VPSA's encryption key.  If 'NO', the
        resulting volume will not be encrypted.  Required.

    :type dedupe: str
    :param dedupe: If set to 'YES', deduplication will be enabled on the
        volume.  If 'NO', it won't.  Optional.

    :type compress: str
    :param compress: If set to 'YES', compression will be enabled on the
        volume.  If 'NO', it won't.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_destination_id(ros_destination_id)
    verify_pool_id(pool_id)
    verify_restore_mode(restore_mode)

    body_values = {'name': verify_field(display_name, "display_name"),
                   'remote_object_store': ros_destination_id,
                   'poolname': pool_id, 'mode': restore_mode,
                   'volname': verify_field(volume_name, "volume"),
                   'crypt': verify_boolean(crypt, "crypt")}

    if local_snapshot_id is None and object_store_key is None:
        raise ValueError('Either "local_snapshot_id" or "object_store_key" '
                         'needs to be passed as a parameter.')

    if local_snapshot_id is not None:
        verify_snapshot_id(local_snapshot_id)
        body_values['local_snapname'] = local_snapshot_id

    if object_store_key is not None:
        body_values['key'] = verify_field(object_store_key, "object_store_key")

    if dedupe is not None:
        body_values["dedupe"] = verify_boolean(dedupe, 'dedupe')

    if compress is not None:
        body_values["compress"] = verify_boolean(compress, 'compress')

    path = '/api/object_storage_restore_jobs.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def pause_ros_restore_job(session, ros_restore_job_id, return_type=None,
                          **kwargs):
    """
    Pauses a remote object storage restore job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job 'name'
        value as returned by get_all_ros_restore_jobs.  For example:
        'rstjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_restore_job_id(ros_restore_job_id)

    path = '/api/object_storage_restore_jobs/{0}/pause.json' \
        .format(ros_restore_job_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def resume_ros_restore_job(session, ros_restore_job_id, return_type=None,
                           **kwargs):
    """
    Resumes a paused remote object storage restore job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job 'name'
        value as returned by get_all_ros_restore_jobs.  For example:
        'rstjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_restore_job_id(ros_restore_job_id)

    path = '/api/object_storage_restore_jobs/{0}/continue.json' \
        .format(ros_restore_job_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def break_ros_restore_job(session, ros_restore_job_id, return_type=None,
                          **kwargs):
    """
    Breaks a remote object storage restore job.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job 'name'
        value as returned by get_all_ros_restore_jobs.  For example:
        'rstjobs-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_restore_job_id(ros_restore_job_id)

    path = '/api/object_storage_restore_jobs/{0}/break.json' \
        .format(ros_restore_job_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def change_ros_restore_job_mode(session, ros_restore_job_id, restore_mode,
                                return_type=None, **kwargs):
    """
    If the given remote object storage restore job is currently in "clone"
    mode, it can be changed to "restore" mode, or vice-versa.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job 'name'
        value as returned by get_all_ros_restore_jobs.  For example:
        'rstjobs-00000001'.  Required.

    :type restore_mode: str
    :param restore_mode: See documentation for create_ros_restore_job.  Only
        "clone" and "restore" are valid values.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_restore_job_id(ros_restore_job_id)
    verify_restore_job_mode(restore_mode)

    verify_restore_mode(restore_mode)
    body_values = {'mode': restore_mode}

    path = '/api/object_storage_restore_jobs/{0}/switch_mode.json' \
        .format(ros_restore_job_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_ros_backup_job_performance(session, ros_backup_job_id, interval=1,
                                   return_type=None, **kwargs):
    """
    Retrieves metering statistics for the remote object storage backup job for
    the specified interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

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
    verify_ros_backup_job_id(ros_backup_job_id)
    interval = verify_interval(interval)

    path = '/api/object_storage_backup_jobs/{0}/performance.json' \
        .format(ros_backup_job_id)

    parameters = {'interval': interval}

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_ros_restore_job_performance(session, ros_restore_job_id, interval=1,
                                    return_type=None, **kwargs):
    """
    Retrieves metering statistics for the remote object storage restore job
    for the specified interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job 'name'
        value as returned by get_all_ros_restore_jobs.  For example:
        'rstjobs-00000001'.  Required.

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
    verify_ros_restore_job_id(ros_restore_job_id)
    interval = verify_interval(interval)

    path = '/api/object_storage_restore_jobs/{0}/performance.json' \
        .format(ros_restore_job_id)

    parameters = {'interval': interval}

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def backup_jobs_rate_limit(session, ros_backup_job_id, limit,
                           return_type=None, **kwargs):
    """
    Retrieves metering statistics for the remote object storage restore job
    for the specified interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bckjobs-00000001'.  Required.

    :type limit: int
    :param limit: Limit rate

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/object_storage_backup_jobs/{0}/rate_limit.json".format(
        ros_backup_job_id)

    body_values = {"limit": limit}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def backup_jobs_update_compression(session, ros_backup_job_id, compression,
                                   return_type=None, **kwargs):
    """
    Retrieves metering statistics for the remote object storage restore job
    for the specified interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Required.

    :type compression: str
    :param compression: If set to 'YES', backup data will be compressed in
        flight.  If 'NO', backup data will not be compressed.  Set to 'YES' by
        default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    # POST /api/object_storage_backup_jobs/{id}/compression.json
    path = "/api/object_storage_backup_jobs/{0}/compression.json".format(
        ros_backup_job_id)
    body_values = {"compression": compression}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
