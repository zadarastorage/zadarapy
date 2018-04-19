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


def get_all_tickets(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all support tickets associated with the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying tickets from.  Optional.

    :type: limit: int
    :param limit: The maximum number of tickets to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if start is not None:
        start = int(start)
        if start < 0:
            raise ValueError('Supplied start ("{0}") cannot be negative.'
                             .format(start))

    if limit is not None:
        limit = int(limit)
        if limit < 0:
            raise ValueError('Supplied limit ("{0}") cannot be negative.'
                             .format(limit))

    method = 'GET'
    path = '/api/tickets.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def create_ticket(session, subject, description, return_type=None):
    """
    Creates a support ticket for the VPSA.  This ticket will be assigned to a
    member of the support staff.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type subject: str
    :param subject: The subject for the ticket (analogous to an e-mail
        subject).  For example: 'Help With Expanding Pool'.  Required.

    :type description: str
    :param description: The full body of the ticket (analogous to an e-mail
        body).  For example: 'I would like more information on best practices
        for expanding my "pool1" storage pool.'  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if subject is None or description is None:
        raise ValueError('A ticket subject and description must be provided.')

    body_values = {'subject': subject, 'description': description}

    method = 'POST'
    path = '/api/tickets.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def close_ticket(session, ticket_id, return_type=None):
    """
    Closes a support ticket for the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ticket_id: int
    :param ticket_id: The support ticket 'id' value as returned by
        get_all_tickets.  For example: '28125'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if ticket_id < 1:
        raise ValueError('The ticket ID should be a positive integer ("{0}") '
                         'was passed.'.format(ticket_id))

    method = 'POST'
    path = '/api/tickets/{0}/close.json'.format(ticket_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_ticket_comments(session, ticket_id, return_type=None):
    """
    Gets all comments associated with the provided support ticket for the
    VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ticket_id: int
    :param ticket_id: The support ticket 'id' value as returned by
        get_all_tickets.  For example: '28125'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if ticket_id < 1:
        raise ValueError('The ticket ID should be a positive integer ("{0}" '
                         'was passed).'.format(ticket_id))

    method = 'GET'
    path = '/api/tickets/{0}/comments.json'.format(ticket_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_ticket_comment(session, ticket_id, comment, return_type=None):
    """
    Adds a comment to an existing support ticket for the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ticket_id: int
    :param ticket_id: The support ticket 'id' value as returned by
        get_all_tickets.  For example: '28125'.  Required.

    :type comment: str
    :param comment: The comment to add to the ticket.  The support staff will
        be notified of this comment when created.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if ticket_id < 1:
        raise ValueError('The ticket ID should be a positive integer ("{0}" '
                         'was passed).'.format(ticket_id))

    if comment is None:
        raise ValueError('A support ticket comment must be provided.')

    body_values = {'comment': comment}

    method = 'POST'
    path = '/api/tickets/{0}/comments.json'.format(ticket_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def create_ticket_zsnap(session, ticket_id, return_type=None):
    """
    Creates a diagnostic "zsnap" file for the VPSA and attaches it to the
    provided support ticket for the VPSA.  This "zsnap" assists support in
    locating any potential issues with the VPSA.  No volume data is included
    in any "zsnap".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type ticket_id: int
    :param ticket_id: The support ticket 'id' value as returned by
        get_all_tickets.  For example: '28125'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if ticket_id < 1:
        raise ValueError('The ticket ID should be a positive integer ("{0}" '
                         'was passed).'.format(ticket_id))

    method = 'POST'
    path = '/api/tickets/{0}/zsnap.json'.format(ticket_id)

    return session.call_api(method=method, path=path, return_type=return_type)
