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


def get_logs(session, sort='DESC', severity=None, start=None, limit=None,
             return_type=None):
    """
    Retrieves logs from the VPSA.

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
    if sort not in ['DESC', 'ASC']:
        raise ValueError('"{0}" is not a valid sort parameter.  Allowed '
                         'values are: "DESC" or "ASC"'.format(sort))

    if sort == 'ASC':
        sort = '[{"property":"msg-time","direction":"ASC"}]'
    else:
        sort = '[{"property":"msg-time","direction":"DESC"}]'

    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/messages.json'

    parameters = {k: v for k, v in (('sort', sort), ('severity', severity),
                                    ('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
