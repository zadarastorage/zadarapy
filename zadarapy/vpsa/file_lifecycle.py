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


from zadarapy.validators import verify_file_category_id


def get_all_categories(session, return_type=None, **kwargs):
    """
    Show file lifecycle categories and their file extensions.

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
    path = '/api/flc/categories_settings.json'

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_category(session, displayname, file_extensions,
                    return_type=None, **kwargs):
    """
    Create a new file lifecycle category with its file extensions.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type displayname: str
    :param displayname: The category displayname 'category_name' value as returned by
        get_all_categories.  For example: 'Video Files'.  Required.

    :type file_extensions: str
    :param file_extensions: The category file extensions 'extension' value as returned by
        get_all_categories.  For example: 'avi,mpg,mpeg'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {'displayname': displayname, 'file_extensions': file_extensions}

    path = '/api/flc/create_category.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_category(session, category, file_extensions,
                    return_type=None, **kwargs):
    """
    Update an existing file lifecycle category to change its file extensions.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type category: str
    :param category: The category ID 'category-ext-name' value as returned by
        get_all_mirrors.  For example: 'category-00000002'.  Required.

    :type file_extensions: str
    :param file_extensions: The category file extensions 'extension' value as returned by
        get_all_categories.  For example: 'avi,mpg,mpeg'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_file_category_id(category)

    body_values = {'category': category, 'file_extensions': file_extensions}

    path = '/api/flc/update_category.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def rename_category(session, category, displayname,
                    return_type=None, **kwargs):
    """
    Update an existing file lifecycle category to change its file extensions.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type category: str
    :param category: The category ID 'category-ext-name' value as returned by
        get_all_mirrors.  For example: 'category-00000002'.  Required.

    :type displayname: str
    :param displayname: The category displayname 'category_name' value as returned by
        get_all_categories.  For example: 'Video Files'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_file_category_id(category)

    body_values = {'category': category, 'displayname': displayname}

    path = '/api/flc/rename_category.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_category(session, category, return_type=None, **kwargs):
    """
    Delete a file lifecycle category.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type category: str
    :param category: The category ID 'category-ext-name' value as returned by
        get_all_mirrors.  For example: 'category-00000002'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_file_category_id(category)

    path = '/api/flc/delete_category.json'

    return session.delete_api(path=path, return_type=return_type, **kwargs)
