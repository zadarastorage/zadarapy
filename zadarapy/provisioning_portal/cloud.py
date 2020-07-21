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

from zadarapy.validators import verify_id
from future.standard_library import install_aliases
install_aliases()


def get_all_clouds(session, return_type=None, **kwargs):
    """
    Retrieves details for all available storage clouds.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/v2/clouds.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_cloud(session, cloud_id, return_type=None, **kwargs):
    """
    Retrieves details for a single cloud.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_id: str|int
    :param cloud_id: The cloud 'key' value as returned by get_clouds.  For
        example: 'aws' or 'aws-jp1'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_id = verify_id(cloud_id)
    path = '/api/v2/clouds/{0}.json'.format(cloud_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)
