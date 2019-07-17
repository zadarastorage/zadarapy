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


def get_account_requests(session, state=None, limit=None, page=None,
                         return_type=None):
    path = "/api/requests.json"

    body_values = {'state': state}
    if limit:
        body_values['limit'] = limit
    if page:
        body_values['page'] = page

    return session.get_api(path=path, body=body_values,
                           return_type=return_type)


def approve_request(session, request_id, return_type=None):
    path = "/api/requests/{0}/approve.json".format(request_id)
    return session.post_api(path=path, return_type=return_type)


def deny_request(session, request_id, return_type=None):
    path = "/api/requests/{0}/deny.json".format(request_id)
    return session.post_api(path=path, return_type=return_type)
