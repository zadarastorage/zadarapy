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

from zadarapy.validators import verify_start_limit


def get_user(session, user_id, return_type=None):
    path = "/api/zios/users/{0}.json".format(user_id)
    return session.get_api(path=path, return_type=return_type)


def get_all_users(session, account_id, start=None, limit=None,
                  return_type=None):
    path = "/api/zios/accounts/{0}/users.json".format(account_id)
    parameters = verify_start_limit(start, limit)
    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type)


def add_new_user(session, account_id, username, email, role,
                 notify_on_events="NO", return_type=None):
    path = "/api/zios/users.json"
    body_values = {'account_id': account_id, 'username': username,
                   'email': email, 'role': role,
                   'notify_on_events': notify_on_events}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def delete_user(session, user_id, return_type=None):
    path = "/api/zios/users/{0}.json".format(user_id)
    return session.delete_api(path=path, return_type=return_type)


def get_auth_token(session, account_id, user, password, return_type=None):
    path = "/api/users/authenticate.json"
    body_values = {'account': account_id, 'user': user, 'password': password}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def disable_user(session, user_id, return_type=None):
    path = "/api/zios/users/{0}/disable.json".format(user_id)
    return session.post_api(path=path, return_type=return_type)


def enable_user(session, user_id, return_type=None):
    path = "/api/zios/users/{0}/enable.json".format(user_id)
    return session.post_api(path=path, return_type=return_type)


def disable_admin_access(session, return_type=None):
    path = "/api/users/admin_access/disable.json"
    return session.post_api(path=path, return_type=return_type)


def reset_token(session, account_id, user, password, return_type=None):
    path = "/api/users/reset_token.json"
    body_values = {'account': account_id, 'user': user, 'password': password}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def change_password(session, account_id, user, password, new_password,
                    return_type=None):
    path = "/api/users/password.json"
    body_values = {'account': account_id, 'user': user, 'password': password,
                   'new_password': new_password}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def reset_password(session, account_id, username, return_type=None):
    path = '/api/zios/users/reset_password.json'
    body_values = {'account': account_id, 'username': username}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def reset_using_temporary_password(session, code, new_password, username,
                                   account, return_type=None):
    path = '/api/users/{0}/password_code'.format(username)
    body_values = {'code': code, 'new_password': new_password,
                   'account': account}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)


def change_user_role(session, user_id, role, return_type=None):
    path = '/api/zios/users/{0}/change_rol.json'.format(user_id)
    body_values = {'role': role}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type)
