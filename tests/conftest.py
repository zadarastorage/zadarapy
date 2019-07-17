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


from zadarapy import session
from zadarapy.vpsa.drives import get_all_drives
import pytest


@pytest.fixture(scope="session")
def zsession():
    return session.Session()


@pytest.fixture(scope="function")
def all_drives(zsession):
    return get_all_drives(zsession)
