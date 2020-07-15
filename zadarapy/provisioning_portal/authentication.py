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

from zadarapy.session import run_outside_of_api


def _generate_token_cmd(path, username, password):
    """
    Retrieves details for all available storage clouds.

    :type path: str
    :param path: API path

    :type username: str
    :param username: User name

    :type password: str
    :param password: Password of the user

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body = '{"username": "%s", "password": "%s"}' % (username, password)
    return "curl -X POST -H 'Content-Type: application/json' -d '%s' %s" % (body, path)


def get_authentication_token(ip, username, password):
    """
    Retrieves details for all available storage clouds.

    :type ip: str
    :param ip: IP of the provisioning portal

    :type username: str
    :param username: User name

    :type password: str
    :param password: Password of the user

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = f"https://{ip}/api/v2/token.json"
    cmd = _generate_token_cmd(path=path, username=username, password=password)

    return run_outside_of_api(cmd)


def reset_authentication_token(ip, username, password):
    """
    Retrieves details for all available storage clouds.

    :type ip: str
    :param ip: IP of the provisioning portal

    :type username: str
    :param username: User name

    :type password: str
    :param password: Password of the user

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = f"https://{ip}/api/v2/token/reset.json"
    cmd = _generate_token_cmd(path=path, username=username, password=password)

    return run_outside_of_api(cmd)
