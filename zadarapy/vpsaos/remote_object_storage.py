#copyright 2019 Zadara Storage, Inc.
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


def get_ros_destinations_from_account(session, container_account,
                             return_type=None, **kwargs):
    """
    Get a list of Remote Object Storage Endpoints in current user's account or in a container's account.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type: container_account: str
    :param container_account: Container account id

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_account_id(container_account)

    path = f'/api/zios/object_storage_destinations.json?container_account={container_account}'

    return session.get_api(path=path,  return_type=return_type, **kwargs)


def get_ros_destination(session, targetExtName, return_type=None,
                        **kwargs):
    """
    Get one Remote Object Storage Endpoint.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type targetExtName: str
    :param targetExtName: External name of the remote object storage. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_ros_target_id(targetExtName)

    path = '/api/zios/object_storage_destinations/{0}.json' \
        .format(targetExtName)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_ros_destination(session, name, type, endpoint, endpoint_url,
                           region, username, password, connectVia, return_type=None, **kwargs):
    """
    Create a Remote Object Storage Endpoint. Connection will be tested.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type name: str
    :param name: Display Name for Remote Object Storage Endpoint. Required.

    :type type: str - AWS_S3 | ZIOS_S3
    :param type: Type for Remote Object Storage Endpoint. Required.

    :type endpoint: str
    :param endpoint: Endpoint for AWS S3 destination type. Optional.

    :type endpoint_url: str
    :param endpoint_url: Endpoint URL for VPSA Object Storage S3 destination type. Optional.

    :type region: str
    :param region: Region for VPSA Object Storage S3 destination type. Required.

    :type: username: str
    :param username: Access Key ID for Remote Object Storage Endpoint. Required.

    :type password: str
    :param password: Secret Access Key for Remote Object Storage Endpoint. Required.

    :type connectVia: str - fe | outnet
    :param connectVia: Connection method for remote object storage. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(name, "name")
    verify_field(type, "type")
    verify_field(region, "region")
    verify_field(username, "username")
    verify_field(password, "password")
    verify_field(connectVia, "connectVia")

    body_values = {'name': name, 'type': type,
                   'region': region, 'username': username,
                   'password': password, 'connectVia': connectVia}

    if endpoint is not None:
        body_values["endpoint"] = endpoint
    else:
        body_values["endpoint_url"] = endpoint_url

    path = '/api/zios/object_storage_destinations.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_ros_destination(session, targetExtName, name, type, region_name, region_name_text,
                           username, password, connectVia, return_type=None, **kwargs):
    """
    Update an Remote Object Storage Endpoint. Connection will be tested.


    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type targetExtName: str
    :param targetExtName: External name of the remote object storage. Required.

    :type name: str
    :param name: Display Name for Remote Object Storage Endpoint. Required.

    :type type: str - AWS_S3 | ZIOS_S3
    :param type: Type for Remote Object Storage Endpoint. Required.

    :type endpoint: str
    :param endpoint: Endpoint for AWS S3 destination type. Required.

    :type region_name: str
    :param region_name: Endpoint for AWS S3 destination type. Required.

    :type region_name_text: str
    :param region_name_text: Region for VPSA Object Storage S3 destination type	. Required.

    :type: username: str
    :param username: Access Key ID for Remote Object Storage Endpoint. Required.

    :type password: str
    :param password: Secret Access Key for Remote Object Storage Endpoint. Required.

    :type connectVia: str - fe | outnet
    :param connectVia: Connection method for remote object storage. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(targetExtName, "targetExtName")
    verify_field(name, "name")
    verify_field(type, "type")
    verify_field(username, "username")
    verify_field(password, "password")
    verify_field(connectVia, "connectVia")

    body_values = {'name': name, 'type': type,
                   'username': username,'password': password,
                   'connectVia': connectVia}

    if region_name is not None:
        body_values["region_name"] = region_name
    else:
        body_values["region_name_text"] = region_name_text

    path = '/api/zios/object_storage_destinations/{0}.json'.format(targetExtName)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)

def remove_ros_destination(session, targetExtName, force, return_type=None,
                           **kwargs):
    """
    Removes a remote object storage destination.  There must not be any remote
    object storage backup jobs associated with this destination.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type targetExtName: str
    :param targetExtName: External name of the remote object storage. Required.

    :type force: str
    :param force force a deletion. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(targetExtName, "targetExtName")
    verify_boolean(force, "force")

    path = '/api/zios/object_storage_destinations/{0}.json' \
        .format(targetExtName)

    body_value = {'force': force}

    return session.delete_api(path=path, body=body_value, return_type=return_type, **kwargs)


