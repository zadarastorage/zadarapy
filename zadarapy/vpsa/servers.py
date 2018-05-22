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
from zadarapy.validators import *


def get_all_servers(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all servers configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying servers from.  Optional.

    :type: limit: int
    :param limit: The maximum number of servers to return.  Optional.

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
    path = '/api/servers.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_server(session, server_id, return_type=None):
    """
    Retrieves details for a single server.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type server_id: str
    :param server_id: The server 'name' value as returned by get_all_servers.
        For example: 'srv-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_server_id(server_id):
        raise ValueError('{0} is not a valid server ID.'.format(server_id))

    method = 'GET'
    path = '/api/servers/{0}.json'.format(server_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_server(session, display_name, ip_address=None, iqn=None,
                  vpsa_chap_user=None, vpsa_chap_secret=None,
                  host_chap_user=None, host_chap_secret=None,
                  ipsec_iscsi='NO', ipsec_nfs='NO', force='NO',
                  return_type=None):
    """
    Creates a new server.  A valid server record must be attached to a volume
    before a client with the corresponding IP or IQN can access the volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the server.  For example:
        'web-01', 'database', etc.  May not contain a single quote (')
        character.  Required.

    :type ip_address: str
    :param ip_address: If using NFS/CIFS, the IP address or subnet as defined
        in CIDR notation of the server.  Either ip_address or iqn must be
        passed to this function (or both).  Optional.

    :type iqn: str
    :param iqn: If using iSCSI/iSER, the IQN of the server.  For example -
        "iqn.1993-08.org.debian:01:dea714656496".  Either ip_address or iqn
        must be passed to this function (or both).  Optional.

    :type vpsa_chap_user: str
    :param vpsa_chap_user: When using iSCSI/iSER, the CHAP user for the VPSA.
        This would be typically entered in the server's iSCSI/iSER initiatior
        configuration.  If set to 'None', a VPSA CHAP user will be auto
        generated.  Optional.

    :type vpsa_chap_secret: str
    :param vpsa_chap_secret: When using iSCSI/iSER, the CHAP secret for the
        VPSA.  This would be typically entered in the server's iSCSI/iSER
        initiatior configuration.  If set to 'None', a VPSA CHAP secret will
        be auto generated.  Must be between 12 to 16 characters in length.
        Optional.

    :type host_chap_user: str
    :param host_chap_user: When using iSCSI/iSER, the CHAP user for the
        server.  If defined, the VPSA will use this to complete mutual CHAP
        authentication with the server.  Note: for Windows systems, the host
        CHAP user must be the server's IQN.  If set to 'None', mutual CHAP
        won't be used.  Optional.

    :type host_chap_secret: str
    :param host_chap_user: When using iSCSI/iSER, the CHAP secret for the
        server.  If defined, the VPSA will use this to complete mutual CHAP
        authentication with the server.  If set to 'None', mutual CHAP won't
        be used.  Must be between 12 to 16 characters in length.  Optional.

    :type ipsec_iscsi: str
    :param ipsec_iscsi: When accessing iSCSI/iSER block volumes from this
        server, if set to 'YES', IPSec encryption will be mandated when
        connecting from this server.  If 'NO', IPSec won't be used.  Set to
        'NO' by default.  Optional.

    :type ipsec_nfs: str
    :param ipsec_nfs: When accessing NFS NAS shares from this server, if set
        to 'YES', IPSec encryption will be mandated when connecting from this
        server.  If 'NO', IPSec won't be used.  Set to 'NO' by default.
        Optional.

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
    body_values = {}

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid volume name.'
                         .format(display_name))

    body_values['display_name'] = display_name

    if ip_address is None and iqn is None:
        raise ValueError('Either ip_address or iqn parameter must be '
                         'defined.')

    if ip_address is not None:
        body_values['iscsi'] = ip_address

    if iqn is not None:
        if not is_valid_iqn(iqn):
            raise ValueError('{0} is not a valid iSCSI/iSER IQN.'
                             .format(iqn))

        body_values['iqn'] = iqn

    if vpsa_chap_user is not None:
        if not is_valid_field(vpsa_chap_user):
            raise ValueError('{0} is not a valid VPSA CHAP user.'
                             .format(vpsa_chap_user))

        body_values['vpsachapuser'] = vpsa_chap_user

    if vpsa_chap_secret is not None:
        if not is_valid_field(vpsa_chap_secret):
            raise ValueError('{0} is not a valid VPSA CHAP secret.'
                             .format(vpsa_chap_secret))

        body_values['vpsachapsecret'] = vpsa_chap_secret

    if host_chap_user is not None:
        if not is_valid_field(host_chap_user):
            raise ValueError('{0} is not a valid host CHAP user.'
                             .format(host_chap_user))

        body_values['hostchapuser'] = host_chap_user

    if host_chap_secret is not None:
        if not is_valid_field(host_chap_secret):
            raise ValueError('{0} is not a valid host CHAP secret.'
                             .format(host_chap_secret))

        body_values['hostchapsecret'] = host_chap_secret

    ipsec_iscsi = ipsec_iscsi.upper()

    if ipsec_iscsi not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid ipsec_iscsi parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(ipsec_iscsi))

    body_values['ipsec_iscsi'] = ipsec_iscsi

    ipsec_nfs = ipsec_nfs.upper()

    if ipsec_nfs not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid ipsec_nfs parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(ipsec_nfs))

    body_values['ipsec_nfs'] = ipsec_nfs

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/servers.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_server(session, server_id, ip_address=None, iqn=None,
                  vpsa_chap_user=None, vpsa_chap_secret=None,
                  host_chap_user=None, host_chap_secret=None,
                  ipsec_iscsi=None, ipsec_nfs=None, force='NO',
                  return_type=None):
    """
    Updates a server.  Parameters set to 'None' will not have their existing
    values changed.  The server must not be attached to any volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type server_id: str
    :param server_id: The server 'name' value as returned by get_all_servers.
        For example: 'srv-00000001'.  Required.

    :type ip_address: str
    :param ip_address: See documentation for create_server.  Optional.

    :type iqn: str
    :param iqn: See documentation for create_server.  Optional.

    :type vpsa_chap_user: str
    :param vpsa_chap_user: See documentation for create_server.  Optional.

    :type vpsa_chap_secret: str
    :param vpsa_chap_secret: See documentation for create_server.  Optional.

    :type host_chap_user: str
    :param host_chap_user: See documentation for create_server.  Optional.

    :type host_chap_secret: str
    :param host_chap_user: See documentation for create_server.  Optional.

    :type ipsec_iscsi: str
    :param ipsec_iscsi: See documentation for create_server.  Optional.

    :type ipsec_nfs: str
    :param ipsec_nfs: See documentation for create_server.  Optional.

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
    if not is_valid_server_id(server_id):
        raise ValueError('{0} is not a valid server ID.'.format(server_id))

    body_values = {}

    if ip_address is not None:
        body_values['iscsi'] = ip_address

    if iqn is not None:
        if not is_valid_iqn(iqn):
            raise ValueError('{0} is not a valid iSCSI/iSER IQN.'
                             .format(iqn))

        body_values['iqn'] = iqn

    if vpsa_chap_user is not None:
        if not is_valid_field(vpsa_chap_user):
            raise ValueError('{0} is not a valid VPSA CHAP user.'
                             .format(vpsa_chap_user))

        body_values['vpsachapuser'] = vpsa_chap_user

    if vpsa_chap_secret is not None:
        if not is_valid_field(vpsa_chap_secret):
            raise ValueError('{0} is not a valid VPSA CHAP secret.'
                             .format(vpsa_chap_secret))

        body_values['vpsachapsecret'] = vpsa_chap_secret

    if host_chap_user is not None:
        if not is_valid_field(host_chap_user):
            raise ValueError('{0} is not a valid host CHAP user.'
                             .format(host_chap_user))

        body_values['hostchapuser'] = host_chap_user

    if host_chap_secret is not None:
        if not is_valid_field(host_chap_secret):
            raise ValueError('{0} is not a valid host CHAP secret.'
                             .format(host_chap_secret))

        body_values['hostchapsecret'] = host_chap_secret

    if ipsec_iscsi is not None:
        ipsec_iscsi = ipsec_iscsi.upper()

        if ipsec_iscsi not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid ipsec_iscsi parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(ipsec_iscsi))

        body_values['ipsec_iscsi'] = ipsec_iscsi

    if ipsec_nfs is not None:
        ipsec_nfs = ipsec_nfs.upper()

        if ipsec_nfs not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid ipsec_nfs parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(ipsec_nfs))

        body_values['ipsec_nfs'] = ipsec_nfs

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"ip_address", "iqn", "vpsa_chap_user", '
                         '"vpsa_chap_secret", "host_chap_user", '
                         '"host_chap_secret", "ipsec_iscsi", "ipsec_nfs"')

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/servers/{0}/config.json'.format(server_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_server(session, server_id, return_type=None):
    """
    Deletes a server.  The server must not be attached to any volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type server_id: str
    :param server_id: The server 'name' value as returned by get_all_servers.
        For example: 'srv-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_server_id(server_id):
        raise ValueError('{0} is not a valid server ID.'.format(server_id))

    method = 'DELETE'
    path = '/api/servers/{0}.json'.format(server_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def rename_server(session, server_id, display_name, return_type=None):
    """
    Sets the "display_name" server parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type server_id: str
    :param server_id: The server 'name' value as returned by get_all_servers.
        For example: 'srv-00000001'.  Required.

    :type display_name: str
    :param display_name: The new "display_name" to set.  May not contain a
        single quote (') character.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_server_id(server_id):
        raise ValueError('{0} is not a valid server ID.'.format(server_id))

    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid server name.'
                         .format(display_name))

    body_values['new_name'] = display_name

    method = 'POST'
    path = '/api/servers/{0}/rename.json'.format(server_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_volumes_attached_to_server(session, server_id, start=None, limit=None,
                                   return_type=None):
    """
    Retrieves details for all volumes attached to the specified server.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type server_id: str
    :param server_id: The server 'name' value as returned by get_all_servers.
        For example: 'srv-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying volumes from.  Optional.

    :type: limit: int
    :param limit: The maximum number of volumes to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_server_id(server_id):
        raise ValueError('{0} is not a valid server ID.'.format(server_id))

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
    path = '/api/servers/{0}/volumes.json'.format(server_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def attach_servers_to_volume(session, servers, volume_id, access_type=None,
                             readonly='NO', force='NO', return_type=None):
    """
    Attaches one or more servers to a volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type servers: str
    :param servers: A comma separated string of servers with no spaces
        around the commas.  The value must match server's 'name'
        attribute.  For example: 'srv-00000001,srv-00000002'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type access_type: str
    :param access_type: When to an NAS share volume, if set to 'NFS', only NFS
        access will be allowed from this server.  If set to 'SMB', only
        SMB/CIFS will be allowed from this server.  If set to None, both NFS
        and SMB/CIFS will be allowed from this server.  Note that when using
        None, the ip address for the server must be defined in CIDR format,
        even if it's a single host ending in /32.  Not relevant for iSCSI
        volumes.  Optional.

    :type readonly: str
    :param readonly: If set to 'YES', the share will only be readable by this
        server.  If set to 'NO', this server will be able to read and write to
        the share.  Optional.

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
    for server in servers.split(','):
        if not is_valid_server_id(server):
            raise ValueError('"{0}" in "{1}" is not a valid server ID.'
                             .format(server, servers))

    body_values = {}

    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values['volume_name'] = volume_id

    if access_type is not None:
        if access_type not in ['NFS', 'SMB', 'BOTH']:
            raise ValueError('"{0}" is not a valid access_type parameter.  '
                             'Allowed values are: "NFS", "SMB", or "BOTH"'
                             .format(access_type))

        # This allows an extra option through the command line utility
        if access_type == 'BOTH':
            access_type = None

        body_values['access_type'] = access_type

    readonly = readonly.upper()

    if readonly not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid readonly parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(access_type))

    body_values['readonly'] = readonly

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/servers/{0}/volumes.json'.format(servers)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_server_performance(session, server_id, interval=1, return_type=None):
    """
    Retrieves metering statistics for the server for the specified interval.
    Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type server_id: str
    :param server_id: The server 'name' value as returned by get_all_servers.
        For example: 'srv-00000001'.  Required.

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
    if not is_valid_server_id(server_id):
        raise ValueError('{0} is not a valid server ID.'.format(server_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/servers/{0}/performance.json'.format(server_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
