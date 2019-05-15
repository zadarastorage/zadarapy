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
from zadarapy.validators import verify_start_limit, is_valid_remote_clone_id, verify_remote_clone_id


def get_all_remote_clones(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all remote clone jobs configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying remote clone jobs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of remote clone jobs to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)

    path = '/api/remote_clones.json'

    return session.get_api(path=path, parameters=parameters, return_type=return_type)


def get_remote_clone(session, remote_clone_job_id, return_type=None):
    """
    Retrieves details for the specified remote clone job configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type remote_clone_job_id: str
    :param remote_clone_job_id: The remote clone job 'job_name' value as returned by
        create_volume_remote_clone.  For example: 'dstrclone-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    is_valid_remote_clone_id(remote_clone_job_id)

    path = '/api/remote_clones/{0}.json'.format(remote_clone_job_id)

    return session.get_api(path=path, return_type=return_type)


def pause_remote_clone(session, remote_clone_job_id, return_type=None):
    """
    Pauses a remote clone job.  This should only be initiated from the source VPSA.
    e.g. the remote clone job ID should start with "dstrclone-".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type remote_clone_job_id: str
    :param remote_clone_job_id: The remote clone job 'name'
        value as returned by get_all_remote_clones.  For example:
        'dstrclone-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_remote_clone_id(remote_clone_job_id)

    path = '/api/remote_clones/{0}/pause.json'.format(remote_clone_job_id)

    return session.post_api(path=path, return_type=return_type)


def resume_remote_clone_job(session, remote_clone_job_id, return_type=None):
    """
    Resumes a paused remote clone job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type remote_clone_job_id: str
    :param remote_clone_job_id: The remote clone job 'name'
        value as returned by get_all_remote_clones.  For example:
        'dstrclone-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_remote_clone_id(remote_clone_job_id)

    path = '/api/remote_clones/{0}/continue.json' \
        .format(remote_clone_job_id)

    return session.post_api(path=path, return_type=return_type)


def break_remote_clone_job(session, remote_clone_job_id, return_type=None):
    """
    Breaks a remote clone job.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

   :type remote_clone_job_id: str
    :param remote_clone_job_id: The remote clone job 'name'
        value as returned by get_all_remote_clones.  For example:
        'dstrclone-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_remote_clone_id(remote_clone_job_id)

    path = '/api/remote_clones/{0}/break.json'\
        .format(remote_clone_job_id)

    return session.post_api(path=path, return_type=return_type)


def switch_remote_clone_mode(session, remote_clone_job_id, is_clone, return_type=None):
    """
    Breaks a remote clone job.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

   :type remote_clone_job_id: str
    :param remote_clone_job_id: The remote clone job 'name'
        value as returned by get_all_remote_clones.  For example:
        'dstrclone-00000001'.  Required.

    :type is_clone: bool
    :param is_clone: True if switch mode to 'clone' else switch to 'retrieve'.
    Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_remote_clone_id(remote_clone_job_id)

    body_values = {'mode': 'clone' if is_clone else 'retrieve'}
    path = '/api/remote_clones/{0}/switch_mode.json'\
        .format(remote_clone_job_id)

    return session.post_api(path=path, body=body_values, return_type=return_type)
