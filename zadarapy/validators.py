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


import re
import socket


def is_valid_cg_id(cg_id):
    """
    Validates a consistency group ID, also known as the consistency group
    "cg_name".  A valid consistency group name should look like: cg-00000001
    - It should always start with "cg-" and end with 8 hexadecimal characters
    in lower case.

    :type cg_id: str
    :param cg_id: The consistency group name to be validated.

    :rtype: bool
    :return: True or False depending on whether drive_id passes validation.
    """
    if cg_id is None:
        return False

    match = re.match('^cg-[0-9a-f]{8}$', cg_id)

    if not match:
        return False

    return True


def is_valid_field(field, allow_quote=False):
    """
    Validates a generic user inputted field, such as a "name" for an
    object.  For now, it basically only validates whether single quote
    characters should be allowed in the string.

    :type field: str
    :param field: The data to be validated.

    :type allow_quote: bool
    :param allow_quote: If True, a single quote character (') will be allowed
        to pass validation.

    :rtype: bool
    :return: True or False depending on whether field passes validation.
    """
    if field is None:
        return False

    if not allow_quote and "'" in field:
        return False

    return True


def is_valid_hostname(hostname):
    """
    Validates hostnames.  A hostname may not be longer than 255 characters.
    Also, each field split by "." is validated against a valid character set
    for hostnames.

    :type hostname: str
    :param hostname: The data to be validated.

    :rtype: bool
    :return: True or False depending on whether hostname passes validation.
    """
    if hostname is None:
        return False

    if len(hostname) > 255:
        return False

    allowed = re.compile('(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)
    match = all(allowed.match(x) for x in hostname.split('.'))

    if not match:
        return False

    return True


def is_valid_ip_address(address):
    """
    Validates IP addresses.  Uses the Python socket library to attempt to
    convert the string input into a valid hexadecimal address.  If unable, it
    will return False.

    :type address: str
    :param address: The data to be validated.

    :rtype: bool
    :return: True or False depending on whether address passes validation.
    """
    if address is None:
        return False

    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def is_valid_mask(mask):
    """
    Validates a UNIX style permissions mask.  Mask must be octal.

    :type mask: str
    :param mask: The mask to be validated.

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


def is_valid_policy_id(policy_id):
    """
    Validates a snapshot policy ID, also known as the snapshot policy "name".
    A valid snapshot policy name should look like: policy-00000001 - It should
    always start with "cg-" and end with 8 hexadecimal characters in lower
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


def is_valid_server_id(server_id):
    """
    Validates a server ID, also known as the server "name".  A valid server
    name should look like: srv-00000001 - It should always start with "srv-"
    and end with 8 hexadecimal characters in lower case.

    :type server_id: str
    :param server_id: The server name to be validated.

    :rtype: bool
    :return: True or False depending on whether drive_id passes validation.
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


def is_valid_volume_id(drive_id):
    """
    Validates drive and volume IDs, also known as the drive/volume "name".
    A valid volume name should look like: volume-00000001 - It should always
    start with "volume-" and end with 8 hexadecimal characters in lower case.

    :type drive_id: str
    :param drive_id: The volume name to be validated.

    :rtype: bool
    :return: True or False depending on whether drive_id passes validation.
    """
    if drive_id is None:
        return False

    match = re.match('^volume-[0-9a-f]{8}$', drive_id)

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

    allowed = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    if not allowed.issuperset(key):
        return False

    return True
