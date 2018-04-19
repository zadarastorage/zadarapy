# Copyright 2018 Zadara Storage, Inc.
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


import json
from zadarapy.validators import *


def upgrade_vpsa_version(session, cloud_name, vpsa_id, image, when=None,
                         return_type=None):
    """
    Upgrade a VPSA to a new version.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type image: str
    :param image: The version to upgrade to.  For example: '16.05-sp2-389'.
        Required.

    :type when: str
    :param when: When to trigger the VPSA version upgrade.  Can be one of
        three values: "now" will initiate the upgrade ASAP - and is the
        default value if "when" parameter isn't passed.  "manual" will prepare
        the standby VC with the new version for a later manually initiated
        completion.  A date can also be passed in "%Y-%m-%d %H:%M" format.  For
        example: "2017-10-20 19:30".  This value is relative to the cloud's
        timezone setting.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_name = cloud_name.strip()

    if not is_valid_field(cloud_name):
        raise ValueError('{0} is not a valid cloud name.'.format(cloud_name))

    if type(vpsa_id) is int:
        vpsa_id = str(vpsa_id)

    if not vpsa_id.isdigit():
        raise ValueError('The VPSA ID should be a positive integer.')

    body_values = {}

    image = image.strip()

    if not is_valid_field(image):
        raise ValueError('{0} is not a valid volume name.'.format(image))

    body_values['image'] = image

    if when is not None:
        when = when.strip()

        if not is_valid_field(when):
            raise ValueError('{0} is not a valid when value.'.format(when))

        body_values['when'] = when

    method = 'POST'
    path = '/api/clouds/{0}/vpsas/{1}/upgrade.json'.format(cloud_name, vpsa_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)
