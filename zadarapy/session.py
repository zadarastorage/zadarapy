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
from urllib.parse import urlencode

import requests
from future.standard_library import install_aliases

install_aliases()

import configparser
import json
import os
from zadarapy.validators import verify_port

DEFAULT_TIMEOUT = 15

FAILURE_RESPONSE = 'API server did not return an HTTP 200, 201 or 302 ' \
                   'response. Status "{0} {1}" was returned instead.  ' \
                   'Please investigate.'

DICT_SECURED_DETAILS = {True: (443, "HTTPS"),
                        False: (80, "HTTP")}


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

    def get_api(self, path, host=None, port=None, key=None,
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
                             parameters=parameters,
                             timeout=timeout, return_type=return_type)

    def post_api(self, path, host=None, port=None, key=None,
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
                             parameters=parameters,
                             timeout=timeout, return_type=return_type)

    def delete_api(self, path, host=None, port=None, key=None,
                   secure=None, body=None,
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
                             parameters=parameters,
                             timeout=timeout, return_type=return_type)

    def put_api(self, path, host=None, port=None, key=None,
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
                             parameters=parameters,
                             timeout=timeout, return_type=return_type)

    def call_api(self, method, path, host=None, port=None, key=None,
                 secure=None, body=None, parameters=None,
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
        host = host or self.zadara_host
        port = port or self.zadara_port
        key = key or self.zadara_key
        secure = secure or self.zadara_secure
        path = path if path.startswith("/") else "/{}".format(path)
        session_port, protocol = DICT_SECURED_DETAILS[secure]

        if port:
            verify_port(port)
        else:
            port = session_port

        api_url = "{}://{}:{}{}".format(protocol.lower(), host, port, path)

        headers = self._get_headers(key=key, return_type=return_type)
        parameters = self._get_parameters(parameters=parameters)
        body = self._get_body(body=body, timeout=timeout)

        self._print(method=method, body=body, headers=headers,
                    params=parameters, api_url=api_url,
                    max_time=session_timeout)

        body = json.dumps(body) if body else body

        try:
            with requests.Session() as session:
                session.headers.update(headers)

                response = session.request(method, url=api_url,
                                           params=parameters,
                                           data=body, headers=headers,
                                           timeout=session_timeout,
                                           verify=True)
        except requests.exceptions.RequestException:
            raise OSError('Could not connect to {0} on port {1} via {2}'.
                          format(host, port, protocol))
        except BaseException as e:
            raise OSError('HTTP request failed: {}'.format(str(e)))

        if response.status_code not in [200, 302, 201]:
            raise RuntimeError(FAILURE_RESPONSE.format(response.status_code,
                                                       response.reason))

        data = response.content

        if return_type == 'raw':
            return data

        if return_type == 'json':
            return data.decode('UTF-8')

        api_return_dict = json.loads(data.decode('UTF-8'))

        if 'status-msg' in api_return_dict:
            raise RuntimeError('A general API error was returned: "{0}".'
                               .format(api_return_dict['status-msg']))

        if 'message' in api_return_dict:
            if 'status' in api_return_dict and api_return_dict['status'] != "success":
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

    @staticmethod
    def _get_headers(key, return_type):
        """
        Get HTTP request headers
         - Provisioning portal expects "X-Token" header,
         - VPSA expects "X-Access-Key".
         - We set them both.

        :param key: Access key
        :param return_type: Return type. 'raw', 'json' or 'xml'
        :return: headers dictionary
        :rtype: dict
        """
        headers = {'X-Access-Key': key, 'X-Token': key, 'x-auth-token': key}
        if return_type != 'raw':
            # Can be json or XML
            headers['Content-Type'] = "application/json"

        return headers

    @staticmethod
    def _get_parameters(parameters):
        """
        :param parameters: Parameters
        :return: Encoded parameters else None
        """
        if parameters:
            assert isinstance(parameters, dict), \
                "Invalid 'params' type. Must be a dictionary type. ({})" \
                 .format(type(parameters))
        return parameters

    @staticmethod
    def _get_body(body, timeout):
        """

        :param body: Body to parse
        :param timeout: API command timeout
        :return: Body to send to request
        """
        body = body or {}
        assert isinstance(body, dict), \
            "Invalid 'body' type. Must be a dictionary type. ({})" \
                .format(type(body))

        body['timeout'] = timeout
        return body

    def _print(self, body, headers, method, params, api_url, max_time):
        """
        Print the command in curl format

        :param body: HTTP request body
        :param headers: HTTP request headers
        :param method: HTTP request method: GET, POST, DELETE, PUT
        :param params: HTTP request parameters
        :param api_url: HTTP request URL
        :param max_time: Maximum  time  in  seconds that you allow
         the whole operation to take.
        """
        if not self._log_function:
            return

        body_str = ''
        if body:
            body_str = "-d '{%s'}" % ", ".join('"{}":"{}"'.format(k, v)
                                               for k, v in body.items())

        headers_str = ''
        if headers:
            headers_str = "-H {}".format(
                " -H ".join('"{}:{}"'.format(k, v)
                            for k, v in headers.items()))

        if params:
            api_url += "?{}".format(urlencode(params))

        msg = "curl --max-time {mx} -X {m} {hd} {b}  '{u}'" \
            .format(m=method.upper(), hd=headers_str, b=body_str, u=api_url,
                    mx=max_time)

        self._log_function(msg)
