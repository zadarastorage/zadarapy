#!/usr/bin/env python

from pprint import pprint

from zadarapy import session
from zadarapy.vpsa.raid_groups import get_all_raid_groups


def main():
    # Create a session that defines endpoint, connectivity method, etc.
    zadara_session = session.Session(host='localhost', key='XXX', port=8080,
                                     secure=False)

    print('List RAID groups - returns a Python dictionary')
    groups = get_all_raid_groups(session=zadara_session)
    pprint(groups)

    print('')
    print('Want JSON instead?')
    groups = get_all_raid_groups(session=zadara_session, return_type='json')

    print(groups)


if __name__ == '__main__':
    main()
