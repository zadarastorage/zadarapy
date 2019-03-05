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
    cloud_name = verify_field(cloud_name, "cloud_name")
    image = verify_field(image, "image")
    vpsa_id = verify_vpsa_id(vpsa_id)

    body_values = {'image': image}

    if when is not None:
        body_values['when'] = verify_field(when, "when")

    method = 'POST'
    path = '/api/clouds/{0}/vpsas/{1}/upgrade.json'.format(cloud_name, vpsa_id)

    return session.call_api(method=method, path=path, body=body_values,
                            return_type=return_type)


def get_all_vpsa_drives(session, cloud_name, vpsa_id, return_type=None):
    """
    Get all VPSAs in cloud

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_vpsa_id(vpsa_id=vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/drives.json".format(cloud_name, vpsa_id)

    return session.get_api(path=path, return_type=return_type)


def get_app_engine(session, cloud_name, app_engine_id, return_type=None):
    """
    Get Application Engine in Cloud

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type app_engine_id: int
    :param app_engine_id: Application engine ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/app_engine_types/{1}.json".format(cloud_name, app_engine_id)

    return session.get_api(path=path, return_type=return_type)


def get_io_engine(session, cloud_name, app_io_id, return_type=None):
    """
    Get Application Engine in Cloud

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type app_io_id: int
    :param app_io_id: IO engine ID. Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/engine_types/{1}.json".format(cloud_name, app_io_id)

    return session.get_api(path=path, return_type=return_type)


def reschedule_upgrade_vpsa(session, cloud_name, vpsa_id, when, return_type=None):
    """
    Reschedule Upgrade VPSA

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vpsa_id: str
    :param vpsa_id: TODO

    :type when: str
    :param when: TODO

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on return_type parameter.
    """
    path = "/api/clouds/{0}/vpsas/{1}/reschedule_upgrade.json".format(cloud_name, vpsa_id)
    body_values = {"when": when}
    return session.post_api(path=path, body=body_values, return_type=return_type)


def change_engine_type(session, cloud_name, vpsa_id, when, app_engine_type=None, engine_type=None, image=None,
                       return_type=None):
    """
    Change VPSA engine type

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

    :type engine_type: str
    :param engine_type: TODO

    :type app_engine_type: str
    :param app_engine_type: TODO

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on return_type parameter.
    """
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/change_engine_type.json".format(cloud_name, vpsa_id)

    body_values = {"when": when}
    if app_engine_type is not None:
        body_values["app_engine_type"] = app_engine_type
    if engine_type is not None:
        body_values["engine_type"] = engine_type
    if image is not None:
        body_values["image"] = image

    return session.post_api(path=path, body=body_values, return_type=return_type)
