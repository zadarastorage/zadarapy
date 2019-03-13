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
from zadarapy.validators import verify_account_id


def get_all_accounts(session, return_type=None):
    path = "/api/zios/accounts.json"
    return session.get_api(path=path, return_type=return_type)


def get_account(session, account_id, return_type=None):
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}.json".format(account_id)
    return session.get_api(path=path, return_type=return_type)


def add_new_account(session, name, return_type=None):
    path = "/api/zios/accounts.json"
    body_values = {'name': name}
    return session.post_api(path=path, body=body_values, return_type=return_type)


def delete_account(session, account_id, force="NO", return_type=None):
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}.json".format(account_id)
    body_values = {'force': force}
    return session.delete_api(path=path, body=body_values, return_type=return_type)


def cleanup_account(session, account_id, return_type=None):
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}/cleanup.json".format(account_id)
    return session.delete_api(path=path, return_type=return_type)


def disable_account(session, account_id, return_type=None):
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}/disable.json".format(account_id)
    return session.post_api(path=path, return_type=return_type)


def enable_account(session, account_id, return_type=None):
    verify_account_id(account_id=account_id)
    path = "/api/zios/accounts/{0}/enable.json".format(account_id)
    return session.post_api(path=path, return_type=return_type)
