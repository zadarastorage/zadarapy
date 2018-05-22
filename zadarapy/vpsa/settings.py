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
from zadarapy.validators import is_valid_pool_id


def get_nfs_domain(session, return_type=None):
    """
    Retrieves the NFS domain for the VPSA.

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
    path = '/api/settings/nfs_domain.json'

    return session.call_api(method=method, path=path, return_type=return_type)


def set_nfs_domain(session, domain, return_type=None):
    """
    Sets the NFS domain for the VPSA.  This is used in conjunction with
    the idmap service on the client and NAS Users on the VPSA to correctly
    map local users to VPSA users.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type domain: str
    :param domain: The NFS domain to set.  This must be a valid DNS domain
        name.  Set to 'localdomain' by default.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'domain': domain}

    method = 'POST'
    path = '/api/settings/nfs_domain.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def set_multizone_read_mode(session, read_mode, return_type=None):
    """
    Modifies where data is read from in multizone environments.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type read_mode: str
    :param read_mode: For multizone environments, if set to 'roundrobin', data
        will be read from storage nodes in all protection zones.  If set to
        'localcopy', data from the local protection zone will be favored.
        'roundrobin' is the default value.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if read_mode not in ['roundrobin', 'localcopy']:
        raise ValueError('"{0}" is not a valid read_mode parameter.  Allowed '
                         'values are: "roundrobin" or "localcopy"'
                         .format(read_mode))

    body_values = {'readmode': read_mode}

    method = 'POST'
    path = '/api/settings/raid_read_mode.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def set_smb_charset(session, charset, force='NO', return_type=None):
    """
    Sets the character set used by the SMB/CIFS server for all SMB/CIFS
    shared volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type charset: str
    :param charset: If set to 'UTF-8', the SMB/CIFS character set will be
        UTF-8.  If set to 'ISO-8859-1', it will be set to ISO-8859-1.  'UTF-8'
        is the default value.  Required.

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

    if charset not in ['UTF-8', 'ISO-8859-1']:
        raise ValueError('"{0}" is not a valid charset parameter.  Allowed '
                         'values are: "UTF-8" or "ISO-8859-1"'
                         .format(charset))

    body_values['charset'] = charset

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/settings/smb_charset.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def set_smb_trusted_domains(session, allow_trusted_domains, force='NO',
                            return_type=None):
    """
    Sets whether or not the SMB/CIFS server should allow Active Directory
    trusted domains.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type allow_trusted_domains: str
    :param allow_trusted_domains: For VPSAs joined to an Active Directory
        domain, if set to 'YES', Active Directory trusted domains will be
        allowed.  If set to 'NO', Active Directory trusted domains will not be
        allowed.  The default value is 'YES'.  Required.

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

    allow_trusted_domains = allow_trusted_domains.upper()

    if allow_trusted_domains not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid allow_trusted_domains '
                         'parameter.  Allowed values are: "YES" or "NO"'
                         .format(allow_trusted_domains))

    body_values['allow'] = allow_trusted_domains

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/settings/smb_trusted_domains.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def set_recycle_bin(session, recycle_bin, return_type=None):
    """
    Turns the recycle bin on or off globally for all pools.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type recycle_bin: str
    :param recycle_bin: If set to 'YES', deleted volumes are moved to the
        recycle bin, where they may be restored in case of accidental
        deletion (volumes are permanently deleted from the recycle bin after
        seven days).  If set to 'NO', deleted volumes are immediately deleted.
        The default value is 'YES'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    recycle_bin = recycle_bin.upper()
    
    if recycle_bin not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid recycle_bin parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(recycle_bin))

    body_values = {'recyclebin': recycle_bin}

    method = 'POST'
    path = '/api/settings/set_recycle_bin.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_public_ip(session, return_type=None):
    """
    Retrieves public IPs associated with the VPSA.

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
    path = '/api/settings/public_ips.json'

    return session.call_api(method=method, path=path, return_type=return_type)


def set_encryption_password(session, password, return_type=None):
    """
    Sets the encryption password globally on the VPSA.  This password is used
    when enabling the encryption option for a volume.  CAUTION: THIS PASSWORD
    IS NOT STORED ON THE VPSA - IT IS THE USER'S RESPONSIBILITY TO MAINTAIN
    ACCESS TO THE PASSWORD.  LOSS OF THE PASSWORD MAY RESULT IN UNRECOVERABLE
    DATA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type password: str
    :param password: The encryption password to set for the VPSA (please read
        the warning above carefully).  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if password is None:
        raise ValueError('A password must be specified.')

    body_values = {'encryption_pwd': password}

    method = 'POST'
    path = '/api/settings/encryption.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_zcs_settings(session, return_type=None):
    """
    Retrieves details for Zadara Container Services, such as the configured
    network, ports, etc.

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
    path = '/api/settings/container_service.json'

    return session.call_api(method=method, path=path, return_type=return_type)


def update_zcs_settings(session, network, lowport, highport,
                        return_type=None):
    """
    Changes various settings for Zadara Container Services.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type network: str
    :param network: The subnet where ZCS containers will get their private IP
        addresses from.  This must be defined in CIDR format.  Do not change
        this setting unless you know what you are doing.  The default value
        is '172.20.20.1/24'.  Required.

    :type lowport: int
    :param lowport: The low end of the port range the ZCS container will be
        allowed to listen to network connections on.  Do not change this
        setting unless you know what you are doing.  Cannot be lower than 9216
        or higher than 10240.  The default value is 9216.  Required.

    :type highport: int
    :param highport: The high end of the port range the ZCS container will be
        allowed to listen to network connections on.  Do not change this
        setting unless you know what you are doing.  Cannot be lower than 9216
        or higher than 10240.  The default value is 10240.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    body_values['network'] = network

    if lowport > highport:
        raise ValueError('The lowport parameter must be a lower number than '
                         'the highport parameter.')

    if lowport < 9216 or lowport > 10240:
        raise ValueError('The lowport parameter must be between 9216 and '
                         '10240 ("{0}" was passed).')

    body_values['lowport'] = lowport

    if highport < 9216 or highport > 10240:
        raise ValueError('The highport parameter must be between 9216 and '
                         '10240 ("{0}" was passed).')

    body_values['highport'] = highport

    method = 'POST'
    path = '/api/settings/container_service.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def create_zcs_image_repository(session, pool_id, return_type=None):
    """
    Creates the ZCS image repository on the specified pool.  ZCS images will
    be stored in this repository.  100 GB will be consumed on the specified
    pool for this repository.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {'pool': pool_id}

    method = 'POST'
    path = '/api/settings/create_images_repository.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def migrate_zcs_image_repository(session, pool_id, return_type=None):
    """
    Migrates the ZCS image repository from the existing pool to the specified
    pool.  100 GB will be freed from the existing pool and consumed on the
    specified pool for this repository.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values = {'pool': pool_id}

    method = 'POST'
    path = '/api/settings/migrate_images_repository.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_zcs_image_repository(session, confirm, return_type=None):
    """
    Deletes the ZCS image repository.  There must be no ZCS images on the
    VPSA.  100 GB will be freed from the pool where it resides.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type confirm: bool
    :param confirm: If True, the ZCS image repository will be deleted.  This
        is a safeguard for this function since it requires no other arguments.

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
                         'the ZCS image repository will not be deleted.')

    method = 'DELETE'
    path = '/api/settings/images_repository.json'

    return session.call_api(method=method, path=path, return_type=return_type)


def download_metering_database(session, return_type='raw'):
    """
    Downloads the metering database from the VPSA.  This will return a stream
    of binary in zip format.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: As noted above, this returns a raw binary stream.
        Output should be redirected to a file with a .zip extension.

    :rtype: str
    :returns: Raw zip file data.
    """
    method = 'GET'
    path = '/api/settings/metering_db'

    return session.call_api(method=method, path=path, return_type=return_type)
