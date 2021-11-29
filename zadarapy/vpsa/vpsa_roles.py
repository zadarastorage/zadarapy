from future.standard_library import install_aliases
from urllib.parse import quote

install_aliases()

from zadarapy.validators import verify_field, verify_start_limit, verify_id

def get_all_roles(session, start=None, limit=None, return_type=None,
                       **kwargs):
    """
    Retrieves details for all configured VPSA roles.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.
    :type start: int
    :param start: The offset to start displaying VPSA roles from.
        Optional.
    :type: limit: int
    :param limit: The maximum number of VPSA roles to return.
        Optional.
    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    
    parameters = verify_start_limit(start, limit)

    path = '/api/roles.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)

def list_all_permissions(session, return_type=None, **kwargs):
    """
    Retrieves details for all kind of permissions.
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
    path = 'api/roles/all_permissions.json'
    api_res = session.get_api(path=path, return_type=return_type, **kwargs)
    return api_res
    


def add_role(session, name, permissions, return_type=None, **kwargs):
    """
    Add role with chosen permissions.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: The role name.  Required.

    :type permissions: list[str]
    :param permissions: The permissions to give this role

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    name = verify_field(name, "name")
    body_values = {'name': name, 'permissions': permissions}
    path = '/api/roles.json'
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)

def update_role(session, role_id, name, permissions, return_type=None, **kwargs):
    """
    Update role with chosen permissions.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type name: str
    :param name: The role name.  Required.

    :type permissions: list[str]
    :param permissions: The permissions to give this role

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    name = verify_field(name, "name")

    body_values = {'name': name, 'permissions': permissions}

    path = '/api/roles/{0}.json'.format(role_id)
    return session.put_api(path=path, body=body_values,
                           return_type=return_type, **kwargs)


def delete_role(session, role_id,return_type=None, **kwargs):
    """
    Delete role.
    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type role_id: str
    :param role_id: The role ID.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).
    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """

    role_id = verify_id(role_id)
    path = '/api/roles/{0}.json'.format(role_id)
    return session.delete_api(path=path, return_type=return_type, **kwargs)


