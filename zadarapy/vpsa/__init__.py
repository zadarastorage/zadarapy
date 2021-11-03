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

from enum import Enum

ERROR_MSG = 'The API server returned an error: "The request has been submitted'


class BaseEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class VPSAInterfaceTypes(BaseEnum):
    FE = 'fe'
    PUBLIC = 'public'
    VNI_PREFIX = 'vni-'


class VolumePolicyApplicationType(BaseEnum):
    USER = 'user'
    FILE_HISTORY = 'file_history'


class SnapshotPolicyApplicationType(BaseEnum):
    USER = 'user'
    FILE_HISTORY = 'shadow_copy'
    MIRROR = 'mirror'
    MIGRATION = 'migration'
    OBS_MIRROR = 'obs_mirror'

