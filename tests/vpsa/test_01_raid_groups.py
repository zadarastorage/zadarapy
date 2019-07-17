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


from zadarapy.validators import is_valid_raid_id
from zadarapy.vpsa.raid_groups import create_raid_group, get_all_raid_groups
import pytest
import uuid


def test_create_raid1_group(zsession, all_drives):
    drive1 = all_drives['response']['disks'][0]['name']
    drive2 = all_drives['response']['disks'][1]['name']
    rg = create_raid_group(zsession, str(uuid.uuid4()), 'RAID1',
                           '{0},{1}'.format(drive1, drive2))

    assert rg['response']['status'] == 0


@pytest.fixture(scope="session")
def all_raid_groups(zsession):
    return get_all_raid_groups(zsession)


def test_get_all_raid_groups(all_raid_groups):
    for rg in all_raid_groups['response']['raid_groups']:
        assert is_valid_raid_id(rg['name'])
