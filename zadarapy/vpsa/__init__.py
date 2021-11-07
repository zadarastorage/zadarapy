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
    FILE_HISTORY = 'file_history'
    MIRROR = 'mirror'
    MIGRATION = 'migration'
    OBS_MIRROR = 'obs_mirror'

class FlcTypes(BaseEnum):
    FILE_DATA_GROWTH_TREND = 'file_data_growth_trend'
    GROWTH_TREND_BY_FILE_TYPE = 'growth_trend_by_file_type'
    UTILIZATION_BY_FILE_SIZE = 'utilization_by_file_size'
    UTILIZATION_BY_AGE = 'utilization_by_age'
    UTILIZATION_BY_ACCESS = 'utilization_by_access'
    UTILIZATION_BY_FILE_TYPE = 'utilization_by_file_type'
    TOP_GROUPS = 'top_groups'
    TOP_USERS = 'top_users'
    
