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


def get_settings_config(session, return_type=None):
    path = "/api/settings_config.json"
    return session.get_api(path=path, return_type=return_type)


def ssl_termination(session, is_terminate, return_type=None):
    """

    :param session:
    :param is_terminate: True iff terminate SSL
    :type is_terminate: bool
    :param return_type:
    :return:
    """
    path = "/api/zios/settings/ssl_termination.json"
    body_values = {"ssltermination": "on" if is_terminate else "off"}
    return session.port_api(path=path, bool=body_values,
                            return_type=return_type)
