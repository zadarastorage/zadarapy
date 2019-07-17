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


import pytest

from zadarapy.session import Session


def test_session_invalid_hostname():
    zsession = Session(host='invalid$.hostname.com')
    with pytest.raises(ValueError):
        zsession.call_api(method='GET', path='/api/invalid.json')


def test_session_invalid_key():
    zsession = Session(key='12345abc')
    with pytest.raises(ValueError):
        zsession.call_api(method='GET', path='/api/invalid.json')


def test_session_port_too_low():
    zsession = Session(port=-1)
    with pytest.raises(ValueError):
        zsession.call_api(method='GET', path='/api/invalid.json')


def test_session_port_too_high():
    zsession = Session(port=65536)
    with pytest.raises(ValueError):
        zsession.call_api(method='GET', path='/api/invalid.json')
