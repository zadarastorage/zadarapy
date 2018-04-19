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


import json
from zadarapy.validators import is_valid_controller_id


def get_all_controllers(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all virtual controllers for the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying controllers from.  Optional.

    :type: limit: int
    :param limit: The maximum number of controllers to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
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
    path = '/api/vcontrollers.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def failover_controller(session, confirm, force='NO', return_type=None):
    """
    Initiates a failover of the current active controller to the standby
    controller.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type confirm: bool
    :param confirm: If True, failover will be performed.  This is a safeguard
        for this function since it requires no other arguments.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSA to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not confirm:
        raise ValueError('The confirm parameter is not set to True - '
                         'failover will not be performed.')

    body_values = {}

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/vcontrollers/failover.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_controller_performance(session, controller_id, interval=1,
                               return_type=None):
    """
    Retrieves metering statistics for the controller for the specified
    interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type controller_id: str
    :param controller_id: The virtual controller 'name' value as returned by
        get_all_controllers.  For example: 'vsa-00000001-vc-0'.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_controller_id(controller_id):
        raise ValueError('{0} is not a valid virtual controller ID.'
                         .format(controller_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/vcontrollers/{0}/performance.json'.format(controller_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_cache_performance(session, interval=1, return_type=None):
    """
    Retrieves metering statistics for the VPSA's SSD cache for the specified
    interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/vcontrollers/cache_performance.json'

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_cache_stats(session, interval=1, return_type=None):
    """
    Retrieves usage statistics for the VPSA's SSD cache for the specified
    interval.  Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/vcontrollers/cache_stats.json'

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
