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
from zadarapy.validators import verify_start_limit, verify_load_balancer_name

def get_load_balancer_groups(session, start=None, limit=None, return_type=None,
                     **kwargs):
    """
    Get a list of Load Balancer Groups.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying accounts from.  Optional.

    :type: limit: int
    :param limit: The maximum number of accounts to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start=start, limit=limit)

    path = "/api/zios/load_balancer_groups.json"
    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_load_balancer_group(session, name, return_type=None, **kwargs):
    """
    Get a single Load Balancer Group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: load balancer name (id).  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_load_balancer_name(name=name)

    path = "/api/zios/load_balancer_groups/{0}.json".format(name)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_iop_metering_load_balancer_group(session, name, service, interval=None, count=None, return_type=None, **kwargs):
    """
    Shows IOPs metering of a load balancer group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: load balancer name (id).  Required.

    :type service: str
    :param service: Proxy.  Required.

    :type interval: int

    :type count: int

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_load_balancer_name(name=name)

    body_values = {"service": service}

    if interval is not None:
        body_values["interval"] = interval
    if count is not None:
        body_values["count"] = count

    path = "/api/zios/load_balancer_groups/{0}/iops.json?service=proxy".format(name)

    return session.get_api(path=path, body_values=body_values, return_type=return_type, **kwargs)


def get_latency_metering_load_balancer_group(session, name, service,
                                             interval=None, count=None, return_type=None, **kwargs):
    """
    Shows latency metering of a load balancer group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: load balancer name (id).  Required.

    :type service: str
    :param service: Proxy.  Required.

    :type interval: int

    :type count: int

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_load_balancer_name(name=name)

    body_values = {"service": service}

    if interval is not None:
        body_values["interval"] = interval
    if count is not None:
        body_values["count"] = count

    path = "/api/zios/load_balancer_groups/{0}/latency.json?service=proxy".format(name)

    return session.get_api(path=path, body_values=body_values, return_type=return_type, **kwargs)


def get_throughput_metering_load_balancer_group(session, name, service,
                                                interval=None, count=None, return_type=None, **kwargs):
    """
    Shows throughput metering of a load balancer group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: load balancer name (id).  Required.

    :type service: str
    :param service: Proxy.  Required.

    :type interval: int

    :type count: int

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_load_balancer_name(name=name)

    body_values = {"service": service}

    if interval is not None:
        body_values["interval"] = interval
    if count is not None:
        body_values["count"] = count

    path = "/api/zios/load_balancer_groups/{0}/throughput.json?service=proxy".format(name)

    return session.get_api(path=path, body_values=body_values, return_type=return_type, **kwargs)
