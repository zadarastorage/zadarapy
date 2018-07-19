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


from future.standard_library import install_aliases
install_aliases()

import http.client
import json
from urllib.parse import quote
from zadarapy.validators import is_valid_email
from zadarapy.validators import is_valid_field


def get_api_key(host, accountname, username, password, port=5000, secure=True):
    """
    Get api_token token for the zios_admin account
    This token can be used for any VPSAOS GUI operations.

    :type host: str
    :param host: The VPSAOS host name. Required.
        example of host name is xxx.zadarazios.com. (no http:// specified)

    :type accountname: str
    :param accountname: The VPSAOS accountname. Required.

    :type username: str
    :param username: The VPSAOS user's username. Required.

    :type password: str
    :param password: The VPSAOS user's password. Required.

    :type port: str
    :param port: The VPSAOS keystone port which is defaulted to 5000. Required.

    :type secure: boolean
    :param secure: The keystone use the secure authentication. Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    if secure:
        conn = http.client.HTTPSConnection(host, port)
    else:
        conn = http.client.HTTPConnection(host, port)

    headers = {}
    headers["Content-Type"] = "application/json"

    body = {}
    user = {}
    pwd = {}

    user['username'] = username
    user['password'] = password
    pwd['passwordCredentials'] = user
    pwd['tenantName'] = accountname
    body['auth'] = pwd

    conn.request("POST", "/v2.0/tokens", headers=headers, body=json.dumps(body))
    response = conn.getresponse()
    data = json.loads(response.read())
    conn.close()
    return data['access']['token']['id']

