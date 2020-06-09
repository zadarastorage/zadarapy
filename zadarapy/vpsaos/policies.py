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
from zadarapy.validators import verify_start_limit, verify_field, verify_capacity

def get_all_policies(session, start=None, limit=None, return_type=None,
                     **kwargs):
    """
    Retrieves details for all Storage policies in the VPSAOS.

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
    parameters = verify_start_limit(start, limit)
    path = '/api/zios/policies.json'
    return session.get_api(path=path, parameters=parameters,
                           secure=True, return_type=return_type, **kwargs)


def get_policy(session, policy_name, return_type=None, **kwargs):
    """
    Retrieves details for a single virtual controller for the VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(policy_name, "policy_name")
    path = '/api/zios/policies/{0}.json'.format(policy_name)
    return session.get_api(path=path, secure=True, return_type=return_type,
                           **kwargs)


def set_default_policy(session, policy_name, return_type=None, **kwargs):
    """
    Set the policy as a default policy

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/zios/policies/{0}/set_default.json'.format(policy_name)

    return session.post_api(path=path, secure=True, return_type=return_type,
                            **kwargs)


def update_storage_policy(session, policy_id, full_description, gb_per_month_cost, return_type=None):
    """
    Set the policy as a default policy

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_id: str
    :param policy_id: ID of the storage policy.  Required.

    :type full_description: str
    :param full_description: Description of storage policy.  Required.

    :type gb_per_month_cost: float
    :param gb_per_month_cost: Cost per month for GB.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
           will return a JSON string.  Otherwise, it will return a Python
           dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
              return_type parameter.
    """
    path = '/api/zios/policies/{0}.json'.format(policy_id)
    body_values = {'full_description': full_description, 'gb_per_month_cost': gb_per_month_cost}
    return session.put_api(path=path, body=body_values, return_type=return_type)


def delete_drives_from_policy(session, policy_name, drive_type, quantity, return_type=None, **kwargs):
    """
    Remove drives from storage policy

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type drive_type: str
    :param drive_type: Type of the drives the user wish to remove from the policy.  Required.
           e.g SAS_300_GB

    :type quantity: int
    :param quantity: Quantity of the drives the user wish to remove from the policy.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/zios/policies/{0}/drives.json'.format(policy_name)
    drive_type = verify_field(drive_type, 'drive_type')
    quantity = verify_capacity(quantity, 'quantity')

    body = {"drives":[{"type": drive_type , "quantity": quantity}]}

    return session.delete_api(path=path, body=body, secure=True, return_type=return_type, **kwargs)


def capacity_over_time(session, policy_name, policy_display_name, interval, return_type=None, **kwargs):
    """
    Retrieves details of storage policy capacity over time

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type policy_display_name: str
    :param policy_display_name: The Policy display name 'name' value as returned by
        get_all_policies, for example '2-Way-Protection'.  Required.

    :type interval: int
    :param interval: Time interval in seconds between each beat in Unix time
        of the capacity.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(policy_name, "policy_name")
    data = {"interval": interval, "name": policy_display_name}

    path = '/api/zios/policies/{0}/capacity_over_time.json'.format(policy_name)
    return session.get_api(path=path, secure=True, body=data, return_type=return_type, **kwargs)


def iops(session, policy_name, policy_display_name, interval, service, return_type=None, **kwargs):
    """
    Retrieves details of storage policy iops over time

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type policy_display_name: str
    :param policy_display_name: The Policy display name 'name' value as returned by
        get_all_policies, for example '2-Way-Protection'.  Required.

    :type interval: int
    :param interval: Time interval in seconds between each beat in Unix time
        of the capacity.  Required.

    :type service: str
    :param service: Mentions if this is for backend or frontend.
           Possible values are 'object' for backend or 'proxy' for frontend.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(policy_name, "policy_name")
    data = {"interval": interval, "name": policy_display_name, "service": service}

    path = '/api/zios/policies/{0}/iops.json'.format(policy_name)
    return session.get_api(path=path, secure=True, body=data, return_type=return_type, **kwargs)


def throughput(session, policy_name, policy_display_name, interval, service, return_type=None, **kwargs):
    """
    Retrieves details of storage policy throughput over time

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type policy_display_name: str
    :param policy_display_name: The Policy display name 'name' value as returned by
        get_all_policies, for example '2-Way-Protection'.  Required.

    :type interval: int
    :param interval: Time interval in seconds between each beat in Unix time
        of the capacity.  Required.

    :type service: str
    :param service: Mentions if this is for backend or frontend.
           Possible values are 'object' for backend or 'proxy' for frontend.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(policy_name, "policy_name")
    data = {"interval": interval, "name": policy_display_name, "service": service}

    path = '/api/zios/policies/{0}/throughput.json'.format(policy_name)
    return session.get_api(path=path, secure=True, body=data, return_type=return_type, **kwargs)


def latency(session, policy_name, policy_display_name, interval, service, return_type=None, **kwargs):
    """
    Retrieves details of storage policy latency over time

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_name: str
    :param policy_name: The Policy name 'name' value as returned by
        get_all_policies.  Required.

    :type policy_display_name: str
    :param policy_display_name: The Policy display name 'name' value as returned by
        get_all_policies, for example '2-Way-Protection'.  Required.

    :type interval: int
    :param interval: Time interval in seconds between each beat in Unix time
        of the capacity.  Required.

    :type service: str
    :param service: Mentions if this is for backend or frontend.
           Possible values are 'object' for backend or 'proxy' for frontend.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_field(policy_name, "policy_name")
    data = {"interval": interval, "name": policy_display_name, "service": service}

    path = '/api/zios/policies/{0}/latency.json'.format(policy_name)
    return session.get_api(path=path, secure=True, body=data, return_type=return_type, **kwargs)
