opyright 2019 Zadara Storage, Inc.
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

from zadarapy.validators import *


def get_replication_jobs(session, return_type=None, **kwargs):
    """
    Get all the replication jobs from ZIOS.

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

    path = '/api/zios/containers_replications.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_replication_job(session, replicationId, return_type=None, **kwargs):
    """
    Get the specified replication jobs from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type replicationId: str
    :param replicationId: The replication job's id

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_field(replicationId, "replicationId")

    path = f'/api/zios/containers_replications.json?replicationId={replicationId}'

    body_values = {'replicationId': replicationId}

    return session.get_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def create_replication_job(session, replicationTargetName, displayName, authUrl, srcBucket, dstBucket,
                           applyDelete=False, createRemoteContainer=False, return_type=None, **kwargs):
    """
    create a replication job from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type replicationTargetName: str
    :param replicationTargetName: Remote Object Storage Endpoint ext-name.
        Destination must be of the same account as the source container's account.

    :type displayName: str
    :param displayName: job display name.

    :type authUrl: str
    :param authUrl: AUTH URL of the source container's account id.

    :type srcBucket: str
    :param srcBucket: Source container name.

    :type dstBucket: str
    :param dstBucket: Destination container name.

    :type applyDelete: str
    :param applyDelete: Delete objects propagation.

    :type createRemoteContainer: str
    :param createRemoteContainer: Create the destination container.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_ros_target_id(replicationTargetName)
    verify_field(displayName, "displayName")
    verify_field(authUrl, "authUrl")
    authToken = session.zadara_key
    verify_field(srcBucket, "srcBucket")
    verify_field(dstBucket, "dstBucket")
    applyDelete = verify_bool_parameter(applyDelete)
    createRemoteContainer = verify_bool_parameter(createRemoteContainer)

    path = '/api/zios/containers_replications.json'

    body_values = {"replicationTargetName": replicationTargetName, "displayName": displayName, "authUrl": authUrl,
                   "authToken": authToken, "srcBucket": srcBucket, "dstBucket": dstBucket, "applyDelete": applyDelete,
                   "createRemoteContainer": createRemoteContainer}

    return session.post_api(path=path, body=body_values,
                           return_type=return_type, **kwargs)


def resume_replication_job(session, replicationId, return_type=None, **kwargs):
    """
    Resume the specified replication jobs from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type replicationId: str
    :param replicationId: The replication job's id

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(replicationId, "replicationId")

    path = '/api/zios/containers_replications/resume.json'

    body_values = {'replicationId': replicationId}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def pause_replication_job(session, replicationId, return_type=None, **kwargs):
    """
    Pause the specified replication jobs from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type replicationId: str
    :param replicationId: The replication job's id

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(replicationId, "replicationId")

    path = '/api/zios/containers_replications/pause.json'

    body_values = {'replicationId': replicationId}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_replication_job(session, replicationId, return_type=None, **kwargs):
    """
    Delete the specified replication jobs from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type replicationId: str
    :param replicationId: The replication job's id

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(replicationId, "replicationId")

    path = '/api/zios/containers_replications/delete.json'

    body_values = {'replicationId': replicationId}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_replication_jobs_statistics(session, replicationTargetName, return_type=None, **kwargs):
    """
    Get statistics of Container Replication Jobs in an account from ZIOS.

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

    verify_ros_target_id(replicationTargetName)

    path = f'/api/zios/stats_of_account.json?replicationTargetName={replicationTargetName}'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_replication_job_statistics(session, replicationId, return_type=None, **kwargs):
    """
    Get statistics of a replication job from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type replicationId: str
    :param replicationId: The replication job's id

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_field(replicationId, "replicationId")

    path = f'/api/zios/containers_replications/replication_job_stats.json?{replicationId}.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)

