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


from zadarapy.validators import verify_field, verify_vpsa_id, verify_cloud_name, verify_capacity, verify_bool_parameter


def upgrade_vpsa_version(session, cloud_name, vpsa_id, image, when=None,
                         return_type=None, **kwargs):
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

    path = '/api/clouds/{0}/vpsas/{1}/upgrade.json'.format(cloud_name, vpsa_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def resume_upgrade(session, cloud_name, vpsa_id, return_type=None, **kwargs):
    """
    Resume VPSA Upgrade

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
    verify_vpsa_id(vpsa_id)
    path = "/api/clouds/{0}/vpsas/{1}/resume_waiting.json" \
        .format(cloud_name, vpsa_id)
    return session.post_api(path=path, return_type=return_type, **kwargs)


def hibernate_vpsa(session, cloud_name, vpsa_id, return_type=None, **kwargs):
    """
    Hibernate VPSA.

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
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/hibernate.json" \
        .format(cloud_name, vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def restore_vpsa(session, cloud_name, vpsa_id, return_type=None, **kwargs):
    """
    Restore VPSA.

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
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/restore.json" \
        .format(cloud_name, vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def create_zsnap(session, cloud_name, vpsa_id, prefix, return_type=None,
                 **kwargs):
    """
    Create Zsnap from CC.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

    :type prefix: str
    :param prefix: Z-Snap prefix

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    vpsa_id = verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/zsnap.json" \
        .format(cloud_name, vpsa_id)

    body_values = {'prefix': prefix}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def assign_public_ip(session, cloud_name, vpsa_id, return_type=None, **kwargs):
    """
    Assign VPSA public IP

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
    vpsa_id = verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/public_ip/assign.json" \
        .format(cloud_name, vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def unassign_public_ip(session, cloud_name, vpsa_id, return_type=None,
                       **kwargs):
    """
    Unassign VPSA public IP

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
    vpsa_id = verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/public_ip/unassign.json" \
        .format(cloud_name, vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def get_all_vpsas(session, cloud_name, return_type=None, **kwargs):
    """
    Get all VPSAs in cloud

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/clouds/{0}/vpsas.json".format(cloud_name)
    return session.get_api(path=path, return_type=return_type, **kwargs)


def failover_vpsa(session, cloud_name, vpsa_id, return_type=None, **kwargs):
    """
    Failover VPSA

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

    path = "/api/clouds/{0}/vpsas/{1}/failover.json" \
        .format(cloud_name, vpsa_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def get_all_vpsa_drives(session, cloud_name, vpsa_id, return_type=None,
                        **kwargs):
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

    return session.get_api(path=path, return_type=return_type, **kwargs)


def add_drives(session, cloud_name, vsa_id, drive_type, drive_quantity,
               skip_validation, return_type=None, **kwargs):
    """
    Add drives to a VPSAOS.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vsa_id: str
    :param vsa_id: The 'vsa_id' value as returned by get_all_vpsaoss.  For
        example: 'vsa-000007de'.  Required.

    :type drive_type: str
    :param drive_type: Drive type internal name.  Required

    :type drive_quantity: int
    :param drive_quantity: Number of drives to add.  Required.

    :type skip_validation: bool
    :param skip_validation: Skips maximum drive validation. Use for admin only. Please notice that exceeding the number
        of drives allowed will waive the support for the VPSA.  Required

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    cloud_name = verify_cloud_name(cloud_name)
    vsa_id = verify_vpsa_id(vsa_id)
    drive_type = verify_field(drive_type, 'drive_type')
    drive_quantity = verify_capacity(drive_quantity, 'drive_quantity')
    skip_validation = verify_bool_parameter(skip_validation)

    body_values = {'drive_type': drive_type, 'quantity': drive_quantity, 'skip_validation': skip_validation}

    path = '/api/clouds/{0}/vpsas/{1}/drives.json'.format(cloud_name, vsa_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_app_engine(session, cloud_name, app_engine_id, return_type=None,
                   **kwargs):
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
    path = "/api/clouds/{0}/app_engine_types/{1}.json" \
        .format(cloud_name, app_engine_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_io_engine(session, cloud_name, app_io_id, return_type=None, **kwargs):
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
    path = "/api/clouds/{0}/engine_types/{1}.json" \
        .format(cloud_name, app_io_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def reschedule_upgrade_vpsa(session, cloud_name, vpsa_id, when,
                            return_type=None, **kwargs):
    """
    Reschedule Upgrade VPSA

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cloud_name: str
    :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
        example: 'zadaralab01'.  Required.

    :type vpsa_id: str
    :type vpsa_id: int
    :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
        example: '2653'.  Required.

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
    path = "/api/clouds/{0}/vpsas/{1}/reschedule_upgrade.json" \
        .format(cloud_name, vpsa_id)
    body_values = {"when": when}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def change_engine_type(session, cloud_name, vpsa_id, when,
                       app_engine_type=None, engine_type=None, image=None,
                       return_type=None, **kwargs):
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
    :param engine_type: CCVM Engine Type

    :type app_engine_type: str
    :param app_engine_type: CCVM Application Engine Typ

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}/change_engine_type.json" \
        .format(cloud_name, vpsa_id)

    body_values = {"when": when}
    if app_engine_type is not None:
        body_values["app_engine_type"] = app_engine_type
    if engine_type is not None:
        body_values["engine_type"] = engine_type
    if image is not None:
        body_values["image"] = image

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_cache(session, cloud_name, vpsa_id, **kwargs):
    """
      Get VPSA cache

      :type session: zadarapy.session.Session
      :param session: A valid zadarapy.session.Session object.  Required.

      :type cloud_name: str
      :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
          example: 'zadaralab01'.  Required.

      :type vpsa_id: int
      :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
          example: '2653'.  Required.

      :type return_type: int
      :param return_type: If this is set to the string 'str', this function
              will return a cache size as a string.  Otherwise, it will return an
              integer.  Optional (will return an integer by default).

      :rtype: int, str
      :returns: Cache size as Int
      return_type parameter.
    """
    verify_vpsa_id(vpsa_id)

    path = "/api/clouds/{0}/vpsas/{1}".format(cloud_name, vpsa_id)

    result = session.get_api(path=path, **kwargs)

    return result["vpsa"]["cache"]


def change_cache(session, cloud_name, vpsa_id, cache, return_type=None, **kwargs):
    """
      Change VPSA cache

      :type session: zadarapy.session.Session
      :param session: A valid zadarapy.session.Session object.  Required.

      :type cloud_name: str
      :param cloud_name: The cloud 'name' as returned by get_all_clouds.  For
          example: 'zadaralab01'.  Required.

      :type vpsa_id: int
      :param vpsa_id: The VPSA 'id' value as returned by get_all_vpsas.  For
          example: '2653'.  Required.

      :type cache: str
      :param cache: New cache size

      :type return_type: str
      :param return_type: If this is set to the string 'json', this function
              will return a JSON string.  Otherwise, it will return a Python
              dictionary.  Optional (will return a Python dictionary by default).

      :rtype: dict, str
      :returns: A dictionary or JSON data set as a string depending on
      return_type parameter.
    """
    verify_vpsa_id(vpsa_id)

    from zadarapy.provisioning_portal.vpsa import verify_cache_argument
    verify_cache_argument(int(cache), 'cache')

    path = "/api/clouds/{0}/vpsas/{1}/change_cache.json" \
        .format(cloud_name, vpsa_id)

    body_values = {"cache": cache}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
