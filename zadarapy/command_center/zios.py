# Copyright 2019 Zadara Storage, Inc.
# Originally authored by Nir Hayun
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

from zadarapy.validators import verify_cloud_name, verify_positive_argument, verify_zios_id


def get_all_zios_objects(session, cloud_name, per_page=30, page=1, return_type=None, **kwargs):
    """
    Retrieves details for all ZIOSs in the cloud.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type page: int
    :param page: The page number to page from.  Optional.

    :type: per_page: int
    :param per_page: The total number of records to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_name = verify_cloud_name(cloud_name)

    page = verify_positive_argument(page, 'page')
    per_page = verify_positive_argument(per_page, 'per_page')

    path = "/api/clouds/{0}/zioses.json?per_page={1}&page={2}".format(cloud_name, per_page, page)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def hibernate_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Hibernate ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/hibernate.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def restore_zios(session, cloud_name, zios_id, return_type=None, **kwargs):
    """
    Restore ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object. Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'. Required.

    :type zios_id: int
    :param zios_id: The ZIOS 'id' value as returned by get_all_zios_objects. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zios_id(zios_id)
    cloud_name = verify_cloud_name(cloud_name)

    path = "/api/clouds/{0}/zioses/{1}/restore.json".format(cloud_name, zios_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)
