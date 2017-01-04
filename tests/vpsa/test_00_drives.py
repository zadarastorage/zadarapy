# Copyright 2016 Zadara Storage, Inc.
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


from zadarapy.validators import is_valid_volume_id
from zadarapy.vpsa.drives import *
import uuid


def test_get_all_drives(all_drives):
    assert all_drives['response']['count'] >= 2

    for drive in all_drives['response']['disks']:
        assert is_valid_volume_id(drive['name'])


def test_get_free_drives(zsession):
    free_drives = get_free_drives(zsession)

    for drive in free_drives['response']['disks']:
        assert drive['raid_group_name'] is None


def test_get_drive(zsession, all_drives):
    drive = get_drive(zsession, all_drives['response']['disks'][0]['name'])

    assert is_valid_volume_id(drive['response']['disk']['name'])


def test_rename_drive(zsession, all_drives):
    new_name = str(uuid.uuid4())

    rename_drive(zsession, all_drives['response']['disks'][0]['name'],
                 new_name)

    drive = get_drive(zsession, all_drives['response']['disks'][0]['name'])

    name = drive['response']['disk']['display_name']

    assert name == new_name


# def test_remove_drive(zsession, all_drives):
#     drive_id = all_drives['response']['disks'][-1]['name']
#
#     remove_drive(zsession, drive_id)
#
#     drives = get_all_drives(zsession)
#
#     for drive in drives['response']['disks']:
#         assert not drive['name'] == drive_id


def test_shred_drive(zsession, all_drives):
    drive_id = all_drives['response']['disks'][0]['name']

    shred_drive(zsession, drive_id)

    drive = get_drive(zsession, all_drives['response']['disks'][0]['name'])

    status = drive['response']['disk']['status']

    assert status.startswith('Shredding')


def test_cancel_shred_drive(zsession, all_drives):
    drive_id = all_drives['response']['disks'][0]['name']

    cancel_shred_drive(zsession, drive_id)

    drive = get_drive(zsession, all_drives['response']['disks'][0]['name'])

    status = drive['response']['disk']['status']

    assert not status.startswith('Shredding')


def test_get_drive_performance(zsession, all_drives):
    drive_id = all_drives['response']['disks'][0]['name']

    performance = get_drive_performance(zsession, drive_id)

    assert performance['response']['count'] == \
        len(performance['response']['usages'])
