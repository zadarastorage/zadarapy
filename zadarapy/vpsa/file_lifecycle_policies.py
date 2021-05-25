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


from zadarapy.validators import verify_boolean, verify_lc_action, verify_flc_policy_id


def get_all_flc_policies(session, volume_name=None, first=None, number=None,
                        order_by=None, descend=None, return_type=None, **kwargs):
    """
    Retrieves details for all file lifecycle policies.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_name: str
    :param volume_name: The volume to filter policies by.  Optional.

    :type first: int
    :param first: The offset to start displaying file lifecycle policies from.  Optional.

    :type: number: int
    :param number: The maximum number of file lifecycle policies to return.  Optional.

    :type: order_by: str
    :param order_by: Order policies by given attribute.  Optional.

    :type: descend: str
    :param descend: Controls order direction (YES | NO).  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    descend = verify_boolean(descend, 'descend')

    list_more_options = [('volume_name', volume_name), ('order_by', order_by), ('descend', descend)]

    parameters = verify_start_limit(first, number, list_more_options)
    parameters['first'] = parameters.pop('start')
    parameters['number'] = parameters.pop('limit')

    path = '/api/flc_policies.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_flc_policy(session, lc_policy_id, return_type=None, **kwargs):
    """
    Retrieves details for an existing file lifecycle policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_flc_policy_id(lc_policy_id)

    path = '/api/flc_policies/{}.json'.format(lc_policy_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_all_flc_policies_rules(session, volume_name=None, policy_name=None, first=None,
                            number=None, return_type=None, **kwargs):
    """
    Retrieves details for the rules attaching file lifecycle policies to volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_name: str
    :param volume_name: Retrieve only rules relevant to the given volume.  Optional.

    :type policy_name: str
    :param policy_name: Retrieve only rules relevant to the given policy.  Optional.

    :type first: int
    :param first: The offset to start displaying file lifecycle policies from.  Optional.

    :type: number: int
    :param number: The maximum number of file lifecycle policies to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    list_more_options = [('volume_name', volume_name), ('policy_name', policy_name)]

    parameters = verify_start_limit(first, number, list_more_options)
    parameters['first'] = parameters.pop('start')
    parameters['number'] = parameters.pop('limit')

    path = '/api/flc_policies/rules.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)

def create_flc_policy(session, display_name, file_selection_criteria, lc_action,
                    enabled=None,dry_run=None, use_recycle_bin=None, whitelist_paths=None,
                    blacklist_paths=None, dest_obs_name=None, return_type=None, **kwargs):
    """
    Create a new file lifecycle policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: Policy name.  Required.

    :type file_selection_criteria: str
    :param file_selection_criteria: The criteria by which the policy files will be selected.
        Should be in a MongoDB $match aggregation format.  Required.

    :type lc_action: str
    :param lc_action: The action that the policy performs on the selected files (archive | expire).  Required.

    :type: enabled: str
    :param enabled: Controls enablement of the policy after it is created (YES | NO).  Optional.

    :type: dry_run: str
    :param dry_run: When the policy is in dry run mode,
        it'll only print its actions to the log instead of actually performing them (YES | NO).  Optional.

    :type: use_recycle_bin: str
    :param use_recycle_bin: When using recycle bin,
        files that are handled by the policy are also copied to the recycle bin (YES | NO).  Optional.

    :type whitelist_paths: str
    :param whitelist_paths: Comma delimited list of paths that the policy should only run on them.  Optional.

    :type blacklist_paths: str
    :param blacklist_paths: Comma delimited list of paths that the policy should not run on.  Optional.

    :type dest_obs_name: str
    :param dest_obs_name: Destination object storage to archive files to. Relevant only for archive policy.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    lc_action = verify_lc_action(lc_action)
    enabled = verify_boolean(enabled, 'enabled')
    dry_run = verify_boolean(dry_run, 'dry_run')
    use_recycle_bin = verify_boolean(use_recycle_bin, 'use_recycle_bin')
    body_values = {'display_name': display_name, 'file_selection_criteria': file_selection_criteria,
                    'lc_action': lc_action, 'enabled': enabled, 'dry_run': dry_run,
                    'use_recycle_bin': use_recycle_bin, 'whitelist_paths': whitelist_paths,
                    'blacklist_paths': blacklist_paths, 'dest_obs_name': dest_obs_name}

    path = '/api/flc_policies.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_flc_policy(session, lc_policy_id, display_name=None, file_selection_criteria=None,
                    lc_action=None, enabled=None,dry_run=None, use_recycle_bin=None,whitelist_paths=None,
                    blacklist_paths=None, dest_obs_name=None, return_type=None, **kwargs):
    """
    Updates an existing file lifecycle policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type display_name: str
    :param display_name: Policy name.  Optional.

    :type file_selection_criteria: str
    :param file_selection_criteria: The criteria by which the policy files will be selected.
        Should be in a MongoDB $match aggregation format.  Optional.

    :type lc_action: str
    :param lc_action: The action that the policy performs on the selected files (archive | expire).  Optional.

    :type: enabled: str
    :param enabled: Controls enablement of the policy after it is created (YES | NO).  Optional.

    :type: dry_run: str
    :param dry_run: When the policy is in dry run mode,
        it'll only print its actions to the log instead of actually performing them (YES | NO).  Optional.

    :type: use_recycle_bin: str
    :param use_recycle_bin: When using recycle bin,
        files that are handled by the policy are also copied to the recycle bin (YES | NO).  Optional.

    :type whitelist_paths: str
    :param whitelist_paths: Comma delimited list of paths that the policy should only run on them.  Optional.

    :type blacklist_paths: str
    :param blacklist_paths: Comma delimited list of paths that the policy should not run on.  Optional.

    :type dest_obs_name: str
    :param dest_obs_name: Destination object storage to archive files to. Relevant only for archive policy.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_flc_policy_id(lc_policy_id)
    lc_action = verify_lc_action(lc_action)
    enabled = verify_boolean(enabled, 'enabled')
    dry_run = verify_boolean(dry_run, 'dry_run')
    use_recycle_bin = verify_boolean(use_recycle_bin, 'use_recycle_bin')

    body_values = {'display_name': display_name, 'file_selection_criteria': file_selection_criteria,
                    'lc_action': lc_action, 'enabled': enabled, 'dry_run': dry_run,
                    'use_recycle_bin': use_recycle_bin, 'whitelist_paths': whitelist_paths,
                    'blacklist_paths': blacklist_paths, 'dest_obs_name': dest_obs_name}

    path = '/api/flc_policies/{}.json'.format(lc_policy_id)

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_flc_policy(session, lc_policy_id, return_type=None, **kwargs):
    """
    Delete an existing file lifecycle policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_flc_policy_id(lc_policy_id)

    path = '/api/flc_policies/{}.json'.format(lc_policy_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def update_flc_policy_scheduling(session, policy_start_time=None, policy_interval=None,
                                return_type=None, **kwargs):
    """
    Updates file lifecycle policies run time scheduling.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type policy_start_time: str
    :param policy_start_time: The start time in seconds from 00:00 AM.  Optional.

    :type policy_interval: int
    :param policy_interval: The interval in seconds between running policies.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'policy_start_time': policy_start_time, 'policy_interval': policy_interval}

    path = '/api/flc_policies/scheduling.json'

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_flc_recycle_bin(session, retention_time=None,
                                return_type=None, **kwargs):
    """
    Configures the recycle bin.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type retention_time: str
    :param retention_time: The time in seconds for retaining files in the recycle bin.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'retention_time': retention_time}

    path = '/api/flc_policies/recycle_bin.json'

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def pause_flc_policy_on_volume(session, lc_policy_id, volume_id,
                                return_type=None, **kwargs):
    """
    Pause a file lifecycle policy for a given volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by volumes.get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'volume_id': volume_id}

    path = '/api/flc_policies/{}/pause.json'.format(lc_policy_id)

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def resume_flc_policy_on_volume(session, lc_policy_id, volume_id,
                                return_type=None, **kwargs):
    """
    Resume a file lifecycle policy for a given volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by volumes.get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'volume_id': volume_id}

    path = '/api/flc_policies/{}/resume.json'.format(lc_policy_id)

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def attach_flc_policy(session, lc_policy_id, volume_id,
                        return_type=None, **kwargs):
    """
    Attach a volume to a file lifecycle policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by volumes.get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'volume_id': volume_id}

    path = '/api/flc_policies/{}/attach.json'.format(lc_policy_id)

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def detach_flc_policy(session, lc_policy_id, volume_id,
                        return_type=None, **kwargs):
    """
    Detach a volume from a file lifecycle policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type lc_policy_id: str
    :param lc_policy_id: The file lifecycle policy ID 'lc_policy_id' value as returned by
        get_all_flc_policies.  For example: 'lc-policy-00000002'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by volumes.get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'volume_id': volume_id}

    path = '/api/flc_policies/{}/detach.json'.format(lc_policy_id)

    return session.put_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
