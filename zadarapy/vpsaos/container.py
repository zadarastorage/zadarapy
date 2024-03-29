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

from zadarapy.validators import verify_versioning, is_valid_minutes, verify_expire_version, verify_account_id, \
    verify_field, verify_bool_parameter, verify_positive_argument


def set_versioning(session, bucket_name, versioning, archive_name, return_type=None, **kwargs):
    """
    Set versioning in a bucket

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type bucket_name: str
    :param bucket_name: Name of the bucket.  Required.

    :type versioning: str
    :param versioning: Type of versioning.
        Can be only x-versions-location or x-history-location.  Required.

    :type archive_name: str
    :param archive_name: Name of the the archive to be created.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    versioning = verify_versioning(versioning)

    path = "/{0}".format(bucket_name)
    headers = {versioning: archive_name}

    return session.put_api(path=path, additional_headers=headers, return_type=return_type,
                           use_port=False, return_header=True, **kwargs)


def add_lifecycle_policy(session, bucket_name, objects_minutes_expiry, objects_expire_version,
                         objects_name_prefix, other_policies=None, return_type=None, **kwargs):
    """
    Add lifecycle policy expiry to a bucket

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type bucket_name: str
    :param bucket_name: Name of the bucket.  Required.

    :type objects_minutes_expiry: int
    :param objects_minutes_expiry: How many minutes will the object be valid and won't expire.  Required.

    :type objects_expire_version: str
    :param objects_expire_version: Type of expiration versioning.
        Can be only current or previous.  Required.

    :type objects_name_prefix: str
    :param objects_name_prefix: Prefix for objects name.  Required.

    :type other_policies: str
    :param other_policies: Other lifecycle policies.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    objects_minutes_expiry = is_valid_minutes(objects_minutes_expiry)
    objects_expire_version = verify_expire_version(objects_expire_version)

    policies = "{\"prefix\": \"%s\", \"%s\": %s}" % (objects_name_prefix,
                                                     objects_expire_version, objects_minutes_expiry)
    if other_policies is not None:
        policies += "," + other_policies.replace("[", "").replace("]", "")

    return set_expiry_lifecycle_policy(session=session, bucket_name=bucket_name, policies=policies)


def set_expiry_lifecycle_policy(session, bucket_name, policies="", return_type=None, **kwargs):
    """
    Set lifecycle policy expiry in a bucket

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type bucket_name: str
    :param bucket_name: Name of the bucket.  Required.

    :type policies: str
    :param policies: Expiry lifecycle policy expiry policy to set.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    api = "https://{}/{}".format(session.zadara_host, bucket_name)
    cmd = "curl %s -X PUT -H 'x-auth-token: %s' -H " \
          "'x-container-meta-objectexpirer: [%s]'" \
          % (api, session.zadara_key, policies)

    return run_outside_of_api(cmd)


def get_container_quota(session, container_name, account_id, return_type=None, **kwargs):
    """
    get information on container quota
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type container_name: str
    :param container_name: container's name to get information about

    :type account_id: str
    :param account_id: id of container's account

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_account_id(account_id)
    verify_field(container_name, "container_name")

    path = "/api/zios/accounts/{0}/containers/{1}/quota.json".format(account_id, container_name)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def set_container_quota(session, container_name, account_id, container_quota_bytes_toggle, container_quota_count_toggle,
                        container_quota_count, container_quota_bytes=None, container_quota_bytes_in_gib=None, return_type=None,
                        **kwargs):
    """
    get information on container quota
    the parameter name change in 22.06 from container_quota_count to container_quota_count_in_gib

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type container_name: str
    :param container_name: container's name to get information about

    :type account_id: str
    :param account_id: id of container's account

    :type container_quota_bytes_toggle: boolean
    :param container_quota_bytes_toggle: Enable capacity quota. Required.

    :type container_quota_bytes: integer
    :param container_quota_bytes: Quota by capacity (bytes)

    :type container_quota_bytes_in_gib: integer
    :param container_quota_bytes_in_gib: Quota by capacity (in GiB)

    :type container_quota_count_toggle: boolean
    :param container_quota_count_toggle: Enable objects count quota. Required.

    :type container_quota_count: integer
    :param container_quota_count: Quota by objects count

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    verify_account_id(account_id)
    verify_field(container_name, "container_name")
    right_container_quota_bytes = ""
    right_container_quota_bytes_name = ""
    if container_quota_bytes_toggle:
        verify_bool_parameter(container_quota_bytes_toggle)
        if container_quota_bytes is not None and not container_quota_bytes:
            right_container_quota_bytes = verify_positive_argument(container_quota_bytes, "container_quota_bytes")
            right_container_quota_bytes_name = "container_quota_bytes"
        else:
            right_container_quota_bytes = verify_positive_argument(container_quota_bytes_in_gib, "container_quota_bytes_in_gib")
            right_container_quota_bytes_name = "container_quota_bytes_in_gib"
    if container_quota_bytes_toggle:
        verify_bool_parameter(container_quota_count_toggle)
        verify_positive_argument(container_quota_count, "container_quota_count")

    path = "/api/zios/accounts/{0}/containers/{1}/quota.json".format(account_id, container_name)

    body_values = {'container_quota_bytes_toggle': container_quota_bytes_toggle,
                   right_container_quota_bytes_name: right_container_quota_bytes,
                   'container_quota_count_toggle': container_quota_count_toggle,
                   'container_quota_count': container_quota_count}

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def create_container(session, name, storage_policy, return_type=None, **kwargs):
    """
    Get a bucketfrom ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: Name of the container.  Required.

    :type storage_policy: str
    :param storage_policy: Name of the storage policy e.g. 2-Way-Protection.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    path = "/{0}".format(name)
    headers = {"x-storage-policy": storage_policy}

    return session.put_api(path=path, additional_headers=headers, use_port=False,
                           return_type=return_type, return_header=True, **kwargs)


def run_outside_of_api(cmd):
    """
    Run command outside of the usual session API due to python limitations
    e.g. when we need to run a command that get headers with a single quote
    and other headers with double quotes python built-in modules fail to do it
    for instance wecan't run this API -
    curl 'https://vsa-0000007e-zadara-qa10.zadarazios.com:443/v1/AUTH_20db47cfaaff46079861b917116decf7/nirhayuntest'
    -X PUT -H 'x-auth-token: gAAAAABelWkqs7uouuMBd5EPopY2HCkQYQKEatQ6Lt52ThEpTNvUKcTBi7pR3iZS2_Wzufgr7GD4unsQlWRb0f'
    -H 'x-container-meta-objectexpirer: [{"prefix": "HAYUN", "curver_after": 259200}]'
    (one header needs to be qith single qutes and the dict in the second header needs to be with a double quote

    :type cmd: str
    :param cmd: A valid ZPI command to execute.  Required.
    """

    from subprocess import Popen, PIPE
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    res = {}
    (res["output"], err) = p.communicate()

    if p.returncode != 0:
        raise AssertionError("Failed to execute commnad: {0}\n{1}".format(cmd, err))

    res["status"] = "success"
    return res
