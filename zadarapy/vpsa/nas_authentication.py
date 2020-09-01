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

from zadarapy.validators import verify_start_limit, verify_name, \
    verify_string, verify_group_name, verify_boolean, verify_field, \
    verify_not_none

__all__ = ["get_active_directory", "get_all_nas_groups", "get_all_nas_users",
           "get_nas_user", "get_nas_group",
           "create_nas_group", "create_nas_user",
           "change_nas_user_smb_password", "delete_nas_group",
           "delete_nas_user",
           "join_active_directory", "edit_active_directory",
           "leave_active_directory", "restore_active_directory", "update_active_directory_dns"]


def get_all_nas_users(session, start=None, limit=None, return_type=None,
                      **kwargs):
    """
    Retrieves details for all NAS users configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying NAS users from.  Optional.

    :type: limit: int
    :param limit: The maximum number of NAS users to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)

    path = '/api/nas/users.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_nas_user(session, username, return_type=None, **kwargs):
    """
    Retrieves details for a single NAS user.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The NAS user's username.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    username = verify_name(username)

    path = '/api/nas/users/{0}.json'.format(username)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_nas_user(session, username, nfs_uid=None, smb_password=None,
                    smb_groupname=None, return_type=None, **kwargs):
    """
    Creates a NAS user.  Either nfs_uid or smb_password (or both) must be
    specified.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The NAS user's username.  Required.

    :type nfs_uid: int
    :param nfs_uid: When using NFS, the UID for the NFS user.  This should
        correspond to the user's UID in the client system's /etc/passwd file.
        "root" and "nobody" users are statically defined by the VPSA.
        Optional.

    :type smb_password: str
    :param smb_password: When using SMB, the password to assign to the SMB
        user.  This is only necessary when not using guest access on the
        volume and when not integrated with an Active Directory server.
        Optional.

    :type smb_groupname: str
    :param smb_groupname: When using SMB, the primary group for the user can
        optionally be designated with the NAS group designated here.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    username = verify_name(username)

    body_values = {'username': username}

    if nfs_uid is None and smb_password is None:
        raise ValueError('Either the nfs_uid or smb_password (or both)'
                         'parameters must be specified.')

    if nfs_uid is not None:
        if nfs_uid < 1 or nfs_uid > 65533:
            raise ValueError('"{0}" is not a valid NFS UID.'.format(nfs_uid))

        body_values['nfs_uid'] = nfs_uid

    if smb_password is not None:
        body_values['password'] = smb_password

    if smb_groupname is not None:
        body_values['groupname'] = smb_groupname

    path = '/api/nas/users.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def change_nas_user_smb_password(session, username, smb_password,
                                 return_type=None, **kwargs):
    """
    Changes the SMB password for a NAS user.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The NAS user's username.  Required.

    :type smb_password: str
    :param smb_password: Changes the SMB password to this value.  Pass an
        empty string to remove the SMB password.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    username = verify_name(username)
    verify_string(smb_password)

    body_values = {'password': smb_password}

    path = '/api/nas/users/{0}/password.json'.format(username)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_nas_user(session, username, return_type=None, **kwargs):
    """
    Deletes a NAS user.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: The NAS user's username.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    username = verify_name(username)

    path = '/api/nas/users/{0}.json'.format(username)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_all_nas_groups(session, start=None, limit=None, return_type=None,
                       **kwargs):
    """
    Retrieves details for all NAS groups configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying NAS groups from.  Optional.

    :type: limit: int
    :param limit: The maximum number of NAS groups to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)

    path = '/api/nas/groups.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_nas_group(session, groupname, return_type=None, **kwargs):
    """
    Retrieves details for a single NAS group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type groupname: str
    :param groupname: The NAS group's groupname.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    groupname = verify_name(groupname)

    path = '/api/nas/groups/{0}.json'.format(groupname)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_nas_group(session, groupname, nfs_gid=None, smb='NO',
                     return_type=None, **kwargs):
    """
    Creates a NAS user.  Either nfs_gid must be specified or smb must be set
    to 'YES' (or both).

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type groupname: str
    :param groupname: The NAS group's groupname.  Required.

    :type nfs_gid: int
    :param nfs_gid: When using NFS, the GID for the NFS user.  This should
        correspond to the group's GID in the client system's /etc/groups file.
        "root" and "nogroup" groups are statically defined by the VPSA.
        Optional.

    :type smb: str
    :param smb: When using SMB, if set to 'YES', this group will be usable by
        SMB/CIFS clients.  If set to 'NO', this group won't be usable by
        SMB/CIFS clients.  Optional (set to 'NO' by default).

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    groupname = verify_group_name(groupname)
    smb = verify_boolean(smb, "smb")
    _check_nfs_gid(nfs_gid, smb)

    body_values = {'group_name': groupname, 'smb': smb}

    if nfs_gid is not None:
        body_values['nfs_gid'] = nfs_gid

    path = '/api/nas/groups.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_nas_group(session, groupname, return_type=None, **kwargs):
    """
    Deletes a NAS group.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type groupname: str
    :param groupname: The NAS group's groupname.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    groupname = verify_group_name(groupname)

    path = '/api/nas/groups/{0}.json'.format(groupname)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_active_directory(session, return_type=None, **kwargs):
    """
    Retrieves details for Active Directory domains configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/active_directory.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def join_active_directory(session, display_name, username, password,
                          dns_domain, netbios_name, dns,
                          uid_range_low=None, uid_range_high=None, return_type=None,
                          **kwargs):
    """
    Joins the VPSA to an Active Directory domain.  After this is done, for all
    NAS SMB shares that should use Active Directory to resolve users and
    groups, be sure to set those shares to use enhanced ACLs for AD objects to
    work correctly.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the Active Directory.  For
        example: 'MyCompany Active Directory'.  May not contain a single quote
        (') character.  Required.

    :type username: str
    :param username: A username that has permission to join the Active
        Directory (typically, part of the "Domain Admins" group).  Required.

    :type password: str
    :param password: The password for the Active Directory "username".
        Required.

    :type dns_domain: str
    :param dns_domain: The DNS domain name for the Active Directory domain to
        be joined.  For example: 'ad.mycompany.com'.  Required.

    :type netbios_name: str
    :param netbios_name: The NetBIOS name for the Active Directory domain.
        For example: 'MYCOMPANY'.  Required.

    :type dns: list, str
    :param dns: A Python list or comma separated string of up to three DNS
        server IP addresses for the Active Directory domain.  Must have at
        least one DNS IP address defined.  The address must be routable by the
        VPSA.  Required.

    :type uid_range_low: int
    :param uid_range_low: Low range ID.  Optional.

    :type uid_range_high: int
    :param uid_range_high: High range ID.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    display_name = verify_field(display_name, display_name)
    verify_not_none(username, 'username')
    verify_not_none(password, 'password')
    verify_not_none(netbios_name, 'netbios_name')
    _check_dns(dns)

    body_values = {'adserver': display_name, 'username': username,
                   'password': password, 'realm': dns_domain,
                   'workgroup': netbios_name, 'dns': dns}

    if uid_range_low is not None:
        body_values['uid_range_low'] = uid_range_low
    if uid_range_high is not None:
        body_values['uid_range_high'] = uid_range_high

    path = '/api/active_directory.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_active_directory_dns(session, dns, return_type=None, **kwargs):
    """
    Updates the DNS servers for the previous joined Active Directory.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type dns: list, str
    :param dns: A Python list or comma separated string of up to three DNS
        server IP addresses for the Active Directory domain.  Must have at
        least one DNS IP address defined.  The address must be routable by the
        VPSA.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    _check_dns(dns)
    body_values = {'dns': dns}

    path = '/api/active_directory/dns.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def edit_active_directory(session, dns, dns_lookup_realm=None, dns_lookup_kdc=None, realm_kdc_servers=None,
                          add_to_ignored_domains=None, remove_from_ignored_domains=None, return_type=None, **kwargs):
    """
    Updates the DNS servers for the previous joined Active Directory.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type dns: list, str
    :param dns: A Python list or comma separated string of up to three DNS
        server IP addresses for the Active Directory domain.  Must have at
        least one DNS IP address defined.  The address must be routable by the
        VPSA.  Required.
    :type dns_lookup_realm: str
    :param dns_lookup_realm: Set auto realm lookup. Can be 'YES' or 'NO'.  Optional
    :type dns_lookup_kdc: str
    :param dns_lookup_kdc: Set auto realm kdc lookup. Can be 'YES' or 'NO'.  Optional
    :type realm_kdc_servers: Dict[str, List[str]]
    :param realm_kdc_servers: Set realm kdc servers.  Optional
        e.g. :{"realm1": ["kdc1","kdc2"], "realm2": ""}
    :type add_to_ignored_domains: List[str]
    :param add_to_ignored_domains: Add domains to ignored domains.  Optional
        Domain NetBIOS name should be used as input. e.g ["kdc1","kdc2"]
    :type remove_from_ignored_domains: List[str]
    :param remove_from_ignored_domains: Remove domains from ignored domains.  Optional
        Domain NetBIOS name should be used as input. e.g ["kdc1","kdc2"]
    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    _check_dns(dns)
    body_values = {'dns': dns}
    if dns_lookup_realm is not None:
        body_values['dns_lookup_realm'] = verify_boolean(dns_lookup_realm, "dns_lookup_realm")

    if dns_lookup_kdc is not None:
        body_values['dns_lookup_kdc'] = verify_boolean(dns_lookup_kdc, "dns_lookup_kdc")

    if realm_kdc_servers is not None:
        body_values['realm_kdc_servers'] = realm_kdc_servers

    if add_to_ignored_domains is not None:
        body_values['add_to_ignored_domains'] = add_to_ignored_domains

    if remove_from_ignored_domains is not None:
        body_values['remove_from_ignored_domains'] = remove_from_ignored_domains

    path = '/api/active_directory/edit.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def leave_active_directory(session, username, password, keep="NO", return_type=None,
                           **kwargs):
    """
    Makes the VPSA leave the previously joined Active Directory.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: A username that has permission to leave the Active
        Directory (typically, part of the "Domain Admins" group).  Required.

    :type password: str
    :param password: The password for the Active Directory "username".
        Required.

    :type keep: str
    :param keep: Should the VPSA keep the active directory.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_not_none(username, "username")
    verify_not_none(password, "password")
    keep = verify_boolean(keep, "keep")

    body_values = {'username': username, 'password': password, "keep": keep, "force": "YES"}

    path = '/api/active_directory/reset.json'

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def restore_active_directory(session, username, password, force='YES',
                             return_type=None, **kwargs):
    """
    Makes the VPSA restore the previously joined Active Directory.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type username: str
    :param username: A username that has permission to leave the Active
        Directory (typically, part of the "Domain Admins" group).  Required.

    :type password: str
    :param password: The password for the Active Directory "username".
        Required.

    :type force: str
    :param force: Force active directory restore. Can be only 'YES' or 'NO'.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_not_none(username, "username")
    verify_not_none(password, "password")
    force = verify_boolean(force, "force")

    body_values = {'username': username, 'password': password, 'force': force}

    path = '/api/active_directory/restore.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


"""
Private functions
"""


def _check_nfs_gid(nfs_gid, smb):
    """

    :type nfs_gid: int
    :param nfs_gid: NFS GID parameter

    :type smb: str
    :param smb: SMB parameter

    :raises ValueError: invalid NFS GID or SMB
    """
    if nfs_gid is None and smb not in ['YES', 'NO']:
        raise ValueError('Either the "nfs_gid" must be defined or "smb" must '
                         'be set to "YES".')

    if nfs_gid is not None:
        if nfs_gid < 1 or nfs_gid > 65533:
            raise ValueError('"{0}" is not a valid NFS GID.'.format(nfs_gid))


def _check_dns(dns):
    """
    Check DNS

    :type dns: str
    :param dns: DNS address

    :rtype: str
    :return: Fixed DNS format

    :raises: ValueError: Invalid DNS parameter
    """
    if type(dns) is str:
        dns = [x.strip() for x in dns.split(',')]

    if type(dns) is not list:
        raise ValueError('The DNS parameter must be a Python list.')
