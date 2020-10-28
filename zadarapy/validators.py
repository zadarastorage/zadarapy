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
from urllib.parse import quote
import re

BAD_VPSA_ID = "The VPSA ID int '(i.e '154') or should be of format: " \
              "'vsa-0000001'. Given: {}"

LIST_APPROVED_STRIPES_SIZES = ['4', '16', '32', '64', '128', '256']

BAD_STRIPE_TYPE = '"{}" is not a valid pool mode. Allowed values are: ' \
                  '"stripe" or "simple"'

BAD_STRIPE_SIZES = '{0} is not a valid stripe size. Allowed values are: {1}'


def is_valid_vpsa_internal_name(vpsa_internal_id):
    """
    Validates a VPSA internal ID. A valid VPSA internal ID should look
    like: vsa-00000001 - It should always start with "vsa-" and end with 8
    hexadecimal characters in lower case.

    :type vpsa_internal_id: str
    :param vpsa_internal_id: The VPSA internal ID to be validated.

    :rtype: bool
    :return: True or False depending on whether vpsa_internal_id passes
     validation.
    """
    if vpsa_internal_id is None:
        return False
    match = re.match(r'^vsa-[0-9a-f]{8}$', vpsa_internal_id)

    if not match:
        return False

    return True


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

    match = re.match(r'^cg-[0-9a-f]{8}$', cg_id)

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

    match = re.match(r'^vsa-[0-9a-f]{8}-vc-[0-9]$', controller_id)

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

    if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$',
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

    match = re.match(r'^(?:iqn\.[0-9]{4}-[0-9]{2}(?:\.[A-Za-z](?:[A-Za-z0-9\-]'
                     r'*[A-Za-z0-9])?)+(?::.*)?|eui\.[0-9A-Fa-f]{16})', iqn)

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

    match = re.match(r'^mgrjob-[0-9a-f]{8}$', mgrjob_id)

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

    match = re.match(r'^(src|dst)jvpsa-[0-9a-f]{8}$', mirror_id)

    if not match:
        return False

    return True


def is_valid_remote_clone_id(remote_clone_job_id):
    """
    Validates a remote clone job ID, also known as the remote clone job
    "job_name". A valid remote clone job name should look like:
    dstrclone-00000001 - It should end with 8 hexadecimal characters in
    lower case.

    :type remote_clone_job_id: str
    :param remote_clone_job_id: The remote clone job name to be validated.

    :rtype: bool
    :return: True or False depending on whether remote_clone_id passes
    validation.
    """
    if remote_clone_job_id is None:
        return False

    match = re.match(r'^(src|dst)rclone-[0-9a-f]{8}$', remote_clone_job_id)

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

    pattern = re.compile(r'^(?:[1-9]?\d|\*)(?:(?:[/-][1-9]?\d)|'
                         r'(?:,[1-9]?\d)+)?$')

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

    match = re.match(r'^policy-[0-9a-f]{8}$', policy_id)

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

    match = re.match(r'^rule-[0-9a-f]{8}$', snap_rule_name)

    if not match:
        return False

    return True


def is_valid_memory_pool(mempool_name):
    """
    Validates Memory pool ID

    :type mempool_name: str
    :param mempool_name: Memory pool name to check

    :rtype: bool
    :return: True or False depending on whether snap_rule_name passes
        validation.
    """
    if mempool_name is None:
        return False

    match = re.match(r'^dgroup-[0-9a-f]{8}$', mempool_name)

    return match is not None


def is_valid_snaprule_name(snap_rule_name):
    """
    Validates a snapshot rule name.
    A snapshot rule name identifies a particular volume being attached to
    a particular snapshot policy. A valid snapshot rule name should look
    like: snaprule-00000001 - It should always start with "rule-" and end
    with 8 hexadecimal characters in lower case.

    :type snap_rule_name: str
    :param snap_rule_name: The snapshot rule name to be validated.

    :rtype: bool
    :return: True or False depending on whether snap_rule_name passes
        validation.
    """
    if snap_rule_name is None:
        return False

    match = re.match(r'^rule-[0-9a-f]{8}$', snap_rule_name)

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
        match = re.match(r'^r?pool-[0-9a-f]{8}$', pool_id)
    else:
        match = re.match(r'^pool-[0-9a-f]{8}$', pool_id)

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


def is_valid_minutes(minutes):
    """
    Validates number of minutes.

    :type minutes: int
    :param minutes: number of minutes to be validated.

    :rtype: bool
    :return: number of seconds in the amount of minutes
    """
    SECONDS_IN_A_MINUTE = 60
    MINUTES_IN_TEN_YEARS = 5256000

    minutes = int(minutes)

    if minutes < 1 or minutes > MINUTES_IN_TEN_YEARS:
        return 0

    return minutes*SECONDS_IN_A_MINUTE


def verify_expire_version(versioning):
    """
    :type: versioning: str
    :param versioning: Type of expiration versioning.
        Can be only current or previous.  Required.

    :return: fixed versioning format

    :raises: ValueError: Invalid start or limit
    """
    VERSION_CONVERT = {"current": "curver_after", "previous": "prever_after"}

    versioning = versioning.lower()
    if versioning not in VERSION_CONVERT.keys():
        raise ValueError("Versioning {0} could not be used, please use either "
                         "x-versions-location or x-history-location.".format(versioning))
    return VERSION_CONVERT[versioning]


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

    match = re.match(r'^RaidGroup-[0-9]+$', raid_id)

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

    match = re.match(r'^bkpjobs-[0-9a-f]{8}$', ros_backup_job_id)

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

    match = re.match(r'^obsdst-[0-9a-f]{8}$', ros_destination_id)

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

    match = re.match(r'^rstjobs-[0-9a-f]{8}$', ros_restore_job_id)

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

    match = re.match(r'^rvpsa-[0-9a-f]{8}$', rvpsa_id)

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

    match = re.match(r'^srv-[0-9a-f]{8}$', server_id)

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

    match = re.match(r'^snap-[0-9a-f]{8}$', snapshot_id)

    if not match:
        return False

    return True


def is_valid_vc_index(vc_index):
    """
    Validates vc_index.  vc_index must be within 0-65535 range.

    :type vc_index: int
    :param vc_index: The vc index to be validated.

    :rtype: bool
    :return: True or False depending on whether vc index passes validation.
    """
    if vc_index is None:
        return False

    vc_index = int(vc_index)

    if vc_index < 0 or vc_index > 65535:
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

    match = re.match(r'^volume-[0-9a-f]{8}$', volume_id)

    if not match:
        return False

    return True


def is_valid_project_id(project_id):
    """
    Validates project IDs, also known as the project "name".
    A valid project name should look like: proj-00000001 - It should always
    start with "proj-" and end with 8 hexadecimal characters in lower case.

    :type project_id: str
    :param project_id: The project name to be validated.

    :rtype: bool
    :return: True or False depending on whether project_id passes validation.
    """
    if project_id is None:
        return False

    match = re.match(r'^project-[0-9a-f]{8}$', project_id)

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

    match = re.match(r'^[A-Za-z-0-9_]+$', vpsa_display_name)

    if not match:
        return False

    return True


def is_valid_vpsaos_account_id(account_id):
    """
    :param account_id: Account ID to check validity
    :return: True iff VPSAOS account is valid
    """
    valid_set = set('0123456789abcdef')
    return all(c in valid_set for c in account_id)


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

    match = re.match(r'^container-[0-9a-f]{8}$', zcs_container_id)

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

    match = re.match(r'^img-[0-9a-f]{8}$', zcs_image_id)

    if not match:
        return False

    return True


def is_valid_ticket_id(ticket_id):
    """
    Validates Zadara Ticket ID

    :type ticket_id: int
    :param ticket_id: The ticket to be validated.

    :rtype: bool
    :return: True or False depending on whether ticket ID passes
        validation.
    """
    return ticket_id > 0


"""
Verifiers
"""


def verify_volume_id(volume_id):
    """
    :param volume_id: Volume ID to verify
    :raises: ValueError: invalid ID
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError("{0} is not a valid volume ID.".format(volume_id))


def verify_project_id(project_id):
    """
    :param project_id: Project ID to verify
    :raises: ValueError: invalid ID
    """
    if not is_valid_project_id(project_id):
        raise ValueError("{0} is not a valid project ID.".format(project_id))


def verify_raid_id(raid_id):
    """
    :param raid_id: RAID ID to verify
    :raises: ValueError: invalid ID
    """
    if not is_valid_raid_id(raid_id):
        raise ValueError('{0} is not a valid RAID group ID.'.format(raid_id))


def verify_snapshot_id(snapshot_id):
    """
    :param snapshot_id: Snbapshot ID to verify
    :raises: ValueError: invalid ID
    """
    if not is_valid_snapshot_id(snapshot_id):
        raise ValueError("{0} is not a valid Snapshot ID.".format(snapshot_id))


def verify_policy_id(policy_id):
    """
    :param policy_id: Snapshot Policy ID to verify
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid snapshot policy ID.'.format(_id)
                for _id in policy_id.split(',') if not is_valid_policy_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_email(email):
    """
    :param email: Email to check
    :raises: ValueError: invalid ID
    """
    if not is_valid_email(email):
        raise ValueError('{0} is not a valid email address.'
                         .format(email))


def verify_volume_av_parameters(enable_on_demand_scan, file_types_to_scan,
                                exclude_file_types, include_file_types, exclude_path):
    if enable_on_demand_scan:
        if file_types_to_scan not in ['all','onlyspecified']:
            raise ValueError("file_types_to_scan must be 'all' or 'onlyspecified'")
        if file_types_to_scan == 'all':
            if include_file_types is not None:
                raise ValueError("include_file_types can contain values only if file_types_to_scan is 'onlyspecified'")
        elif file_types_to_scan == 'onlyspecified':
            if exclude_file_types is not None:
                raise ValueError("exclude_file_types can contain values only if file_types_to_scan is 'all'")
        else:
            raise ValueError("file_types_to_scan can be only 'all' or 'onlyspecified'")
    else:
        if file_types_to_scan or exclude_file_types or include_file_types or exclude_path:
            raise ValueError('enable_on_demand_scan is False, the other parameters can not have values')


def verify_field(field_name, title, allow_quote=False):
    """

    :type field_name: str
    :param field_name: Display name

    :type title: str
    :param title: Field name

    :type allow_quote: bool
    :param allow_quote: If True, a single quote character (') will be allowed
        to pass validation.

    :return: Fixed field format
    :rtype: str

    :raises: ValueError: invalid ID
    """
    if field_name is not None:
        field_name = field_name.strip()
        if not is_valid_field(field_name, allow_quote=allow_quote):
            raise ValueError(
                '{} is not a valid {} name.'.format(field_name, title))

    return field_name


def verify_cloud_name(cloud_name):
    """
    :type cloud_name: str
    :param cloud_name: Cloud name

    :rtype: str
    :return: Fixed Cloud ID

    :raises: ValueError: Invalid capacity
    """
    cloud_name = cloud_name.strip()
    if not is_valid_field(cloud_name):
        raise ValueError('{0} is not a valid cloud name.'.format(cloud_name))

    return cloud_name


def verify_id(v_id):
    """
    :type v_id: str|int
    :param v_id: ID to check, which can only be a number

    :rtype: str
    :return: Fixed cloud ID

    :raises: ValueError: Invalid capacity
    """
    v_id = str(v_id)
    if not v_id.isdigit():
        raise ValueError("Cloud ID {0} is not a valid ID".format(v_id))

    return v_id


def verify_vpsa_id(vpsa_id):
    """
    :type vpsa_id: str|int
    :param vpsa_id: VPSA ID to check

    :rtype: str
    :return: Fixed VPSA ID

    :raises: ValueError: Invalid capacity
    """
    vpsa_id = str(vpsa_id)
    if not vpsa_id.isdigit() and not vpsa_id.startswith("vsa-"):
        raise ValueError(BAD_VPSA_ID.format(vpsa_id))

    return vpsa_id


def verify_zios_id(zios_id):
    """
    :type zios_id: str|int
    :param zios_id: VPSA ID to check

    :rtype: str
    :return: Fixed VPSA ID

    :raises: ValueError: Invalid capacity
    """
    zios_id = str(zios_id)
    if not zios_id.isdigit() and not zios_id.startswith("vsa-"):
        raise ValueError(BAD_VPSA_ID.format(zios_id))

    return zios_id


def verify_vpsa_internal_id(vpsa_internal_id):
    """
    :type vpsa_internal_id: str|int
    :param vpsa_internal_id: VPSA internal ID to check

    :rtype: str
    :return: Fixed VPSA internal ID

    :raises: ValueError: Invalid capacity
    """
    vpsa_id = str(vpsa_internal_id)

    if not is_valid_vpsa_internal_name(vpsa_internal_id):
        raise ValueError(
            '{0} is not a valid VPSA internal ID.'.format(vpsa_internal_id))

    return vpsa_id


def verify_policy_type_id(policy_type_id):
    """
    :type policy_type_id: str
    :param policy_type_id: policy type id - e.g. storage-policy-00000001

    :rtype: int
    :return: Fixed policy type ID

    :raises: ValueError: policy type id
    """
    if not re.match("storage-policy-\d+", policy_type_id):
        raise ValueError('{0} is not a valid policy type ID.'.format(policy_type_id))

    return int(policy_type_id.split("-")[2])


def verify_capacity(capacity, obj_name):
    """
    :type capacity: int
    :param capacity: Capacity to check

    :type obj_name: str
    :param obj_name: Object name to chekc. Example: pool, volume, etc.

    :rtype: int
    :return: Fixed capacity format

    :raises: ValueError: Invalid capacity
    """
    capacity = int(capacity)
    if capacity < 1:
        raise ValueError(
            '{0} capacity must be >= 1 GB ("{1}" was given)'.format(obj_name,
                                                                    capacity))
    return capacity


def verify_raid_groups(raid_groups):
    """
    :type raid_groups: str
    :param raid_groups: RAID groups ID

    :raises: ValueError: Invalid RAID group ID
    """
    for raid_group in raid_groups.split(','):
        if not is_valid_raid_id(raid_group):
            raise ValueError(
                '"{0}" in "{1}" is not a valid RAID group ID.'.format(
                    raid_group, raid_groups))


def verify_multiplier(num, multiplier):
    """
    Verifies that num % multiplier equals 0

    :type num: int|str
    :param num: Number to verify
    :type multiplier: int
    :param multiplier: Multiplier to module by

    :raises: ValueError: Invalid number
    """
    num = int(num)
    if num % multiplier != 0:
        raise ValueError('"{0}" % "{1}" Does not equal 0'.format(num, multiplier))


def verify_pool_type(pooltype):
    """
    :type pooltype: str
    :param pooltype: Pool type

    :raises: ValueError: Invalid Pool type
    """
    valid_pool_types = ['Transactional', 'Repository', 'Archival', 'Iops-Optimized', 'Balanced', 'Throughput-Optimized']
    if pooltype not in valid_pool_types:
        raise ValueError('"{0}" is not a valid pool type.  Allowed values are: {1}'.format(pooltype, str(valid_pool_types)))


def verify_start_limit_sort_severity(start, limit, sort, severity):
    """
    :type start: int
    :param start: The offset to start displaying snapshot policies from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of snapshot policies to return.
        Optional.

    :type sort: str
    :param sort: If set to 'DESC', logs will be returned newest first.  If set
        to 'ASC', logs are returned oldest first.  Optional (set to 'DESC' by
        default).

    :type severity: int
    :param severity: If set to None, all logs are returned.  If set to an
        integer, only messages for that severity are returned.  For example,
        critical messages have a 3 severity while warning messages have a 4
        severity.  Optional (will bet set to None by default).


    :return: Dictionary contains start and limit parameters
    :rtype: dict

    :raises: ValueError: Invalid start or limit
    """
    sort = sort.upper()

    if sort not in ['DESC', 'ASC']:
        raise ValueError('"{0}" is not a valid sort parameter. '
                         'Allowed values are: "DESC" or "ASC"'.format(sort))

    sort = '[{{"property":"msg-time","direction":"{sort}"}}]'.format(sort=sort)
    parameters = verify_start_limit(start, limit,
                                    [('sort', sort), ('severity', severity)])

    return parameters


def verify_start_limit(start, limit, list_options=None):
    """
    :type start: int
    :param start: The offset to start displaying snapshot policies from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of snapshot policies to return.
        Optional.

    :type: list_more_options: list
    :param list_options: List more options to add

    :return: Dictionary contains start and limit parameters
    :rtype: dict

    :raises: ValueError: Invalid start or limit
    """
    list_options = [] if list_options is None else list_options

    start = verify_positive_argument(start, 'start') if start else start
    limit = verify_positive_argument(limit, 'limit') if limit else limit

    tuple_all_options = [('start', start), ('limit', limit)] + list_options

    parameters = get_parameters_options(tuple_all_options)
    return parameters


def verify_versioning(versioning):
    """
    :type: versioning: str
    :param versioning: Type of versioning.
        Can be only x-versions-location or x-history-location.  Required.

    :return: fixed versioning format

    :raises: ValueError: Invalid start or limit
    """
    versioning = versioning.lower()
    if versioning not in ["x-versions-location", "x-history-location"]:
        raise ValueError("Versioning {0} could not be used, please use either "
                         "x-versions-location or x-history-location.".format(versioning))
    return versioning


def get_parameters_options(tuple_options):
    """
    :param tuple_options: List of tuples of option name and value
    :return: Dictionary of parameters key and value
    :rtype: dict
    """
    return {k: v for k, v in tuple_options if v is not None}


def verify_policy_creation(create_policy):
    """
    :param create_policy: Create policy pattern
    :raises: ValueError: invalid policy
    """
    if not is_valid_policy_creation(create_policy):
        raise ValueError(
            '"{0}" is not a valid snapshot policy creation frequency.'.format(
                create_policy))


def verify_snaprule_id(snap_rule_id):
    """
    :param snap_rule_id: Snapshot rule ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid Snapshot rule ID.'.format(_id)
                for _id in snap_rule_id.split(',') if
                not is_valid_snaprule_name(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_memory_pool(mempool_id):
    """
    :param mempool_id: Memory pool ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid Memory Pool ID.'.format(_id)
                for _id in mempool_id.split(',') if
                not is_valid_memory_pool(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_pool_id(pool_id, remote_pool_allowed=False):
    """
    :type remote_pool_allowed: bool
    :param remote_pool_allowed: Also validate remote pool IDs as described
        above.

    :type pool_id: str
    :param pool_id: Pool ID

    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid Pool ID.'.format(_id)
                for _id in pool_id.split(',') if
                not is_valid_pool_id(_id, remote_pool_allowed)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_cg_id(cg_id):
    """
    :param cg_id: CG ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid consistency group ID.'.format(_id)
                for _id in cg_id.split(',') if not is_valid_cg_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_remote_vpsa_id(rvpsa_id):
    """
    :param rvpsa_id: Remote VPSA ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid remote VPSA ID.'.format(_id)
                for _id in rvpsa_id.split(',') if not is_valid_rvpsa_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_mirror_id(mirror_id):
    """
    :param mirror_id: Mirror Job ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid Mirror ID.'.format(_id)
                for _id in mirror_id.split(',') if not is_valid_mirror_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_remote_clone_id(remote_clone_job_id):
    """
    :param remote_clone_job_id: Remote Clone Job ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid Remote Clone ID.'.format(_id)
                for _id in remote_clone_job_id.split(',') if
                not is_valid_remote_clone_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_controller_id(controller_id):
    """
    :param controller_id: Controller ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid virtual controller ID.'.format(_id)
                for _id in controller_id.split(',') if
                not is_valid_controller_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_zcs_container_id(zcs_container_id):
    """
    :param zcs_container_id: ZCS continer ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid ZCS container ID.'.format(_id)
                for _id in zcs_container_id.split(',') if
                not is_valid_zcs_container_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_zcs_image_id(zcs_image_id):
    """
    :param zcs_image_id: ZCS Image ID
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid ZCS image ID.'.format(_id)
                for _id in zcs_image_id.split(',') if
                not is_valid_zcs_image_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_migration_job_id(mgrjob_id):
    """

    :type mgrjob_id: str
    :param mgrjob_id: Migration Job ID

    :raises: ValueError: invalid ID
    """

    list_err = ['{0} is not a valid Migration Job ID.'.format(_id)
                for _id in mgrjob_id.split(',') if not is_valid_mgrjob_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_ros_destination_id(ros_destination_id):
    """
    :param ros_destination_id: ROS destination ID to check
    :raises: ValueError: invalid ID
    """
    list_err = [
        '{0} is not a valid remote object storage destination ID.'.format(_id)
        for _id in ros_destination_id.split(',') if
        not is_valid_ros_destination_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_ros_backup_job_id(ros_backup_job_id):
    """
    :param ros_backup_job_id: ROS backup job ID to check
    :raises: ValueError: invalid ID
    """
    list_err = [
        '{0} is not a valid remote object storage backup job ID.'.format(_id)
        for _id in ros_backup_job_id.split(',') if
        not is_valid_ros_backup_job_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_ros_restore_job_id(ros_restore_job_id):
    """
    :type ros_restore_job_id: str
    :param ros_restore_job_id: ROS restore job ID to check
    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid remote object storage ID.'.format(_id)
                for _id in ros_restore_job_id.split(',')
                if not is_valid_ros_restore_job_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_restore_job_mode(restore_mode):
    """
    :type restore_mode: str
    :param restore_mode: Restore job mode to verify. Should be: restore, clone
    """
    list_available_modes = ['restore', 'clone']
    if restore_mode not in list_available_modes:
        raise ValueError("Invalid restore job mode '{}'."
                         " Supported types: '{}'".
                         format(restore_mode, ",".join(list_available_modes)))


def verify_server_id(server_id):
    """
    :type server_id: str
    :param server_id: Server ID to check

    :raises: ValueError: invalid ID
    """
    list_err = ['{0} is not a valid server ID.'.format(_id) for _id in
                server_id.split(',')
                if not is_valid_server_id(_id)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_ticket_id(ticket_id):
    """
     :type ticket_id: int
     :param ticket_id: Ticket ID to check

     :raises: ValueError: invalid ID
     """
    if not is_valid_ticket_id(ticket_id):
        raise ValueError(
            '{0} is not a valid Ticket ID. [Should be positive]'.format(
                ticket_id))


def verify_boolean(flag, title):
    """
    :type: str
    :param flag: Boolean parameter to check

    :type: str
    :param title: Name of boolean parameter to print

    :rtype: str
    :return: Fix flag format

    :raises: ValueError: invalid form
    """
    if flag is None:
        return None
    flag = str(flag).upper()
    if flag not in ['YES', 'NO']:
        raise ValueError('"{}" is not a valid {} parameter. '
                         'Allowed values are: "YES" or "NO"'
                         .format(flag, title))
    return flag


def verify_bool(flag):
    """
    :type: str
    :param flag: Boolean parameter to check

    :rtype: str
    :return: Fix flag format

    :raises: ValueError: invalid form
    """
    if flag is None:
        return None
    flag = str(flag).upper()
    if flag not in ['YES', 'NO']:
        raise ValueError('"{}" is not a valid parameter. '
                         'Allowed values are: "YES" or "NO"'
                         .format(flag))
    return flag


def verify_bool_parameter(bool_param):
    """
    :type: bool
    :param bool_param: Boolean parameter to check

    :rtype: str
    :return: Fixed format

    :raises: ValueError: invalid form
    """
    if bool_param is None:
        return None
    if bool_param is True:
        return "true"
    if bool_param is False:
        return "false"

    raise ValueError('"{}" is not a valid parameter. Allowed values are: True or False'.format(bool_param))


def verify_on_off(flag):
    """
    :type: str
    :param flag: On/Off parameter to check

    :rtype: str
    :return: Fix flag format

    :raises: ValueError: invalid form
    """
    if flag is None:
        return None
    flag = str(flag).lower()
    if flag not in ['on', 'off']:
        raise ValueError('"{}" is not a valid parameter. '
                         'Allowed values are: "ON" or "OFF"'
                         .format(flag))
    return flag


def verify_group_project_polarity(group, project):
    """
    :type: str
    :param group: On/Off parameter to compare

    :type: str
    :param project: On/Off parameter to compare

    :raises: ValueError: invalid values
    """
    group = str(group).lower()
    project = str(project).lower()
    if group == 'on' and project == 'on':
        raise ValueError("Only one of 'Group'/'Project' quotas can be 'on'")


def verify_interval(interval):
    """
    :type interval: int
    :param interval: Time interval

    :return: Fixed interval format
    :rtype: int

    :raises: ValueError: invalid interval
    """
    interval = int(interval)
    if interval < 1:
        raise ValueError(
            'Interval must be at least 1 second ({0} was supplied).'.format(
                interval))

    return interval


def verify_group_name(group_name):
    """
    :type group_name: str
    :param group_name: Group name

    :rtype: str
    :return: Fixed username

    :raises: ValueError: Invalid username
    """
    if group_name in ['root', 'nogroup']:
        raise ValueError(
            'The root and nogroup users are assigned on every VPSA')

    return quote(group_name.strip())


def verify_name(username):
    """
    :type username: str
    :param username: username

    :rtype: str
    :return: Fixed username

    :raises: ValueError: Invalid username
    """

    if username in ['root', 'nobody']:
        raise ValueError(
            'The root and nobody users are assigned on every VPSA')

    return quote(username.strip())


def verify_string(smb_password):
    """
    :type smb_password: str
    :param smb_password: Changes the SMB password to this value.  Pass an
        empty string to remove the SMB password.

    :raises: ValueError: Invalid username
    """
    if type(smb_password) is not str:
        raise ValueError('A string must be passed for smb_password.')


def verify_not_none(str_to_check, title):
    """
    :type: str
    :param str_to_check: Boolean parameter to check

    :type: str
    :param title: Name of boolean parameter to print

    :raises: ValueError: Invalid input
    """
    if str_to_check is None:
        raise ValueError('The {} parameter must be passed.'.format(title))


def verify_mode(mode):
    """
    :type mode: str
    :param mode: Pool mode. i.e: stripe, simple

    :raises: ValueError: Invalid input
    """
    if mode not in ['stripe', 'simple']:
        raise ValueError(BAD_STRIPE_TYPE.format(mode))


def verify_drives(drives):
    """
    :type drives: str
    :param drives: Drives to check

    :raises: ValueError: Invalid input
    """
    list_err = ['"{0}" in "{1}" is not a valid drive ID.'.format(drive, drives)
                for drive in drives.split(',')
                if not is_valid_volume_id(drive)]
    if list_err:
        raise ValueError("\n".join(list_err))


def verify_positive_argument(param, title):
    """

    :type param: int
    :param param: Parameter to check

    :type title: str
    :param title: Interval parameter

    :rtype: int
    :return: Fix parameter format
    """
    if param is not None:
        param = int(param)
        if param < 1:
            raise ValueError(
                'Supplied {0} interval ("{1}") must be at least one'.format(
                    title, param))
    return param


def verify_cache_argument(param, title):
    """

    :type param: int
    :param param: Parameter to check

    :type title: str
    :param title: Interval parameter

    :rtype: int
    :return: Fix parameter format
    """
    if param is not None:
        param = int(param)
        if param % 200 != 0:
            raise ValueError(
                'Supplied {0} interval ("{1}") must be a multiplier of 200'.format(
                    title, param))
    return param


def verify_raid_type(protection):
    """
    :param protection: Protection to check
    :raises: ValueError: Invalid input
    """
    if protection not in ['RAID1', 'RAID5', 'RAID6']:
        raise ValueError('"{0}" is not a valid RAID type.  Allowed values '
                         'are: "RAID1", "RAID5", and "RAID6"'
                         .format(protection))
    return protection


def verify_stripe_size(stripe_size):
    """
    Verify stripe size

    :type stripe_size: str
    :param stripe_size: Stripe size to check
    :raises: ValueError: Invalid input
    """

    stripe_size = str(stripe_size)
    if stripe_size not in LIST_APPROVED_STRIPES_SIZES:
        raise ValueError(BAD_STRIPE_SIZES.format(
            stripe_size, ", ".join(LIST_APPROVED_STRIPES_SIZES)))


def verify_min_max(minimum, maximum):
    """
    :type minimum: int
    :param minimum: Minimum speed in MB per second

    :type maximum: int
    :param maximum: Maximum speed in MB per second

    :return: Fixed minimum, maximum
    :rtype: tuple
    """
    minimum = int(minimum)
    maximum = int(maximum)

    if minimum < 0 or maximum < 0:
        raise ValueError('Minimum speed ({0}) and maximum speed ({1}) must '
                         'both be a positive integer.'
                         .format(minimum, maximum))

    if minimum > maximum:
        raise ValueError('Minimum speed ({0}) must be less than maximum speed '
                         '({1}).'.format(minimum, maximum))

    return minimum, maximum


def verify_port(proxy_port):
    """
    :type: int
    :param proxy_port: Proxy tport to check

    :raises: ValueError: Invalid input
    """
    proxy_port = int(proxy_port)

    if proxy_port not in range(1, 65535):
        raise ValueError(
            '{0} is not a valid proxy port number.'.format(proxy_port))


def verify_restore_mode(restore_mode):
    """
    :type restore_mode: str
    :param restore_mode: Restore mode to check

    :raises: ValueError: Invalid input
    """
    if restore_mode not in ['restore', 'clone', 'import_seed']:
        raise ValueError('{0} is not a valid restore_mode parameter.  '
                         'Allowed values are: "restore", "clone", or '
                         '"import_seed"'.format(restore_mode))


def verify_vc_index(vc_index):
    """
    :param vc_index: VC index to check
    :raises: ValueError
    """
    if not is_valid_vc_index(vc_index=vc_index):
        raise ValueError('{0} is not a valid vc index.'
                         .format(vc_index))


def verify_access_type(access_type):
    """
    :param access_type: Access type to check
    :raises: ValueError: Invalid input
    """

    if access_type not in [None, 'NFS', 'SMB', 'BOTH']:
        raise ValueError('"{0}" is not a valid access_type parameter.  '
                         'Allowed values are: "NFS", "SMB", or "BOTH"'
                         .format(access_type))


def verify_read_mode(read_mode):
    """
    :param read_mode: Read mode to check
    :raises: ValueError: Invalid input
    """
    if read_mode not in ['roundrobin', 'localcopy']:
        raise ValueError('"{0}" is not a valid read_mode parameter.  Allowed '
                         'values are: "roundrobin" or "localcopy"'
                         .format(read_mode))


def verify_charset(charset):
    """
    :param charset: Charset to check
    :raises: ValueError: Invalid input
    """
    if charset not in ['UTF-8', 'ISO-8859-1']:
        raise ValueError('"{0}" is not a valid charset parameter.  Allowed '
                         'values are: "UTF-8" or "ISO-8859-1"'
                         .format(charset))


def verify_low_high_port(lowport, highport):
    """
    :type lowport: int
    :param lowport: Low Port

    :type highport: int
    :param highport: High Port

    :raises: ValueError: Invalid input
    """

    if lowport > highport:
        raise ValueError('The lowport parameter must be a lower number than '
                         'the highport parameter.')

    if lowport < 9216 or lowport > 10240:
        raise ValueError('The lowport parameter must be between 9216 and '
                         '10240 ("{0}" was passed).')

    if highport < 9216 or highport > 10240:
        raise ValueError('The highport parameter must be between 9216 and '
                         '10240 ("{0}" was passed).')


def verify_readahead(readaheadkb):
    """
    :type readaheadkb: str
    :param readaheadkb: Readahead KB to check

    :rtype: str
    :return: readahread

    :raises: ValueError: Invalid input
    """
    if readaheadkb not in ['16', '64', '128', '256', '512']:
        raise ValueError('"{0}" is not a valid readaheadkb parameter.  '
                         'Allowed values are: "16", "64", "128", "256", '
                         'or "512"'.format(readaheadkb))

    return readaheadkb


def verify_netmask(netmask, title):
    """
    :type netmask: str
    :param netmask: netmask

    :type title: str
    :param title: Title to print

    :rtype: str
    :return: netmask

    :raises: ValueError: Invalid input
    """
    if not is_valid_mask(netmask):
        raise ValueError('{0} must be a valid octal UNIX '
                         'style permission mask ("{1}" was given).'
                         .format(title, netmask))
    return netmask


def verify_percentage(percentage):
    """
    :type percentage: int
    :param percentage: Percentage to verify

    :rtype: bool
    :return: True if percentage is between 0 and 100

    :raises: ValueError: Invalid input
    """
    if isinstance(percentage,int):
        if 0 <= percentage <= 100:
            return True

    raise ValueError('Percentage {0} should be and int between 0 and 100'.format(percentage))


def verify_snapshot_rule_name(snapshot_rule_name):
    """
    :type: str
    :param snapshot_rule_name: Rule name to check

    :rtype: str
    :return: Snapshot rule name

    :raises: ValueError: Invalid input
    """
    if not is_valid_snapshot_rule_name(snapshot_rule_name):
        raise ValueError('{0} is not a valid snapshot rule name.'
                         .format(snapshot_rule_name))

    return snapshot_rule_name


"""
VPSAOS (ZIOS)
"""


def verify_account_id(account_id):
    """
    Verify Account ID

    :type account_id: str|int
    :param account_id: Account ID

    :return: Fixed account ID
    :rtype: True iff IO engine ID is valid
    """
    account_id = str(account_id)
    if len(account_id) != 32:
        raise ValueError(
            'The Account ID should be of length 32. Given: {}.'.format(
                account_id))
    return account_id


def verify_load_balancer_name(name):
    """
    Verify Load Balancer name

    :param name: Load Balancer name
    """
    if not isinstance(name, str):
        raise ValueError('Load Balancer name is not a string.')
    if not re.match("lbg-\d+", name):
        raise ValueError('Load Balancer name is not in the right format.')


def verify_encryption_state(state):
    """
    Verify encryption state to be 'enable' or 'disable'

    :param state: State to check
    """
    if state not in ('enable', 'disable'):
        raise ValueError('{0} is not a valid state.'.format(state))


def verify_io_engine_id(io_engine_id):
    """
    :param io_engine_id: IO engine ID to check
    :return: True iff IO engine ID is valid
    """
    if 'vsa.' not in io_engine_id:
        raise ValueError('{0} is not a valid IO engine type.'
                         .format(io_engine_id))


def verify_zcs_engine_id(zcs_engine_id):
    """
    :param zcs_engine_id: ZCS engine ID to check
    :return: True iff ZCS engine ID is valid
    """
    if zcs_engine_id not in ['None', 'tiny', 'small', 'medium', 'large',
                             'xlarge']:
        raise ValueError('{0} is not a valid ZCS engine type.'
                         .format(zcs_engine_id))


def verify_volume_type(type):
    """
    :param type: Vol type to check
    :return: True iff Vol type ID is valid
    """
    if type not in ['user', 'group', 'project']:
        raise ValueError('Volume scope can be only user, group or project')


def verify_nas_type(type):
    """
    :param type: Vol type to check
    :return: True iff NAS type ID is valid
    """
    if type not in ['ad', 'uid', 'nas']:
        raise ValueError('Volume scope can be only ad, uid or nas')
