# Copyright 2020 Zadara Storage, Inc.
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


def clean_file_contents(session, file_path, return_type=None, **kwargs):
    """
    Clean file content (delete it's content)

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type file_path: str
    :param file_path: Path to file which we need to clean.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/clean_file_content'
    body = {"file_path": file_path}
    return session.post_api(path=path, body=body, secure=False, return_type=return_type, **kwargs)


def mkdir(session, folder_path, return_type=None, **kwargs):
    """
    Equivalent to 'mkdir -p' in Linux

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type folder_path: str
    :param folder_path: Path to file which we need to clean.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/mkdir'
    body = {"folder_path": folder_path}
    return session.post_api(path=path, body=body, secure=False, return_type=return_type, **kwargs)


def read_file(session, file_path, return_type=None, **kwargs):
    """
    Return file content

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type file_path: str
    :param file_path: Path to file which we need to clean.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/read_file'
    body = {"file_path": file_path}
    return session.get_api(path=path, body=body, return_type=return_type, **kwargs)


def is_file_exist(session, file_path, return_type=None, **kwargs):
    """
    Check if a file exist

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type file_path: str
    :param file_path: Path to file which we need to clean.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/is_file_exist'
    body = {"file_path": file_path}
    return session.get_api(path=path, body=body, secure=False, return_type=return_type, **kwargs)


def search_in_file(session, search_string, file_path, return_type=None, **kwargs):
    """
    Equivilant to 'grep' - Searches for a string in a file

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type search_string: str
    :param search_string: Path to file which we need to clean.  Required.

    :type file_path: str
    :param file_path: Path to file which we need to clean.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/search_in_file'
    body = {"search_string": search_string, "file_path": file_path}
    return session.get_api(path=path, body=body, secure=False, return_type=return_type, **kwargs)


def tail_lines(session, file_path, lines_number, return_type=None, **kwargs):
    """
    Clean file content (delete it's content)

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type file_path: str
    :param file_path: Path to file which we need to clean.  Required.

    :type lines_number: str
    :param lines_number: Number of lines to tail.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    path = '/api/tail_lines'
    body = {"file_path": file_path, "lines_number": lines_number}
    return session.get_api(path=path, body=body, secure=False, return_type=return_type, **kwargs)
