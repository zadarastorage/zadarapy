# Copyright 2015 Zadara Storage, Inc.
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


import configparser
import http.client
import json
import os
from urllib.parse import urlencode
from zadarapy.validators import is_valid_hostname
from zadarapy.validators import is_valid_ip_address
from zadarapy.validators import is_valid_zadara_key


class Session(object):
    """
    The session object should be instantiated before making any calls to the
    API endpoint.  It will gather the required authentication credentials, as
    well as the URL to utilize, then make the calls to the API.
    """

    def __init__(self, host=None, key=None, configfile=None, secure=True):
        """
        Configuration details for working with the API will be gathered from
        the following, in order or preference:

        * From a keyword argument passed to the this object at instantiation
        * From the appropriate environment variable, if it exists
        * From the config file, if it exists (~/.zadarapy by default)

        If no suitable configuration is found, an exception will be thrown.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This should
            be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.

        :type key: str
        :param key: The API key for the connecting user.

        :type configfile: str
        :param configfile: Full path to configuration file that defines values
            needed for this object.

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS, otherwise
            HTTP will be used.
        """
        self._config = None

        # If a config file exists, parse it
        if configfile is not None:
            if os.path.isfile(configfile):
                self._config = configparser.ConfigParser()
                self._config.read(configfile)

        if self._config is None and os.path.isfile('~/.zadarapy'):
            self._config = configparser.ConfigParser()
            self._config.read('~/.zadarapy')

        # Hostname for API endpoint
        if host is not None:
            self._host = host
        elif os.getenv('ZADARA_HOST') is not None:
            self._host = os.getenv('ZADARA_HOST')
        elif self._config is not None:
            if self._config['DEFAULT'].get('host', None) is not None:
                self._host = self._config['DEFAULT'].get('host')
        else:
            raise ValueError('The API hostname was not defined.')

        # Authorization key for API endpoint
        if key is not None:
            self._key = key
        elif os.getenv('ZADARA_KEY') is not None:
            self._key = os.getenv('ZADARA_KEY')
        elif self._config is not None:
            if self._config['DEFAULT'].get('key', None) is not None:
                self._key = self._config['DEFAULT'].get('key')
        else:
            raise ValueError('The API authentication key was not defined.')

        # If HTTPS or HTTP should be used
        true_values = ['True', 'true', 'Yes', 'yes', 'On', 'on', 'Y', 'y']

        if os.getenv('ZADARA_SECURE') in true_values:
            self._secure = True
        elif self._config is not None:
            if self._config['DEFAULT'].get('secure', None) in true_values:
                self._secure = True
            else:
                self._secure = False
        elif secure is False:
            self._secure = False
        else:
            self._secure = True

    def call_api(self, method, path, host=None, key=None, secure=None,
                 body=None, parameters=None, return_type=None):
        """
        Makes the actual REST call to the Zadara API endpoint.  If host, key,
        and/or secure are set as None, the instance variables will be used as
        default values.

        Zadara supports both JSON and XML for its API, but please note that
        this module uses and expects JSON.

        :type method: str
        :param method: The HTTP verb being used for the REST call.  Can be
            'GET' or 'POST'.  Required.

        :type path: str
        :param path: The path of the API endpoint, for example:
            '/api/vpsas.json'.  Required.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This should
            be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.  Required.

        :type key: str
        :param key: The API key for the connecting user.  Required.

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS, otherwise
            HTTP will be used.  Required.

        :type body: str
        :param body: For POST calls, a body should be supplied that *only*
            contains a valid JSON data set.  No "key" should be supplied for
            this value.  Optional.

        :type parameters: dict
        :param parameters: A Python dictionary of key value pairs that will be
            passed as URL parameters.  Optional.

        :type return_type: str
        :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by default).

        :rtype: dict, str
        :returns: A dictionary or JSON data set as a string depending on
            return_type parameter.
        """
        # Validate all inputs
        if host is None:
            host = self._host

        if key is None:
            key = self._key

        if secure is None:
            secure = self._secure

        if not is_valid_hostname(self._host) and not is_valid_ip_address(
                self._host):
            raise ValueError(
                '{0} is not a valid hostname or IP address'.format(self._host))

        if not is_valid_zadara_key(self._key):
            raise ValueError('{0} is not a valid API key'.format(self._key))

        if secure:
            conn = http.client.HTTPSConnection(host)
        else:
            conn = http.client.HTTPConnection(host)

        headers = {"Content-Type": "application/json",
                   "X-Access-Key": key}

        # Ignore parameters if set to None or an empty dictionary is passed.
        if parameters:
            url = path + '?' + urlencode(parameters)
        else:
            url = path

        conn.request(method, url, headers=headers, body=body)

        response = conn.getresponse()

        if response.status != 200:
            conn.close()
            raise RuntimeError('API server did not return an HTTP 200 '
                               'response.  Status "{0} {1}" was returned '
                               'instead.  Please investigate.'
                               .format(response.status, response.reason))

        data = response.read()

        conn.close()

        api_return_dict = json.loads(data.decode('UTF-8'))

        if api_return_dict['response']['status'] != 0:
            raise ValueError('The API server returned an error: "{0}" - '
                             'exiting.'
                             .format(api_return_dict['response']['message']))

        if return_type == 'json':
            return data.decode('UTF-8')
        else:
            return api_return_dict
