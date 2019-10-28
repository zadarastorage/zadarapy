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
import json

from zadarapy.validators import verify_boolean, \
    verify_field, verify_start_limit, verify_volume_id, verify_zcs_image_id, \
    is_valid_field, verify_zcs_container_id, \
    verify_memory_pool, is_valid_volume_id
from zadarapy.vpsa import ERROR_MSG


def get_all_zcs_images(session, start=None, limit=None, return_type=None,
                       **kwargs):
    """
    Retrieves details for all Zadara Container Services (ZCS) images
    configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying ZCS images from.  Optional.

    :type: limit: int
    :param limit: The maximum number of ZCS images to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)
    path = '/api/images.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_zcs_image(session, zcs_image_id, return_type=None, **kwargs):
    """
    Retrieves details for a single Zadara Container Services (ZCS) image.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_image_id: str
    :param zcs_image_id: The ZCS image 'name' value as returned by
        get_all_zcs_images.  For example: 'img-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_image_id(zcs_image_id)

    path = '/api/images/{0}.json'.format(zcs_image_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_zcs_image(session, display_name, path, volume_id=None,
                     return_type=None, **kwargs):
    """
    Creates a new Zadara Container Services (ZCS) image.  Running container
    instances are created from these images.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the ZCS image.  For
        example: 'ubuntu', 'SSH', etc.  May not contain a single quote
        (') character.  Required.

    :type path: str
    :param path: When importing from Docker Hub, this is the name of the
        Docker image; for example: 'ubuntu' or 'zadara/ssh'.  When importing
        from a volume (requires the volume_id parameter), the full path on the
        volume to the Docker image tar file; for example:
        'images/testimage.tar'.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  When specified, the ZCS image will be
        imported from this volume.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    display_name = verify_field(display_name, "display_name")
    path = verify_field(path, "ZCS image path")

    body_values = {'name': display_name, 'path': path}

    # We'll inflect the required "mode" parameter by detecting if volume_id
    # is defined.
    if volume_id is not None:
        verify_volume_id(volume_id)
        body_values['mode'] = 'volume'

    else:
        body_values['mode'] = 'docker'

    path = '/api/images.json'

    try:
        res = session.post_api(path=path, body=body_values,
                               return_type=return_type, **kwargs)
    except RuntimeError as exc:
        err = str(exc)
        # The API server returned an error: "The request has been submitted".
        if err.startswith(ERROR_MSG):
            res = {'response': {"status": 0}}
        else:
            raise

    return res


def delete_zcs_image(session, zcs_image_id, return_type=None, **kwargs):
    """
    Deletes a Zadara Container Services (ZCS) image.  There must not be any
    spawned containers using this image.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_image_id: str
    :param zcs_image_id: The ZCS image 'name' value as returned by
        get_all_zcs_images.  For example: 'img-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_image_id(zcs_image_id)

    path = '/api/images/{0}.json'.format(zcs_image_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_all_zcs_containers_by_image(session, zcs_image_id, start=None,
                                    limit=None, return_type=None, **kwargs):
    """
    Retrieves details for all Zadara Container Services (ZCS) containers
    instantiated from the specified ZCS image.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_image_id: str
    :param zcs_image_id: The ZCS image 'name' value as returned by
        get_all_zcs_images.  For example: 'img-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying ZCS containers from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of ZCS containers to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_image_id(zcs_image_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/images/{0}/containers.json'.format(zcs_image_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_all_zcs_containers(session, start=None, limit=None, return_type=None,
                           **kwargs):
    """
    Retrieves details for all Zadara Container Services (ZCS) containers
    configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying ZCS containers from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of ZCS containers to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    parameters = verify_start_limit(start, limit)

    path = '/api/containers.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_zcs_container(session, zcs_container_id, return_type=None, **kwargs):
    """
    Retrieves details for a single Zadara Container Services (ZCS) container.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_container_id: str
    :param zcs_container_id: The ZCS container 'name' value as returned by
        get_all_zcs_containers.  For example: 'container-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_container_id(zcs_container_id)

    path = '/api/containers/{0}.json'.format(zcs_container_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_zcs_container(session, display_name, zcs_image_id, start,
                         use_public_ip='NO', entrypoint=None, volumes=None,
                         args=None, envvars=None, links=None, memorypoolname=None,
                         return_type=None, **kwargs):
    """
    Creates a Zadara Container Services (ZCS) container.  Requires a valid ZCS
    image to instantiate from.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name: A text label to assign to the ZCS container.  For
        example: 'web-01', 'database', etc.  May not contain a single quote
        (') character.  Required.

    :type zcs_image_id: str
    :param zcs_image_id: The ZCS image 'name' value as returned by
        get_all_zcs_images.  For example: 'img-00000001'.  The container will
        be instantiated from this image.  Required.

    :type start: str
    :param start: If set to 'YES', the ZCS container will be started
        immediately after creation.  If 'NO', it will not be started.
        Required.

    :type use_public_ip: str
    :param use_public_ip: If set to 'YES', the ZCS container will listen on
        VPSA's public IP address (only valid on VPSAs with a public IP
        address).  If set to 'NO', the container will listen on the same
        private IP address that is used for addressing the storage.  Optional
        (set to 'NO' by default).

    :type entrypoint: str
    :param entrypoint: The full path to the program or script inside the ZCS
        container to run when the container starts.  For example:
        "/usr/local/bin/entry.sh".  It is important to define a correct
        entrypoint either via this function or a "RUN" statement in the
        Dockerfile, as when a VPSA needs to initiate a failover, the container
        will be started automatically on the standby controller and the
        container should automatically initiate any needed setup/program.
        This should only be the path to the script/program.  Only the path to
        the script/program should be defined without arguments.  To pass
        arguments to the script/program, use the "args" parameter of this
        function.  Optional.

    :type volumes: list, str
    :param volumes: A Python list of Python dictionaries that contain several
        pieces of information about the NAS share volumes (NFS/SMB only, no
        iSCSI/ISER) that should be attached to the container when launched.
        If passed as a string, a conversion to a Python list via json.loads
        will be attempted.  Every list item should be a dictionary that
        contains the following keys:

        * "name" - This key should contain the volume 'name' value as
          returned by get_all_volumes.  For example: 'volume-00000001'.
          Required.
        * "path" - This key should contain the full path inside of the
          container where the volume will be mounted.  If the path doesn't
          exist in the container, it will be created.  Required.
        * "access" - If this key is set to 'rw', the volume will be mounted as
          both readable and writable.  If set to 'r', the volume will be
          mounted as read only.  Required.

        An example would be:

        [{"name":"volume-00000001","path":"/vol1","access":"rw"},
         {"name":"volume-00000002","path":"/vol2","access":"r"}]

    :type links: list, str
    :param links: A Python list that contain container identifiers that will be
        linked to the new container

        An example would be:
        ["container-00000001" , "container-00000002"]

    :type args: list, str
    :param args: A Python list of Python dictionaries that contain arguments
        to pass to the ZCS container entry point program or script as defined
        by "entrypoint".  If passed as a string, a conversion to a Python list
        via json.loads will be attempted.  Every list item should be a
        dictionary that contains one key, "arg", whose value is the argument
        to pass to the ZCS container.  For example, if the entrypoint is
        "/usr/sbin/sshd", these arguments will be passed to sshd.  e.g.:

        [{"arg":"-p 2222"},{"arg":"-f /etc/ssh/sshd_config"}]

    :type envvars: list, str
    :param envvars: A Python list of Python dictionaries that contain
        information about environment variables to pass into the ZCS
        container.  If passed as a string, a conversion to a Python list via
        json.loads will be attempted.  Every list item should be a dictionary
        that contains the the following keys:

        * "variable" - This key should contain the name of the environment
          variable to create.  For example: "IP_ADDRESS".
        * "value" - This key should contain the value for the corresponding
          "variable".  For example "172.20.125.100".

        For example, say that part of the entry point script adds an item to a
        Redis server.  Environment variables could be used by the script to
        determine the IP address, username, and password of the Redis server.
        e.g.:

        [{"variable":"IP_ADDRESS","value":"172.20.125.100"},
         {"variable":"USERNAME","value":"zcs_container_01"},
         {"variable":"PASSWORD","value":"very_strong_password"}]

    :type memorypoolname: str
    :param memorypoolname: Memory Pool ID

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    display_name = verify_field(display_name, 'display_name')
    verify_zcs_image_id(zcs_image_id)
    start = verify_boolean(start, "start")
    use_public_ip = verify_boolean(use_public_ip, "use_public_ip")
    body_values = {'name': display_name, 'imagename': zcs_image_id,
                   'start': start, 'use_public_ip': use_public_ip,
                   'entrypoint': entrypoint, 'link': links}

    if volumes is not None:
        if type(volumes) is str:
            volumes = json.loads(volumes)

        if type(volumes) is not list:
            raise ValueError('The passed "volumes" parameter is not a Python '
                             'list.')

        for v in volumes:
            if type(v) is not dict:
                raise ValueError('Each item in the "volumes" list must be a '
                                 'Python dictionary.')

            if 'name' not in v:
                raise ValueError('The required "volume" key was not found in '
                                 'the name dictionary.')

            if not is_valid_volume_id(v['name']):
                raise ValueError('{0} is not a valid volume ID.'
                                 .format(v['name']))

            if 'path' not in v:
                raise ValueError('The required "path" key was not found in '
                                 'the volume dictionary.')

            v['path'] = v['path'].strip()

            if not is_valid_field(v['path']):
                raise ValueError('"{0}" is not a valid ZCS container volume '
                                 'mount point.'.format(v['path']))

            if 'access' not in v:
                raise ValueError('The required "access" key was not found in '
                                 'the volume dictionary.')

            if v['access'] not in ['rw', 'r']:
                raise ValueError('"{0}" is not a valid "access" key in the '
                                 'volume dictionary.  Allowed values are: '
                                 '"rw" or "r"'.format(v['access']))

        body_values['volumes'] = volumes

    if args is not None:
        if type(args) is str:
            args = json.loads(args)

        if type(args) is not list:
            raise ValueError('The passed "args" parameter is not a Python '
                             'list.')

        for v in args:
            if type(v) is not dict:
                raise ValueError('Each item in the "args" list must be a '
                                 'Python dictionary.')

            if 'arg' not in v:
                raise ValueError('The required "arg" key was not found in '
                                 'the args dictionary.')

            v['arg'] = v['arg'].strip()

            if not is_valid_field(v['arg']):
                raise ValueError('{0} is not a valid ZCS container argument '
                                 'value.'.format(v['arg']))

        body_values['args'] = args

    if envvars is not None:
        if type(volumes) is str:
            envvars = json.loads(envvars)

        if type(envvars) is not list:
            raise ValueError('The passed "envvars" parameter is not a Python '
                             'list.')

        for v in envvars:
            if type(v) is not dict:
                raise ValueError('Each item in the "envvars" list must be a '
                                 'Python dictionary.')

            if 'variable' not in v:
                raise ValueError('The required "variable" key was not found '
                                 'in the envvars dictionary.')

            v['variable'] = v['variable'].strip()

            if not is_valid_field(v['variable']):
                raise ValueError('{0} is not a valid ZCS container '
                                 'environment variable name.'
                                 .format(v['variable']))

            if 'value' not in v:
                raise ValueError('The required "value" key was not found in '
                                 'the envvars dictionary.')

            # Don't strip leading or trailing whitespace here since a variable
            # may contain any ad-hoc value depending on use case.
            if not is_valid_field(v['value']):
                raise ValueError('{0} is not a valid ZCS container '
                                 'environment variable value.'
                                 .format(v['value']))

        body_values['envvars'] = envvars

    if memorypoolname:
        body_values['memorypoolname'] = memorypoolname

    path = '/api/containers.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def start_zcs_container(session, zcs_container_id, return_type=None, **kwargs):
    """
    Starts a stopped Zadara Container Services (ZCS) container.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_container_id: str
    :param zcs_container_id: The ZCS container 'name' value as returned by
        get_all_zcs_containers.  For example: 'container-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_container_id(zcs_container_id)

    path = '/api/containers/{0}/start.json'.format(zcs_container_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def stop_zcs_container(session, zcs_container_id, return_type=None, **kwargs):
    """
    Stops a running Zadara Container Services (ZCS) container.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_container_id: str
    :param zcs_container_id: The ZCS container 'name' value as returned by
        get_all_zcs_containers.  For example: 'container-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_container_id(zcs_container_id)

    path = '/api/containers/{0}/stop.json'.format(zcs_container_id)

    try:
        res = session.post_api(path=path, return_type=return_type, **kwargs)
    except RuntimeError as exc:
        err = str(exc)
        # The API server returned an error: "The request has been submitted".
        if err.startswith(ERROR_MSG):
            res = {'response': {"status": 0}}
        else:
            raise

    return res


def delete_zcs_container(session, zcs_container_id, return_type=None,
                         **kwargs):
    """
    Deletes a Zadara Container Services (ZCS) container.  The container must
    first be stopped.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_container_id: str
    :param zcs_container_id: The ZCS container 'name' value as returned by
        get_all_zcs_containers.  For example: 'container-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_container_id(zcs_container_id)

    path = '/api/containers/{0}.json'.format(zcs_container_id)

    try:
        res = session.delete_api(path=path, return_type=return_type, **kwargs)
    except RuntimeError as exc:
        err = str(exc)
        # The API server returned an error: "The request has been submitted".
        if err.startswith(ERROR_MSG):
            res = {'response': {"status": 0}}
        else:
            raise

    return res


def get_container_performance(session, zcs_container_id, return_type=None,
                              **kwargs):
    """
    Get Container performance

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type zcs_container_id: str
    :param zcs_container_id: The ZCS container 'name' value as returned by
        get_all_zcs_containers.  For example: 'container-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_zcs_container_id(zcs_container_id)

    path = "/api/containers/{0}/performance.json".format(zcs_container_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)()


def get_memory_pool(session, mempool_id, return_type=None, **kwargs):
    """
    Retrieves details for a single Memory Pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mempool_id: str
    :param mempool_id: The memory pool 'name' value as returned by
    get_all_memory_pools. For example: 'dgroup-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_memory_pool(mempool_id)

    path = 'api/container_memory_pools/{0}.json'.format(mempool_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_all_memory_pools(session, return_type=None, **kwargs):
    """
    Retrieves details for all Memory Pools in VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = "/api/container_memory_pools.json"
    return session.get_api(path=path, return_type=return_type, **kwargs)


def delete_memory_pool(session, mempool_id, return_type=None, **kwargs):
    """
    Retrieves details for a single Memory Pool.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mempool_id: str
    :param mempool_id: The memory pool 'name' value as returned by
    get_all_memory_pools. For example: 'dgroup-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    verify_memory_pool(mempool_id)

    path = 'api/container_memory_pools/{0}.json'.format(mempool_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def create_mem_pool(session, display_name, mb, return_type=None, **kwargs):
    """
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type display_name: str
    :param display_name:Display name

    :type mb: str
    :param mb:  memory limit in MB

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
            will return a JSON string.  Otherwise, it will return a Python
            dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
    return_type parameter.
    """
    display_name = verify_field(display_name, "display_name")

    path = "/api/container_memory_pools.json"

    body_values = {'name': display_name, 'mb': mb}

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)
