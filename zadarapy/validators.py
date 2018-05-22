# Copyright 2015 Zadara Storage, Inc.
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

import re


def is_valid_cg_id(cg_id):
    """
    Validates a consistency group ID, also known as the consistency group
    "cg_name".  A valid consistency group name should look like: cg-00000001
    - It should always start with "cg-" and end with 8 hexadecimal characters
    in lower case.

    :type cg_id: str
    :param cg_id: The consistency group name to be validated.

    :rtype: bool
    :return: True or False depending on whether cg_id passes validation.
    """
    if cg_id is None:
        return False

    match = re.match('^cg-[0-9a-f]{8}$', cg_id)

    if not match:
        return False

    return True


def is_valid_controller_id(controller_id):
    """
    Validates a virtual controller ID, also known as the virtual controller
    "name".  A valid virtual controller name should look like:
    vsa-00000001-vc-0 - It should always start with "vsa-", followed by 8
    hexadecimal characters in lower case and a hyphen, then with the VC
    identifier, typically "vc-0" or "vc-1".

    :type controller_id: str
    :param controller_id: The virtual controller name to be validated.

    :rtype: bool
    :return: True or False depending on whether controller_id passes
        validation.
    """
    if controller_id is None:
        return False

    match = re.match('^vsa-[0-9a-f]{8}-vc-[0-9]$', controller_id)

    if not match:
        return False

    return True


def is_valid_email(email):
    """
    Validates an email address.

    :type email: str
    :param email: The email address to be validated.

    :rtype: bool
    :return: True or False depending on whether field passes validation.
    """
    if email is None:
        return False

    if not re.match('^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$',
                    email):
        return False

    return True


def is_valid_field(field, allow_quote=False, minimum=None, maximum=None):
    """
    Validates a generic user inputted field, such as a "name" for an
    object.  For now, it basically only validates whether single quote
    characters should be allowed in the string.

    :type field: str
    :param field: The data to be validated.

    :type allow_quote: bool
    :param allow_quote: If True, a single quote character (') will be allowed
        to pass validation.

    :type minimum: int
    :param minimum: If defined, values with fewer characters than this value
        will be rejected.

    :type maximum: int
    :param maximum: If defined, values with more characters than this value
        will be rejected.

    :rtype: bool
    :return: True or False depending on whether field passes validation.
    """
    if field is None:
        return False

    if not allow_quote and "'" in field:
        return False

    if minimum:
        if len(field) < minimum:
            return False

    if maximum:
        if len(field) > maximum:
            return False

    return True


def is_valid_iqn(iqn):
    """
    Validates if an iSCSI/iSER IQN is well formed.

    :type iqn: str
    :param iqn: The IQN to validate.  For example:
        'iqn.1993-08.org.debian:01:dea714656496'

    :rtype: bool
    :return: True or False depending on whether iqn passes validation.
    """
    if iqn is None:
        return False

    match = re.match('^(?:iqn\.[0-9]{4}-[0-9]{2}(?:\.[A-Za-z](?:[A-Za-z0-9\-]'
                     '*[A-Za-z0-9])?)+(?::.*)?|eui\.[0-9A-Fa-f]{16})', iqn)

    if not match:
        return False

    return True


def is_valid_mask(mask):
    """
    Validates a UNIX style permissions mask.  Mask must be octal.

    :type mask: str
    :param mask: The octal mask to be validated.  For example: '0755'.

    :rtype: bool
    :return: True or False depending on whether mask passes validation.
    """
    if mask is None:
        return False

    if not mask.isdigit():
        return False

    if len(mask) != 4:
        return False

    mask_values = ['0', '1', '2', '4', '5', '6', '7']

    if mask[0] != '0':
        return False

    for value in mask[1:]:
        if value not in mask_values:
            return False

    return True


def is_valid_mgrjob_id(mgrjob_id):
    """
    Validates a migration job ID, also known as the migration job
    "migration_job_name".  A valid migration job name should look like:
    mgrjob-00000001 - It should always start with "mgrjob-" and end with 8
    hexadecimal characters in lower case.

    :type mgrjob_id: str
    :param mgrjob_id: The consistency group name to be validated.

    :rtype: bool
    :return: True or False depending on whether cg_id passes validation.
    """
    if mgrjob_id is None:
        return False

    match = re.match('^mgrjob-[0-9a-f]{8}$', mgrjob_id)

    if not match:
        return False

    return True


def is_valid_mirror_id(mirror_id):
    """
    Validates a mirror job ID, also known as the mirror job "job_name".
    A valid mirror job name should look like: srcjvpsa-00000001 - It should
    always start with "srcjvpsa-" or "dstjvpsa-" and end with 8 hexadecimal
    characters in lower case.

    :type mirror_id: str
    :param mirror_id: The mirror job name to be validated.

    :rtype: bool
    :return: True or False depending on whether mirror_id passes validation.
    """
    if mirror_id is None:
        return False

    match = re.match('^(src|dst)jvpsa-[0-9a-f]{8}$', mirror_id)

    if not match:
        return False

    return True


def is_valid_policy_creation(policy_creation):
    """
    Performs a loose validation the snapshot creation frequency for a snapshot
    policy is valid.  The frequency should be defined in UNIX cron style
    format.  For example: "0 3 * * *".  This isn't perfect because invalid
    numbers (e.g. 65 for minute, 25 for hour) are accepted.

    :type policy_creation: str
    :param policy_creation: The snapshot creation frequency to be validated.

    :rtype: bool
    :return: True or False depending on whether policy_creation passes
        validation.
    """
    if policy_creation is None:
        return False

    if policy_creation.lower() == "manual":
        return True

    creation_split = policy_creation.split(' ')

    if len(creation_split) != 5:
        return False

    pattern = re.compile('^(?:[1-9]?\d|\*)(?:(?:[/-][1-9]?\d)|'
                         '(?:,[1-9]?\d)+)?$')

    for v in creation_split:
        match = pattern.match(v)

        if not match:
            return False

    return True


def is_valid_policy_id(policy_id):
    """
    Validates a snapshot policy ID, also known as the snapshot policy "name".
    A valid snapshot policy name should look like: policy-00000001 - It should
    always start with "policy-" and end with 8 hexadecimal characters in lower
    case.

    :type policy_id: str
    :param policy_id: The snapshot policy name to be validated.

    :rtype: bool
    :return: True or False depending on whether policy_id passes validation.
    """
    if policy_id is None:
        return False

    match = re.match('^policy-[0-9a-f]{8}$', policy_id)

    if not match:
        return False

    return True


def is_valid_smb_hidden_files(smb_hidden_files):
    """
    Validates smbhiddenfiles NAS volume parameter.  String should be forward
    slash (/) delimited.

    :type smb_hidden_files: str
    :param smb_hidden_files: The smbhiddenfiles parameter to be validated.

    :rtype: bool
    :return: True or False depending on whether smb_hidden_files passes
        validation.
    """
    if smb_hidden_files is None:
        return False

    if not smb_hidden_files.startswith("/") or \
       not smb_hidden_files.endswith("/"):
        return False

    return True


def is_valid_snapshot_rule_name(snap_rule_name):
    """
    Validates a snapshot rule name.
    A snapshot rule name identifies a particular volume being attached to
    a particular snapshot policy. A valid snapshot rule name should look
    like: rule-00000001 - It should always start with "rule-" and end
    with 8 hexadecimal characters in lower case.

    :type snap_rule_name: str
    :param snap_rule_name: The snapshot rule name to be validated.

    :rtype: bool
    :return: True or False depending on whether snap_rule_name passes
        validation.
    """
    if snap_rule_name is None:
        return False

    match = re.match('^rule-[0-9a-f]{8}$', snap_rule_name)

    if not match:
        return False

    return True


def is_valid_pool_id(pool_id, remote_pool_allowed=False):
    """
    Validates a storage pool ID, also known as the pool "name".  A valid pool
    name should look like: pool-00000001 - It should always start with
    "pool-" and end with 8 hexadecimal characters in lower case.  If
    remote_pool_allowed is True, this function will also validate remote pool
    names in the format of rpool-00000001.

    :type pool_id: str
    :param pool_id: The storage pool name to be validated.

    :type remote_pool_allowed: bool
    :param remote_pool_allowed: Also validate remote pool IDs as described
        above.

    :rtype: bool
    :return: True or False depending on whether pool_id passes validation.
    """
    if pool_id is None:
        return False

    if remote_pool_allowed:
        match = re.match('^r?pool-[0-9a-f]{8}$', pool_id)
    else:
        match = re.match('^pool-[0-9a-f]{8}$', pool_id)

    if not match:
        return False

    return True


def is_valid_port(port):
    """
    Validates port range.  Port must be within 1-65535 range.

    :type port: int
    :param port: Theport to be validated.

    :rtype: bool
    :return: True or False depending on whether hostname passes validation.
    """
    if port is None:
        return False

    port = int(port)

    if port < 1 or port > 65535:
        return False

    return True


def is_valid_raid_id(raid_id):
    """
    Validates a RAID group ID, also known as the RAID group "name".  A valid
    RAID group name should look like: RaidGroup-1 - It should always start with
    "RaidGroup-" and end with a variable amount of digits.

    :type raid_id: str
    :param raid_id: The RAID group name to be validated.

    :rtype: bool
    :return: True or False depending on whether raid_id passes validation.
    """
    if raid_id is None:
        return False

    match = re.match('^RaidGroup-[0-9]+$', raid_id)

    if not match:
        return False

    return True


def is_valid_ros_backup_job_id(ros_backup_job_id):
    """
    Validates a remote object storage backup job ID, also known as the remote
    object storage backup job "name".  A valid remote VPSA name should look
    like: bkpjobs-00000001 - It should always start with "bkpjobs-" and end
    with 8 hexadecimal characters in lower case.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: The remote object storage backup job name to
        be validated.

    :rtype: bool
    :return: True or False depending on whether ros_backup_job_id passes
        validation.
    """
    if ros_backup_job_id is None:
        return False

    match = re.match('^bkpjobs-[0-9a-f]{8}$', ros_backup_job_id)

    if not match:
        return False

    return True


def is_valid_ros_destination_id(ros_destination_id):
    """
    Validates a remote object storage destination ID, also known as the remote
    object storage destination "name".  A valid remote object storage
    destination name should look like: obsdst-00000001 - It should always
    start with "obsdst-" and end with 8 hexadecimal characters in lower case.

    :type ros_destination_id: str
    :param ros_destination_id: The remote object storage destination name to
        be validated.

    :rtype: bool
    :return: True or False depending on whether ros_destination_id passes
        validation.
    """
    if ros_destination_id is None:
        return False

    match = re.match('^obsdst-[0-9a-f]{8}$', ros_destination_id)

    if not match:
        return False

    return True


def is_valid_ros_restore_job_id(ros_restore_job_id):
    """
    Validates a remote object storage restore job ID, also known as the remote
    object storage restore job "name".  A valid remote VPSA name should look
    like: rstjobs-00000001 - It should always start with "rstjobs-" and end
    with 8 hexadecimal characters in lower case.

    :type ros_restore_job_id: str
    :param ros_restore_job_id: The remote object storage restore job name to
        be validated.

    :rtype: bool
    :return: True or False depending on whether ros_restore_job_id passes
        validation.
    """
    if ros_restore_job_id is None:
        return False

    match = re.match('^rstjobs-[0-9a-f]{8}$', ros_restore_job_id)

    if not match:
        return False

    return True


def is_valid_rvpsa_id(rvpsa_id):
    """
    Validates a remote VPSA ID, also known as the remote VPSA "name".  A valid
    remote VPSA name should look like: rvpsa-00000001 - It should always start
    with "rvpsa-" and end with 8 hexadecimal characters in lower case.

    :type rvpsa_id: str
    :param rvpsa_id: The remote VPSA name to be validated.

    :rtype: bool
    :return: True or False depending on whether rvpsa_id passes validation.
    """
    if rvpsa_id is None:
        return False

    match = re.match('^rvpsa-[0-9a-f]{8}$', rvpsa_id)

    if not match:
        return False

    return True


def is_valid_server_id(server_id):
    """
    Validates a server ID, also known as the server "name".  A valid server
    name should look like: srv-00000001 - It should always start with "srv-"
    and end with 8 hexadecimal characters in lower case.

    :type server_id: str
    :param server_id: The server name to be validated.

    :rtype: bool
    :return: True or False depending on whether server_id passes validation.
    """
    if server_id is None:
        return False

    match = re.match('^srv-[0-9a-f]{8}$', server_id)

    if not match:
        return False

    return True


def is_valid_snapshot_id(snapshot_id):
    """
    Validates a snapshot ID, also known as the snapshot "name".  A valid
    snapshot policy name should look like: snap-00000001 - It should
    always start with "snap-" and end with 8 hexadecimal characters in lower
    case.

    :type snapshot_id: str
    :param snapshot_id: The snapshot policy name to be validated.

    :rtype: bool
    :return: True or False depending on whether snapshot_id passes validation.
    """
    if snapshot_id is None:
        return False

    match = re.match('^snap-[0-9a-f]{8}$', snapshot_id)

    if not match:
        return False

    return True


def is_valid_volume_id(volume_id):
    """
    Validates drive and volume IDs, also known as the drive/volume "name".
    A valid volume name should look like: volume-00000001 - It should always
    start with "volume-" and end with 8 hexadecimal characters in lower case.

    :type volume_id: str
    :param volume_id: The drive or volume name to be validated.

    :rtype: bool
    :return: True or False depending on whether volume_id passes validation.
    """
    if volume_id is None:
        return False

    match = re.match('^volume-[0-9a-f]{8}$', volume_id)

    if not match:
        return False

    return True


def is_valid_vpsa_display_name(vpsa_display_name):
    """
    Validates a Zadara VPSA display name.  Only alphanumeric characters and
    underscore are allowed.

    :type vpsa_display_name: str
    :param vpsa_display_name: The VPSA display name to be validated.

    :rtype: bool
    :return: True or False depending on whether vpsa_display_name passes
        validation.
    """
    if vpsa_display_name is None:
        return False

    match = re.match('^[A-Za-z-0-9_]+$', vpsa_display_name)

    if not match:
        return False

    return True


def is_valid_zadara_key(key):
    """
    Validates a Zadara API key.  An API key should be 20 characters in length,
    and only consist of numbers and upper case letters.

    :type key: str
    :param key: The API key to be validated.

    :rtype: bool
    :return: True or False depending on whether key passes validation.
    """
    if key is None:
        return False

    if len(key) != 20:
        return False

    allowed = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz012345'
                  '6789')

    if not allowed.issuperset(key):
        return False

    return True


def is_valid_zcs_container_id(zcs_container_id):
    """
    Validates Zadara Container Services (ZCS) container IDs, also known as the
    ZCS container "name".  A valid ZCS container name should look like:
    container-00000001 - It should always start with "container-" and end with
    8 hexadecimal characters in lower case.

    :type zcs_container_id: str
    :param zcs_container_id: The ZCS container name to be validated.

    :rtype: bool
    :return: True or False depending on whether zcs_container_id passes
        validation.
    """
    if zcs_container_id is None:
        return False

    match = re.match('^container-[0-9a-f]{8}$', zcs_container_id)

    if not match:
        return False

    return True


def is_valid_zcs_image_id(zcs_image_id):
    """
    Validates Zadara Container Services (ZCS) image IDs, also known as the ZCS
    image "name".  A valid ZCS image name should look like: img-00000001 - It
    should always start with "img-" and end with 8 hexadecimal characters in
    lower case.

    :type zcs_image_id: str
    :param zcs_image_id: The ZCS image name to be validated.

    :rtype: bool
    :return: True or False depending on whether zcs_image_id passes
        validation.
    """
    if zcs_image_id is None:
        return False

    match = re.match('^img-[0-9a-f]{8}$', zcs_image_id)

    if not match:
        return False

    return True
