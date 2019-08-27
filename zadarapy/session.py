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

from future.standard_library import install_aliases

install_aliases()

import configparser
import http.client
import json
import os
from urllib.parse import urlencode
from zadarapy.validators import verify_port

DEFAULT_TIMEOUT = 15

FAILURE_RESPONSE = 'API server did not return an HTTP 200, 201 or 302 ' \
                   'response. Status "{0} {1}" was returned instead.  ' \
                   'Please investigate.'


class Session(object):
    """
    The session object should be instantiated before making any calls to the
    API endpoint.  It will gather the required authentication credentials, as
    well as the URL to utilize, then make the calls to the API.
    """
    zadara_host = None
    zadara_port = None
    zadara_key = None
    zadara_secure = None

    def __init__(self, host=None, port=None, key=None, configfile=None,
                 secure=True, default_timeout=None, log_function=None):
        """
        Configuration details for working with the API will be gathered from
        the following, in order or preference:

        * From a keyword argument passed to the this object at instantiation
        * From the appropriate environment variable, if it exists
        * From the config file, if it exists (~/.zadarapy by default)

        If no suitable configuration is found, an exception will be thrown.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This
            should be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.

        :type port: int
        :param port: The port for the API endpoint.  If set to None, the
            default port for the HTTP mode will be used (80 for HTTP, 443 for
            HTTPS).  Optional.

        :type key: str
        :param key: The API key for the connecting user.

        :type configfile: str
        :param configfile: Full path to configuration file that defines values
            needed for this object.

        :type secure: bool
        :param secure: If False, the API call will be made over HTTP,
            otherwise HTTPS will be used.

        :type default_timeout: int
        :param default_timeout: Default timeout to each HTTP request.

        :type log_function: function
        :param log_function: Function variable to a log function to print the
                API command Session sends. Default=None, means no print
        """
        self._log_function = log_function
        self._default_timeout = default_timeout or DEFAULT_TIMEOUT
        assert self._default_timeout > 0, "timeout must be a positive int type"

        self._config = None

        # If a config file exists, parse it
        if configfile is not None:
            if os.path.isfile(configfile):
                self._config = configparser.ConfigParser()
                self._config.read(configfile)

        if self._config is None and configfile is None:
            configfile = os.path.expanduser('~/.zadarapy')

            if os.path.isfile(configfile):
                self._config = configparser.ConfigParser()
                self._config.read(configfile)

        # Hostname for API endpoint
        if host is not None:
            self.zadara_host = host
        elif os.getenv('ZADARA_HOST') is not None:
            self.zadara_host = os.getenv('ZADARA_HOST')
        elif self._config is not None:
            if self._config.defaults().get('host', None) is not None:
                self.zadara_host = self._config.defaults().get('host')
        else:
            raise ValueError('The API hostname was not defined.')

        # Port for API endpoint
        if port is not None:
            self.zadara_port = port
        elif os.getenv('ZADARA_PORT') is not None:
            self.zadara_port = os.getenv('ZADARA_PORT')
        elif self._config is not None:
            if self._config.defaults().get('port', None) is not None:
                self.zadara_port = self._config.defaults().get('port')
        else:
            self.zadara_port = None

        # Authorization key for API endpoint
        if key is not None:
            self.zadara_key = key
        elif os.getenv('ZADARA_KEY') is not None:
            self.zadara_key = os.getenv('ZADARA_KEY')
        elif self._config is not None:
            if self._config.defaults().get('key', None) is not None:
                self.zadara_key = self._config.defaults().get('key')
        else:
            raise ValueError('The API authentication key was not defined.')

        # If HTTPS or HTTP should be used
        false_values = ['false', 'no', 'off', 'n']

        if secure is False:
            self.zadara_secure = False
        elif os.getenv('ZADARA_SECURE') is not None:
            if os.getenv('ZADARA_SECURE').lower() in false_values:
                self.zadara_secure = False
        elif self._config is not None:
            if self._config.defaults().get('secure', None) is not None:
                if self._config.defaults().get('secure').lower() in \
                        false_values:
                    self.zadara_secure = False

        if self.zadara_secure is None:
            self.zadara_secure = True

    def get_api(self, path, host=None, port=None, key=None, url_encode=False,
                secure=None, body=None, parameters=None, timeout=None,
                return_type=None):
        """
        Makes the actual GET REST call to the Zadara API endpoint.
        If host, key, and/or secure are set as None, the instance variables
        will be used as default values.

        Zadara supports both JSON and XML for its API, but please note that
        this module uses and expects JSON.

        :type path: str
        :param path: The path of the API endpoint, for example:
            '/api/vpsas.json'.  Required.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This
            should be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.  Required.

        :type port: int
        :param port: The port for the API endpoint.  If set to None, the
            default port for the HTTP mode will be used (80 for HTTP, 443 for
            HTTPS).  Optional.

        :type key: str
        :param key: The API key for the connecting user.  Required.

        :type url_encode: bool
        :param url_encode: True iff encode using urlencode

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS,
            otherwise HTTP will be used.  Required.

        :type body: Dict
        :param body: For POST calls, a body should be supplied that *only*
            contains a valid JSON data set.  No "key" should be supplied for
            this value.  Optional.

        :type parameters: dict
        :param parameters: A Python dictionary of key value pairs that will be
            passed as URL parameters.  Optional.

        :type timeout: int
        :param timeout: API command timeout. When None, it will use the default
        timeout.  Optional.

        :type return_type: str
        :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by
            default).

        :rtype: dict, str
        :returns: A dictionary or JSON data set as a string depending on
            return_type parameter.
        """
        return self.call_api(method="GET", path=path, host=host, port=port,
                             key=key, secure=secure, body=body,
                             parameters=parameters, url_encode=url_encode,
                             timeout=timeout, return_type=return_type)

    def post_api(self, path, host=None, port=None, key=None, url_encode=False,
                 secure=None, body=None, parameters=None, timeout=None,
                 return_type=None):
        """
        Makes the actual POST REST call to the Zadara API endpoint.
        If host, key, and/or secure are set as None, the instance variables
        will be used as default values.

        Zadara supports both JSON and XML for its API, but please note that
        this module uses and expects JSON.

        :type path: str
        :param path: The path of the API endpoint, for example:
            '/api/vpsas.json'.  Required.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This
            should be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.  Required.

        :type port: int
        :param port: The port for the API endpoint.  If set to None, the
            default port for the HTTP mode will be used (80 for HTTP, 443 for
            HTTPS).  Optional.

        :type key: str
        :param key: The API key for the connecting user.  Required.

        :type url_encode: bool
        :param url_encode: True iff encode using urlencode

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS,
            otherwise HTTP will be used.  Required.

        :type body: Dict
        :param body: For POST calls, a body should be supplied that *only*
            contains a valid JSON data set.  No "key" should be supplied for
            this value.  Optional.

        :type parameters: dict
        :param parameters: A Python dictionary of key value pairs that will be
            passed as URL parameters.  Optional.

        :type timeout: int
        :param timeout: API command timeout. When None, it will use the default
        timeout.  Optional.

        :type return_type: str
        :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by
            default).

        :rtype: dict, str
        :returns: A dictionary or JSON data set as a string depending on
            return_type parameter.
        """
        return self.call_api(method="POST", path=path, host=host, port=port,
                             key=key, secure=secure, body=body,
                             parameters=parameters, url_encode=url_encode,
                             timeout=timeout, return_type=return_type)

    def delete_api(self, path, host=None, port=None, key=None,
                   url_encode=False, secure=None, body=None,
                   parameters=None, timeout=None, return_type=None):
        """
        Makes the actual DELETE REST call to the Zadara API endpoint.
        If host, key, and/or secure are set as None, the instance variables
        will be used as default values.

        Zadara supports both JSON and XML for its API, but please note that
        this module uses and expects JSON.

        :type path: str
        :param path: The path of the API endpoint, for example:
            '/api/vpsas.json'.  Required.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This
            should be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.  Required.

        :type port: int
        :param port: The port for the API endpoint.  If set to None, the
            default port for the HTTP mode will be used (80 for HTTP, 443 for
            HTTPS).  Optional.

        :type key: str
        :param key: The API key for the connecting user.  Required.

        :type url_encode: bool
        :param url_encode: True iff encode using urlencode

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS,
            otherwise HTTP will be used.  Required.

        :type body: Dict
        :param body: For POST calls, a body should be supplied that *only*
            contains a valid JSON data set.  No "key" should be supplied for
            this value.  Optional.

        :type parameters: dict
        :param parameters: A Python dictionary of key value pairs that will be
            passed as URL parameters.  Optional.

        :type timeout: int
        :param timeout: API command timeout. When None, it will use the default
        timeout.  Optional.

        :type return_type: str
        :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by
            default).

        :rtype: dict, str
        :returns: A dictionary or JSON data set as a string depending on
            return_type parameter.
        """
        return self.call_api(method="DELETE", path=path, host=host, port=port,
                             key=key, secure=secure, body=body,
                             parameters=parameters, url_encode=url_encode,
                             timeout=timeout, return_type=return_type)

    def put_api(self, path, host=None, port=None, key=None, url_encode=False,
                secure=None, body=None, parameters=None, timeout=None,
                return_type=None):
        """
        Makes the actual PUT call to the Zadara API endpoint.  If host, key,
        and/or secure are set as None, the instance variables will be used as
        default values.

        Zadara supports both JSON and XML for its API, but please note that
        this module uses and expects JSON.

        :type path: str
        :param path: The path of the API endpoint, for example:
            '/api/vpsas.json'.  Required.

        :type host: str
        :param host: The hostname or IP address of the Zadara API.  This
            should be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.  Required.

        :type port: int
        :param port: The port for the API endpoint.  If set to None, the
            default port for the HTTP mode will be used (80 for HTTP, 443 for
            HTTPS).  Optional.

        :type key: str
        :param key: The API key for the connecting user.  Required.

        :type url_encode: bool
        :param url_encode: True iff encode using urlencode

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS,
            otherwise HTTP will be used.  Required.

        :type body: Dict
        :param body: For POST calls, a body should be supplied that *only*
            contains a valid JSON data set.  No "key" should be supplied for
            this value.  Optional.

        :type parameters: dict
        :param parameters: A Python dictionary of key value pairs that will be
            passed as URL parameters.  Optional.

        :type timeout: int
        :param timeout: API command timeout. When None, it will use the default
        timeout.  Optional.

        :type return_type: str
        :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by
            default).

        :rtype: dict, str
        :returns: A dictionary or JSON data set as a string depending on
            return_type parameter.
        """
        return self.call_api(method="PUT", path=path, host=host, port=port,
                             key=key, secure=secure, body=body,
                             url_encode=url_encode, parameters=parameters,
                             timeout=timeout, return_type=return_type)

    def call_api(self, method, path, host=None, port=None, key=None,
                 url_encode=False, secure=None, body=None, parameters=None,
                 timeout=None, return_type=None):
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
        :param host: The hostname or IP address of the Zadara API.  This
            should be passed directly instead of part of a URL.  e.g.
            'vsa-00000578-aws.zadaravpsa.com', not
            'https://vsa-00000578-aws.zadaravpsa.com/'.  Required.

        :type port: int
        :param port: The port for the API endpoint.  If set to None, the
            default port for the HTTP mode will be used (80 for HTTP, 443 for
            HTTPS).  Optional.

        :type key: str
        :param key: The API key for the connecting user.  Required.

        :type url_encode: bool
        :param url_encode: True iff encode using urlencode

        :type secure: bool
        :param secure: If True, the API call will be made over HTTPS,
            otherwise HTTP will be used.  Required.

        :type body: Dict
        :param body: For POST calls, a body should be supplied that *only*
            contains a valid JSON data set.  No "key" should be supplied for
            this value.  Optional.

        :type parameters: dict
        :param parameters: A Python dictionary of key value pairs that will be
            passed as URL parameters.  Optional.

        :type timeout: int
        :param timeout: API command timeout. When None, it will use the default
        timeout.  Optional.

        :type return_type: str
        :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by
            default).

        :rtype: dict, str
        :returns: A dictionary or JSON data set as a string depending on
            return_type parameter.
        """
        if timeout is None:
            timeout = self._default_timeout
        else:
            assert timeout > 0, "timeout must be a positive int type"

        session_timeout = timeout + 5

        # Validate all inputs
        if host is None:
            host = self.zadara_host

        if port is None:
            port = self.zadara_port

        if key is None:
            key = self.zadara_key

        if secure is None:
            secure = self.zadara_secure

        if port is not None:
            verify_port(port)

        # http.client can accept None port and use default, but we need to
        # define it here so debug info can be outputted later on error.
        if secure:
            if port is None:
                port = 443

            protocol = 'HTTPS'

            # Set timeout for each command
            conn = http.client.HTTPSConnection(host, port,
                                               timeout=session_timeout)
        else:
            if port is None:
                port = 80

            protocol = 'HTTP'

            # Set timeout for each command
            conn = http.client.HTTPConnection(host, port,
                                              timeout=session_timeout)

        headers = {}

        if return_type != 'raw':
            headers['Content-Type'] = "application/json"

        # Provisioning portal expects "X-Token" header, whereas VPSA expects
        # "X-Access-Key".  Just set both.
        headers['X-Access-Key'] = key
        headers['X-Token'] = key
        headers['x-auth-token'] = key

        # Ignore parameters if set to None or an empty dictionary is passed.
        if parameters:
            url = path + '?' + urlencode(parameters)
        else:
            url = path

        try:
            # URL encode for body
            if url_encode is True:
                body = urlencode(body)
            else:
                body = json.dumps(body)

            if body == 'null':
                body = None
            else:
                body['timeout'] = timeout

            # Log function
            if self._log_function:
                body_str = """'-d {}'""".format(body) if body else ''
                headers_str = "-H {}".format(" -H ".join(
                    '"{}: {}"'.format(k, v) for k, v in headers.items()))
                port_str = ":{}".format(port) if port else ''

                msg = 'curl -X {m} {hd} {b} {hs}{p}{u}'\
                    .format(m=method, hd=headers_str, b=body_str, hs=host,
                            p=port_str, u=url)

                self._log_function(msg)

            conn.request(method, url, headers=headers, body=body)
            response = conn.getresponse()
        except BaseException as exc:
            raise OSError('Could not connect to {0} on port {1} via {2}: {3}'.
                          format(host, port, protocol, str(exc)))

        # Support 201 - Created HTTP RC
        if response.status not in [200, 302, 201]:
            conn.close()
            raise RuntimeError(FAILURE_RESPONSE.format(response.status,
                                                       response.reason))

        data = response.read()

        conn.close()

        if return_type == 'raw':
            return data

        if return_type == 'json':
            return data.decode('UTF-8')

        api_return_dict = json.loads(data.decode('UTF-8'))

        if 'status-msg' in api_return_dict:
            raise RuntimeError('A general API error was returned: "{0}".'
                               .format(api_return_dict['status-msg']))

        if 'message' in api_return_dict:
            raise RuntimeError('A general API error was returned: "{0}".'
                               .format(api_return_dict['message']))

        if 'response' in api_return_dict:
            if 'status' in api_return_dict['response']:
                if api_return_dict['response']['status'] != 0:
                    try:
                        err = api_return_dict['response']['message']
                    except KeyError:
                        # ZIOS
                        err = api_return_dict['response']['status_msg']

                    raise RuntimeError(
                        'The API server returned an error: "{0}".'.format(err))

        return api_return_dict
