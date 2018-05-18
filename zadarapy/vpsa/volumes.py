# Copyright 2015 Zadara Storage, Inc.
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
from zadarapy.validators import *


def get_all_volumes(session, start=None, limit=None, showonlyblock='NO',
                    showonlyfile='NO', display_name=None, return_type=None):
    """
    Retrieves details for all volumes configured on the VPSA.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying volumes from.  Optional.

    :type: limit: int
    :param limit: The maximum number of volumes to return.  Optional.

    :type showonlyblock: str
    :param showonlyblock: If set to 'YES', only block volumes will be
        displayed.  If 'NO', it will show any volume.  Set to 'NO' by default.
        Optional.

    :type showonlyfile: str
    :param showonlyfile: If set to 'YES', only NAS volumes will be displayed.
        If 'NO', it will show any volume.  Set to 'NO' by default.  Optional.

    :type display_name: str
    :param display_name: The text label assigned to the volume to search for.
        For example: 'user-files', 'database', etc.  May not contain a single
        quote (') character.  If set to None type, it will show any volume.
        Optional.

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

    showonlyblock = showonlyblock.upper()

    if showonlyblock not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid showonlyblock parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(showonlyblock))

    showonlyfile = showonlyfile.upper()

    if showonlyfile not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid showonlyfile parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(showonlyfile))

    if display_name is not None:
        display_name = display_name.strip()

        if not is_valid_field(display_name):
            raise ValueError('{0} is not a valid volume name.'
                             .format(display_name))

    method = 'GET'
    path = '/api/volumes.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit),
                                    ('showonlyblock', showonlyblock),
                                    ('showonlyfile', showonlyfile),
                                    ('display_name', display_name))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_free_volumes(session, start=None, limit=None, return_type=None):
    """
    Retrieves details for all volumes that do not have any attached server
    records.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type start: int
    :param start: The offset to start displaying volumes from.  Optional.

    :type: limit: int
    :param limit: The maximum number of volumes to return.  Optional.

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
    path = '/api/volumes/free.json'

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def get_volume(session, volume_id, return_type=None):
    """
    Retrieves details for a single volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    method = 'GET'
    path = '/api/volumes/{0}.json'.format(volume_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_volume(session, pool_id, display_name, capacity, block,
                  attachpolicies='YES', crypt='NO', dedupe='NO',
                  compress='NO', export_name=None, atimeupdate='NO',
                  nfsrootsquash='NO', readaheadkb='512', smbonly='NO',
                  smbguest='NO', smbwindowsacl='NO', smbfilecreatemask='0744',
                  smbdircreatemask='0755', smbmaparchive='YES',
                  smbaiosize='NO', smbbrowseable='YES', smbhiddenfiles=None,
                  smbhideunreadable='NO', smbhideunwriteable='NO',
                  smbhidedotfiles='YES', smbstoredosattributes='NO',
                  smbenableoplocks='YES', return_type=None):
    """
    Creates a new volume.  The 'block' parameter determines if it should be a
    block (iSCSI, iSER, or Fiber Channel) volume or NAS file share (NFS and/or
    SMB/CIFS).

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type pool_id: str
    :param pool_id: The pool 'name' value as returned by get_all_pools.  For
        example: 'pool-00000001'.  The volume will be created on this pool.
        Required.

    :type display_name: str
    :param display_name: A text label to assign to the volume.  For example:
        'user-files', 'database', etc.  May not contain a single quote (')
        character.  Required.

    :type capacity: int
    :param capacity: The total capacity in GB for the volume.  Volumes are
        thinly provisioned by default, so this capacity may even exceed the
        underlying pool's capacity.  Required.

    :type block: str
    :param block: If set to 'YES', this will be a block (iSCSI, iSER) volume.
        If 'NO', it will be a NAS share/filesystem volume (NFS and/or
        SMB/CIFS).  Required.

    :type attachpolicies: str
    :param attachpolicies: If set to 'YES', the default snapshot policies for
        the VPSA will be attached to this volume.  If 'NO', they won't.  Set
        to 'YES' by default.  Optional.

    :type crypt: str
    :param crypt: If set to 'YES', the volume will be encrypted with the
        VPSA's encryption password, as defined by the storage administrator.
        If 'NO', it won't.  Optional.

    :type dedupe: str
    :param dedupe: If set to 'YES', deduplication will be enabled on the
        volume.  If 'NO', it won't.  Optional.

    :type compress: str
    :param compress: If set to 'YES', compression will be enabled on the
        volume.  If 'NO', it won't.  Optional.

    :type export_name: str
    :param export_name: For NAS shares, the export name will be the part of
        the last part of the path in the mount location.  For example, in
        10.10.1.67:/export/user-files - 'user-files' is the export name.  If
        not passed to this function, the export name will be set to the same
        value as 'display_name'.  Optional.

    :type atimeupdate: str
    :param atimeupdate: For NAS shares, if set to 'YES', the access time value
        for a file or directory will be updated every time a user accesses it.
        This incurs a performance penalty.  If 'NO', the atime parameter will
        be only updated occasionally.  Set to 'NO' by default.  Optional.

    :type nfsrootsquash: str
    :param nfsrootsquash: For NAS shares, when using NFS, if set to 'YES',
        root squash will be enabled for this volume, which disables the 'root'
        user's ability to mount the volume.  If set to 'NO', the 'root' user
        will be able to mount the volume.  Set to 'NO' by default.  Optional.

    :type readaheadkb: str
    :param readaheadkb: Sets the read ahead size in KB.  Read ahead will
        attempt to prefetch data ahead of the existing IO request in an
        attempt to improve throughput.  For most workloads, the default value
        of 512KB should be ok - though if IOs are expected to be small and
        random, a smaller value might help performance.  Allowed values are:
        16, 64, 128, 256, or 512.  Set to '512' by default.  Optional.

    :type smbonly: str
    :param smbonly: For NAS shares, if set to 'YES', this volume will be
        optimized for SMB/CIFS access only, and therefore will no longer be
        accessible by NFS clients.  If 'NO', both NFS and SMB/CIFS clients
        will be able to use this share.  Set to 'NO' by default.  Optional.

    :type smbguest: str
    :param smbguest: For NAS shares, when using SMB/CIFS, if set to 'YES',
        clients with valid server records attached to this volume will be able
        to access it via SMB/CIFS without providing a username and password.
        This is often useful for SMB/CIFS volumes that aren't integrated with
        an Active Directory domain.  If 'NO', a valid username and password as
        defined in the 'NAS Users' section will be required.  Set to 'NO' by
        default.  Optional.

    :type smbwindowsacl: str
    :param smbwindowsacl: For NAS shares, when using SMB/CIFS, if set to
        'YES', extended Windows ACLs will be used, which allows for Windows
        users and groups to be used for defining file and folder permissions.
        This is useful particularly for Active Directory integrated VPSAs.
        If 'NO', Windows ACLs won't be used.  Optional.

    :type smbfilecreatemask: str
    :param smbfilecreatemask: For NAS shares, when using SMB/CIFS, files will
        be created on the volume using this UNIX style mask.  For example,
        '0744' will make new files readable and writable by the user owner
        with the archive attribute set if 'smbmaparchive' is set to 'YES',
        readable by the group owner, and readable by all other users.  If
        'smbmaparchive' is set to yes, the mask should set the 'execute' bit
        on files to ensure the archive attribute is set properly.  Set to
        '0744' by default.  Optional.

    :type smbdircreatemask: str
    :param smbdircreatemask: For NAS shares, when using SMB/CIFS, folders will
        be created on the volume using this UNIX style mask.  For example,
        '0755' will make new folders readable, writable, and listable by the
        user owner, readable and listable by the user group, and readable and
        listable by all other users.  Set to '0755' by default.  Optional.

    :type smbmaparchive: str
    :param smbmaparchive: For NAS shares, when using SMB/CIFS, if set to
        'YES', files will have the 'Archive' attribute set when the file has
        UNIX executable permission.  This should be left on unless you know
        what you're doing.  If set to 'NO', the 'Archive' attribute won't be
        set for UNIX executable files.  Set to 'YES' by default.  Optional.

    :type smbaiosize: str
    :param smbaiosize: For NAS shares, when using SMB/CIFS, if set to 'YES',
        files larger than 16KB will be read asynchronously to improve
        performance.  This can help workloads that are small and serial in
        nature.  If set to 'NO', asynchronous reads are disabled.  Set to 'NO'
        by default.  Optional.

    :type smbbrowseable: str
    :param smbbrowseable: For NAS shares, when using SMB/CIFS, if set to
        'YES', the share will be visible when browsing the VPSA IP; i.e. at
        \\ip.of.vpsa.  If set to 'NO', the share will not be visible.  This
        is not an access control, regardless of visibility, the share is
        reachable if the user enters the full UNC of the share and has the
        needed permissions - this just shows or hides the share when browsing.
        Set to 'YES' by default.  Optional.

    :type smbhiddenfiles: str
    :param smbhiddenfiles: For NAS shares, when using SMB/CIFS, this is a
        forward slash delimited list of filenames and/or wildcards to be
        hidden from users by the VPSA.  For example, the string
        '/desktop.ini/$*/hidden*/' will hide all files named desktop.ini, or
        starting with the character '$', or starting with the string 'hidden'.
        If set to None, no custom hiding rules will be enforced.  This
        is not an access control, regardless of visibility, the files are
        reachable if the user enters the full UNC of the file and has the
        needed permissions - this just hides the file when browsing.
        Optional.

    :type smbhideunreadable: str
    :param smbhideunreadable: For NAS shares, when using SMB/CIFS, if set to
        'YES', any file or folder unreadable by the user due to permissions
        will also be hidden from the user while browsing the share.  If set to
        'NO', then unreadable files and folders  will be shown when browsing,
        but will still be unreadable.  Set to 'NO' by default.  Optional.

    :type smbhideunwriteable: str
    :param smbhideunwriteable: For NAS shares, when using SMB/CIFS, if set to
        'YES', any file or folder unwriteable by the user due to permissions
        will also be hidden from the user while browsing the share.  If set to
        'NO', then unwriteable files and folders will be shown when browsing,
        but will still be unwriteable.  Set to 'NO' by default.  Optional.

    :type smbhidedotfiles: str
    :param smbhidedotfiles: For NAS shares, when using SMB/CIFS, if set to
        'YES', files or folders that start with a period (.) will be hidden
        from the user while browsing the share.  If set to 'NO', then files or
        folders will be shown when browsing.  This is not an access control,
        regardless of visibility, the files are reachable if the user enters
        the full UNC of the file and has the needed permissions - this just
        hides the files or folders when browsing.  Set to 'YES' by default.
        Optional.

    :type smbstoredosattributes: str
    :param smbstoredosattributes: For NAS shares, when using SMB/CIFS, if set
        to 'YES', files or folders will keep any extended DOS attributes
        assigned to them from the client.  For example; "Hidden", "Archive",
        "Read-Only", and "System".  It will also preserve file and folder
        creation times from the client.  If set to 'NO', DOS attributes will
        not be preserved from the client.  Setting this to 'YES' may incur a
        performance penalty under heavy loads.  Set to 'NO' by default.
        Optional.

    :type smbenableoplocks: str
    :param smbenableoplocks: For NAS shares, when using SMB/CIFS, if set to
        'YES', the VPSA will maintain oplock information from clients; i.e.
        read only, write, exclusive write, etc.  If set to 'NO', the VPSA will
        not maintain oplock information, allowing any client to take any
        permissible operation.  Set to 'YES' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values['pool'] = pool_id

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid volume name.'
                         .format(display_name))

    body_values['name'] = display_name

    capacity = int(capacity)

    if capacity < 1:
        raise ValueError('Volume must be >= 1 GB ("{0}" was given).'
                         .format(capacity))

    body_values['capacity'] = '{0}G'.format(capacity)

    block = block.upper()

    if block not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid block parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(block))

    body_values['block'] = block

    attachpolicies = attachpolicies.upper()

    if attachpolicies not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid attachpolicies parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(attachpolicies))

    body_values['attachpolicies'] = attachpolicies

    crypt = crypt.upper()

    if crypt not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid crypt parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(crypt))

    body_values['crypt'] = crypt

    dedupe = dedupe.upper()

    if dedupe not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid dedupe parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(dedupe))

    body_values['dedupe'] = dedupe

    compress = compress.upper()

    if compress not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid compress parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(compress))

    body_values['compress'] = compress

    # If block is set to 'YES', enable thin provisioning by default.  This
    # only needs to be set for block volumes, as NAS shares will always be
    # thinly provisioned.  The else section contains parameters that are only
    # relevant for NAS shares.
    if block == 'YES':
        body_values['thin'] = 'YES'
    else:
        if export_name is not None:
            if not is_valid_field(export_name):
                raise ValueError('{0} is not a valid export name.'
                                 .format(export_name))

            body_values['export_name'] = export_name

        atimeupdate = atimeupdate.upper()

        if atimeupdate not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid atimeupdate parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(atimeupdate))

        body_values['atimeupdate'] = atimeupdate

        nfsrootsquash = nfsrootsquash.upper()

        if nfsrootsquash not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid nfsrootsquash parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(nfsrootsquash))

        body_values['nfsrootsquash'] = nfsrootsquash

        if readaheadkb not in ['16', '64', '128', '256', '512']:
            raise ValueError('"{0}" is not a valid readaheadkb parameter.  '
                             'Allowed values are: "16", "64", "128", "256", '
                             'or "512"'
                             .format(readaheadkb))

        body_values['readaheadkb'] = readaheadkb

        smbonly = smbonly.upper()

        if smbonly not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbonly parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbonly))

        body_values['smbonly'] = smbonly

        smbguest = smbguest.upper()

        if smbguest not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbguest parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbguest))

        body_values['smbguest'] = smbguest

        smbwindowsacl = smbwindowsacl.upper()

        if smbwindowsacl not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbwindowsacl parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbwindowsacl))

        body_values['smbwindowsacl'] = smbwindowsacl

        if not is_valid_mask(smbfilecreatemask):
            raise ValueError('smbfilecreatemask must be a valid octal UNIX '
                             'style permission mask ("{0}" was given).'
                             .format(smbfilecreatemask))

        body_values['smbfilecreatemask'] = smbfilecreatemask

        if not is_valid_mask(smbdircreatemask):
            raise ValueError('smbdircreatemask must be a valid octal UNIX '
                             'style permission mask ("{0}" was given).'
                             .format(smbdircreatemask))

        body_values['smbdircreatemask'] = smbdircreatemask

        smbmaparchive = smbmaparchive.upper()

        if smbmaparchive not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbmaparchive parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbmaparchive))

        body_values['smbmaparchive'] = smbmaparchive

        smbaiosize = smbaiosize.upper()

        if smbaiosize not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbaiosize parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbaiosize))

        # smbaiosize needs to convert 'YES' to '16384', and 'NO' to '1', per
        # what the API backend expects.
        if smbaiosize == 'YES':
            smbaiosize = '16384'
        else:
            smbaiosize = '1'

        body_values['smbaiosize'] = smbaiosize

        smbbrowseable = smbbrowseable.upper()

        if smbbrowseable not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbbrowseable parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbbrowseable))

        body_values['smbbrowseable'] = smbbrowseable

        if smbhiddenfiles is not None:
            if not is_valid_smb_hidden_files(smbhiddenfiles):
                raise ValueError(
                    '"{0}" is not a valid smbhiddenfiles parameter.  String '
                    'must start and end with a forward slash (/).'
                    .format(smbhiddenfiles))

            body_values['smbhiddenfiles'] = smbhiddenfiles

        smbhideunreadable = smbhideunreadable.upper()

        if smbhideunreadable not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbhideunreadable '
                             'parameter.  Allowed values are: "YES" or "NO"'
                             .format(smbbrowseable))

        body_values['smbhideunreadable'] = smbhideunreadable

        smbhideunwriteable = smbhideunwriteable.upper()

        if smbhideunwriteable not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbhideunwriteable '
                             'parameter.  Allowed values are: "YES" or "NO"'
                             .format(smbhideunwriteable))

        body_values['smbhideunwriteable'] = smbhideunwriteable

        smbhidedotfiles = smbhidedotfiles.upper()

        if smbhidedotfiles not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbhidedotfiles '
                             'parameter.  Allowed values are: "YES" or "NO"'
                             .format(smbhidedotfiles))

        body_values['smbhidedotfiles'] = smbhidedotfiles

        smbstoredosattributes = smbstoredosattributes.upper()

        if smbstoredosattributes not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbstoredosattributes '
                             'parameter.  Allowed values are: "YES" or "NO"'
                             .format(smbstoredosattributes))

        body_values['smbstoredosattributes'] = smbstoredosattributes

        smbenableoplocks = smbenableoplocks.upper()

        if smbenableoplocks not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbenableoplocks '
                             'parameter.  Allowed values are: "YES" or "NO"'
                             .format(smbenableoplocks))

        body_values['smbenableoplocks'] = smbenableoplocks

    method = 'POST'
    path = '/api/volumes.json'

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def update_volume_nas_options(session, volume_id, atimeupdate=None,
                              smbonly=None, smbguest=None, smbwindowsacl=None,
                              smbfilecreatemask=None,
                              smbdircreatemask=None, smbmaparchive=None,
                              smbaiosize=None, nfsrootsquash=None,
                              return_type=None):
    """
    Change various settings related to NAS shares.  Parameters set to 'None'
    will not have their existing values changed.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type atimeupdate: str
    :param atimeupdate: See documentation for create_volume.  Optional.

    :type smbonly: str
    :param smbonly: See documentation for create_volume.  Optional.

    :type smbguest: str
    :param smbguest: See documentation for create_volume.  Optional.

    :type smbwindowsacl: str
    :param smbwindowsacl: See documentation for create_volume.  Optional.

    :type smbfilecreatemask: str
    :param smbfilecreatemask: See documentation for create_volume.  Optional.

    :type smbdircreatemask: str
    :param smbdircreatemask: See documentation for create_volume.  Optional.

    :type smbmaparchive: str
    :param smbmaparchive: See documentation for create_volume.  Optional.

    :type smbaiosize: str
    :param smbaiosize: See documentation for create_volume.  Optional.

    :type nfsrootsquash: str
    :param nfsrootsquash: See documentation for create_volume.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values = {}

    if atimeupdate is not None:
        atimeupdate = atimeupdate.upper()

        if atimeupdate not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid atimeupdate parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(atimeupdate))

        body_values['atimeupdate'] = atimeupdate

    if smbonly is not None:
        smbonly = smbonly.upper()

        if smbonly not in ['YES', 'NO']:
                raise ValueError('"{0}" is not a valid smbonly parameter.  '
                                 'Allowed values are: "YES" or "NO"'
                                 .format(smbonly))

        body_values['smbonly'] = smbonly

    if smbguest is not None:
        smbguest = smbguest.upper()

        if smbguest not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbguest parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbguest))

        body_values['smbguest'] = smbguest

    if smbwindowsacl is not None:
        smbwindowsacl = smbwindowsacl.upper()

        if smbwindowsacl not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbwindowsacl parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbwindowsacl))

        body_values['smbwindowsacl'] = smbwindowsacl

    if smbfilecreatemask is not None:
        if not is_valid_mask(smbfilecreatemask):
            raise ValueError('smbfilecreatemask must be a valid octal UNIX '
                             'style permission mask ("{0}" was given).'
                             .format(smbfilecreatemask))

        body_values['smbfilecreatemask'] = smbfilecreatemask

    if smbdircreatemask is not None:
        if not is_valid_mask(smbdircreatemask):
            raise ValueError('smbdircreatemask must be a valid octal UNIX '
                             'style permission mask ("{0}" was given).'
                             .format(smbdircreatemask))

        body_values['smbdircreatemask'] = smbdircreatemask

    if smbmaparchive is not None:
        smbmaparchive = smbmaparchive.upper()

        if smbmaparchive not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbmaparchive parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbmaparchive))

        body_values['smbmaparchive'] = smbmaparchive

    if smbaiosize is not None:
        smbaiosize = smbaiosize.upper()

        if smbaiosize not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid smbaiosize parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(smbaiosize))

        # smbaiosize needs to convert 'YES' to '16384', and 'NO' to '1', per
        # what the API backend expects.
        if smbaiosize == 'YES':
            smbaiosize = '16384'
        else:
            smbaiosize = '1'

        body_values['smbaiosize'] = smbaiosize

    if nfsrootsquash is not None:
        nfsrootsquash = nfsrootsquash.upper()

        if nfsrootsquash not in ['YES', 'NO']:
            raise ValueError('"{0}" is not a valid nfsrootsquash parameter.  '
                             'Allowed values are: "YES" or "NO"'
                             .format(nfsrootsquash))

        body_values['nfsrootsquash'] = nfsrootsquash

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"atimeupdate", "smbonly", "smbguest", '
                         '"smbwindowsacl", "smbfilecreatemask", '
                         '"smbdircreatemask", "smbmaparchive", "smbaiosize", '
                         '"nfsrootsquash"')

    method = 'PUT'
    path = '/api/volumes/{0}.json'.format(volume_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_volume(session, volume_id, force='NO', return_type=None):
    """
    Deletes a volume.  If the recycle bin is enabled, volume will be moved to
    the pool's recycle bin, where it can either be recovered, or it will be
    automatically removed after seven days.  If recycle bin is disabled, the
    volume will be immediately deleted.  Volume purge/deletion is
    irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSA to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values = {}

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    body = json.dumps(body_values)

    method = 'DELETE'
    path = '/api/volumes/{0}.json'.format(volume_id)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def rename_volume(session, volume_id, display_name, return_type=None):
    """
    Sets the "display_name" volume parameter to a new value.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type display_name: str
    :param display_name: The new "display_name" to set.  May not contain a
        single quote (') character.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid volume name.'
                         .format(display_name))

    body_values['new_name'] = display_name

    method = 'POST'
    path = '/api/volumes/{0}/rename.json'.format(volume_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def expand_volume(session, volume_id, capacity, return_type=None):
    """
    Expands the volume by the capacity parameter.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type capacity: int
    :param capacity: The capacity in GB by which to expand the volume.
        Volumes are thinly provisioned by default, so this capacity may even
        exceed the underlying pool's capacity.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values = {}

    capacity = int(capacity)

    if capacity < 1:
        raise ValueError('Volume must be expanded by >= 1 GB ("{0}" was'
                         'given).'.format(capacity))

    body_values['capacity'] = '{0}G'.format(capacity)

    method = 'POST'
    path = '/api/volumes/{0}/expand.json'.format(volume_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_servers_attached_to_volume(session, volume_id, start=None, limit=None,
                                   return_type=None):
    """
    Retrieves details for all server records attached to the specified volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type start: int
    :param start: The offset to start displaying servers from.  Optional.

    :type: limit: int
    :param limit: The maximum number of servers to return.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

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
    path = '/api/volumes/{0}/servers.json'.format(volume_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def detach_servers_from_volume(session, volume_id, servers, force='NO',
                               return_type=None):
    """
    Detach one or more server records from a volume.  Caution: detaching a
    server record from a volume while an affected server is using the volume
    will result in errors.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type servers: str
    :param servers: A comma separated string of servers with no spaces
        around the commas.  The value must match server's 'name'
        attribute.  For example: 'srv-00000001,srv-00000002'.  Required.

    :type force: str
    :param force: If set to 'YES', ignore non-critical warnings and force the
        VPSA to accept the request.  If 'NO', return message on warning and
        abort.  Set to 'NO' by default.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values = {}

    for server in servers.split(','):
        if not is_valid_server_id(server):
            raise ValueError('"{0}" in "{1}" is not a valid server ID.'
                             .format(server, servers))

    body_values['servers'] = servers

    force = force.upper()

    if force not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid force parameter.  Allowed '
                         'values are: "YES" or "NO"'.format(force))

    body_values['force'] = force

    method = 'POST'
    path = '/api/volumes/{0}/detach.json'.format(volume_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def set_volume_export_name(session, volume_id, export_name, return_type=None):
    """
    Changes the export name at the end of the network path for NAS shares.
    Volume must not have any attached server records.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type export_name: str
    :param export_name: See documentation for create_volume.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    body_values = {}

    if not is_valid_field(export_name):
        raise ValueError('{0} is not a valid export name.'
                         .format(export_name))

    body_values['exportname'] = export_name

    method = 'PUT'
    path = '/api/volumes/{0}/export_name.json'.format(volume_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_volume_attached_snapshot_policies(session, cg_id, start=None,
                                          limit=None, return_type=None):
    """
    Retrieves details for all snapshot policies attached to this volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Required.

    :type start: int
    :param start: The offset to start displaying snapshot policies from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of snapshot policies to return.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

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
    path = '/api/consistency_groups/{0}/snapshot_policies.json'\
           .format(cg_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def add_volume_snapshot_policy(session, cg_id, policy_id, return_type=None):
    """
    Attaches a snapshot policy to the volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Required.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter. Upon success, the dictionary will contain an
        entry like 'response':{'snapshot_rule_name': 'rule-00000003'...},
        which identifies the snapshot rule that has been created by adding the
        snapshot policy to the volume.
    """
    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

    body_values = {}

    if not is_valid_policy_id(policy_id):
        raise ValueError('{0} is not a valid snapshot policy ID.'
                         .format(policy_id))

    body_values['policy'] = policy_id

    method = 'POST'
    path = '/api/consistency_groups/{0}/attach_policy.json'.format(cg_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def remove_volume_snapshot_policy(session, snapshot_rule_name,
                                  delete_snapshots, return_type=None):
    """
    Removes a snapshot policy from a volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type snapshot_rule_name: str
    :param snapshot_rule_name: The name of the snapshot rule, as returned by
        the 'add_volume_snapshot_policy' API. For example: 'rule-00000003'.
        Required.

    :type delete_snapshots: str
    :param delete_snapshots: If set to 'YES', all snapshots created by the
        specified policy will be deleted.  If 'NO', they won't.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_snapshot_rule_name(snapshot_rule_name):
        raise ValueError('{0} is not a valid snapshot rule name.'
                         .format(snapshot_rule_name))

    body_values = {}

    delete_snapshots = delete_snapshots.upper()

    if delete_snapshots not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid delete_snapshots parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(delete_snapshots))

    body_values['delete_snapshots'] = delete_snapshots

    method = 'POST'
    path = '/api/consistency_groups/{0}/detach_policy.json'\
        .format(snapshot_rule_name)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_all_snapshots(session, cg_id, ros_backup_job_id=None, start=None,
                      limit=None, return_type=None):
    """
    Retrieves details for all snapshots either for a local volume or remote
    object storage backup job.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume; or get_all_ros_backup_jobs for
        the desired remote object storage backup job.  For example:
        'cg-00000001'.  Required.

    :type ros_backup_job_id: str
    :param ros_backup_job_id: If retrieving snapshots for a remote object
        storage backup job, the remote object storage backup job 'name'
        value as returned by get_all_ros_backup_jobs.  For example:
        'bkpjobs-00000001'.  Optional.

    :type start: int
    :param start: The offset to start displaying snapshots from.
        Optional.

    :type: limit: int
    :param limit: The maximum number of snapshots to return.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

    application = None

    if ros_backup_job_id is not None:
        if not is_valid_ros_backup_job_id(ros_backup_job_id):
            raise ValueError('{0} is not a valid remote object storage '
                             'backup job ID.'.format(ros_backup_job_id))

        application = 'obs_mirror'

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
    path = '/api/consistency_groups/{0}/snapshots.json'.format(cg_id)

    parameters = {k: v for k, v in (('start', start), ('limit', limit),
                                    ('jobname', ros_backup_job_id),
                                    ('application', application))
                  if v is not None}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)


def create_volume_snapshot(session, cg_id, display_name, return_type=None):
    """
    Creates a new snapshot for the specified volume.  Manually initiated
    snapshots will fall under the "On Demand" snapshot policy.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Required.

    :type display_name: str
    :param display_name: A text label to assign to the snapshot.  For example:
        'pre-upgrade-snapshot'.  May not contain a single quote (') character.
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

    body_values = {}

    display_name = display_name.strip()

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid snapshot name.'
                         .format(display_name))

    body_values['display_name'] = display_name

    method = 'POST'
    path = '/api/consistency_groups/{0}/snapshots.json'.format(cg_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def delete_volume_snapshot(session, snapshot_id, return_type=None):
    """
    Deletes a volume's snapshot.  This action is irreversible.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type snapshot_id: str
    :param snapshot_id: The snapshot 'name' value as returned by
        get_all_volume_snapshots for the desired volume.  For example:
        'snap-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_snapshot_id(snapshot_id):
        raise ValueError('{0} is not a valid snapshot ID.'
                         .format(snapshot_id))

    method = 'DELETE'
    path = '/api/snapshots/{0}.json'.format(snapshot_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def get_volume_migration(session, mgrjob_id, return_type=None):
    """
    Retrieves details for a running volume migration job.  The job is queried
    using the consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes.  To check if a volume is currently migrating, check if
    the value for the volume's "status" parameter is set to "Migrating".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mgrjob_id: str
    :param mgrjob_id: The migration job 'migration_job_name' value as returned
        by get_all_volumes for the desired volume.  For example:
        'mgrjob-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mgrjob_id(mgrjob_id):
        raise ValueError('{0} is not a valid migration job ID.'
                         .format(mgrjob_id))

    method = 'GET'
    path = '/api/consistency_groups/{0}/show_migration.json'.format(mgrjob_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def migrate_volume(session, cg_id, pool_id, migrate_snaps='YES',
                   return_type=None):
    """
    Starts migrating a volume to a different storage pool.  The job is created
    using the consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Required.

    :type pool_id: str
    :param pool_id: The destination pool 'name' value as returned by
        get_all_pools.  For example: 'pool-00000001'.  Required.

    :type migrate_snaps: str
    :param migrate_snaps: If set to 'YES', all snapshots for this volume will
        be migrated.  If 'NO', they won't.  Set to 'YES' by default.
        Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

    body_values = {}

    if not is_valid_pool_id(pool_id):
        raise ValueError('{0} is not a valid pool ID.'.format(pool_id))

    body_values['poolname'] = pool_id

    migrate_snaps = migrate_snaps.upper()

    if migrate_snaps not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid migrate_snaps parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(migrate_snaps))

    body_values['migratesnaps'] = migrate_snaps

    method = 'POST'
    path = '/api/consistency_groups/{0}/migrate.json'.format(cg_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def pause_volume_migration(session, mgrjob_id, return_type=None):
    """
    Pause a running volume migration job.  The job is paused using the
    consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mgrjob_id: str
    :param mgrjob_id: The migration job 'migration_job_name' value as returned
        by get_all_volumes for the desired volume.  For example:
        'mgrjob-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mgrjob_id(mgrjob_id):
        raise ValueError('{0} is not a valid migration job ID.'
                         .format(mgrjob_id))

    method = 'POST'
    path = '/api/migration_jobs/{0}/pause.json'.format(mgrjob_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def resume_volume_migration(session, mgrjob_id, return_type=None):
    """
    Resume a paused volume migration job.  The job is resumed using the
    consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mgrjob_id: str
    :param mgrjob_id: The migration job 'migration_job_name' value as returned
        by get_all_volumes for the desired volume.  For example:
        'mgrjob-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mgrjob_id(mgrjob_id):
        raise ValueError('{0} is not a valid migration job ID.'
                         .format(mgrjob_id))

    method = 'POST'
    path = '/api/migration_jobs/{0}/continue.json'.format(mgrjob_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def cancel_volume_migration(session, mgrjob_id, return_type=None):
    """
    Cancel a volume migration job.  The job is canceled using the consistency
    group ID (cg_name) for the volume, as returned by get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type mgrjob_id: str
    :param mgrjob_id: The migration job 'migration_job_name' value as returned
        by get_all_volumes for the desired volume.  For example:
        'mgrjob-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_mgrjob_id(mgrjob_id):
        raise ValueError('{0} is not a valid migration job ID.'
                         .format(mgrjob_id))

    method = 'POST'
    path = '/api/migration_jobs/{0}/abort.json'.format(mgrjob_id)

    return session.call_api(method=method, path=path, return_type=return_type)


def create_clone(session, cg_id, display_name, snapshot_id=None,
                 return_type=None):
    """
    Create a clone from a volume or a snapshot.  If a valid snapshot id is
    passed, the clone will present the data at the time the snapshot was
    taken.  If not, the clone will have the contents of the volume at the time
    the clone was initiated.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Required.

    :type display_name: str
    :param display_name: A text label to assign to the clone.  For example:
        'database-20151101'.  May not contain a single quote (') character.
        Required.

    :type snapshot_id: str
    :param snapshot_id: The snapshot 'name' value as returned by
        get_all_volume_snapshots for the desired volume.  For example:
        'snap-00000001'.  If no snapshot is specified, the clone will have the
        contents of the volume at the time the clone was initiated.  Optional.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    body_values = {}

    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid clone name.'
                         .format(display_name))

    body_values['name'] = display_name

    if snapshot_id is not None:
        if not is_valid_snapshot_id(snapshot_id):
            raise ValueError('{0} is not a valid snapshot ID.'
                             .format(snapshot_id))

        body_values['snapshot'] = snapshot_id

    method = 'POST'
    path = '/api/consistency_groups/{0}/clone.json'.format(cg_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def create_volume_mirror(session, cg_id, display_name, remote_pool_id,
                         policies, remote_volume_name, wan_optimization='YES',
                         return_type=None):
    """
    Create a mirror job for a volume.  A volume can be mirrored to another
    pool on the same VPSA, or to another VPSA with which a "Remote VPSA"
    relationship has been established.  Mirroring is asynchronous and based on
    the specified snapshot policies.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Required.

    :type display_name: str
    :param display_name: A text label to assign to the mirror job.  For
        example: 'Daily Mirror to West Region'.  May not contain a single
        quote (') character.  Required.

    :type remote_pool_id: str
    :param remote_pool_id: The pool to which the volume will be mirrored.
        This can be a different pool on the same VPSA (the pool 'name' value
        as returned by get_all_pools - example: 'pool-00000001'), or to a pool
        on a remote VPSA (the remote pool 'name' value as returned by
        get_all_remote_vpsa_pools - example: 'rpool-00000001').  Required.

    :type policies: str
    :param policies: A comma separated string of snapshot policies with no
        spaces around the commas.  These snapshot policies will be used to
        determine the frequency of the volume mirror.  The value must match
        policy's 'name' attribute.  For example:
        'policy-00000001,policy-00000002'.  Required.

    :type remote_volume_name: str
    :param remote_volume_name: A text label to assign to the remote volume
        that is generated by the mirror job.  This name must not already be
        taken by another volume or another mirrored volume on the remote VPSA.
        May not contain a single quote (') character.  Required.

    :type wan_optimization: str
    :param wan_optimization: If set to 'YES', the mirror will attempt to
        reduce the amount of data needing to be synchronized to the remote
        side at the expense of more load on the source VPSA.  If set to 'NO',
        more data will be sent by the mirror with less load on the source
        VPSA.  Set to 'YES' by default.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_cg_id(cg_id):
        raise ValueError('{0} is not a valid consistency group ID.'
                         .format(cg_id))

    body_values = {}

    if not is_valid_field(display_name):
        raise ValueError('{0} is not a valid remote mirror name.'
                         .format(display_name))

    body_values['display_name'] = display_name

    if not is_valid_pool_id(remote_pool_id, remote_pool_allowed=True):
        raise ValueError('{0} is not a valid remote pool ID.'
                         .format(remote_pool_id))

    body_values['remote_pool'] = remote_pool_id

    for policy in policies.split(','):
        if not is_valid_policy_id(policy):
            raise ValueError('"{0}" in "{1}" is not a valid snapshot policy '
                             'ID.'.format(policy, policies))

    body_values['policy'] = policies

    if not is_valid_field(remote_volume_name):
        raise ValueError('{0} is not a valid remote volume name.'
                         .format(remote_volume_name))

    body_values['new_cg_name'] = remote_volume_name

    wan_optimization = wan_optimization.upper()

    if wan_optimization not in ['YES', 'NO']:
        raise ValueError('"{0}" is not a valid wan_optimization parameter.  '
                         'Allowed values are: "YES" or "NO"'
                         .format(wan_optimization))

    body_values['wan_optimization'] = wan_optimization

    method = 'POST'
    path = '/api/consistency_groups/{0}/mirror.json'.format(cg_id)

    body = json.dumps(body_values)

    return session.call_api(method=method, path=path, body=body,
                            return_type=return_type)


def get_volume_performance(session, volume_id, interval=1, return_type=None):
    """
    Retrieves metering statistics for the volume for the specified interval.
    Default interval is one second.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type interval: int
    :param interval: The interval to collect statistics for, in seconds.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    if not is_valid_volume_id(volume_id):
        raise ValueError('{0} is not a valid volume ID.'.format(volume_id))

    interval = int(interval)

    if interval < 1:
        raise ValueError('Interval must be at least 1 second ({0} was'
                         'supplied).'.format(interval))

    method = 'GET'
    path = '/api/volumes/{0}/performance.json'.format(volume_id)

    parameters = {'interval': interval}

    return session.call_api(method=method, path=path, parameters=parameters,
                            return_type=return_type)
