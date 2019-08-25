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
from zadarapy.validators import verify_start_limit_sort_severity, \
    verify_start_limit


def get_logs(session, severity, attr_key, attr_value, start=None, limit=None,
             return_type=None, **kwargs):
    """
    Retrieves event logs from ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type severity: int
    :param severity: If set to None, all logs are returned.  If set to an
        integer, only messages for that severity are returned.  For example,
        critical messages have a 3 severity while warning messages have a 4
        severity.  Optional (will bet set to None by default).

    :type attr_key: str
    :param attr_key: Attribute key to get

    :type attr_value: str
    :param attr_value: Attribute value to get

    :type start: int
    :param start: The offset to start displaying logs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of logs to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    list_more_options = [('severity', severity),
                         ('attr_key', attr_key),
                         ('attr_value', attr_value)]

    parameters = verify_start_limit(start, limit, list_more_options)

    path = '/api/messages.json'
    body_values = {}

    return session.get_api(path=path, parameters=parameters, body=body_values,
                           return_type=return_type, **kwargs)


def get_access_logs(session, sort='DESC', severity=None, start=None,
                    limit=None, return_type=None, **kwargs):
    """
    Retrieves access logs from the ZIOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type sort: str
    :param sort: If set to 'DESC', logs will be returned newest first.  If set
        to 'ASC', logs are returned oldest first.  Optional (set to 'DESC' by
        default).

    :type severity: int
    :param severity: If set to None, all logs are returned.  If set to an
        integer, only messages for that severity are returned.  For example,
        critical messages have a 3 severity while warning messages have a 4
        severity.  Optional (will bet set to None by default).

    :type start: int
    :param start: The offset to start displaying logs from.  Optional.

    :type: limit: int
    :param limit: The maximum number of logs to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit_sort_severity(start, limit, sort, severity)
    path = "/api/access_logs.json"
    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)
