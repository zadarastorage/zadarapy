#!/usr/bin/env python
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


import argparse
import sys
from pprint import pprint

from terminaltables import AsciiTable
from terminaltables import SingleTable

from zadarapy import __version__
from zadarapy import session
from zadarapy.command_center import vpsaos
from zadarapy.provisioning_portal import cloud
from zadarapy.provisioning_portal import vpsa
from zadarapy.vpsa import container_services
from zadarapy.vpsa import controllers
from zadarapy.vpsa import drives
from zadarapy.vpsa import logs
from zadarapy.vpsa import mirrors
from zadarapy.vpsa import nas_authentication
from zadarapy.vpsa import pools
from zadarapy.vpsa import raid_groups
from zadarapy.vpsa import remote_object_storage
from zadarapy.vpsa import servers
from zadarapy.vpsa import settings
from zadarapy.vpsa import snapshot_policies
from zadarapy.vpsa import tickets
from zadarapy.vpsa import volumes
from zadarapy.vpsa import vpsa_users
from zadarapy.vpsaos import controllers as vpsaos_controllers
from zadarapy.vpsaos import drives as vpsaos_drives
from zadarapy.vpsaos import settings as vpsaos_settings

ACTIVE_DIRECTORY_DNS_OPTION = {
    'option_positional': ['--dns'],
    'option_keywords': {
        'dest': 'param_dns',
        'metavar': '<xxx.xxx.xxx.xxx,yyy.yyy.yyy.yyy>',
        'type': str,
        'required': True,
        'help': 'A comma separated list of up to three DNS server IP '
                'addresses for the Active Directory domain.  Must have at '
                'least one DNS IP address defined.'
    }
}

ACTIVE_DIRECTORY_USERNAME_OPTION = {
    'option_positional': ['--username'],
    'option_keywords': {
        'dest': 'param_username',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'A username that has administrative permission to the Active '
                'Directory (typically, part of the "Domain Admins" group).'
    }
}

ACTIVE_DIRECTORY_PASSWORD_OPTION = {
    'option_positional': ['--password'],
    'option_keywords': {
        'dest': 'param_password',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The password for the Active Directory "username"'
    }
}

CAPACITY_OPTION = {
    'option_positional': ['--capacity'],
    'option_keywords': {
        'dest': 'param_capacity',
        'metavar': '<n>',
        'type': int,
        'required': True,
        'help': 'The capacity in GB to create/expand by.  Required.'
    }
}

CG_ID_OPTION = {
    'option_positional': ['--cg-id'],
    'option_keywords': {
        'dest': 'param_cg_id',
        'metavar': '<cg-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The volume "cg_name" value as returned by "volumes list".  '
                'For example: "cg-00000001".  Required.'
    }
}

CLOUD_ID_OPTION = {
    'option_positional': ['--cloud-id'],
    'option_keywords': {
        'dest': 'param_cloud_id',
        'metavar': '<cloud-name>',
        'type': str,
        'required': True,
        'help': 'The cloud "name" value as returned by "vpsa-operations '
                'list-clouds".  For example: "volume-00000001".  Required.'
    }
}

CLOUD_NAME_OPTION = {
    'option_positional': ['--cloud-name'],
    'option_keywords': {
        'dest': 'param_cloud_name',
        'metavar': '<cloud-name>',
        'type': str,
        'required': True,
        'help': 'The cloud "name" value as returned by "vpsa-operations '
                'list-clouds".  For example: "zadara-dev2".  Required.'
    }
}

COMPRESSION_OPTION = {
    'option_positional': ['--compression'],
    'option_keywords': {
        'dest': 'param_compression',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'YES',
        'help': 'If set to "YES", backup data will be compressed in flight.  '
                'If "NO", backup data will not be compressed.  Set to "YES" '
                'by default.'
    }
}

CONTROLLER_ID_OPTION = {
    'option_positional': ['--controller-id'],
    'option_keywords': {
        'dest': 'param_controller_id',
        'metavar': '<vsa-xxxxxxxx-vc-x>',
        'type': str.lower,
        'required': True,
        'help': 'The virtual controller "name" value as returned by '
                '"controllers list.  For example: "volume-00000001".  '
                'Required.'
    }
}

CRYPT_OPTION = {
    'option_positional': ['--crypt'],
    'option_keywords': {
        'dest': 'param_crypt',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'If YES, at rest encryption will be enabled for the volume '
                'using the VPSA encryption key defined by the user.  If NO, '
                'encryption will not be enabled.  Default: NO'
    }
}

DELETE_SNAPSHOTS_OPTION = {
    'option_positional': ['--delete-snapshots'],
    'option_keywords': {
        'dest': 'param_delete_snapshots',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'required': True,
        'help': 'If set to YES, all snapshots taken by the specified policy '
                'will be deleted.  If set to NO, taken snapshots will be '
                'retained.  Required.'
    }
}

DISPLAY_NAME_OPTION = {
    'option_positional': ['--display-name'],
    'option_keywords': {
        'dest': 'param_display_name',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The display name to set for the item.  Required.'
    }
}

DRIVE_ID_OPTION = {
    'option_positional': ['--drive-id'],
    'option_keywords': {
        'dest': 'param_drive_id',
        'metavar': '<volume-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The drive "name" value as returned by "drives list".  For '
                'example: "volume-00002a73".  Required.'
    }
}

DRIVE_TYPE_OPTION = {
    'option_positional': ['--drive-type'],
    'option_keywords': {
        'dest': 'param_drive_type',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The drive type.  Required.'
    }
}

DRIVE_QUANTITY_OPTION = {
    'option_positional': ['--drive-quantity'],
    'option_keywords': {
        'dest': 'param_drive_quantity',
        'metavar': '<n>',
        'type': int,
        'required': True,
        'help': 'The number of drives to be added.  Required.'
    }
}

ENCRYPTION_PWD_OPTION = {
    'option_positional': ['--encryption-pwd'],
    'option_keywords': {
        'dest': 'param_encryption_pwd',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The encryption password.  Required.'
    }
}

FORCE_OPTION = {
    'option_positional': ['--force'],
    'option_keywords': {
        'dest': 'param_force',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'If set to YES, ignore non-critical warnings and force the '
                'VPSA to accept the request.  If NO, return message on '
                'warning and abort.  Default: NO'
    }
}

IMAGE_OPTION = {
    'option_positional': ['--image'],
    'option_keywords': {
        'dest': 'param_image',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The VPSAOS "image" for example zios-00.00-1389.img. Required'
    }
}

INTERVAL_OPTION = {
    'option_positional': ['--interval'],
    'option_keywords': {
        'dest': 'param_interval',
        'metavar': '<n>',
        'type': int,
        'default': 1,
        'help': 'The interval to retrieve statistics for in minutes.  '
                'Default: 1'
    }
}

LIMIT_OPTION = {
    'option_positional': ['--limit'],
    'option_keywords': {
        'dest': 'param_limit',
        'metavar': '<n>',
        'type': int,
        'help': 'The maximum number of items to return'
    }
}

MIGRATION_ID_OPTION = {
    'option_positional': ['--migration-id'],
    'option_keywords': {
        'dest': 'param_mgrjob_id',
        'metavar': '<mgrjob-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The volume "migration_job_name" value as returned by '
                '"volumes show-migration-job".  For example: '
                '"mgrjob-00000001".  Required.'

    }
}

MIRROR_ID_OPTION = {
    'option_positional': ['--mirror-id'],
    'option_keywords': {
        'dest': 'param_mirror_id',
        'metavar': '<srcjvpsa-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The mirror job "job_name" value as returned by "mirrors '
                'list".  For example: "srcjvpsa-00000001".  Must be run on '
                'the mirror\'s source VPSA.  Required.'

    }
}

NAME_OPTION = {
    'option_positional': ['--name'],
    'option_keywords': {
        'dest': 'param_name',
        'metavar': '<volume-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The drive "name" value as returned by "drives list".  For '
                'example: "volume-00000001".  Required.'
    }
}

NAS_GROUPNAME_OPTION = {
    'option_positional': ['--groupname'],
    'option_keywords': {
        'dest': 'param_groupname',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The NAS "groupname".  Required.'
    }
}

NAS_USERNAME_OPTION = {
    'option_positional': ['--username'],
    'option_keywords': {
        'dest': 'param_username',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The NAS "username".  Required.'
    }
}

POLICY_DESC_OPTION = {
    'option_positional': ['--policy-desc'],
    'option_keywords': {
        'dest': 'param_policy_desc',
        'metavar': '<xxx>',
        'type': str,
        'help': 'The policy description.'
    }
}

POLICY_ID_OPTION = {
    'option_positional': ['--policy-id'],
    'option_keywords': {
        'dest': 'param_policy_id',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The policy "id".  Required.'
    }
}

POLICY_NAME_OPTION = {
    'option_positional': ['--policy-name'],
    'option_keywords': {
        'dest': 'param_policy_name',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The policy name.  Required.'
    }
}

POLICY_TYPE_ID_OPTION = {
    'option_positional': ['--policy-type-id'],
    'option_keywords': {
        'dest': 'param_policy_type_id',
        'metavar': '<n>',
        'type': int,
        'required': True,
        'help': 'Policy type id.  Required.'
    }
}

POOL_CACHE_OPTION = {
    'option_positional': ['--cache'],
    'option_keywords': {
        'dest': 'param_cache',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'required': True,
        'help': 'Toggles the storage pool SSD cache.  Required.'
    }
}

POOL_COW_CACHE_OPTION = {
    'option_positional': ['--cowcache'],
    'option_keywords': {
        'dest': 'param_cowcache',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'required': True,
        'help': 'Toggles the storage pool CoW cache.  Required.'
    }
}

POOL_ID_OPTION = {
    'option_positional': ['--pool-id'],
    'option_keywords': {
        'dest': 'param_pool_id',
        'metavar': '<pool-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The storage pool "name" value as returned by "pools list".  '
                'For example: "pool-00000001".  Required.'
    }
}

POOL_RAID_GROUPS_OPTION = {
    'option_positional': ['--raid-groups'],
    'option_keywords': {
        'dest': 'param_raid_groups',
        'metavar': '<RaidGroup-n,RaidGroup-n>',
        'type': str,
        'required': True,
        'help': 'A comma separated list of RAID groups to use for the '
                'storage pool with no spaces.  e.g.: '
                '"RaidGroup-3,RaidGroup-4".  Required.'
    }
}

PREFIX_OPTION = {
    'option_positional': ['--prefix'],
    'option_keywords': {
        'dest': 'param_prefix',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'Prefix for the zsnap.  Required.'
    }
}

QUANTITY_OPTION = {
    'option_positional': ['--quantity'],
    'option_keywords': {
        'dest': 'param_quantity',
        'metavar': '<n>',
        'type': int,
        'required': True,
        'help': 'The number of vcs to be removed.  Required.'
    }
}

RAID_GROUP_ID_OPTION = {
    'option_positional': ['--raid-group-id'],
    'option_keywords': {
        'dest': 'param_raid_id',
        'metavar': '<RaidGroup-n>',
        'type': str,
        'required': True,
        'help': 'The RAID group "name" value as returned by "raid-groups '
                'list".  For example: "RaidGroup-1".  Required.'
    }
}

REMOTE_POOL_ID_OPTION = {
    'option_positional': ['--remote-pool-id'],
    'option_keywords': {
        'dest': 'param_remote_pool_id',
        'metavar': '<rpool-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The remote storage pool "name" value as returned by '
                '"mirrors list-remote-pools".  For example: '
                '"rpool-00000001".  Required.'
    }
}

REMOTE_VPSA_ID_OPTION = {
    'option_positional': ['--remote-vpsa-id'],
    'option_keywords': {
        'dest': 'param_rvpsa_id',
        'metavar': '<rvpsa-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The remote VPSA "name" value as returned by '
                '"mirrors list-remote-vpsas".  For example: '
                '"rvpsa-00000001".  Required.'
    }
}

ROS_BACKUP_JOB_ID_OPTION = {
    'option_positional': ['--ros-backup-job-id'],
    'option_keywords': {
        'dest': 'param_ros_backup_job_id',
        'metavar': '<bkpjobs-xxxxxxxx>',
        'type': str.lower,
        'help': 'The remote object storage backup job "name" value as '
                'returned by "remote-object-storage list-backup-jobs".  For '
                'example: "bkpjobs-00000001".'
    }
}

ROS_DESTINATION_ID_OPTION = {
    'option_positional': ['--ros-destination-id'],
    'option_keywords': {
        'dest': 'param_ros_destination_id',
        'metavar': '<obsdst-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The remote object storage destination "name" value as '
                'returned by "remote-object-storage list-destinations".  '
                'For example: "obsdst-00000001".  Required.'
    }
}

ROS_RESTORE_JOB_ID_OPTION = {
    'option_positional': ['--ros-restore-job-id'],
    'option_keywords': {
        'dest': 'param_ros_restore_job_id',
        'metavar': '<rstjobs-xxxxxxxx>',
        'type': str.lower,
        'help': 'The remote object storage restore job "name" value as '
                'returned by "remote-object-storage list-restore-jobs".  For '
                'example: "rstjobs-00000001".'
    }
}

ROS_RESTORE_MODE_OPTION = {
    'option_positional': ['--restore-mode'],
    'option_keywords': {
        'dest': 'param_restore_mode',
        'choices': ['restore', 'clone', 'import_seed'],
        'type': str.lower,
        'required': True,
        'help': 'When set to "restore", the volume can be immediately '
                'attached to servers; data is retrieved from object storage '
                'on demand and in a background process; and all data will '
                'eventually be restored.  When set to "clone", the volume '
                'can be immediately attached to servers; and starting with '
                'zero capacity, data is retrieved from object storage only '
                'on-demand when accessed by the attached servers.  When set '
                'to "import_seed", a full capacity clone is created, '
                'including snapshot time-stamping; The volume can be '
                'attached to servers only after the volume\'s data was fully '
                'retrieved from object storage; use this mode to import '
                'initial data seed for remote mirroring.  Required.'
    }
}

SERVER_ID_OPTION = {
    'option_positional': ['--server-id'],
    'option_keywords': {
        'dest': 'param_server_id',
        'metavar': '<srv-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The server "name" value as returned by "servers list".  For '
                'example: "srv-00000001".  Required.'
    }
}

SERVER_ID_LIST_OPTION = {
    'option_positional': ['--server-ids'],
    'option_keywords': {
        'dest': 'param_servers',
        'metavar': '<srv-xxxxxxxx,srv-yyyyyyyy>',
        'type': str.lower,
        'required': True,
        'help': 'A comma separated list of server records, or one server '
                'record without any commas.'
    }
}

SNAPSHOT_ID_OPTION = {
    'option_positional': ['--snapshot-id'],
    'option_keywords': {
        'dest': 'param_snapshot_id',
        'metavar': '<snap-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The snapshot "name" value as returned by "volumes '
                'list-snapshots".  For example: "snap-00000001".  Required.'
    }
}

SNAPSHOT_POLICY_ID_OPTION = {
    'option_positional': ['--snapshot-policy-id'],
    'option_keywords': {
        'dest': 'param_policy_id',
        'metavar': '<policy-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The snapshot policy "name" value as returned by '
                '"snapshot-policies list".  For example: "policy-00000001".  '
                'Required.'
    }
}

SSE_OPTION = {
    'option_positional': ['--sse'],
    'option_keywords': {
        'dest': 'param_sse',
        'metavar': '<xxxxx>',
        'type': str,
        'required': True,
        'help': 'The remote object storage destination SSE: NO, AES256, KMS or KMSKEYID.  Required.'
    }
}

START_OPTION = {
    'option_positional': ['--start'],
    'option_keywords': {
        'dest': 'param_start',
        'metavar': '<n>',
        'type': int,
        'help': 'The offset to start displaying items from'
    }
}

STATE_OPTION = {
    'option_positional': ['--state'],
    'option_keywords': {
        'dest': 'param_state',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The encryption state enable/disable.  Required'
    }
}

TICKET_ID_OPTION = {
    'option_positional': ['--ticket-id'],
    'option_keywords': {
        'dest': 'param_ticket_id',
        'metavar': '<n>',
        'type': int,
        'help': 'The ticket "id" value as returned by "tickets list".  For '
                'example: 103538.  Required.'
    }
}

VC_INDEX_OPTION = {
    'option_positional': ['--vc-index'],
    'option_keywords': {
        'dest': 'param_vc_index',
        'metavar': '<n>',
        'type': int,
        'required': True,
        'help': 'The virtual controller "index" value as returned by '
                '"VPSAOS controllers list. '
                'Required.'
    }
}

VOLUME_ID_OPTION = {
    'option_positional': ['--volume-id'],
    'option_keywords': {
        'dest': 'param_volume_id',
        'metavar': '<volume-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The volume "name" value as returned by "volumes list".  For '
                'example: "volume-00000001".  Required.'
    }
}

VOLUME_BLOCK_OPTION = {
    'option_positional': ['--block'],
    'option_keywords': {
        'dest': 'param_block',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'required': True,
        'help': 'If YES, the volume will be block (iSCSI/iSER).  If NO, it '
                'will be a NAS volume (NFS/SMB).  Required.'
    }
}

VOLUME_ATTACHPOLICIES_OPTION = {
    'option_positional': ['--attachpolicies'],
    'option_keywords': {
        'dest': 'param_attachpolicies',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'YES',
        'help': 'If YES, the default snapshot policies for the VPSA will be '
                'attached.  If NO, no snapshot policies will be assigned.  '
                'Default: YES'
    }
}

VOLUME_EXPORT_NAME_OPTION = {
    'option_positional': ['--export-name'],
    'option_keywords': {
        'dest': 'param_export_name',
        'metavar': '<xxx>',
        'type': str,
        'help': 'If set, the last part of the NFS/SMB export path will be '
                'set to this value.  If not set, display_name will be used.'
    }
}

VOLUME_ATIMEUPDATE_OPTION = {
    'option_positional': ['--atimeupdate'],
    'option_keywords': {
        'dest': 'param_atimeupdate',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'If YES, NAS shares will updated last accessed time each '
                'time a file is accessed (impacts performance).  Default: NO'
    }
}

VOLUME_NFSROOTSQUASH_OPTION = {
    'option_positional': ['--nfsrootsquash'],
    'option_keywords': {
        'dest': 'param_nfsrootsquash',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'For NAS shares, when using NFS, if YES, root squash is  '
                'enabled.  Default: NO'
    }
}

VOLUME_READAHEADKB_OPTION = {
    'option_positional': ['--readaheadkb'],
    'option_keywords': {
        'dest': 'param_readaheadkb',
        'choices': ['16', '64', '128', '256', '512'],
        'type': str,
        'default': '512',
        'help': 'Sets the read ahead size in KB.  Default: 512'
    }
}

VOLUME_SMBONLY_OPTION = {
    'option_positional': ['--smbonly'],
    'option_keywords': {
        'dest': 'param_smbonly',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'If YES, NAS shares will be accessible only via SMB '
                '(improves performance).  Default: NO'
    }
}

VOLUME_SMBGUEST_OPTION = {
    'option_positional': ['--smbguest'],
    'option_keywords': {
        'dest': 'param_smbguest',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'If YES, authentication will not be required to login to and '
                'read/write from/to a SMB share.  Default: NO'
    }
}

VOLUME_SMBWINDOWSACL_OPTION = {
    'option_positional': ['--smbwindowsacl'],
    'option_keywords': {
        'dest': 'param_smbwindowsacl',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'If YES, extended ACLs will be enabled for SMB shares.  '
                'Default: NO'
    }
}

VOLUME_SMBFILECREATEMASK_OPTION = {
    'option_positional': ['--smbfilecreatemask'],
    'option_keywords': {
        'dest': 'param_smbfilecreatemask',
        'metavar': '<nnnn>',
        'type': str,
        'default': '0744',
        'help': 'For NAS shares, the permissions assigned to new files '
                'created through SMB shares.  Default: 0744'
    }
}

VOLUME_SMBDIRCREATEMASK_OPTION = {
    'option_positional': ['--smbdircreatemask'],
    'option_keywords': {
        'dest': 'param_smbdircreatemask',
        'metavar': '<nnnn>',
        'type': str,
        'default': '0755',
        'help': 'For NAS shares, the permissions assigned to new directories '
                'created through SMB shares.  Default: 0755'
    }
}

VOLUME_SMBMAPARCHIVE_OPTION = {
    'option_positional': ['--smbmaparchive'],
    'option_keywords': {
        'dest': 'param_smbmaparchive',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'YES',
        'help': 'For NAS shares, when using SMB, if YES, a file\'s execute '
                'bit will be used to flag the Archive file attribute.  '
                'Default: YES'
    }
}

VOLUME_SMBAIOSIZE_OPTION = {
    'option_positional': ['--smbaiosize'],
    'option_keywords': {
        'dest': 'param_smbaiosize',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'NO',
        'help': 'For NAS shares, when using SMB, if YES, file reads will be '
                'performed asynchronously, which improves performance for '
                'some workloads.  Default: NO'
    }
}

VOLUME_SMBBROWSEABLE_OPTION = {
    'option_positional': ['--smbbrowseable'],
    'option_keywords': {
        'dest': 'param_smbbrowseable',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'YES',
        'help': 'For NAS shares, when using SMB, if YES, the share will be '
                'visible when browsing the VPSA IP; i.e. at \\\\ip.of.vpsa.  '
                'Default: YES'
    }
}

VOLUME_HIDDENFILES_OPTION = {
    'option_positional': ['--hiddenfiles'],
    'option_keywords': {
        'dest': 'param_hiddenfiles',
        'metavar': '</xxx/yyy/zzz/>',
        'type': str,
        'help': 'For NAS shares, when using SMB/CIFS, this is a forward '
                'delimited list of filenames and/or wildcards to be hidden '
                'from users by the VPSA.'
    }
}

VPSA_ID_OPTION = {
    'option_positional': ['--vpsa-id'],
    'option_keywords': {
        'dest': 'param_vpsa_id',
        'metavar': '<vpsa-id>',
        'type': int,
        'required': True,
        'help': 'The VPSA "id" value as returned by "vpsa-operations '
                'list-vpsas".  For example: "2653".  Required.'
    }
}

VPSA_USERNAME_OPTION = {
    'option_positional': ['--username'],
    'option_keywords': {
        'dest': 'param_username',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The VPSA "username" value as returned by "vpsa-users list". '
                'Required.'
    }
}

VPSA_PASSWORD_OPTION = {
    'option_positional': ['--password'],
    'option_keywords': {
        'dest': 'param_password',
        'metavar': '<xxx>',
        'type': str,
        'required': True,
        'help': 'The password for the supplied VPSA "username".  Required.'
    }
}

VSA_ID_OPTION = {
    'option_positional': ['--vsa-id'],
    'option_keywords': {
        'dest': 'param_vsa_id',
        'metavar': '<vsa-id>',
        'type': str,
        'required': True,
        'help': 'The "vsa_id" value as returned by "vpsa-operations '
                'list-vpsas".  For example: "vsa-000007de".  Required.'
    }
}

WAN_OPTIMIZATION_OPTION = {
    'option_positional': ['--wan-optimization'],
    'option_keywords': {
        'dest': 'param_wan_optimization',
        'choices': ['YES', 'NO'],
        'type': str.upper,
        'default': 'YES',
        'help': 'If set to \'YES\', the mirror will attempt to reduce the '
                'amount of data needing to be synchronized to the remote '
                'side at the expense of more load on the source VPSA.  '
                'If set to \'NO\', more data will be sent by the mirror with '
                'less load on the source VPSA.  Set to \'YES\' by default.'
    }
}

ZCS_CONTAINER_ID_OPTION = {
    'option_positional': ['--zcs-container-id'],
    'option_keywords': {
        'dest': 'param_zcs_container_id',
        'metavar': '<container-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The ZCS container "name" value as returned by '
                '"container-services list-containers".  For example: '
                '"container-00000001".  Required.'
    }
}

ZCS_IMAGE_ID_OPTION = {
    'option_positional': ['--zcs-image-id'],
    'option_keywords': {
        'dest': 'param_zcs_image_id',
        'metavar': '<img-xxxxxxxx>',
        'type': str.lower,
        'required': True,
        'help': 'The ZCS image "name" value as returned by '
                '"container-services list-images".  For example: '
                '"img-00000001".  Required.'
    }
}

COMMANDS_DICT = [
    {
        'command_name': 'container-services',
        'help': 'Commands related to Zadara Container Services (ZCS)',
        'subcommands': [
            {
                'subcommand_info': ('create-container',
                                    container_services.create_zcs_container),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    ZCS_IMAGE_ID_OPTION,
                    {
                        'option_positional': ['--start'],
                        'option_keywords': {
                            'dest': 'param_start',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'help': 'If set to YES, the container will be '
                                    'started on creation.  If set to NO, '
                                    'the container will be created in the '
                                    'stopped state'
                        }
                    },
                    {
                        'option_positional': ['--use-public-ip'],
                        'option_keywords': {
                            'dest': 'param_use_public_ip',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to YES, the ZCS container will '
                                    'listen on VPSA\'s public IP address '
                                    '(only valid on VPSAs with a public IP '
                                    'address).  If set to NO, the '
                                    'container will listen on the same '
                                    'private IP address that is used for '
                                    'addressing the storage.  Set to NO by '
                                    'default.'
                        }
                    },
                    {
                        'option_positional': ['--entrypoint'],
                        'option_keywords': {
                            'dest': 'param_entrypoint',
                            'metavar': '</path/to/entry/program>',
                            'type': str,
                            'help': 'The full path to the program or script '
                                    'inside the ZCS container to run when '
                                    'the container starts.  For example: '
                                    '"/usr/local/bin/entry.sh"'
                        }
                    },
                    {
                        'option_positional': ['--volumes'],
                        'option_keywords': {
                            'dest': 'param_volumes',
                            'metavar': '<valid_json>',
                            'type': str,
                            'help': 'Please see documentation from the '
                                    'zadarapy module, function '
                                    'create_zcs_container, parameter volumes '
                                    'for more on how use this parameter'
                        }
                    },
                    {
                        'option_positional': ['--args'],
                        'option_keywords': {
                            'dest': 'param_args',
                            'metavar': '<valid_json>',
                            'type': str,
                            'help': 'Please see documentation from the '
                                    'zadarapy module, function '
                                    'create_zcs_container, parameter args '
                                    'for more on how use this parameter'
                        }
                    },
                    {
                        'option_positional': ['--envvars'],
                        'option_keywords': {
                            'dest': 'param_envvars',
                            'metavar': '<valid_json>',
                            'type': str,
                            'help': 'Please see documentation from the '
                                    'zadarapy module, function '
                                    'create_zcs_container, parameter envvars '
                                    'for more on how use this parameter'
                        }
                    }
                ],
                'subcommand_return_key': 'container_name',
                'subcommand_help': 'Creates a new ZCS container from the '
                                   'provided ZCS image ID'
            },
            {
                'subcommand_info': ('create-image',
                                    container_services.create_zcs_image),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--path'],
                        'option_keywords': {
                            'dest': 'param_path',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'When importing from Docker Hub, this is '
                                    'the name of the Docker image; for '
                                    'example: "ubuntu" or "zadara/ssh".  '
                                    'When importing from a volume (requires '
                                    'the --volume-id parameter), the full '
                                    'path on the volume to the Docker image '
                                    'tar file; for example: '
                                    '"images/testimage.tar".'
                        }
                    },
                    {
                        'option_positional': ['--volume-id'],
                        'option_keywords': {
                            'dest': 'param_volume_id',
                            'metavar': '<volume-xxxxxxxx>',
                            'type': str.lower,
                            'help': 'The volume "name" value as returned by '
                                    '"volumes list".  For example: '
                                    '"volume-00000001".  When specified, the '
                                    'ZCS image will be imported from this '
                                    'volume instead of Docker Hub.'
                        }
                    }
                ],
                'subcommand_return_key': 'image_name',
                'subcommand_help': 'Creates a ZCS image'
            },
            {
                'subcommand_info': ('delete-container',
                                    container_services.delete_zcs_container),
                'subcommand_options': [
                    ZCS_CONTAINER_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a ZCS container.  The container '
                                   'must first be stopped.'
            },
            {
                'subcommand_info': ('delete-image',
                                    container_services.delete_zcs_image),
                'subcommand_options': [
                    ZCS_IMAGE_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a ZCS image if no containers '
                                   'exist from the image'
            },
            {
                'subcommand_info': ('get-container',
                                    container_services.get_zcs_container),
                'subcommand_options': [
                    ZCS_IMAGE_ID_OPTION
                ],
                'subcommand_return_key': 'images',
                'subcommand_help': 'Displays details for a single ZCS '
                                   'container'
            },
            {
                'subcommand_info': ('get-image',
                                    container_services.get_zcs_image),
                'subcommand_options': [
                    ZCS_IMAGE_ID_OPTION
                ],
                'subcommand_return_key': 'image',
                'subcommand_help': 'Displays details for a single ZCS image'
            },
            {
                'subcommand_info': ('list-containers',
                                    container_services.
                                    get_all_zcs_containers),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'containers',
                'subcommand_help': 'Displays details for all ZCS containers '
                                   'on the VPSA'
            },
            {
                'subcommand_info': ('list-containers-by-image',
                                    container_services.
                                    get_all_zcs_containers_by_image),
                'subcommand_options': [
                    ZCS_IMAGE_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'containers',
                'subcommand_help': 'Displays details for all ZCS containers '
                                   'on the VPSA spawned from the specified '
                                   'ZCS image'
            },
            {
                'subcommand_info': ('list-images',
                                    container_services.get_all_zcs_images),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'images',
                'subcommand_help': 'Displays details for all ZCS images on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('start-container',
                                    container_services.start_zcs_container),
                'subcommand_options': [
                    ZCS_CONTAINER_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Starts a container that is currently '
                                   'stopped'
            },
            {
                'subcommand_info': ('stop-container',
                                    container_services.stop_zcs_container),
                'subcommand_options': [
                    ZCS_CONTAINER_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Stops a container that is currently '
                                   'running'
            }
        ]
    },
    {
        'command_name': 'controllers',
        'help': 'Commands related to virtual controllers',
        'subcommands': [
            {
                'subcommand_info': ('cache-performance',
                                    controllers.get_cache_performance),
                'subcommand_options': [
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'zcache_usages',
                'subcommand_help': 'Gets performance statistics for the '
                                   'SSD pool cache'
            },
            {
                'subcommand_info': ('cache-stats',
                                    controllers.get_cache_stats),
                'subcommand_options': [
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets usage and hit rate statistics for '
                                   'the SSD pool cache'
            },
            {
                'subcommand_info': ('controller-performance',
                                    controllers.get_controller_performance),
                'subcommand_options': [
                    CONTROLLER_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a '
                                   'virtual controller'
            },
            {
                'subcommand_info': ('failover',
                                    controllers.failover_controller),
                'subcommand_options': [
                    {
                        'option_positional': ['--confirm'],
                        'option_keywords': {
                            'dest': 'param_confirm',
                            'action': 'store_true',
                            'required': True,
                            'help': 'Controller failover will only be '
                                    'performed if this flag is passed.'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Initiate a controller failover - the '
                                   'standby controller becomes active.'
            },
            {
                'subcommand_info': ('list', controllers.get_all_controllers),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'vcontrollers',
                'subcommand_help': 'Displays details for all virtual '
                                   'controllers on the VPSA'
            }
        ]
    },
    {
        'command_name': 'drives',
        'help': 'Commands related to individual drives',
        'subcommands': [
            {
                'subcommand_info': ('get', drives.get_drive),
                'subcommand_options': [
                    DRIVE_ID_OPTION
                ],
                'subcommand_return_key': 'disk',
                'subcommand_help': 'Displays details for a single drive on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('list', drives.get_all_drives),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'disks',
                'subcommand_help': 'Displays details for all drives attached '
                                   'to the VPSA'
            },
            {
                'subcommand_info': ('list-free', drives.get_free_drives),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'disks',
                'subcommand_help': 'Displays details for all drives '
                                   'available for use on the VPSA (not '
                                   'currently in a RAID group)'
            },
            {
                'subcommand_info': ('performance',
                                    drives.get_drive_performance),
                'subcommand_options': [
                    DRIVE_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a drive'
            },
            {
                'subcommand_info': ('remove', drives.remove_drive),
                'subcommand_options': [
                    DRIVE_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Removes an unused drive from the VPSA'
            },
            {
                'subcommand_info': ('rename', drives.rename_drive),
                'subcommand_options': [
                    DRIVE_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the display name for a drive'
            },
            {
                'subcommand_info': ('replace', drives.replace_drive),
                'subcommand_options': [
                    DRIVE_ID_OPTION,
                    {
                        'option_positional': ['--to_drive_id'],
                        'option_keywords': {
                            'dest': 'param_to_drive_id',
                            'metavar': '<volume-xxxxxxxx>',
                            'type': str.lower,
                            'required': True,
                            'help': 'The drive ID of the drive that will '
                                    'will be used as the replacement.  '
                                    'Required.'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Replaces the drive identified by id with '
                                   'the drive identified by display_name.'
            },
            {
                'subcommand_info': ('shred', drives.shred_drive),
                'subcommand_options': [
                    DRIVE_ID_OPTION,
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Shreds all data on a drive.  THIS ACTION '
                                   'IS IRREVERSIBLE.'
            },
            {
                'subcommand_info': ('shred-cancel',
                                    drives.cancel_shred_drive),
                'subcommand_options': [
                    DRIVE_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Cancels a currently running shred drive '
                                   'process.'
            }
        ]
    },
    {
        'command_name': 'logs',
        'help': 'Commands related to VPSA logs',
        'subcommands': [
            {
                'subcommand_info': ('list', logs.get_logs),
                'subcommand_options': [
                    {
                        'option_positional': ['--sort'],
                        'option_keywords': {
                            'dest': 'param_sort',
                            'choices': ['ASC', 'DESC'],
                            'type': str.upper,
                            'default': 'DESC',
                            'help': 'If set to DESC, logs will be returned '
                                    'newest first.  If set to ASC, logs are '
                                    'returned oldest first.  Default is DESC'
                        }
                    },
                    {
                        'option_positional': ['--severity'],
                        'option_keywords': {
                            'dest': 'param_severity',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'If not defined, all logs are returned.  '
                                    'If set to an integer, only messages for '
                                    'that severity are returned.  For '
                                    'example, critical messages have a 3 '
                                    'severity while warning messages have a '
                                    '4 severity.'
                        }
                    },
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'messages',
                'subcommand_help': 'Displays logs from the VPSA'
            },
        ]
    },
    {
        'command_name': 'migration',
        'help': 'Commands related to migrating volumes',
        'subcommands': [
            {
                'subcommand_info': ('cancel-volume-migration',
                                    volumes.cancel_volume_migration),
                'subcommand_options': [
                    MIGRATION_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Cancels a volume migration job.'
            },
            {
                'subcommand_info': ('migrate-volume', volumes.migrate_volume),
                'subcommand_options': [
                    CG_ID_OPTION,
                    POOL_ID_OPTION,
                    {
                        'option_positional': ['--migrate-snapshots'],
                        'option_keywords': {
                            'dest': 'param_migrate_snaps',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'YES',
                            'help': 'If set to YES, all of the affected '
                                    'volume\'s snapshots will be migrated '
                                    'along with the volume.  Defaults to YES.'
                        }
                    }
                ],
                'subcommand_return_key': 'migration_job_name',
                'subcommand_help': 'Migrates a volume from one storage pool '
                                   'to another - this can be done while '
                                   'clients continue to use the affected '
                                   'volume.'
            },
            {
                'subcommand_info': ('pause-volume-migration',
                                    volumes.pause_volume_migration),
                'subcommand_options': [
                    MIGRATION_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Pauses a running volume migration job'
            },
            {
                'subcommand_info': ('resume-volume-migration',
                                    volumes.resume_volume_migration),
                'subcommand_options': [
                    MIGRATION_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resumes a paused volume migration job'
            },
            {
                'subcommand_info': ('show-volume-migration',
                                    volumes.get_volume_migration),
                'subcommand_options': [
                    CG_ID_OPTION
                ],
                'subcommand_return_key': 'migration_job',
                'subcommand_help': 'Displays details for a volume migration '
                                   'job'
            }
        ]
    },
    {
        'command_name': 'mirrors',
        'help': 'Commands related to mirroring volumes',
        'subcommands': [
            {
                'subcommand_info': ('add-additional-policy',
                                    mirrors.add_mirror_snapshot_policy),
                'subcommand_options': [
                    MIRROR_ID_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Adds an additional snapshot policy to an '
                                   'existing mirror job'
            },
            {
                'subcommand_info': ('break', mirrors.break_mirror),
                'subcommand_options': [
                    MIRROR_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Breaks a mirror job'
            },
            {
                'subcommand_info': ('change-wan-optimization',
                                    mirrors.update_mirror_wan_optimization),
                'subcommand_options': [
                    MIRROR_ID_OPTION,
                    WAN_OPTIMIZATION_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes a mirror job\'s WAN optimization '
                                   'setting.'
            },
            {
                'subcommand_info': ('create-mirror',
                                    volumes.create_volume_mirror),
                'subcommand_options': [
                    CG_ID_OPTION,
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--policy-id'],
                        'option_keywords': {
                            'dest': 'param_policies',
                            'metavar': '<snap-xxxxxxxx,snap-yyyyyyyy>',
                            'type': str,
                            'help': 'The snapshot policy "name" value as '
                                    'returned by "volumes '
                                    'list-snapshot-policies".  For example: '
                                    'example: "policy-00000001".  Mirroring '
                                    'frequency is based on the frequency of '
                                    'specified policies.  Can be more than '
                                    'one policy, comma separated, with no '
                                    'spaces.  Required.'
                        }
                    },
                    REMOTE_POOL_ID_OPTION,
                    {
                        'option_positional': ['--remote-volume-name'],
                        'option_keywords': {
                            'dest': 'param_remote_volume_name',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The display name to set for the remote '
                                    'volume.  Required.'
                        }
                    },
                    WAN_OPTIMIZATION_OPTION
                ],
                'subcommand_return_key': 'vpsa_mirror_job_name',
                'subcommand_help': 'Creates an asynchronous mirror job to a '
                                   'remote VPSA based on the provided '
                                   'snapshot policies.'
            },
            {
                'subcommand_info': ('discover', mirrors.discover_remote_vpsa),
                'subcommand_options': [
                    {
                        'option_positional': ['--ip-address'],
                        'option_keywords': {
                            'dest': 'param_ip_address',
                            'metavar': '<xxx.xxx.xxx.xxx>',
                            'type': str,
                            'help': 'The IP address of the remote VPSA'
                        }
                    },
                    {
                        'option_positional': ['--username'],
                        'option_keywords': {
                            'dest': 'param_username',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The username of the admin GUI user on '
                                    'the remote VPSA'
                        }
                    },
                    {
                        'option_positional': ['--password'],
                        'option_keywords': {
                            'dest': 'param_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The password of the admin GUI user on '
                                    'the remote VPSA'
                        }
                    },
                    {
                        'option_positional': ['--public'],
                        'option_keywords': {
                            'dest': 'param_public',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to YES, the remote VPSA will be '
                                    'discovered through the VPSA\'s public '
                                    'IP address, if assigned.  If NO, the '
                                    'private data/management IP will be used '
                                    '(remote VPSA must be routable). '
                                    'Defaults to NO.'
                        }
                    }
                ],
                'subcommand_return_key': 'remote_vpsa_name',
                'subcommand_help': 'Discovers a remote VPSA for use as a '
                                   'mirror target'
            },
            {
                'subcommand_info': ('get-remote-vpsa',
                                    mirrors.get_remote_vpsa),
                'subcommand_options': [
                    REMOTE_VPSA_ID_OPTION
                ],
                'subcommand_return_key': 'remote_vpsa',
                'subcommand_help': 'Displays details for a single remote '
                                   'VPSA discovered by the VPSA'
            },
            {
                'subcommand_info': ('list-mirror-jobs',
                                    mirrors.get_all_mirrors),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'vpsa_mirror_jobs',
                'subcommand_help': 'Displays details for all mirror jobs on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('list-remote-pools',
                                    mirrors.get_remote_vpsa_pools),
                'subcommand_options': [
                    REMOTE_VPSA_ID_OPTION
                ],
                'subcommand_return_key': 'remote_pools',
                'subcommand_help': 'Displays details for all pools on the '
                                   'provided remote VPSA'
            },
            {
                'subcommand_info': ('list-remote-vpsas',
                                    mirrors.get_all_remote_vpsas),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'remote_vpsas',
                'subcommand_help': 'Displays details for all remote VPSAs '
                                   'discovered by the VPSA'
            },
            {
                'subcommand_info': ('list-suggested-mirrors',
                                    mirrors.get_suggested_mirrors),
                'subcommand_options': [
                    REMOTE_VPSA_ID_OPTION,
                    CG_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'sugested_jobs',
                'subcommand_help': 'Displays details of suggested volumes '
                                   'from which previously broken mirrors can '
                                   'can be resumed from remote VPSA'
            },
            {
                'subcommand_info': ('pause', mirrors.pause_mirror),
                'subcommand_options': [
                    MIRROR_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Pauses a running mirror job'
            },
            {
                'subcommand_info': ('refresh-remote-vpsa',
                                    mirrors.refresh_remote_vpsa),
                'subcommand_options': [
                    REMOTE_VPSA_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Refreshes details about a remote VPSA, '
                                   'such as remote pools and their usage'
            },
            {
                'subcommand_info': ('remove-remote-vpsa',
                                    mirrors.remove_remote_vpsa),
                'subcommand_options': [
                    REMOTE_VPSA_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Removes a discovered remote VPSA that '
                                   'has no associated mirror jobs'
            },
            {
                'subcommand_info': ('remove-policy',
                                    mirrors.remove_mirror_snapshot_policy),
                'subcommand_options': [
                    MIRROR_ID_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION,
                    DELETE_SNAPSHOTS_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Removes a snapshot policy from an '
                                   'existing mirror job'
            },
            {
                'subcommand_info': ('resume-broken-mirror',
                                    mirrors.resume_broken_mirror),
                'subcommand_options': [
                    REMOTE_VPSA_ID_OPTION,
                    DISPLAY_NAME_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION,
                    {
                        'option_positional': ['--local-snapshot-id'],
                        'option_keywords': {
                            'dest': 'param_local_snapshot_id',
                            'metavar': '<snap-xxxxxxxx>',
                            'type': str,
                            'required': True,
                            'help': 'The local snapshot "src_snap_name" '
                                    'value as returned by "mirrors '
                                    'list-suggested-mirrors".  For '
                                    'example: "snap-00000001".  Required.'
                        }
                    },
                    {
                        'option_positional': ['--remote-snapshot-id'],
                        'option_keywords': {
                            'dest': 'param_remote_snapshot_id',
                            'metavar': '<snap-xxxxxxxx>',
                            'type': str,
                            'required': True,
                            'help': 'The local snapshot "dst_snap_name" '
                                    'value as returned by "mirrors '
                                    'list-suggested-mirrors".  For '
                                    'example: "snap-00000001".  Required.'
                        }
                    },
                    WAN_OPTIMIZATION_OPTION
                ],
                'subcommand_return_key': 'vpsa_mirror_job_name',
                'subcommand_help': 'Resumes a previously broken mirror job '
                                   'if a suitable snapshot can be found on '
                                   'the remote VPSA'
            },
            {
                'subcommand_info': ('resume-paused-mirror',
                                    mirrors.resume_paused_mirror),
                'subcommand_options': [
                    MIRROR_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resumes a paused mirror job'
            }
        ]
    },
    {
        'command_name': 'nas-authentication',
        'help': 'Commands related to NFS and SMB authentication',
        'subcommands': [
            {
                'subcommand_info': ('change-user-smb-password',
                                    nas_authentication.
                                    change_nas_user_smb_password),
                'subcommand_options': [
                    NAS_USERNAME_OPTION,
                    {
                        'option_positional': ['--smb-password'],
                        'option_keywords': {
                            'dest': 'param_smb_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The new SMB password to set'
                        }
                    },
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the SMB password for the '
                                   'provided NAS username'
            },
            {
                'subcommand_info': ('create-group',
                                    nas_authentication.create_nas_group),
                'subcommand_options': [
                    NAS_GROUPNAME_OPTION,
                    {
                        'option_positional': ['--nfs-gid'],
                        'option_keywords': {
                            'dest': 'param_nfs_gid',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'When using NFS, this is the '
                                    'groupname\'s uid as returned by "id -g '
                                    '<username>" on the client system'
                        }
                    },
                    {
                        'option_positional': ['--smb'],
                        'option_keywords': {
                            'dest': 'param_smb',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'When using SMB, if set to YES, this '
                                    'group will be usable by SMB/CIFS '
                                    'clients.  If set to NO, this group '
                                    'won\'t be usable by SMB/CIFS clients.  '
                                    'Default is set to NO'
                        }
                    }
                ],
                'subcommand_return_key': 'nas_group_name',
                'subcommand_help': 'Creates a new NAS group on the VPSA'
            },
            {
                'subcommand_info': ('create-user',
                                    nas_authentication.create_nas_user),
                'subcommand_options': [
                    NAS_USERNAME_OPTION,
                    {
                        'option_positional': ['--nfs-uid'],
                        'option_keywords': {
                            'dest': 'param_nfs_uid',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'When using NFS, this is the username\'s '
                                    'uid as returned by "id <username>" on '
                                    'the client system'
                        }
                    },
                    {
                        'option_positional': ['--smb-password'],
                        'option_keywords': {
                            'dest': 'param_smb_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'When using SMB, the password to assign '
                                    'to the SMB user.  This is only '
                                    'necessary when not using guest access '
                                    'on the volume and when not integrated '
                                    'with an Active Directory server.'
                        }
                    },
                    {
                        'option_positional': ['--smb-groupname'],
                        'option_keywords': {
                            'dest': 'param_smb_groupname',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'When using SMB, the primary group for '
                                    'the user can optionally be designated '
                                    'with the NAS group designated here.'
                        }
                    }
                ],
                'subcommand_return_key': 'nas_user_name',
                'subcommand_help': 'Creates a new NAS user on the VPSA'
            },
            {
                'subcommand_info': ('delete-group',
                                    nas_authentication.delete_nas_group),
                'subcommand_options': [
                    NAS_GROUPNAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a NAS group'
            },
            {
                'subcommand_info': ('delete-user',
                                    nas_authentication.delete_nas_user),
                'subcommand_options': [
                    NAS_USERNAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a NAS user'
            },
            {
                'subcommand_info': ('get-active-directory',
                                    nas_authentication.get_active_directory),
                'subcommand_options': [],
                'subcommand_return_key': 'smb_ads',
                'subcommand_help': 'Displays details for the currently '
                                   'configured Active Directory on the VPSA'
            },
            {
                'subcommand_info': ('get-group',
                                    nas_authentication.get_nas_group),
                'subcommand_options': [
                    NAS_GROUPNAME_OPTION
                ],
                'subcommand_return_key': 'group',
                'subcommand_help': 'Displays details for a single NAS group '
                                   'on the VPSA'
            },
            {
                'subcommand_info': ('get-user',
                                    nas_authentication.get_nas_user),
                'subcommand_options': [
                    NAS_USERNAME_OPTION
                ],
                'subcommand_return_key': 'user',
                'subcommand_help': 'Displays details for a single NAS user '
                                   'on the VPSA'
            },
            {
                'subcommand_info': ('join-active-directory',
                                    nas_authentication.join_active_directory),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    ACTIVE_DIRECTORY_USERNAME_OPTION,
                    ACTIVE_DIRECTORY_PASSWORD_OPTION,
                    {
                        'option_positional': ['--dns-domain'],
                        'option_keywords': {
                            'dest': 'param_dns_domain',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The DNS domain name for the Active '
                                    'Directory domain to be joined.  For '
                                    'example: "ad.mycompany.com"'
                        }
                    },
                    {
                        'option_positional': ['--netbios-name'],
                        'option_keywords': {
                            'dest': 'param_netbios_name',
                            'metavar': '<xxx>',
                            'type': str.upper,
                            'required': True,
                            'help': 'The NetBIOS name for the Active '
                                    'Directory domain.  For example: '
                                    '"MYCOMPANY"'
                        }
                    },
                    ACTIVE_DIRECTORY_DNS_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Joins a VPSA to an Active Directory - '
                                   'which enables user and group integration '
                                   'for SMB shares'
            },
            {
                'subcommand_info': ('leave-active-directory',
                                    nas_authentication.
                                    leave_active_directory),
                'subcommand_options': [
                    ACTIVE_DIRECTORY_USERNAME_OPTION,
                    ACTIVE_DIRECTORY_PASSWORD_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Makes the VPSA leave the configured '
                                   'Active Directory'
            },
            {
                'subcommand_info': ('list-groups',
                                    nas_authentication.get_all_nas_groups),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'groups',
                'subcommand_help': 'Displays details for all NAS groups on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('list-users',
                                    nas_authentication.get_all_nas_users),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'users',
                'subcommand_help': 'Displays details for all NAS users on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('update-active-directory-dns',
                                    nas_authentication.
                                    update_active_directory_dns),
                'subcommand_options': [
                    ACTIVE_DIRECTORY_DNS_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Change the DNS servers for the Active '
                                   'Directory domain'
            },
        ]
    },
    {
        'command_name': 'pools',
        'help': 'Commands related to storage pools',
        'subcommands': [
            {
                'subcommand_info': ('cache', pools.set_pool_cache),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    POOL_CACHE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Toggles the SSD caching for a pool'
            },
            {
                'subcommand_info': ('capacity-alerts',
                                    pools.update_pool_capacity_alerts),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    {
                        'option_positional': ['--capacityhistory'],
                        'option_keywords': {
                            'dest': 'param_capacityhistory',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'The number of minutes used to calculate '
                                    'pool exhaustion.'
                        }
                    },
                    {
                        'option_positional': ['--alertmode'],
                        'option_keywords': {
                            'dest': 'param_alertmode',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'The number of minutes before the '
                                    'storage pool is predicted to reach '
                                    'space exhaustion'
                        }
                    },
                    {
                        'option_positional': ['--protectedmode'],
                        'option_keywords': {
                            'dest': 'param_protectedmode',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'The number of minutes until pool space '
                                    'exhaustion before protected mode is '
                                    'enabled'
                        }
                    },
                    {
                        'option_positional': ['--emergencymode'],
                        'option_keywords': {
                            'dest': 'param_emergencymode',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'Start deleting old snapshots when '
                                    'number of GB free is under this value'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Change capacity alert settings'
            },
            {
                'subcommand_info': ('cowcache', pools.set_pool_cowcache),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    POOL_COW_CACHE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Toggles the CoW caching for a pool'
            },
            {
                'subcommand_info': ('create', pools.create_pool),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    POOL_RAID_GROUPS_OPTION,
                    CAPACITY_OPTION,
                    {
                        'option_positional': ['--pooltype'],
                        'option_keywords': {
                            'dest': 'param_pooltype',
                            'choices': ['Archival', 'Repository',
                                        'Transactional'],
                            'default': 'Repository',
                            'type': str,
                            'required': True,
                            'help': 'The storage pool type to create.  '
                                    'Default: Repository'
                        }
                    },
                    POOL_CACHE_OPTION,
                    {
                        'option_positional': ['--mode'],
                        'option_keywords': {
                            'dest': 'param_mode',
                            'choices': ['simple', 'stripe'],
                            'type': str.lower,
                            'default': 'stripe',
                            'help': 'The storage pool striping mode to use.  '
                                    'Default: stripe'
                        }
                    }
                ],
                'subcommand_return_key': 'pool_name',
                'subcommand_help': 'Creates a new storage pool'
            },
            {
                'subcommand_info': ('delete', pools.delete_pool),
                'subcommand_options': [
                    POOL_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a storage pool'
            },
            {
                'subcommand_info': ('expand', pools.add_raid_groups_to_pool),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    POOL_RAID_GROUPS_OPTION,
                    CAPACITY_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Expands a storage pool with the provided '
                                   'RAID groups'
            },
            {
                'subcommand_info': ('get', pools.get_pool),
                'subcommand_options': [
                    POOL_ID_OPTION
                ],
                'subcommand_return_key': 'pool',
                'subcommand_help': 'Displays details for a single storage '
                                   'pool on the VPSA'
            },
            {
                'subcommand_info': ('list', pools.get_all_pools),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'pools',
                'subcommand_help': 'Displays details for all storage pools '
                                   'on the VPSA'
            },
            {
                'subcommand_info': ('list-raid-groups',
                                    pools.get_raid_groups_in_pool),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'raid_groups',
                'subcommand_help': 'Displays all RAID groups in the storage '
                                   'pool'
            },
            {
                'subcommand_info': ('list-volumes',
                                    pools.get_volumes_in_pool),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'volumes',
                'subcommand_help': 'Displays all volumes in the storage pool'
            },
            {
                'subcommand_info': ('list-volumes-mirror',
                                    pools.
                                    get_pool_mirror_destination_volumes),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'volumes',
                'subcommand_help': 'Displays all mirror destination volumes '
                                   'in the storage pool'
            },
            {
                'subcommand_info': ('list-volumes-recycle-bin',
                                    pools.get_volumes_in_pool_recycle_bin),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'volumes',
                'subcommand_help': 'Displays all volumes currently in the '
                                   'pool\'s recycle bin'
            },
            {
                'subcommand_info': ('performance',
                                    pools.get_pool_performance),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a '
                                   'storage pool'
            },
            {
                'subcommand_info': ('rename', pools.rename_pool),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the display name for a storage '
                                   'pool'
            }
        ],
    },
    {
        'command_name': 'raid-groups',
        'help': 'Commands related to RAID groups',
        'subcommands': [
            {
                'subcommand_info': ('create', raid_groups.create_raid_group),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--disks'],
                        'option_keywords': {
                            'dest': 'param_disk',
                            'metavar': '<volume-xxxxxxxx,volume-yyyyyyyy>',
                            'type': str,
                            'required': True,
                            'help': 'A comma separated list of drive IDs '
                                    'to use for the RAID group with no '
                                    'spaces.  e.g.: '
                                    '"volume-00000001,volume-00000002".  '
                                    'Required.'
                        }
                    },
                    {
                        'option_positional': ['--protection'],
                        'option_keywords': {
                            'dest': 'param_protection',
                            'choices': ['RAID1', 'RAID5', 'RAID6'],
                            'type': str.upper,
                            'required': True,
                            'help': 'The RAID type to use.  Required.'
                        }
                    },
                    {
                        'option_positional': ['--spare'],
                        'option_keywords': {
                            'dest': 'param_hot_spare',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'Assign a hot spare to the RAID group.  '
                                    'Default: NO'
                        }
                    },
                    {
                        'option_positional': ['--stripe-size'],
                        'option_keywords': {
                            'dest': 'param_stripe_size',
                            'choices': [4, 16, 32, 64, 128, 256],
                            'type': int,
                            'default': 64,
                            'help': 'The stripe size to use - RAID5 and '
                                    'RAID6 only.  Default: 64'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': 'raidgroup_name',
                'subcommand_help': 'Creates a new RAID group from provided '
                                   'drives'
            },
            {
                'subcommand_info': ('delete', raid_groups.delete_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes an unused RAID group from the '
                                   'VPSA'
            },
            {
                'subcommand_info': ('get', raid_groups.get_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION
                ],
                'subcommand_return_key': 'raid_group',
                'subcommand_help': 'Displays details for a single RAID group '
                                   'on the VPSA'
            },
            {
                'subcommand_info': ('hot-spare-add',
                                    raid_groups.add_hot_spare_to_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                    {
                        'option_positional': ['--disk'],
                        'option_keywords': {
                            'dest': 'param_drive_id',
                            'metavar': '<volume-xxxxxxxx>',
                            'type': str,
                            'required': True,
                            'help': 'The drive "name" value as returned by '
                                    '"drives list".  For example: '
                                    '"volume-00002a73".  Required.'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Adds a hot spare to a RAID group using '
                                   'an available drive'
            },
            {
                'subcommand_info': ('hot-spare-remove',
                                    raid_groups.
                                    remove_hot_spare_from_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Removes the hot spare from a RAID group'
            },
            {
                'subcommand_info': ('list', raid_groups.get_all_raid_groups),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'raid_groups',
                'subcommand_help': 'Displays details for all RAID groups on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('list-disks',
                                    raid_groups.get_drives_in_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'disks',
                'subcommand_help': 'Displays all disks used in the provided '
                                   'RAID group'
            },
            {
                'subcommand_info': ('list-free',
                                    raid_groups.get_free_raid_groups),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'raid_groups',
                'subcommand_help': 'Displays details for all RAID groups '
                                   'available for use on the VPSA (not '
                                   'currently in a storage pool)'
            },
            {
                'subcommand_info': ('media-scan-pause',
                                    raid_groups.pause_raid_group_media_scan),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Pauses a media scan for a RAID5 or RAID6 '
                                   'RAID group'
            },
            {
                'subcommand_info': ('media-scan-start',
                                    raid_groups.start_raid_group_media_scan),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Starts a media scan for a RAID5 or RAID6 '
                                   'RAID group'
            },
            {
                'subcommand_info': ('performance',
                                    raid_groups.get_raid_group_performance),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a RAID '
                                   'group'
            },
            {
                'subcommand_info': ('rename', raid_groups.rename_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the display name for a RAID '
                                   'group'
            },
            {
                'subcommand_info': ('repair', raid_groups.repair_raid_group),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Repairs a RAID group with an available '
                                   'drive'
            },
            {
                'subcommand_info': ('resync-speed',
                                    raid_groups.
                                    update_raid_group_resync_speed),
                'subcommand_options': [
                    RAID_GROUP_ID_OPTION,
                    {
                        'option_positional': ['--minimum'],
                        'option_keywords': {
                            'dest': 'param_minimum',
                            'metavar': 'n',
                            'type': int,
                            'help': 'The minimum MB/s to resync at'
                        }
                    },
                    {
                        'option_positional': ['--maximum'],
                        'option_keywords': {
                            'dest': 'param_maximum',
                            'metavar': 'n',
                            'type': int,
                            'help': 'The maximum MB/s to resync at'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Updates the speed at which a degraded '
                                   'RAID group will resync'
            }
        ]
    },
    {
        'command_name': 'remote-object-storage',
        'help': 'Commands related to remote object storage (B2S3) backups',
        'subcommands': [
            {
                'subcommand_info': ('backup-job-performance',
                                    remote_object_storage.
                                    get_ros_backup_job_performance),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a remote '
                                   'object storage backup job'
            },
            {
                'subcommand_info': ('break-backup-job',
                                    remote_object_storage.
                                    break_ros_backup_job),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION,
                    DELETE_SNAPSHOTS_OPTION,
                    {
                        'option_positional': ['--purge-data'],
                        'option_keywords': {
                            'dest': 'param_purge_data',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to "YES", all data related to '
                                    'this backup job will be deleted on the '
                                    'remote object storage destination '
                                    'endpoint.  If "NO", the data will '
                                    'remain on the endpoint.  Set to "NO" '
                                    'by default.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Breaks a remote object storage backup '
                                   'job - this action is irreversible'
            },
            {
                'subcommand_info': ('break-restore-job',
                                    remote_object_storage.
                                    break_ros_restore_job),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Breaks a remote object storage restore '
                                   'job - this action is irreversible'
            },
            {
                'subcommand_info': ('change-backup-job-compression',
                                    remote_object_storage.
                                    update_ros_backup_job_compression),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION,
                    COMPRESSION_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the compression setting for a '
                                   'remote object storage backup job'
            },
            {
                'subcommand_info': ('change-restore-job-mode',
                                    remote_object_storage.
                                    change_ros_restore_job_mode),
                'subcommand_options': [
                    ROS_RESTORE_JOB_ID_OPTION,
                    ROS_RESTORE_MODE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the restore mode for a remote '
                                   'object storage restore job'
            },
            {
                'subcommand_info': ('create-backup-job',
                                    remote_object_storage.
                                    create_ros_backup_job),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    ROS_DESTINATION_ID_OPTION,
                    VOLUME_ID_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION,
                    COMPRESSION_OPTION,
                    SSE_OPTION
                ],
                'subcommand_return_key': 'obs_backup_job_name',
                'subcommand_help': 'Create a new remote object storage '
                                   'backup job based on the provided volume '
                                   'and snapshot policy'
            },
            {
                'subcommand_info': ('create-destination',
                                    remote_object_storage.
                                    create_ros_destination),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--bucket'],
                        'option_keywords': {
                            'dest': 'param_bucket',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The destination object storage bucket '
                                    'name'
                        }
                    },
                    {
                        'option_positional': ['--endpoint'],
                        'option_keywords': {
                            'dest': 'param_endpoint',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The destination object storage '
                                    'hostname.  For example, '
                                    's3.amazonaws.com'
                        }
                    },
                    {
                        'option_positional': ['--username'],
                        'option_keywords': {
                            'dest': 'param_username',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The username/access key of the object '
                                    'storage bucket'
                        }
                    },
                    {
                        'option_positional': ['--password'],
                        'option_keywords': {
                            'dest': 'param_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The password/secret key of the object '
                                    'storage bucket'
                        }
                    },
                    {
                        'option_positional': ['--public'],
                        'option_keywords': {
                            'dest': 'param_public',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to YES, the remote object '
                                    'storage destination will be accessed '
                                    'through the VPSA\'s public IP address, '
                                    'if assigned.  If NO, the private '
                                    'data/management IP will be used (remote '
                                    'object storage must be routable or '
                                    'reachable via proxy). Defaults to NO.'
                        }
                    },
                    {
                        'option_positional': ['--use-proxy'],
                        'option_keywords': {
                            'dest': 'param_use_proxy',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to YES, the remote object '
                                    'storage destination will be accessed '
                                    'through the specified HTTP proxy '
                                    'server.  If NO, a direct routed '
                                    'connection will be used (remote '
                                    'object storage endpoint must be '
                                    'routable from source IP). Defaults to '
                                    'NO.'
                        }
                    },
                    {
                        'option_positional': ['--proxy-host'],
                        'option_keywords': {
                            'dest': 'param_proxy_host',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'If --use-proxy is set to YES, the HTTP '
                                    'proxy hostname or IP to connect to the '
                                    'endpoint through'
                        }
                    },
                    {
                        'option_positional': ['--proxy-port'],
                        'option_keywords': {
                            'dest': 'param_proxy_host',
                            'metavar': '<n>',
                            'type': int,
                            'help': 'If --use-proxy is set to YES, the HTTP '
                                    'proxy port number to connect to the '
                                    'endpoint through'
                        }
                    },
                    {
                        'option_positional': ['--proxy-username'],
                        'option_keywords': {
                            'dest': 'param_proxy_username',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'If --use-proxy is set to YES, the HTTP '
                                    'proxy username to connect to the '
                                    'endpoint through - do not define to not '
                                    'use authentication'
                        }
                    },
                    {
                        'option_positional': ['--proxy-password'],
                        'option_keywords': {
                            'dest': 'param_proxy_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'If --use-proxy is set to YES, the HTTP '
                                    'proxy password to connect to the '
                                    'endpoint through - do not define to not '
                                    'use authentication'
                        }
                    },
                ],
                'subcommand_return_key': 'obs_destination',
                'subcommand_help': 'Create a new remote object storage '
                                   'destination where backups may be stored'
            },
            {
                'subcommand_info': ('create-restore-job',
                                    remote_object_storage.
                                    create_ros_restore_job),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    ROS_DESTINATION_ID_OPTION,
                    POOL_ID_OPTION,
                    ROS_RESTORE_MODE_OPTION,
                    {
                        'option_positional': ['--volume-name'],
                        'option_keywords': {
                            'dest': 'param_volume_name',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The display name to set for the '
                                    'restored volume.  Required.'
                        }
                    },
                    {
                        'option_positional': ['--local-snapshot-id'],
                        'option_keywords': {
                            'dest': 'param_local_snapshot_id',
                            'metavar': '<snap-xxxxxxxx>',
                            'type': str,
                            'help': 'Either --local-snapshot-id or '
                                    '--object-store-key must be passed.  '
                                    'When --local-snapshot-id is used, the '
                                    'restore job is initiated based on the '
                                    'original internal snapshot ID'
                        }
                    },
                    {
                        'option_positional': ['--object-store-key'],
                        'option_keywords': {
                            'dest': 'param_object_store_key',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'Either --local-snapshot-id or '
                                    '--object-store-key must be passed.  '
                                    'When --object-store-key is used, it is '
                                    'the full object storage key for the '
                                    '"path" to the individual snapshot to be '
                                    'restored.  For example: '
                                    '"cloud1.'
                                    'C97E9A00ADE7489BB08A9AB3B0B6484F/'
                                    'myvpsa.vsa-00000169/'
                                    'myvol.volume-00000011/'
                                    '2015-07-01T09:26:01+'
                                    '0000_snap-0000003e/".  This is useful '
                                    'when there is no local_snapshot_id to '
                                    'reference; for example, if the snapshot '
                                    'is being restored to a different VPSA '
                                    'than the original source.'
                        }
                    },
                    CRYPT_OPTION
                ],
                'subcommand_return_key': 'obs_restore_job_name',
                'subcommand_help': 'Create a new remote object storage '
                                   'restore job to the provided pool based '
                                   'on the provided volume and snapshot policy'
            },
            {
                'subcommand_info': ('get-backup-job',
                                    remote_object_storage.
                                    get_ros_backup_job),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION
                ],
                'subcommand_return_key': 'obs_backup_job',
                'subcommand_help': 'Displays details for a single remote '
                                   'object storage backup job'
            },
            {
                'subcommand_info': ('get-destination',
                                    remote_object_storage.
                                    get_ros_destination),
                'subcommand_options': [
                    ROS_DESTINATION_ID_OPTION
                ],
                'subcommand_return_key': 'obs_destination',
                'subcommand_help': 'Displays details for a single remote '
                                   'object storage destination'
            },
            {
                'subcommand_info': ('get-restore-job',
                                    remote_object_storage.
                                    get_ros_restore_job),
                'subcommand_options': [
                    ROS_RESTORE_JOB_ID_OPTION
                ],
                'subcommand_return_key': 'obs_backup_job',
                'subcommand_help': 'Displays details for a single remote '
                                   'object storage restore job'
            },
            {
                'subcommand_info': ('list-backup-jobs',
                                    remote_object_storage.
                                    get_all_ros_backup_jobs),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'obs_backup_jobs',
                'subcommand_help': 'Displays details for all remote object '
                                   'storage backup jobs'
            },
            {
                'subcommand_info': ('list-destination-backup-jobs',
                                    remote_object_storage.
                                    get_all_ros_destination_backup_jobs),
                'subcommand_options': [
                    ROS_DESTINATION_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'obs_backup_jobs',
                'subcommand_help': 'Displays details for all remote object '
                                   'storage backup jobs by destination'
            },
            {
                'subcommand_info': ('list-destinations',
                                    remote_object_storage.
                                    get_all_ros_destinations),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'obs_destinations',
                'subcommand_help': 'Displays details for all remote object '
                                   'storage destinations'
            },
            {
                'subcommand_info': ('list-restore-jobs',
                                    remote_object_storage.
                                    get_all_ros_restore_jobs),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'obs_restore_jobs',
                'subcommand_help': 'Displays details for all remote object '
                                   'storage restore jobs'
            },
            {
                'subcommand_info': ('list-destination-restore-jobs',
                                    remote_object_storage.
                                    get_all_ros_destination_restore_jobs),
                'subcommand_options': [
                    ROS_DESTINATION_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'obs_restore_jobs',
                'subcommand_help': 'Displays details for all remote object '
                                   'storage restore jobs by destination'
            },
            {
                'subcommand_info': ('pause-backup-job',
                                    remote_object_storage.
                                    pause_ros_backup_job),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Pauses a remote object storage backup '
                                   'job'
            },
            {
                'subcommand_info': ('pause-restore-job',
                                    remote_object_storage.
                                    pause_ros_restore_job),
                'subcommand_options': [
                    ROS_RESTORE_JOB_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Pauses a remote object storage restore '
                                   'job'
            },
            {
                'subcommand_info': ('remove-destination',
                                    remote_object_storage.
                                    remove_ros_destination),
                'subcommand_options': [
                    ROS_DESTINATION_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Removes a remote object storage '
                                   'destination'
            },
            {
                'subcommand_info': ('replace-backup-job-snapshot-policy',
                                    remote_object_storage.
                                    replace_ros_backup_job_snapshot_policy),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Replaces the remote object storage '
                                   'backup job snapshot policy with the '
                                   'specified policy'
            },
            {
                'subcommand_info': ('restore-job-performance',
                                    remote_object_storage.
                                    get_ros_restore_job_performance),
                'subcommand_options': [
                    ROS_RESTORE_JOB_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a remote '
                                   'object storage restore job'
            },
            {
                'subcommand_info': ('resume-backup-job',
                                    remote_object_storage.
                                    resume_ros_backup_job),
                'subcommand_options': [
                    ROS_BACKUP_JOB_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resumes a paused remote object storage '
                                   'backup job'
            },
            {
                'subcommand_info': ('resume-restore-job',
                                    remote_object_storage.
                                    resume_ros_restore_job),
                'subcommand_options': [
                    ROS_RESTORE_JOB_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resumes a paused remote object storage '
                                   'restore job'
            }
        ]
    },
    {
        'command_name': 'servers',
        'help': 'Commands related to servers',
        'subcommands': [
            {
                'subcommand_info': ('attach-volume',
                                    servers.attach_servers_to_volume),
                'subcommand_options': [
                    SERVER_ID_LIST_OPTION,
                    VOLUME_ID_OPTION,
                    {
                        'option_positional': ['--access-type'],
                        'option_keywords': {
                            'dest': 'param_access_type',
                            'choices': ['NFS', 'SMB', 'BOTH'],
                            'type': str.upper,
                            'help': 'For NAS shares, the protocol to grant '
                                    'access with.'
                        }
                    },
                    {
                        'option_positional': ['--readonly'],
                        'option_keywords': {
                            'dest': 'param_readonly',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to "YES", the attached servers '
                                    'will only be able to read the provided '
                                    'volume.  Default: "NO"'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Attaches one or more server records to a '
                                   'volume.'
            },
            {
                'subcommand_info': ('create', servers.create_server),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--ip-address'],
                        'option_keywords': {
                            'dest': 'param_ip_address',
                            'metavar': '<xxx.xxx.xxx.xxx/yy>',
                            'type': str,
                            'help': 'The source IP or CIDR of the server.  '
                                    'Required for NAS share access, optional '
                                    'for iSCSI.'
                        }
                    },
                    {
                        'option_positional': ['--iqn'],
                        'option_keywords': {
                            'dest': 'param_iqn',
                            'metavar': '<iqn.xxx:xx:xxx>',
                            'type': str,
                            'help': 'The server\'s iSCSI IQN.  Required for '
                                    'iSCSI access, optional for NAS shares.'
                        }
                    },
                    {
                        'option_positional': ['--vpsa-chap-user'],
                        'option_keywords': {
                            'dest': 'param_vpsa_chap_user',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The VPSA\'s iSCSI CHAP username.  If '
                                    'not supplied, a random value will be '
                                    'generated.'
                        }
                    },
                    {
                        'option_positional': ['--vpsa-chap-secret'],
                        'option_keywords': {
                            'dest': 'param_vpsa_chap_secret',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The VPSA\'s iSCSI CHAP secret.  If not '
                                    'supplied, a random value will be '
                                    'generated.'
                        }
                    },
                    {
                        'option_positional': ['--host-chap-user'],
                        'option_keywords': {
                            'dest': 'param_host_chap_user',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The server\'s iSCSI CHAP username for '
                                    'mutual authentication.  If not '
                                    'supplied, mutual CHAP authentication '
                                    'will not be used.'
                        }
                    },
                    {
                        'option_positional': ['--host-chap-secret'],
                        'option_keywords': {
                            'dest': 'param_host_chap_secret',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The server\'s iSCSI CHAP secret for '
                                    'mutual authentication.  If not '
                                    'supplied, mutual CHAP authentication '
                                    'will not be used.'
                        }
                    },
                    {
                        'option_positional': ['--ipsec-iscsi'],
                        'option_keywords': {
                            'dest': 'param_ipsec_iscsi',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to "YES", mandate IPSec for '
                                    'iSCSI connections from this server.  '
                                    'Default: NO'
                        }
                    },
                    {
                        'option_positional': ['--ipsec-nfs'],
                        'option_keywords': {
                            'dest': 'param_ipsec_nfs',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to "YES", mandate IPSec for '
                                    'NFS connections from this server.  '
                                    'Default: "NO"'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': 'server_name',
                'subcommand_help': 'Creates a new server record'
            },
            {
                'subcommand_info': ('delete', servers.delete_server),
                'subcommand_options': [
                    SERVER_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a server record not currently '
                                   'attached to any volume.'
            },
            {
                'subcommand_info': ('get', servers.get_server),
                'subcommand_options': [
                    SERVER_ID_OPTION
                ],
                'subcommand_return_key': 'server',
                'subcommand_help': 'Displays details for a single server '
                                   'record.'
            },
            {
                'subcommand_info': ('list', servers.get_all_servers),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'servers',
                'subcommand_help': 'Displays details for all server records.'
            },
            {
                'subcommand_info': ('list-attached-volumes',
                                    servers.get_volumes_attached_to_server),
                'subcommand_options': [
                    SERVER_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'volumes',
                'subcommand_help': 'Displays all volumes attached to the '
                                   'specified server record.'
            },
            {
                'subcommand_info': ('performance',
                                    servers.get_server_performance),
                'subcommand_options': [
                    SERVER_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a server '
                                   'record.'
            },
            {
                'subcommand_info': ('rename', servers.rename_server),
                'subcommand_options': [
                    SERVER_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes the display name for a server '
                                   'record.'
            }
        ]
    },
    {
        'command_name': 'settings',
        'help': 'Commands related to VPSA settings',
        'subcommands': [
            {
                'subcommand_info': ('create-zcs-image-repository',
                                    settings.create_zcs_image_repository),
                'subcommand_options': [
                    POOL_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Creates a ZCS image repository on the '
                                   'specified pool - this consumes 100GB of '
                                   'space from the pool'
            },
            {
                'subcommand_info': ('delete-zcs-image-repository',
                                    settings.delete_zcs_image_repository),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    {
                        'option_positional': ['--confirm'],
                        'option_keywords': {
                            'dest': 'param_confirm',
                            'action': 'store_true',
                            'required': True,
                            'help': 'ZCS image repository will only be '
                                    'deleted if this flag is passed.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes the ZCS image repository'
            },
            {
                'subcommand_info': ('disable-defrag',
                                    settings.disable_defrag),
                'subcommand_options': [],
                'subcommand_return_key': None,
                'subcommand_help': 'Disables NAS share (XFS) defragging on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('download-metering-database',
                                    settings.download_metering_database),
                'subcommand_options': [],
                'subcommand_return_key': None,
                'subcommand_help': 'Downloads the metering database'
            },
            {
                'subcommand_info': ('enable-defrag',
                                    settings.enable_defrag),
                'subcommand_options': [],
                'subcommand_return_key': None,
                'subcommand_help': 'Enables NAS share (XFS) defragging on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('get-nfs-domain',
                                    settings.get_nfs_domain),
                'subcommand_options': [],
                'subcommand_return_key': 'nfs_domain',
                'subcommand_help': 'Displays the NFS domain for the VPSA'
            },
            {
                'subcommand_info': ('get-public-ip',
                                    settings.get_public_ip),
                'subcommand_options': [],
                'subcommand_return_key': 'public_ips',
                'subcommand_help': 'Retrieves public IPs associated with the '
                                   'VPSA'
            },
            {
                'subcommand_info': ('get-zcs-settings',
                                    settings.get_zcs_settings),
                'subcommand_options': [],
                'subcommand_return_key': 'container_service_settings',
                'subcommand_help': 'Retrieves details for Zadara Container '
                                   'Services, such as the configured '
                                   'network, ports, etc.'
            },
            {
                'subcommand_info': ('migrate-zcs-image-repository',
                                    settings.migrate_zcs_image_repository),
                'subcommand_options': [
                    POOL_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Migrates the ZCS image repository to the '
                                   'specified pool'
            },
            {
                'subcommand_info': ('set-encryption-password',
                                    settings.set_encryption_password),
                'subcommand_options': [
                    {
                        'option_positional': ['--password'],
                        'option_keywords': {
                            'dest': 'param_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'Sets the password used to encrypt '
                                    'volumes.  CAUTION: THIS PASSWORD IS NOT '
                                    'STORED ON THE VPSA - IT IS THE USER\'S '
                                    'RESPONSIBILITY TO MAINTAIN ACCESS TO '
                                    'THE PASSWORD.  LOSS OF THE PASSWORD MAY '
                                    'RESULT IN UNRECOVERABLE DATA.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Sets the encryption password globally on '
                                   'the VPSA.  This password is used when '
                                   'enabling the encryption option for a '
                                   'volume.'
            },
            {
                'subcommand_info': ('set-multizone-read-mode',
                                    settings.set_multizone_read_mode),
                'subcommand_options': [
                    {
                        'option_positional': ['--read-mode'],
                        'option_keywords': {
                            'dest': 'param_read_mode',
                            'choices': ['roundrobin', 'localcopy'],
                            'type': str.lower,
                            'required': True,
                            'help': 'For multizone environments, if set to '
                                    '"roundrobin", data will be read from '
                                    'storage nodes in all protection zones.  '
                                    'If set to "localcopy", data from the '
                                    'local protection zone will be favored.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Modifies where data is read from in '
                                   'multizone environments'
            },
            {
                'subcommand_info': ('set-nfs-domain',
                                    settings.set_nfs_domain),
                'subcommand_options': [
                    {
                        'option_positional': ['--domain'],
                        'option_keywords': {
                            'dest': 'param_create_policy',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'Sets the NFS domain to the provided '
                                    'value'
                        }
                    }
                ],
                'subcommand_return_key': 'nfs_domain',
                'subcommand_help': 'Displays the NFS domain for the VPSA'
            },
            {
                'subcommand_info': ('set-recycle-bin',
                                    settings.set_recycle_bin),
                'subcommand_options': [
                    {
                        'option_positional': ['--recycle-bin'],
                        'option_keywords': {
                            'dest': 'param_recycle_bin',
                            'choices': ['YES', 'NO'],
                            'required': True,
                            'help': 'If set to YES, deleted volumes are '
                                    'moved to the recycle bin, where they '
                                    'may be restored in case of accidental '
                                    'deletion (volumes are permanently '
                                    'deleted from the recycle bin after '
                                    'seven days).  If set to NO, deleted '
                                    'volumes are immediately deleted.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Turns the recycle bin on or off globally '
                                   'for all pools.'
            },
            {
                'subcommand_info': ('set-smb-charset',
                                    settings.set_smb_charset),
                'subcommand_options': [
                    {
                        'option_positional': ['--charset'],
                        'option_keywords': {
                            'dest': 'param_charset',
                            'choices': ['UTF-8', 'ISO-8859-1'],
                            'type': str.upper,
                            'required': True,
                            'help': 'Sets the SMB character set to either '
                                    'UTF-8 or ISO-8859-1 depending on the '
                                    'passed value'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Sets the character set used by the '
                                   'SMB/CIFS server for all SMB/CIFS shared '
                                   'volumes'
            },
            {
                'subcommand_info': ('set-smb-trusted-domains',
                                    settings.set_smb_trusted_domains),
                'subcommand_options': [
                    {
                        'option_positional': ['--allow-trusted-domains'],
                        'option_keywords': {
                            'dest': 'param_allow_trusted_domains',
                            'choices': ['YES', 'NO'],
                            'required': True,
                            'help': 'For VPSAs joined to an Active Directory '
                                    'domain, if set to YES, Active Directory '
                                    'trusted domains will be allowed.  If '
                                    'set to NO, Active Directory trusted '
                                    'domains will not be allowed.'
                        }
                    },
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Sets whether or not the SMB/CIFS server '
                                   'should allow Active Directory trusted '
                                   'domains'
            }
        ]
    },
    {
        'command_name': 'snapshot-policies',
        'help': 'Commands related to snapshot policies',
        'subcommands': [
            {
                'subcommand_info': ('create',
                                    snapshot_policies.create_snapshot_policy),
                'subcommand_options': [
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--create-policy'],
                        'option_keywords': {
                            'dest': 'param_create_policy',
                            'metavar': '<x x x x x> -or- "manual"',
                            'type': str,
                            'required': True,
                            'help': 'The frequency to take snapshots.  This '
                                    'is defined in UNIX cron style format.  '
                                    'For example: "0 3 * * *" would take a '
                                    'snapshot at 3 AM every day.  If '
                                    '"manual", an On Demand policy will be '
                                    'created.'
                        }
                    },
                    {
                        'option_positional': ['--local-delete-policy'],
                        'option_keywords': {
                            'dest': 'param_local_delete_policy',
                            'metavar': '<n>',
                            'type': int,
                            'required': True,
                            'help': 'The number of snapshots to retain on '
                                    'the local VPSA before removing.  For '
                                    'example, if 10 is specified, when the '
                                    '11th snapshot is created, the oldest '
                                    'snapshot will be deleted.'
                        }
                    },
                    {
                        'option_positional': ['--remote-delete-policy'],
                        'option_keywords': {
                            'dest': 'param_remote_delete_policy',
                            'metavar': '<n>',
                            'type': int,
                            'required': True,
                            'help': 'The number of snapshots to retain on '
                                    'the remote VPSA before removing.  For '
                                    'example, if 10 is specified, when the '
                                    '11th snapshot is created, the oldest '
                                    'snapshot will be deleted.'
                        }
                    },
                    {
                        'option_positional': ['--allow-empty'],
                        'option_keywords': {
                            'dest': 'param_allow_empty',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to YES, snapshots will be taken '
                                    'even when no data has been changed on '
                                    'the volume (creates empty snapshots).  '
                                    'If set to NO, snapshots will only be '
                                    'created if data has changed.  Set to NO '
                                    'by default.'
                        }
                    }
                ],
                'subcommand_return_key': 'snapshot_policy_name',
                'subcommand_help': 'Creates a new snapshot policy'
            },
            {
                'subcommand_info': ('delete',
                                    snapshot_policies.delete_snapshot_policy),
                'subcommand_options': [
                    SNAPSHOT_POLICY_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a snapshot policy - the policy '
                                   'must not be in use by any volume or '
                                   'mirror'
            },
            {
                'subcommand_info': ('get',
                                    snapshot_policies.get_snapshot_policy),
                'subcommand_options': [
                    SNAPSHOT_POLICY_ID_OPTION
                ],
                'subcommand_return_key': 'snapshot_policy',
                'subcommand_help': 'Displays details for a single snapshot '
                                   'policy'
            },
            {
                'subcommand_info': ('list',
                                    snapshot_policies.
                                    get_all_snapshot_policies),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'snapshot_policies',
                'subcommand_help': 'Displays details for all snapshot '
                                   'policies'
            },
            {
                'subcommand_info': ('rename',
                                    snapshot_policies.rename_snapshot_policy),
                'subcommand_options': [
                    SNAPSHOT_POLICY_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Renames a snapshot policy'
            }
        ],
    },
    {
        'command_name': 'tickets',
        'help': 'Commands related to VPSA support tickets',
        'subcommands': [
            {
                'subcommand_info': ('close', tickets.close_ticket),
                'subcommand_options': [
                    TICKET_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Closes the support ticket with the '
                                   'provided ticket ID'
            },
            {
                'subcommand_info': ('create-comment',
                                    tickets.create_ticket_comment),
                'subcommand_options': [
                    TICKET_ID_OPTION,
                    {
                        'option_positional': ['--comment'],
                        'option_keywords': {
                            'dest': 'param_comment',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The comment to add to the ticket'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Creates a new comment in an existing '
                                   'support ticket by the provided ticket ID'
            },
            {
                'subcommand_info': ('create-ticket', tickets.create_ticket),
                'subcommand_options': [
                    {
                        'option_positional': ['--subject'],
                        'option_keywords': {
                            'dest': 'param_subject',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The subject for the ticket (analogous '
                                    'to an e-mail subject).  For example: '
                                    '"Help With Expanding Pool"'
                        }
                    },
                    {
                        'option_positional': ['--description'],
                        'option_keywords': {
                            'dest': 'param_description',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The full body of the ticket (analogous '
                                    'to an e-mail body).  For example: '
                                    '"I would like more information on best '
                                    'practices for expanding my "pool1" '
                                    'storage pool."'
                        }
                    }
                ],
                'subcommand_return_key': 'ticket_id',
                'subcommand_help': 'Creates a new support ticket for the VPSA'
            },
            {
                'subcommand_info': ('create-zsnap',
                                    tickets.create_ticket_zsnap),
                'subcommand_options': [
                    TICKET_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Creates a diagnostic file called a '
                                   '"zsnap" for support staff to review'
            },
            {
                'subcommand_info': ('get-comments',
                                    tickets.get_ticket_comments),
                'subcommand_options': [
                    TICKET_ID_OPTION
                ],
                'subcommand_return_key': 'comments',
                'subcommand_help': 'Displays details for all comments for a '
                                   'support ticket'
            },
            {
                'subcommand_info': ('list', tickets.get_all_tickets),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'tickets',
                'subcommand_help': 'Displays details for all support tickets '
                                   'created from the VPSA'
            }
        ]
    },
    {
        'command_name': 'volumes',
        'help': 'Commands related to volumes',
        'subcommands': [
            {
                'subcommand_info': ('attach-snapshot-policy',
                                    volumes.add_volume_snapshot_policy),
                'subcommand_options': [
                    CG_ID_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Attaches a snapshot policy to the '
                                   'provided consistency group ID.'
            },
            {
                'subcommand_info': ('clone', volumes.create_clone),
                'subcommand_options': [
                    CG_ID_OPTION,
                    DISPLAY_NAME_OPTION,
                    {
                        'option_positional': ['--snapshot-id'],
                        'option_keywords': {
                            'dest': 'param_snapshot_id',
                            'metavar': '<snap-xxxxxxxx>',
                            'type': str,
                            'help': 'The snapshot "name" value as returned '
                                    'by "volumes list-snapshots".  For '
                                    'example: "snap-00000001".  If no '
                                    'snapshot is specified, the clone will '
                                    'be taken from the current volume '
                                    'contents.  Optional.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Clones a volume with its current data, '
                                   'or based on a snapshot.'
            },
            {
                'subcommand_info': ('create', volumes.create_volume),
                'subcommand_options': [
                    POOL_ID_OPTION,
                    DISPLAY_NAME_OPTION,
                    CAPACITY_OPTION,
                    VOLUME_BLOCK_OPTION,
                    VOLUME_ATTACHPOLICIES_OPTION,
                    CRYPT_OPTION,
                    VOLUME_EXPORT_NAME_OPTION,
                    VOLUME_ATIMEUPDATE_OPTION,
                    VOLUME_NFSROOTSQUASH_OPTION,
                    VOLUME_READAHEADKB_OPTION,
                    VOLUME_SMBONLY_OPTION,
                    VOLUME_SMBGUEST_OPTION,
                    VOLUME_SMBWINDOWSACL_OPTION,
                    VOLUME_SMBFILECREATEMASK_OPTION,
                    VOLUME_SMBDIRCREATEMASK_OPTION,
                    VOLUME_SMBMAPARCHIVE_OPTION,
                    VOLUME_SMBAIOSIZE_OPTION,
                    VOLUME_SMBBROWSEABLE_OPTION
                ],
                'subcommand_return_key': 'vol_name',
                'subcommand_help': 'Creates a new volume on the provided pool'
            },
            {
                'subcommand_info': ('create-snapshot',
                                    volumes.create_volume_snapshot),
                'subcommand_options': [
                    CG_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': 'snapshot_name',
                'subcommand_help': 'Creates a snapshot'
            },
            {
                'subcommand_info': ('delete', volumes.delete_volume),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    FORCE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a volume.  By default, deleted '
                                   'volumes are moved to the pool\'s recycle '
                                   'bin.'
            },
            {
                'subcommand_info': ('delete-snapshot',
                                    volumes.delete_volume_snapshot),
                'subcommand_options': [
                    SNAPSHOT_ID_OPTION,
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a snapshot'
            },
            {
                'subcommand_info': ('detach-servers',
                                    volumes.detach_servers_from_volume),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    SERVER_ID_LIST_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Detaches a list of server records (or '
                                   'one server record without any commas) '
                                   'from a volume.  Please ensure the '
                                   'effected servers are not using the '
                                   'volume.'
            },
            {
                'subcommand_info': ('detach-snapshot-policy',
                                    volumes.remove_volume_snapshot_policy),
                'subcommand_options': [
                    CG_ID_OPTION,
                    SNAPSHOT_POLICY_ID_OPTION,
                    DELETE_SNAPSHOTS_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Detaches a snapshot policy from the '
                                   'provided consistency group ID.'
            },
            {
                'subcommand_info': ('expand', volumes.expand_volume),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    CAPACITY_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Expands a volume'
            },
            {
                'subcommand_info': ('export-name',
                                    volumes.set_volume_export_name),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    VOLUME_EXPORT_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Changes a NAS share\'s export name'
            },
            {
                'subcommand_info': ('get', volumes.get_volume),
                'subcommand_options': [
                    VOLUME_ID_OPTION
                ],
                'subcommand_return_key': 'volume',
                'subcommand_help': 'Displays details for a single volume on '
                                   'the VPSA'
            },
            {
                'subcommand_info': ('list', volumes.get_all_volumes),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION,
                    {
                        'option_positional': ['--showonlyblock'],
                        'option_keywords': {
                            'dest': 'param_showonlyblock',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to "YES", only block volumes '
                                    'will be displayed.  If "NO", it will '
                                    'show any volume.  Default: NO'
                        },
                    },
                    {
                        'option_positional': ['--showonlyfile'],
                        'option_keywords': {
                            'dest': 'param_showonlyfile',
                            'choices': ['YES', 'NO'],
                            'type': str.upper,
                            'default': 'NO',
                            'help': 'If set to "YES", only NAS volumes will '
                                    'be displayed.  If "NO", it will show '
                                    'any volume.  Default: NO'
                        },
                    },
                    {
                        'option_positional': ['--display-name'],
                        'option_keywords': {
                            'dest': 'param_display_name',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The text label assigned to the volume '
                                    'to search for; e.g. "user-files".  If '
                                    'not specified, it will show any '
                                    'volume.  Optional.'
                        },
                    },
                ],
                'subcommand_return_key': 'volumes',
                'subcommand_help': 'Displays details for all volumes on the '
                                   'VPSA'
            },
            {
                'subcommand_info': ('list-free', volumes.get_free_volumes),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'volumes',
                'subcommand_help': 'Displays details for all volumes not '
                                   'currently attached to any servers'
            },
            {
                'subcommand_info': ('list-servers',
                                    volumes.get_servers_attached_to_volume),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'servers',
                'subcommand_help': 'Displays all servers attached to the '
                                   'provided volume'
            },
            {
                'subcommand_info': ('list-snapshot-policies',
                                    volumes.
                                    get_volume_attached_snapshot_policies),
                'subcommand_options': [
                    CG_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'snapshot_policies',
                'subcommand_help': 'Displays all snapshot policies attached '
                                   'to the provided volume'
            },
            {
                'subcommand_info': ('list-snapshots',
                                    volumes.get_all_snapshots),
                'subcommand_options': [
                    CG_ID_OPTION,
                    ROS_BACKUP_JOB_ID_OPTION,
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'snapshots',
                'subcommand_help': 'Displays all snapshots taken by the '
                                   'provided consistency group ID.  If a '
                                   'remote object storage backup job is '
                                   'specified, then only its snapshots will '
                                   'be displayed.'
            },
            {
                'subcommand_info': ('performance',
                                    volumes.get_volume_performance),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    INTERVAL_OPTION
                ],
                'subcommand_return_key': 'usages',
                'subcommand_help': 'Gets performance statistics for a volume.'
            },
            {
                'subcommand_info': ('rename', volumes.rename_volume),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    DISPLAY_NAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Renames a volume'
            },
            {
                'subcommand_info': ('update-comment',
                                    volumes.update_volume_comment),
                'subcommand_options': [
                    VOLUME_ID_OPTION,
                    {
                        'option_positional': ['--comment'],
                        'option_keywords': {
                            'dest': 'param_comment',
                            'metavar': '<xxx>',
                            'type': str,
                            'help': 'The new comment to set.  Required.'
                        },
                    },
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Updates the comment field for a volume.'
            },
        ]
    },
    {
        'command_name': 'vpsa-operations',
        'help': 'Commands related to creating, editing, and deleting VPSAs',
        'subcommands': [
            {
                'subcommand_info': ('delete-vpsa', vpsa.delete_vpsa),
                'subcommand_options': [
                    VPSA_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a VPSA.  This is a moderated '
                                   'action and must be approved by an '
                                   'administrator.'
            },
            {
                'subcommand_info': ('get-cloud', cloud.get_cloud),
                'subcommand_options': [
                    CLOUD_ID_OPTION
                ],
                'subcommand_return_key': 'provider',
                'subcommand_help': 'Displays details for a single Zadara '
                                   'storage cloud'
            },
            {
                'subcommand_info': ('get-vpsa', vpsa.get_vpsa),
                'subcommand_options': [
                    VPSA_ID_OPTION
                ],
                'subcommand_return_key': 'vpsa',
                'subcommand_help': 'Displays details for a single VPSA'
            },
            {
                'subcommand_info': ('list-clouds',
                                    cloud.get_all_clouds),
                'subcommand_options': [],
                'subcommand_return_key': 'providers',
                'subcommand_help': 'Displays details for all available '
                                   'Zadara storage clouds'
            },
            {
                'subcommand_info': ('list-vpsas',
                                    vpsa.get_all_vpsas),
                'subcommand_options': [],
                'subcommand_return_key': 'vpsas',
                'subcommand_help': 'Displays details for all VPSAs'
            }
        ]
    },
    {
        'command_name': 'vpsa-users',
        'help': 'Commands related to VPSA GUI and API users',
        'subcommands': [
            {
                'subcommand_info': ('change-password-by-code',
                                    vpsa_users.
                                    change_vpsa_user_password_by_code),
                'subcommand_options': [
                    VPSA_USERNAME_OPTION,
                    {
                        'option_positional': ['--code'],
                        'option_keywords': {
                            'dest': 'param_code',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The reset password code as e-mailed to '
                                    'the user'
                        }
                    },
                    {
                        'option_positional': ['--new-password'],
                        'option_keywords': {
                            'dest': 'param_new_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The new password for the supplied VPSA '
                                    'username'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resets a user\'s password if the current '
                                   'password is unknown.  Use subcommand '
                                   '"generate-password-reset-code" to '
                                   'generate a new code.'
            },
            {
                'subcommand_info': ('change-password-by-password',
                                    vpsa_users.
                                    change_vpsa_user_password_by_password),
                'subcommand_options': [
                    VPSA_USERNAME_OPTION,
                    {
                        'option_positional': ['--existing-password'],
                        'option_keywords': {
                            'dest': 'param_existing_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The existing password for the supplied '
                                    'VPSA username'
                        }
                    },
                    {
                        'option_positional': ['--new-password'],
                        'option_keywords': {
                            'dest': 'param_new_password',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The new password for the supplied VPSA '
                                    'username'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resets a user\'s password if the current '
                                   'password is known.  Use '
                                   'change-password-by-code if it is unknown.'
            },
            {
                'subcommand_info': ('create', vpsa_users.create_vpsa_user),
                'subcommand_options': [
                    {
                        'option_positional': ['--username'],
                        'option_keywords': {
                            'dest': 'param_username',
                            'metavar': '<xxx>',
                            'type': str,
                            'required': True,
                            'help': 'The VPSA user\'s desired username'
                        }
                    },
                    {
                        'option_positional': ['--email'],
                        'option_keywords': {
                            'dest': 'param_email',
                            'metavar': '<xxx@yyy.zzz>',
                            'type': str,
                            'required': True,
                            'help': 'The VPSA user\'s email address'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Creates a VPSA user - may only be done '
                                   'by the VPSA primary user.  User will '
                                   'receive a temporary password at the '
                                   'provided email address and will be '
                                   'forced to change it.'
            },
            {
                'subcommand_info': ('delete', vpsa_users.delete_vpsa_user),
                'subcommand_options': [
                    VPSA_USERNAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Deletes a VPSA user - may only be done '
                                   'by the VPSA primary user'
            },
            {
                'subcommand_info': ('disable-cloud-admin-access',
                                    vpsa_users.disable_cloud_admin_access),
                'subcommand_options': [
                    {
                        'option_positional': ['--confirm'],
                        'option_keywords': {
                            'dest': 'param_confirm',
                            'action': 'store_true',
                            'required': True,
                            'help': 'Cloud admin access will only be '
                                    'disabled if this flag is passed.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Disables the ability of a storage cloud '
                                   'administrator to access the VPSA GUI of '
                                   'this VPSA to assist in troubleshooting.  '
                                   'This does not grant access to any volume '
                                   'data.  Enabled by default.'
            },
            {
                'subcommand_info': ('enable-cloud-admin-access',
                                    vpsa_users.enable_cloud_admin_access),
                'subcommand_options': [
                    {
                        'option_positional': ['--confirm'],
                        'option_keywords': {
                            'dest': 'param_confirm',
                            'action': 'store_true',
                            'required': True,
                            'help': 'Cloud admin access will only be '
                                    'enabled if this flag is passed.'
                        }
                    }
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Enables the ability of a storage cloud '
                                   'administrator to access the VPSA GUI of '
                                   'this VPSA to assist in troubleshooting.  '
                                   'This does not grant access to any volume '
                                   'data.  Enabled by default.'
            },
            {
                'subcommand_info': ('generate-password-reset-code',
                                    vpsa_users.
                                    generate_vpsa_user_password_reset_code),
                'subcommand_options': [
                    VPSA_USERNAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'E-mails a password reset code to the '
                                   'supplied username\'s e-mail address.  '
                                   'Used in conjunction with the '
                                   '"change-password-by-code" subcommand.'
            },
            {
                'subcommand_info': ('get-api-key',
                                    vpsa_users.get_vpsa_user_api_key),
                'subcommand_options': [
                    VPSA_USERNAME_OPTION,
                    VPSA_PASSWORD_OPTION
                ],
                'subcommand_return_key': 'user',
                'subcommand_help': 'Displays details for a user, including '
                                   'the API "access_key", authorized by the '
                                   'provided VPSA username and password - an '
                                   'API access key is not needed to call '
                                   'this command.'
            },
            {
                'subcommand_info': ('list', vpsa_users.get_all_vpsa_users),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'users',
                'subcommand_help': 'Displays details for all GUI and API '
                                   'users on the VPSA'
            },
            {
                'subcommand_info': ('reset-api-key',
                                    vpsa_users.reset_vpsa_user_api_key),
                'subcommand_options': [
                    VPSA_USERNAME_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Resets a user\'s API access key for the '
                                   'given username - may only be done by an '
                                   'administrative user'
            }
        ]
    },
    {
        'command_name': 'vpsaos-controllers',
        'help': 'Commands related to VPSAOS virtual controllers',
        'subcommands': [
            {
                'subcommand_info': ('get',
                                    vpsaos_controllers.get_virtual_controller),
                'subcommand_options': [
                    VC_INDEX_OPTION
                ],
                'subcommand_return_key': 'vc',
                'subcommand_help': 'Displays details for a single virtual '
                                   'controller on the VPSAOS'
            },
            {
                'subcommand_info':
                    ('get-drives',
                     vpsaos_controllers.get_virtual_controller_drives),
                'subcommand_options': [
                    VC_INDEX_OPTION
                ],
                'subcommand_return_key': 'disks',
                'subcommand_help': 'Displays drives for a virtual controller'
            },
            {
                'subcommand_info': ('list',
                                    vpsaos_controllers.get_all_controllers),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'vcs',
                'subcommand_help': 'Displays details for all virtual '
                                   'controllers on the VPSAOS'
            },
            {
                'subcommand_info': ('remove-proxy-vcs',
                                    vpsaos_controllers.remove_proxy_vcs),
                'subcommand_options': [
                    QUANTITY_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Removes proxy VCs '
            }
        ]
    },
    {
        'command_name': 'vpsaos-drives',
        'help': 'Commands related to VPSAOS drives',
        'subcommands': [
            {
                'subcommand_info': ('get', vpsaos_drives.get_one_drive),
                'subcommand_options': [
                    NAME_OPTION
                ],
                'subcommand_return_key': 'disk',
                'subcommand_help': 'Displays details for a single drive '
                                   'on the VPSAOS'
            },
            {
                'subcommand_info': ('list', vpsaos_drives.get_all_drives),
                'subcommand_options': [
                    LIMIT_OPTION,
                    START_OPTION
                ],
                'subcommand_return_key': 'disks',
                'subcommand_help': 'Displays details for all drives '
                                   'on the VPSAOS'
            },
        ]
    },
    {
        'command_name': 'vpsaos-operations',
        'help': 'Commands related to adding proxy vcs, drives to VPSAOS',
        'subcommands': [
            {
                'subcommand_info': ('add-drives', vpsaos.add_drives),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION,
                    DRIVE_TYPE_OPTION,
                    DRIVE_QUANTITY_OPTION,
                    POLICY_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Add drives to the VPSAOS'
            },
            {
                'subcommand_info': ('add-proxy-vcs', vpsaos.add_proxy_vcs),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Add proxy vc to the VPSAOS '
            },
            {
                'subcommand_info': ('add-storage-policy',
                                    vpsaos.add_storage_policy),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION,
                    POLICY_NAME_OPTION,
                    POLICY_DESC_OPTION,
                    DRIVE_TYPE_OPTION,
                    DRIVE_QUANTITY_OPTION,
                    POLICY_TYPE_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Add storage policy to the VPSAOS'
            },
            {
                'subcommand_info': ('assign-publicip', vpsaos.assign_publicip),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Assign public ip from VPSAOS '
            },
            {
                'subcommand_info': ('create-zsnap', vpsaos.create_zsnap),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION,
                    PREFIX_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Create a VPSAOS zsnap '
            },
            {
                'subcommand_info': ('get-vpsaos', vpsaos.get_one_vpsaos),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': 'zios',
                'subcommand_help': 'Return the details of a single VPSAOS '
            },
            {
                'subcommand_info': ('get-vpsaoss', vpsaos.get_all_vpsaoss),
                'subcommand_options': [
                    CLOUD_NAME_OPTION
                ],
                'subcommand_return_key': 'zioses',
                'subcommand_help': 'Return a list of all VPSAOSs '
            },
            {
                'subcommand_info': ('get-vpsaos-accounts',
                                    vpsaos.get_vpsaos_accounts),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': 'accounts',
                'subcommand_help': 'Return the list of VPSAOS accounts '
            },
            {
                'subcommand_info': ('get-vpsaos-comments',
                                    vpsaos.get_vpsaos_comments),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': 'comments',
                'subcommand_help': 'Return the list of VPSAOS comments '
            },
            {
                'subcommand_info': ('get-vpsaos-drives',
                                    vpsaos.get_vpsaos_drives),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': 'drives',
                'subcommand_help': 'Return the list of VPSAOS drives '
            },
            {
                'subcommand_info': ('get-vpsaos-sps', vpsaos.get_vpsaos_sps),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': 'zios_storage_policies',
                'subcommand_help': 'Return the list of VPSAOS storage policies'
            },
            {
                'subcommand_info': ('get-vpsaos-vcs', vpsaos.get_vpsaos_vcs),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': 'virtual_controllers',
                'subcommand_help':
                    'Return the list of VPSAOS virtual controllers '
            },
            {
                'subcommand_info': ('unassign-publicip',
                                    vpsaos.unassign_publicip),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Unassign public ip from VPSAOS '
            },
            {
                'subcommand_info': ('upgrade-vpsaos-image',
                                    vpsaos.upgrade_vpsaos_image),
                'subcommand_options': [
                    CLOUD_NAME_OPTION,
                    VSA_ID_OPTION,
                    IMAGE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Upgrade VPSAOS Software image '
            },
        ]
    },
    {
        'command_name': 'vpsaos-settings',
        'help': 'Commands related to VPSAOS settings like encryption',
        'subcommands': [
            {
                'subcommand_info': ('set-encryption',
                                    vpsaos_settings.set_encryption),
                'subcommand_options': [
                    ENCRYPTION_PWD_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Set encryption. '
            },
            {
                'subcommand_info': ('set-encryption-state',
                                    vpsaos_settings.set_encryption_state),
                'subcommand_options': [
                    STATE_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Set encryption state. '
            },
            {
                'subcommand_info': ('restore-encryption',
                                    vpsaos_settings.restore_encryption),
                'subcommand_options': [
                    ENCRYPTION_PWD_OPTION
                ],
                'subcommand_return_key': None,
                'subcommand_help': 'Restore encryption. '
            },
        ]
    }
]


def format_return(data, vertical=False):
    """
    Format the returned Python dictionary or list of dictionaries into human
    readable format.

    :type data: dict, list
    :param data: The data to be formatted.  This is typically the path to the
        'subcommand_return_key' in the returned dictionary from the API.

    :type vertical: bool
    :param vertical: If True, output will be displayed in a vertical format.
        This makes the output of large amount of columns easier to read.

    :rtype list
    :return: If a non empty list or dictionary, a human readable table will be
        generated and returned.  If an empty list is detected, a simple
        message will be returned.
    """
    if vertical:
        table_data = []
        table_formatted = []

        if type(data) is list:
            if len(data) > 0:
                for return_dict in data:
                    items = []
                    for key, value in sorted(return_dict.items()):
                        items.append([str(key), str(value)])
                    table_data.append(items)
            else:
                return 'An empty result set was returned'
        else:
            items = []
            for key, value in sorted(data.items()):
                items.append([str(key), str(value)])

            table_data.append(items)

        for row in table_data:
            table = SingleTable(row)
            table.inner_heading_row_border = False
            title = None
            for item in row:
                # Prefer display name if it exists
                if item[0] == 'display_name':
                    title = item[1]
                    break
                if item[0] == 'name':
                    title = item[1]
                    break
            if title is not None:
                table.title = title

            table_formatted.append(table.table)

        return table_formatted
    else:
        table_data = [[]]

        if type(data) is list:
            if len(data) > 0:
                for key in sorted(data[0]):
                    table_data[0].append(key)

                for return_dict in data:
                    row = []

                    for key in sorted(return_dict):
                        row.append(str(return_dict[key]))

                    table_data.append(row)
            else:
                return 'An empty result set was returned'
        else:
            row = []

            for key, value in sorted(data.items()):
                table_data[0].append(key)
                row.append(str(value))

            table_data.append(row)

        return [AsciiTable(
            table_data, 'Count: ' + str(len(table_data) - 1)
        ).table]


def check_positive(value):
    """
    Integer type check

    :param value: Value to check
    :return: True iff value is a positive int
    :raises: argparse.ArgumentTypeError: Invalid positive int value
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value"
                                         % value)
    return ivalue


def main():
    # Parent Parsers
    apiparser = argparse.ArgumentParser(add_help=False)

    group1 = apiparser.add_argument_group('Connection Arguments')
    group2 = apiparser.add_argument_group('Display Arguments')
    group3 = apiparser.add_argument_group('General Arguments')

    group1.add_argument('-c', '--api-configfile', type=str,
                        dest='configfile',
                        metavar='</path/to/configuration/file>',
                        help='Values such as the API endpoint and API key '
                             'can be parsed from this file, which is in '
                             'INI format.  Defaults to ~/.zadarapy')
    group1.add_argument('-H', '--api-hostname', type=str, dest='host',
                        metavar='<API hostname>',
                        help='The API hostname can be provided here - '
                             'alternatively, it can be defined through '
                             'the ZADARA_HOST environment variable, or a '
                             'configuration file')
    group1.add_argument('-i', '--insecure', action='store_true',
                        help='If passed, clear-text HTTP will be used '
                             'instead of encrypted HTTPS')
    group1.add_argument('-k', '--api-key', type=str, dest='key',
                        metavar='<API key>',
                        help='The API key can be provided here -  '
                             'alternatively, it can be defined through '
                             'the ZADARA_KEY environment variable, or a '
                             'configuration file')
    group1.add_argument('-p', '--api-port', type=int, dest='port',
                        metavar='<API port>',
                        help='The API port can be provided here -  '
                             'alternatively, it can be defined through '
                             'the ZADARA_PORT environment variable, or a '
                             'configuration file')

    group2.add_argument('-j', '--json', action='store_true',
                        help='If passed, a JSON string will be returned '
                             'instead of human readable format')
    group2.add_argument('-r', '--return-fields', type=str, dest='fields',
                        metavar='fieldname1,fieldname2',
                        help='For commands that display API return data, '
                             'this optionally defines which specific fields, '
                             'by key name, to return.  Multiple fields can '
                             'be specified as comma delimited.  For example: '
                             'display_name,pool_name')
    group2.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output for debugging '
                             'purposes')
    group2.add_argument('-V', '--vertical', action='store_true',
                        help='Display output in vertical form with a single '
                             'output table per row - this makes viewing '
                             'large amounts of output easier')

    # API command timeout: default is <session.DEFAULT_TIMEOUT> seconds (15)
    group3.add_argument('-t', '--timeout', type=check_positive, dest='timeout',
                        action='store', default=session.DEFAULT_TIMEOUT,
                        help='API command timeout. Default: {} seconds'
                        .format(session.DEFAULT_TIMEOUT))

    # Main Parser
    parser = argparse.ArgumentParser(
        prog='zadarapy',
        description='%(prog)s is a command line utility that runs commands '
                    'against a storage cloud or VPSA via the REST API using '
                    'the zadarapy Python module'
    )

    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(__version__),
                        help='Prints the %(prog)s version and exits')

    # Sub Parsers
    commandsparser = parser.add_subparsers(
        title='Commands - run "zadarapy <command> --help" for more '
              'information about each command',
        dest='command',
        metavar='command'
    )

    commandsparser.required = True

    for command in COMMANDS_DICT:
        commandparser = commandsparser.add_parser(command['command_name'],
                                                  description=command['help'],
                                                  help=command['help'])

        if 'subcommands' in command:
            subcommandparser = commandparser.add_subparsers(
                title='Sub Commands - run "zadarapy <command> <subcommand> '
                      '--help for more information about each subcommand',
                metavar='subcommand', dest='subcommand'
            )

            subcommandparser.required = True

            for subcommand in command['subcommands']:
                subcommand_name, _ = subcommand['subcommand_info']
                sub_action = subcommandparser.add_parser(
                    subcommand_name,
                    description=subcommand['subcommand_help'],
                    help=subcommand['subcommand_help'], parents=[apiparser]
                )

                # Group 4 is for command arguments
                group4 = sub_action.add_argument_group('Command Arguments')

                for subcommand_option in subcommand['subcommand_options']:
                    group4.add_argument(
                        *subcommand_option['option_positional'],
                        **subcommand_option['option_keywords']
                    )

    # Dispatcher
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    parsed_args = vars(parser.parse_args())

    secure = True

    if parsed_args['insecure']:
        secure = False

    try:
        parsed_args['param_session'] = session.Session(
            host=parsed_args['host'],
            port=parsed_args['port'],
            key=parsed_args['key'],
            configfile=parsed_args['configfile'],
            secure=secure
        )
    except ValueError as err:
        print('There was an error with a parameter passed to the API: "{0}"'
              .format(err))

    params = {k[6:]: v for k, v in parsed_args.items()
              if k.startswith('param_')}

    if parsed_args['json']:
        params['return_type'] = 'json'

    for command in COMMANDS_DICT:
        if command['command_name'] != parsed_args['command']:
            continue

        if 'subcommands' in command:
            for subcommand in command['subcommands']:
                subcommand_name, subcommand_function = \
                    subcommand['subcommand_info']

                if subcommand_name != parsed_args['subcommand']:
                    continue

                try:
                    if parsed_args['verbose']:
                        if params['session'].zadara_secure:
                            protocol = 'HTTPS'
                        else:
                            protocol = 'HTTP'

                        print('Connecting to {0} on port {1} with API key '
                              '{2} over protocol {3}'
                              .format(params['session'].zadara_host,
                                      params['session'].zadara_port,
                                      params['session'].zadara_key,
                                      protocol))

                        print('Parameters sent to the zadarapy function '
                              '"{0}":'.format(subcommand_function.__name__))

                        pprint(params)

                    result = subcommand_function(
                        timeout=parsed_args['timeout'], **params)

                    if parsed_args['json']:
                        print(result)
                    else:
                        if parsed_args['verbose']:
                            print('Raw Python dictionary response:')
                            pprint(result)

                        if subcommand['subcommand_return_key'] is not None:
                            # Calls to e-Commerce do not have 'response' key
                            # and some API calls don't return a response key
                            # if the response is empty
                            if 'response' in result:
                                try:
                                    sub = subcommand['subcommand_return_key']
                                    data = result['response'][sub]
                                except KeyError:
                                    print('An empty result set was returned')
                                    sys.exit(0)
                            else:
                                try:
                                    sub = subcommand['subcommand_return_key']
                                    data = result[sub]
                                except KeyError:
                                    print('An empty result set was returned')
                                    sys.exit(0)

                            if parsed_args['fields'] is not None:
                                fields = [x.strip() for x in
                                          parsed_args['fields'].split(',')]

                                response = []

                                for x in data:
                                    response.append(
                                        {k: v for k, v in x.items()
                                         if k in fields}
                                    )
                            else:
                                response = data

                            if type(response) not in [dict, list]:
                                print(response)
                                sys.exit(0)

                            tables = format_return(
                                data=response,
                                vertical=parsed_args['vertical']
                            )

                            if type(tables) in [int, str]:
                                print(tables)
                            else:
                                for table in tables:
                                    print(table)
                        else:
                            print('Command returned success')

                    sys.exit(0)
                except RuntimeError as err:
                    print('There was an error at runtime returned by the '
                          'API: "{0}"'.format(err))
                    sys.exit(1)
                except ValueError as err:
                    print('There was an error with a parameter passed to the '
                          'API: "{0}"'.format(err))
                    sys.exit(1)


if __name__ == '__main__':
    main()
