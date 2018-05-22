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


from future.standard_library import install_aliases
install_aliases()

import json
from urllib.parse import quote
from zadarapy.validators import is_valid_field


def get_all_nas_users(session, start=None, limit=None, return_type=None):
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
    path = '/api/nas/users.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_nas_user(session, username, return_type=None):
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
    username = quote(username.strip())

    method = 'GET'
    path = '/api/nas/users/{0}.json'.format(username)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_nas_user(session, username, nfs_uid=None, smb_password=None,
                    smb_groupname=None, return_type=None):
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
    body_values = {}

    if username in ['root', 'nobody']:
        raise ValueError('The root and nobody users are assigned on every '
                         'VPSA')

    body_values['username'] = quote(username.strip())

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

    method = 'POST'
    path = '/api/nas/users.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def change_nas_user_smb_password(session, username, smb_password,
                                 return_type=None):
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
    body_values = {}

    username = quote(username.strip())

    if type(smb_password) is not str:
        raise ValueError('A string must be passed for smb_password.')

    body_values['password'] = smb_password

    method = 'POST'
    path = '/api/nas/users/{0}/password.json'.format(username)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_nas_user(session, username, return_type=None):
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
    username = quote(username.strip())

    if username in ['root', 'nobody']:
        raise ValueError('The root and nobody users cannot be deleted.')

    method = 'DELETE'
    path = '/api/nas/users/{0}.json'.format(username)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_all_nas_groups(session, start=None, limit=None, return_type=None):
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
    path = '/api/nas/groups.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_nas_group(session, groupname, return_type=None):
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
    groupname = quote(groupname.strip())

    method = 'GET'
    path = '/api/nas/groups/{0}.json'.format(groupname)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_nas_group(session, groupname, nfs_gid=None, smb='NO',
                     return_type=None):
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
    body_values = {}

    if groupname in ['root', 'nogroup']:
        raise ValueError('The root and nogroup group are assigned on every '
                         'VPSA')

    body_values['groupname'] = quote(groupname.strip())

    smb = smb.upper()

    if nfs_gid is None and smb not in ['YES', 'NO']:
        raise ValueError('Either the "nfs_gid" must be defined or "smb" must '
                         'be set to "YES".')

    if nfs_gid is not None:
        if nfs_gid < 1 or nfs_gid > 65533:
            raise ValueError('"{0}" is not a valid NFS GID.'.format(nfs_gid))

        body_values['nfs_gid'] = nfs_gid

    if smb not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid smb parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(smb))

    body_values['smb'] = smb

    method = 'POST'
    path = '/api/nas/groups.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_nas_group(session, groupname, return_type=None):
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
    groupname = quote(groupname.strip())

    if groupname in ['root', 'nogroup']:
        raise ValueError('The root and nogroup group are assigned on every '
                         'VPSA')

    method = 'DELETE'
    path = '/api/nas/groups/{0}.json'.format(groupname)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_active_directory(session, return_type=None):
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
    method = 'GET'
    path = '/api/active_directory.json'

    return session.call_api(method=method, path=path, return_type=return_type)


def join_active_directory(session, display_name, username, password,
                          dns_domain, netbios_name, dns, return_type=None):
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

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid Active Directory name.'
                         .format(display_name))

    body_values['adserver'] = display_name

    if username is None:
        raise ValueError('The username parameter must be passed.')

    body_values['username'] = username

    if password is None:
        raise ValueError('The password parameter must be passed.')

    body_values['password'] = password

    body_values['realm'] = dns_domain

    if netbios_name is None:
        raise ValueError('The netbios_name parameter must be passed.')

    body_values['workgroup'] = netbios_name

    if type(dns) is str:
        dns = [x.strip() for x in dns.split(',')]

    if type(dns) is not list:
        raise ValueError('The dns parameter must be a Python list.')

    body_values['dns'] = dns

    method = 'POST'
    path = '/api/active_directory.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_active_directory_dns(session, dns, return_type=None):
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
    body_values = {}

    if type(dns) is str:
        dns = [x.strip() for x in dns.split(',')]

    if type(dns) is not list:
        raise ValueError('The dns parameter must be a Python list.')

    body_values['dns'] = dns

    method = 'POST'
    path = '/api/active_directory/dns.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def leave_active_directory(session, username, password, return_type=None):
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

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if username is None:
        raise ValueError('The username parameter must be passed.')

    body_values['username'] = username

    if password is None:
        raise ValueError('The password parameter must be passed.')

    body_values['password'] = password

    method = 'POST'
    path = '/api/active_directory/reset.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)
