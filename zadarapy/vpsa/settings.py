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


from zadarapy.validators import verify_boolean, \
    verify_pool_id, verify_read_mode, verify_charset, verify_not_none, \
    verify_low_high_port, verify_bool


def get_vpsa_config(session, return_type=None, **kwargs):
    """
    Retrieves various configuration details for the VPSA.

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
    path = '/api/config.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def settings_config(session, return_type=None, **kwargs):
    """
    Retrieves current settings configuration details for the VPSA.

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
    path = '/api/return_type.json'
    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_nfs_domain(session, return_type=None, **kwargs):
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
    path = '/api/settings/nfs_domain.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def set_nfs_domain(session, domain, return_type=None, **kwargs):
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

    path = '/api/settings/nfs_domain.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_multizone_read_mode(session, read_mode, return_type=None, **kwargs):
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
    verify_read_mode(read_mode)
    body_values = {'readmode': read_mode}

    path = '/api/settings/raid_read_mode.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_smb_charset(session, charset, force='NO', return_type=None, **kwargs):
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
    verify_charset(charset)
    force = verify_boolean(force, "force")

    body_values = {'charset': charset, 'force': force}

    path = '/api/settings/smb_charset.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_smb_trusted_domains(session, allow_trusted_domains, force='NO',
                            return_type=None, **kwargs):
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
    allow_trusted_domains = verify_boolean(allow_trusted_domains,
                                           "allow_trusted_domains")
    force = verify_boolean(force, "force")

    body_values = {'allow': allow_trusted_domains, 'force': force}

    path = '/api/settings/smb_trusted_domains.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_smb_netbios_name(session, smb_netbios_name, force="YES", return_type=None, **kwargs):
    """
      Get VPSA cache

      :type session: zadarapy.session.Session
      :param session: A valid zadarapy.session.Session object.  Required.

      :type smb_netbios_name: str
      :param smb_netbios_name: The smb netbios name to set.  Required.

      :type force: str
      :param force: Force smb netbios name when volumes with SMB permissions exist.  Optional.

      :type return_type: str
      :param return_type: If this is set to the string 'str', this function
              will return a cache size as a string.  Otherwise, it will return an
              integer.  Optional (will return an integer by default).

      :rtype: int, str
      :returns: Cache size as Int
      return_type parameter.
    """
    force = verify_bool(force)

    body_values = {"netbios_name": smb_netbios_name, "force": force}
    path = "/api/settings/smb_netbios_name.json"

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def set_recycle_bin(session, recycle_bin, return_type=None, **kwargs):
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
    recycle_bin = verify_boolean(recycle_bin, "recycle_bin")

    body_values = {'recyclebin': recycle_bin}

    path = '/api/settings/set_recycle_bin.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_public_ip(session, return_type=None, **kwargs):
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
    path = '/api/settings/public_ips.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def use_aws_kms_store(session, region, kmskeyid, access_id, secret,
                      encryption_pwd=None, old_encryption_pwd=None,
                      return_type=None, **kwargs):
    """
    Sets the encryption password globally on the VPSA.  This password is used
    when enabling the encryption option for a volume.  CAUTION: THIS PASSWORD
    IS NOT STORED ON THE VPSA - IT IS THE USER'S RESPONSIBILITY TO MAINTAIN
    ACCESS TO THE PASSWORD.  LOSS OF THE PASSWORD MAY RESULT IN UNRECOVERABLE
    DATA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type region: str
    :param region: The AWS KMS region code to set.  Required.

    :type kmskeyid: str
    :param kmskeyid: The AWS KMS key id to set.  Required.

    :type access_id: str
    :param access_id: The AWS KMS access id to set.  Required.

    :type secret: str
    :param secret: The AWS KMS secret password to set.  Required.

    :type encryption_pwd: str
    :param encryption_pwd: The master encryption password to set.  Required.

    :type old_encryption_pwd: str
    :param old_encryption_pwd: Old master encryption password. Required if
        setting a new password and older password is already set.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'region': region, 'kmskeyid': kmskeyid,
                   'access_id': access_id, 'secret': secret}

    if encryption_pwd:
        body_values['encryption_pwd'] = encryption_pwd

    if old_encryption_pwd:
        body_values['old_encryption_pwd'] = old_encryption_pwd

    path = '/api/settings/encryption.json'

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def restore_aws_kms_store(session, region, kmskeyid, access_id, secret, return_type=None, **kwargs):
    """
    Restore the encryption password globally on the VPSA.  This password is used
    when enabling the encryption option for a volume.  CAUTION: THIS PASSWORD
    IS NOT STORED ON THE VPSA - IT IS THE USER'S RESPONSIBILITY TO MAINTAIN
    ACCESS TO THE PASSWORD.  LOSS OF THE PASSWORD MAY RESULT IN UNRECOVERABLE
    DATA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type region: str
    :param region: The AWS KMS region code to set.  Required.

    :type kmskeyid: str
    :param kmskeyid: The AWS KMS key id to set.  Required.

    :type access_id: str
    :param access_id: The AWS KMS access id to set.  Required.

    :type secret: str
    :param secret: The AWS KMS secret password to set.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'region': region, 'kmskeyid': kmskeyid,
                   'access_id': access_id, 'secret': secret}

    path = '/api/settings/restore_encryption_aws.json'

    return session.post_api(path=path, body=body_values, return_type=return_type, **kwargs)


def remove_encryption_kms(session, return_type=None, **kwargs):
    """
    Remove encryption KMS on the VPSA

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
    path = '/api/settings/remove_encryption_kms.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def set_encryption_password(session, password, old_password=None,
                            return_type=None, **kwargs):
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

    :type old_password: str
    :param old_password: The old encryption password to set for the VPSA
    (please read the warning above carefully).  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_not_none(password, "password")

    body_values = {'encryption_pwd': password}
    if old_password:
        body_values['old_encryption_pwd'] = old_password

    path = '/api/settings/encryption.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def restore_encryption_password(session, password, return_type=None, **kwargs):
    """
    In cases where an encryption password is set on a VPSA, this can be used
    to restore the password.  For example, when restoring a VPSA from
    hibernation, the encryption password must be restored before encrypted
    volumes become available.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type password: str
    :param password: The existing encryption password of the VPSA.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_not_none(password, "password")

    body_values = {'encryption_pwd': password}

    path = '/api/settings/restore_encryption.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_zcs_settings(session, return_type=None, **kwargs):
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
    path = '/api/settings/container_service.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def update_zcs_settings(session, network, lowport, highport,
                        return_type=None, **kwargs):
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
    verify_low_high_port(lowport, highport)

    body_values = {'network': network, 'lowport': lowport,
                   'highport': highport}

    path = '/api/settings/container_service.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def create_zcs_image_repository(session, pool_id, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)

    body_values = {'pool': pool_id}

    path = '/api/settings/create_images_repository.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def migrate_zcs_image_repository(session, pool_id, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)

    body_values = {'pool': pool_id}

    path = '/api/settings/migrate_images_repository.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_zcs_image_repository(session, confirm, return_type=None, **kwargs):
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

    path = '/api/settings/images_repository.json'

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def download_metering_database(session, return_type='raw', **kwargs):
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
    path = '/api/settings/metering_db'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def enable_defrag(session, return_type=None, **kwargs):
    """
    Enables NAS share (XFS) defragging on the VPSA.

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
    path = '/api/settings/defrag_enable.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def disable_defrag(session, return_type=None, **kwargs):
    """
    Disables NAS share (XFS) defragging on the VPSA.

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
    path = '/api/settings/defrag_disable.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def start_defrag(session, return_type=None, **kwargs):
    """
    Starts NAS share (XFS) defragging on the VPSA.

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
    path = '/api/settings/defrag_start.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def stop_defrag(session, return_type=None, **kwargs):
    """
    Stops NAS share (XFS) defragging on the VPSA.

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
    path = '/api/settings/defrag_stop.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def enable_trim(session, return_type=None, **kwargs):
    """
     Enables volumes File System trim.

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
    path = '/api/settings/trim_enable.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def disable_trim(session, return_type=None, **kwargs):
    """
     Disables volumes File System trim.

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
    path = '/api/settings/trim_disable.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def start_trim(session, return_type=None, **kwargs):
    """
     Starts volumes File System trim.

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
    path = '/api/settings/trim_start.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)


def stop_trim(session, return_type=None, **kwargs):
    """
     Stops volumes File System trim.

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
    path = '/api/settings/trim_stop.json'

    return session.post_api(path=path, return_type=return_type, **kwargs)