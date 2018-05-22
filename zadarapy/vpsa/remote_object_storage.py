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


def get_all_ros_destinations(session, start=None, limit=None,
                             return_type=None):
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
    path = '/api/object_storage_destinations.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_ros_destination(session, ros_destination_id, return_type=None):
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
    if not is_valid_ros_destination_id(ros_destination_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'destination ID.'.format(ros_destination_id))

    method = 'GET'
    path = '/api/object_storage_destinations/{0}.json'\
           .format(ros_destination_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_ros_destination(session, display_name, bucket, endpoint, username,
                           password, public, use_proxy, proxy_host=None,
                           proxy_port=None, proxy_username=None,
                           proxy_password=None, return_type=None):
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
    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid remote object store destination '
                         'name.'.format(display_name))

    body_values['name'] = display_name

    bucket = bucket.strip()

    if not is_valid_field(bucket):
        raise ValueError('{0} is not a valid remote object store bucket name.'
                         .format(bucket))

    body_values['bucket'] = bucket

    body_values['endpoint'] = endpoint

    if not is_valid_field(username):
        raise ValueError('{0} is not a valid object storage username.'
                         .format(username))

    body_values['username'] = username

    if not is_valid_field(password):
        raise ValueError('{0} is not a valid object storage password.'
                         .format(password))

    body_values['password'] = password

    public = public.upper()

    if public in ['YES', 'NO']:
        if public == 'YES':
            body_values['connectVia'] = 'public'
        else:
            body_values['connectVia'] = 'fe'
    else:
        raise ValueError('{0} is not a valid public parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(public))

    use_proxy = use_proxy.upper()

    if use_proxy in ['YES', 'NO']:
        if use_proxy == 'YES':
            body_values['use_proxy'] = 'true'
        else:
            body_values['use_proxy'] = 'false'
    else:
        raise ValueError('{0} is not a valid use_proxy parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(use_proxy))

    if use_proxy == 'YES':
        body_values['proxyhost'] = proxy_host

        proxy_port = int(proxy_port)

        if proxy_port not in range(1, 65535):
            raise ValueError('{0} is not a valid proxy port number.'
                             .format(proxy_port))

        body_values['proxyport'] = proxy_port

        if proxy_username is not None:
            if not is_valid_field(proxy_username):
                raise ValueError('{0} is not a valid proxy username.'
                                 .format(proxy_username))

            body_values['proxyuser'] = proxy_username

        if proxy_password is not None:
            if not is_valid_field(proxy_password):
                raise ValueError('{0} is not a valid proxy password.'
                                 .format(proxy_password))

            body_values['proxypassword'] = proxy_password

    method = 'POST'
    path = '/api/object_storage_destinations.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_ros_destination(session, ros_destination_id, bucket=None,
                           endpoint=None, username=None, password=None,
                           public=None, use_proxy=None, proxy_host=None,
                           proxy_port=None, proxy_username=None,
                           proxy_password=None, return_type=None):
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
    if not is_valid_ros_destination_id(ros_destination_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'destination ID.'.format(ros_destination_id))

    body_values = {}

    if bucket is not None:
        bucket = bucket.strip()

        if not is_valid_field(bucket):
            raise ValueError('{0} is not a valid remote object store bucket '
                             'name.'.format(bucket))

        body_values['bucket'] = bucket

    if endpoint is not None:
        body_values['endpoint'] = endpoint

    if username is not None:
        if not is_valid_field(username):
            raise ValueError('{0} is not a valid object storage username.'
                             .format(username))

        body_values['username'] = username

    if password is not None:
        if not is_valid_field(password):
            raise ValueError('{0} is not a valid object storage password.'
                             .format(password))

        body_values['password'] = password

    if public is not None:
        public = public.upper()

        if public in ['YES', 'NO']:
            if public == 'YES':
                body_values['connectVia'] = 'public'
            else:
                body_values['connectVia'] = 'fe'
        else:
            raise ValueError('{0} is not a valid public parameter.  Allowed '
                             'values are: "YES" or "NO"'.format(public))

    if use_proxy is not None:
        use_proxy = use_proxy.upper()

        if use_proxy in ['YES', 'NO']:
            if use_proxy == 'YES':
                body_values['use_proxy'] = 'true'
            else:
                body_values['use_proxy'] = 'false'
        else:
            raise ValueError('{0} is not a valid use_proxy parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(use_proxy))

    if proxy_host is not None or use_proxy == 'YES':
        body_values['proxyhost'] = proxy_host

    if proxy_port is not None or use_proxy == 'YES':
        proxy_port = int(proxy_port)

        if proxy_port not in range(1, 65535):
            raise ValueError('{0} is not a valid proxy port number.'
                             .format(proxy_port))

        body_values['proxyport'] = proxy_port

    if proxy_username is not None:
        if proxy_username is not None:
            if not is_valid_field(proxy_username):
                raise ValueError('{0} is not a valid proxy username.'
                                 .format(proxy_username))

            body_values['proxyuser'] = proxy_username

    if proxy_password is not None:
        if proxy_password is not None:
            if not is_valid_field(proxy_password):
                raise ValueError('{0} is not a valid proxy password.'
                                 .format(proxy_password))

            body_values['proxypassword'] = proxy_password

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"bucket", "endpoint", "username", "password", '
                         '"public", "use_proxy", "proxy_host", "proxy_port", '
                         '"proxy_username", "proxy_password"')

    method = 'PUT'
    path = '/api/object_storage_destinations/{0}.json'\
           .format(ros_destination_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def remove_ros_destination(session, ros_destination_id, return_type=None):
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
    if not is_valid_ros_destination_id(ros_destination_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'destination ID.'.format(ros_destination_id))

    method = 'DELETE'
    path = '/api/object_storage_destinations/{0}.json'\
           .format(ros_destination_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_all_ros_destination_backup_jobs(session, ros_destination_id,
                                        start=None, limit=None,
                                        return_type=None):
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
    if not is_valid_ros_destination_id(ros_destination_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'destination ID.'.format(ros_destination_id))

    method = 'GET'
    path = '/api/object_storage_destinations/{0}/backup_jobs.json'\
           .format(ros_destination_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_all_ros_destination_restore_jobs(session, ros_destination_id,
                                         start=None, limit=None,
                                         return_type=None):
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
    method = 'GET'
    path = '/api/object_storage_destinations/{0}/restore_jobs.json'\
           .format(ros_destination_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_all_ros_backup_jobs(session, start=None, limit=None,
                            return_type=None):
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
    method = 'GET'
    path = '/api/object_storage_backup_jobs.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_ros_backup_job(session, ros_backup_job_id, return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    method = 'GET'
    path = '/api/object_storage_backup_jobs/{0}.json'\
           .format(ros_backup_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_ros_backup_job(session, display_name, ros_destination_id,
                          volume_id, policy_id, compression='YES',
                          return_type=None):
    """
    Creates a new remote object storage backup job.  Backups are based on
    snapshots taken by the specified snapshot policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the remote object storage
        backup job.  For example: 'Daily S3 Backup'.  May not contain a single
        quote (') character.  Required.

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
    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid remote object storage backup '
                         'job name.'.format(display_name))

    body_values['name'] = display_name

    if not is_valid_ros_destination_id(ros_destination_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'destination ID.'.format(ros_destination_id))

    body_values['destination'] = ros_destination_id

    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values['volume'] = volume_id

    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values['policy'] = policy_id

    compression = compression.upper()

    if compression not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid compression parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(compression))

    body_values['compression'] = compression

    method = 'POST'
    path = '/api/object_storage_backup_jobs.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def pause_ros_backup_job(session, ros_backup_job_id, return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    method = 'POST'
    path = '/api/object_storage_backup_jobs/{0}/pause.json'\
           .format(ros_backup_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def resume_ros_backup_job(session, ros_backup_job_id, return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    method = 'POST'
    path = '/api/object_storage_backup_jobs/{0}/continue.json'\
           .format(ros_backup_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def break_ros_backup_job(session, ros_backup_job_id, purge_data,
                         delete_snapshots, return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    body_values = {}

    purge_data = purge_data.upper()

    if purge_data not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid purge_data parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(purge_data))

    body_values['purge_data'] = purge_data

    delete_snapshots = delete_snapshots.upper()

    if delete_snapshots not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid delete_snapshots parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(delete_snapshots))

    body_values['delete_snapshots'] = delete_snapshots

    method = 'POST'
    path = '/api/object_storage_backup_jobs/{0}/break.json'\
           .format(ros_backup_job_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_ros_backup_job_compression(session, ros_backup_job_id, compression,
                                      return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    body_values = {}

    compression = compression.upper()

    if compression not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid compression parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(compression))

    body_values['compression'] = compression

    method = 'POST'
    path = '/api/object_storage_backup_jobs/{0}/compression.json'\
           .format(ros_backup_job_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def replace_ros_backup_job_snapshot_policy(session, ros_backup_job_id,
                                           policy_id, return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    body_values = {}

    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values['policyname'] = policy_id

    method = 'POST'
    path = '/api/object_storage_backup_jobs/{0}/replace_snapshot_policy.json'\
           .format(ros_backup_job_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_all_ros_restore_jobs(session, start=None, limit=None,
                             return_type=None):
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
    method = 'GET'
    path = '/api/object_storage_restore_jobs.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_ros_restore_job(session, ros_restore_job_id, return_type=None):
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
    if not is_valid_ros_restore_job_id(ros_restore_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'restore job ID.'.format(ros_restore_job_id))

    method = 'GET'
    path = '/api/object_storage_restore_jobs/{0}.json'\
           .format(ros_restore_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_ros_restore_job(session, display_name, ros_destination_id, pool_id,
                           restore_mode, volume_name, local_snapshot_id,
                           object_store_key, crypt, return_type=None):
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
        raise ValueError('{0} is not a valid remote object storage backup '
                         'job name.'.format(display_name))

    body_values['name'] = display_name

    if not is_valid_ros_destination_id(ros_destination_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'destination ID.'.format(ros_destination_id))

    body_values['remote_object_store'] = ros_destination_id

    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values['poolname'] = pool_id

    if restore_mode not in ['restore', 'clone', 'import_seed']:
        raise ValueError('{0} is not a valid restore_mode parameter.  '
                         'Allowed values are: "restore", "clone", or '
                         '"import_seed"'.format(restore_mode))

    body_values['mode'] = restore_mode

    volume_name = volume_name.strip()

    if not is_valid_field(volume_name):
        raise ValueError('{0} is not a valid volume name.'
                         .format(volume_name))

    body_values['volname'] = volume_name

    if local_snapshot_id is None and object_store_key is None:
        raise ValueError('Either "local_snapshot_id" or "object_store_key" '
                         'needs to be passed as a parameter.')

    if local_snapshot_id is not None:
        if not is_valid_snapshot_id(local_snapshot_id):
            raise ValueError('{0} is not a valid local snapshot ID.'
                             .format(local_snapshot_id))

        body_values['local_snapname'] = local_snapshot_id

    if object_store_key is not None:
        if not is_valid_field(object_store_key):
            raise ValueError('{0} is not a valid object storage key.'
                             .format(object_store_key))

        body_values['key'] = object_store_key

    crypt = crypt.upper()

    if crypt not in ['YES', 'NO']:
        raise ValueError('{0} is not a valid crypt parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(crypt))

    body_values['crypt'] = crypt

    method = 'POST'
    path = '/api/object_storage_restore_jobs.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def pause_ros_restore_job(session, ros_restore_job_id, return_type=None):
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
    if not is_valid_ros_restore_job_id(ros_restore_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'restore job ID.'.format(ros_restore_job_id))

    method = 'POST'
    path = '/api/object_storage_restore_jobs/{0}/pause.json'\
           .format(ros_restore_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def resume_ros_restore_job(session, ros_restore_job_id, return_type=None):
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
    if not is_valid_ros_restore_job_id(ros_restore_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'restore job ID.'.format(ros_restore_job_id))

    method = 'POST'
    path = '/api/object_storage_restore_jobs/{0}/continue.json'\
           .format(ros_restore_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def break_ros_restore_job(session, ros_restore_job_id, return_type=None):
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
    if not is_valid_ros_restore_job_id(ros_restore_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'restore job ID.'.format(ros_restore_job_id))

    method = 'POST'
    path = '/api/object_storage_restore_jobs/{0}/break.json'\
           .format(ros_restore_job_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def change_ros_restore_job_mode(session, ros_restore_job_id, restore_mode,
                                return_type=None):
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
    if not is_valid_ros_restore_job_id(ros_restore_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'restore job ID.'.format(ros_restore_job_id))

    body_values = {}

    if restore_mode not in ['restore', 'clone']:
        raise ValueError('{0} is not a valid restore_mode parameter.  '
                         'Allowed values are: "restore" or "clone"'
                         .format(restore_mode))

    body_values['mode'] = restore_mode

    method = 'POST'
    path = '/api/object_storage_restore_jobs/{0}/switch_mode.json'\
           .format(ros_restore_job_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_ros_backup_job_performance(session, ros_backup_job_id, interval=1,
                                   return_type=None):
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
    if not is_valid_ros_backup_job_id(ros_backup_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'backup job ID.'.format(ros_backup_job_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/object_storage_backup_jobs/{0}/performance.json'\
           .format(ros_backup_job_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_ros_restore_job_performance(session, ros_restore_job_id, interval=1,
                                    return_type=None):
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
    if not is_valid_ros_restore_job_id(ros_restore_job_id):
        raise ValueError('{0} is not a valid remote object storage '
                         'restore job ID.'.format(ros_restore_job_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/object_storage_restore_jobs/{0}/performance.json'\
           .format(ros_restore_job_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
