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


from zadarapy.validators import verify_snapshot_id, verify_boolean, \
    verify_field, verify_start_limit, verify_cg_id, verify_policy_id, \
    verify_ros_backup_job_id, verify_readahead, verify_netmask, \
    verify_volume_id, verify_volume_av_parameters, verify_pool_id, \
    verify_capacity, verify_server_id, verify_snapshot_rule_name, \
    verify_interval, verify_snaprule_id, verify_volume_type, \
    verify_nas_type, verify_bool, verify_on_off, verify_project_id, \
    verify_group_project_polarity, verify_bool_parameter


def get_all_volumes(session, start=None, limit=None, showonlyblock='NO',
                    showonlyfile='NO', display_name=None, return_type=None,
                    **kwargs):
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
    showonlyblock = verify_boolean(showonlyblock, "showonlyblock")
    showonlyfile = verify_boolean(showonlyfile, "showonlyfile")
    display_name = verify_field(display_name, "display_name")

    parameters = verify_start_limit(start=start, limit=limit,
                                    list_options=[
                                        ('showonlyblock', showonlyblock),
                                        ('showonlyfile', showonlyfile),
                                        ('display_name', display_name)])
    path = '/api/volumes.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_free_volumes(session, start=None, limit=None, return_type=None,
                     **kwargs):
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
    parameters = verify_start_limit(start, limit)

    path = '/api/volumes/free.json'

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_volume(session, volume_id, return_type=None, **kwargs):
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
    verify_volume_id(volume_id)

    path = '/api/volumes/{0}.json'.format(volume_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_volume(session, pool_id, display_name, capacity, block,
                  attachpolicies='YES', crypt='NO', dedupe='NO',
                  compress='NO', export_name=None, atimeupdate='NO',
                  nfsrootsquash='NO', readaheadkb='512', smbonly='NO',
                  smbguest='NO', smbwindowsacl='NO', smbfilecreatemask='0744',
                  smbdircreatemask='0755', smbmaparchive='YES',
                  smbaiosize='NO', smbbrowseable='YES', smbhiddenfiles=None,
                  smbhideunreadable='NO', smbhideunwriteable='NO',
                  smbhidedotfiles='YES', smbstoredosattributes='NO',
                  smbenableoplocks='YES', auto_expand=None, max_expand=None,
                  auto_expand_by=None, return_type=None, **kwargs):
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
    verify_pool_id(pool_id)
    display_name = verify_field(display_name, "display_name")
    capacity = verify_capacity(capacity, "Volume")
    block = verify_boolean(block, "block")
    attachpolicies = verify_boolean(attachpolicies, "attachpolicies")
    crypt = verify_boolean(crypt, "crypt")
    dedupe = verify_boolean(dedupe, "dedupe")
    compress = verify_boolean(compress, "compress")

    body_values = {'pool': pool_id, 'name': display_name,
                   'capacity': '{0}G'.format(capacity), 'block': block,
                   'attachpolicies': attachpolicies, 'crypt': crypt,
                   'dedupe': dedupe, 'compress': compress}

    # If block is set to 'YES', enable thin provisioning by default.  This
    # only needs to be set for block volumes, as NAS shares will always be
    # thinly provisioned.  The else section contains parameters that are only
    # relevant for NAS shares.
    if block == 'YES':
        body_values['thin'] = 'YES'
    else:
        if export_name is not None:
            body_values['export_name'] = verify_field(export_name,
                                                      "export_name")

        body_values['atimeupdate'] = verify_boolean(atimeupdate, "atimeupdate")
        body_values['nfsrootsquash'] = verify_boolean(nfsrootsquash,
                                                      "nfsrootsquash")
        body_values['readaheadkb'] = verify_readahead(readaheadkb)
        body_values['smbonly'] = verify_boolean(smbonly, "smbonly")
        body_values['smbguest'] = verify_boolean(smbguest, "smbguest")
        body_values['smbwindowsacl'] = verify_boolean(smbwindowsacl,
                                                      "smbwindowsacl")
        body_values['smbfilecreatemask'] = verify_netmask(smbfilecreatemask,
                                                          "smbfilecreatemask")
        body_values['smbdircreatemask'] = verify_netmask(smbdircreatemask,
                                                         "smbdircreatemask")
        body_values['smbmaparchive'] = verify_boolean(smbmaparchive,
                                                      "smbmaparchive")
        body_values['smbbrowseable'] = verify_boolean(smbbrowseable,
                                                      "smbbrowseable")
        body_values['smbhideunreadable'] = \
            verify_boolean(smbhideunreadable, "smbhideunreadable")
        body_values['smbhideunwriteable'] = \
            verify_boolean(smbhideunwriteable, "smbhideunwriteable")
        body_values['smbhidedotfiles'] = verify_boolean(smbhidedotfiles,
                                                        "smbhidedotfiles")
        body_values['smbstoredosattributes'] = verify_boolean(
            smbstoredosattributes,
            "smbstoredosattributes")
        body_values['smbenableoplocks'] = verify_boolean(smbenableoplocks,
                                                         "smbenableoplocks")

        smbaiosize = verify_boolean(smbaiosize, "smbaiosize")
        body_values['smbaiosize'] = '16384' if smbaiosize == 'YES' else '1'

    if auto_expand is not None:
        body_values['autoexpand'] = verify_boolean(auto_expand, "auto_expand")
    if max_expand is not None:
        body_values['maxexpand'] = max_expand
    if auto_expand_by is not None:
        body_values['autoexpandby'] = auto_expand_by
    if smbhiddenfiles is not None:
        body_values['smbhiddenfiles'] = smbhiddenfiles

    path = '/api/volumes.json'

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_volume_nas_options(session, volume_id, atimeupdate=None,
                              smbonly=None, smbguest=None, smbwindowsacl=None,
                              smbfilecreatemask=None,
                              smbdircreatemask=None, smbmaparchive=None,
                              smbaiosize=None, nfsrootsquash=None,
                              return_type=None, **kwargs):
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
    verify_volume_id(volume_id)
    body_values = {}

    if smbmaparchive is not None:
        body_values['smbmaparchive'] = verify_boolean(smbmaparchive,
                                                      "smbmaparchive")

    if atimeupdate is not None:
        body_values['atimeupdate'] = verify_boolean(atimeupdate, "atimeupdate")

    if smbonly is not None:
        body_values['smbonly'] = verify_boolean(smbonly, "smbonly")

    if smbguest is not None:
        body_values['smbguest'] = verify_boolean(smbguest, "smbguest")

    if smbwindowsacl is not None:
        body_values['smbwindowsacl'] = verify_boolean(smbwindowsacl,
                                                      "smbwindowsacl")

    if smbfilecreatemask is not None:
        body_values['smbfilecreatemask'] = verify_netmask(smbfilecreatemask,
                                                          "smbfilecreatemask")

    if smbdircreatemask is not None:
        body_values['smbdircreatemask'] = verify_netmask(smbdircreatemask,
                                                         "smbdircreatemask")

    smbaiosize = verify_boolean(smbaiosize, "smbaiosize")
    body_values['smbaiosize'] = '16384' if smbaiosize == 'YES' else '1'

    if nfsrootsquash is not None:
        body_values['nfsrootsquash'] = verify_boolean(nfsrootsquash,
                                                      "nfsrootsquash")

    if not body_values:
        raise ValueError('At least one of the following must be set: '
                         '"atimeupdate", "smbonly", "smbguest", '
                         '"smbwindowsacl", "smbfilecreatemask", '
                         '"smbdircreatemask", "smbmaparchive", "smbaiosize", '
                         '"nfsrootsquash"')

    path = '/api/volumes/{0}.json'.format(volume_id)

    return session.put_api(path=path, body=body_values,
                           return_type=return_type, **kwargs)


def update_volume_comment(session, volume_id, comment, return_type=None,
                          **kwargs):
    """
    Set a new comment on the volume.  Comments can be set on either block or
    file volumes.  There is one comment per volume, and it starts empty by
    default when a new volume is created.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type comment: str
    :param comment: The new comment to set.  For example: "test share".
        Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)

    body_values = {"new_comment": comment}

    path = '/api/volumes/{0}/update_comment.json'.format(volume_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_volume(session, volume_id, force='NO', return_type=None, **kwargs):
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
    verify_volume_id(volume_id)
    force = verify_boolean(force, "force")

    body_values = {'force': force}

    path = '/api/volumes/{0}.json'.format(volume_id)

    return session.delete_api(path=path, body=body_values,
                              return_type=return_type, **kwargs)


def rename_volume(session, volume_id, display_name, return_type=None,
                  **kwargs):
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
    verify_volume_id(volume_id)
    display_name = verify_field(display_name, "display_name")

    body_values = {'new_name': display_name}

    path = '/api/volumes/{0}/rename.json'.format(volume_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def expand_volume(session, volume_id, capacity, return_type=None, **kwargs):
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
    verify_volume_id(volume_id)
    capacity = verify_capacity(capacity, "Volume")

    body_values = {'capacity': '{0}G'.format(capacity)}

    path = '/api/volumes/{0}/expand.json'.format(volume_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_servers_attached_to_volume(session, volume_id, start=None, limit=None,
                                   return_type=None, **kwargs):
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
    verify_volume_id(volume_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/volumes/{0}/servers.json'.format(volume_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def detach_servers_from_volume(session, volume_id, servers, force='NO',
                               return_type=None, **kwargs):
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
    verify_volume_id(volume_id)
    verify_server_id(servers)
    force = verify_boolean(force, "force")

    body_values = {'servers': servers, 'force': force}

    path = '/api/volumes/{0}/detach.json'.format(volume_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def set_volume_export_name(session, volume_id, export_name, return_type=None,
                           **kwargs):
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
    verify_volume_id(volume_id)
    export_name = verify_field(export_name, "export_name")

    body_values = {'exportname': export_name}

    path = '/api/volumes/{0}/export_name.json'.format(volume_id)

    return session.put_api(path=path, body=body_values,
                           return_type=return_type, **kwargs)


def get_volume_attached_snapshot_policies(session, cg_id, start=None,
                                          limit=None, return_type=None,
                                          **kwargs):
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
    verify_cg_id(cg_id)
    parameters = verify_start_limit(start, limit)

    path = '/api/consistency_groups/{0}/snapshot_policies.json' \
        .format(cg_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def add_volume_snapshot_policy(session, cg_id, policy_id, return_type=None,
                               **kwargs):
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
    verify_cg_id(cg_id)
    verify_policy_id(policy_id)

    body_values = {'policy': policy_id}

    path = '/api/consistency_groups/{0}/attach_policy.json'.format(cg_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def remove_volume_snapshot_policy(session, snapshot_rule_name,
                                  delete_snapshots, return_type=None,
                                  **kwargs):
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
    verify_snapshot_rule_name(snapshot_rule_name)
    delete_snapshots = verify_boolean(delete_snapshots, "delete_snapshots")

    body_values = {'delete_snapshots': delete_snapshots}

    path = '/api/consistency_groups/{0}/detach_policy.json' \
        .format(snapshot_rule_name)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_all_snapshots(session, cg_id, ros_backup_job_id=None, policy_id=None,
                      start=None, limit=None, return_type=None, **kwargs):
    """
    Retrieves details for all snapshots either for a local volume or remote
    object storage backup job.

    :type policy_id: str
    :param policy_id: The snapshot policy 'name' value as returned by
        get_all_snapshot_policies.  For example: 'policy-00000001'.  Required.

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
    verify_cg_id(cg_id)

    list_more_options = []

    if policy_id is not None:
        verify_policy_id(policy_id)
        list_more_options = [('jobname', policy_id), ('application', 'user')]

    elif ros_backup_job_id is not None:
        verify_ros_backup_job_id(ros_backup_job_id)
        list_more_options = [('jobname', ros_backup_job_id),
                             ('application', 'obs_mirror')]

    parameters = verify_start_limit(start, limit, list_more_options)

    path = '/api/consistency_groups/{0}/snapshots.json'.format(cg_id)

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def create_volume_snapshot(session, cg_id, display_name, return_type=None,
                           **kwargs):
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
    verify_cg_id(cg_id)
    display_name = verify_field(display_name, "display_name")
    body_values = {'display_name': display_name}

    path = '/api/consistency_groups/{0}/snapshots.json'.format(cg_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def delete_volume_snapshot(session, snapshot_id, return_type=None, **kwargs):
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
    verify_snapshot_id(snapshot_id)

    path = '/api/snapshots/{0}.json'.format(snapshot_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def get_volume_migration(session, cg_id, return_type=None, **kwargs):
    """
    Retrieves details for a running volume migration job.  The job is queried
    using the consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes. Note that after volume migration successfully completes,
    the consistency group ID of the volume will change.  The new consistency
    group ID is returned by this API via the 'dst_cg_name' parameter, whereas
    the current consistency group ID is also returned by this API, via the
    'src_cg_name' parameter. To check if a volume is currently migrating,
    check if the value for the volume's "status" parameter is set to
    "Migrating".

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type cg_id: str
    :param cg_id: The consistency group 'cg_name' value as returned by
        get_all_volumes for the desired volume.  For example: 'cg-00000001'.
        Note that this can be either the current consistency group ID, or
        the future consistency group ID, which is also returned by this
        API as explained above.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_cg_id(cg_id)

    path = '/api/consistency_groups/{0}/show_migration.json'.format(cg_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def migrate_volume(session, cg_id, pool_id, migrate_snaps='YES',
                   return_type=None, **kwargs):
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
    verify_cg_id(cg_id)
    verify_pool_id(pool_id)
    migrate_snaps = verify_boolean(migrate_snaps, "migrate_snaps")

    body_values = {'poolname': pool_id, 'migratesnaps': migrate_snaps}

    path = '/api/consistency_groups/{0}/migrate.json'.format(cg_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def pause_volume_migration(session, migration_cg_id, return_type=None,
                           **kwargs):
    """
    Pause a running volume migration job.  The job is paused using the
    consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type migration_cg_id: str
    :param migration_cg_id: The consistency group 'cg_name' value as returned
    by get_all_volumes for the desired volume.  For example: 'cg-00000001'.
            Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_cg_id(migration_cg_id)

    path = '/api/migration_jobs/{0}/pause.json'.format(migration_cg_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def resume_volume_migration(session, migration_cg_id, return_type=None,
                            **kwargs):
    """
    Resume a paused volume migration job.  The job is resumed using the
    consistency group ID (cg_name) for the volume, as returned by
    get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type migration_cg_id: str
    :param migration_cg_id: The consistency group 'cg_name' value as returned
    by get_all_volumes for the desired volume.  For example: 'cg-00000001'.
            Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_cg_id(migration_cg_id)

    path = '/api/migration_jobs/{0}/continue.json'.format(migration_cg_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def cancel_volume_migration(session, migration_cg_id, return_type=None,
                            **kwargs):
    """
    Cancel a volume migration job.  The job is canceled using the consistency
    group ID (cg_name) for the volume, as returned by get_all_volumes.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type migration_cg_id: str
    :param migration_cg_id: The consistency group 'cg_name' value as returned
     by get_all_volumes for the desired volume.  For example: 'cg-00000001'.
             Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_cg_id(migration_cg_id)

    path = '/api/migration_jobs/{0}/abort.json'.format(migration_cg_id)

    return session.post_api(path=path, return_type=return_type, **kwargs)


def create_clone(session, cg_id, display_name, snapshot_id=None,
                 return_type=None, **kwargs):
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
    verify_cg_id(cg_id)
    display_name = verify_field(display_name, "display_name")
    body_values = {'name': display_name}

    if snapshot_id:
        verify_snapshot_id(snapshot_id)
        body_values['snapshot_id'] = snapshot_id

    path = '/api/consistency_groups/{0}/clone.json'.format(cg_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def create_volume_mirror(session, cg_id, display_name, remote_pool_id,
                         policies, remote_volume_name, wan_optimization='YES',
                         return_type=None, **kwargs):
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
    verify_cg_id(cg_id)
    display_name = verify_field(display_name, "display_name")
    verify_pool_id(pool_id=remote_pool_id, remote_pool_allowed=True)
    verify_policy_id(policies)
    remote_volume_name = verify_field(remote_volume_name, "remote_volume_name")
    wan_optimization = verify_boolean(wan_optimization, "wan_optimization")

    body_values = {'display_name': display_name, 'remote_pool': remote_pool_id,
                   'policy': policies,
                   'new_cg_name': remote_volume_name,
                   'wan_optimization': wan_optimization}

    path = '/api/consistency_groups/{0}/mirror.json'.format(cg_id)

    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def get_volume_performance(session, volume_id, interval=1, return_type=None,
                           **kwargs):
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
    verify_volume_id(volume_id)
    interval = verify_interval(interval)

    path = '/api/volumes/{0}/performance.json'.format(volume_id)

    parameters = {'interval': interval}

    return session.get_api(path=path, parameters=parameters,
                           return_type=return_type, **kwargs)


def get_snapshot(session, snap_id, return_type=None, **kwargs):
    """
    Retrieves details for a single volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type snap_id: str
    :param snap_id: The Snapshot 'name' value as returned by get_allsnapshots.
        For example: 'snap-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_snapshot_id(snap_id)

    path = "/api/snapshots/{0}.json".format(snap_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def delete_volume_from_recycle_bin(session, volume_id, return_type=None,
                                   **kwargs):
    """
    Retrieves details for a single volume.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The Volume 'name' value as returned by get_all_volumes.
        For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)

    path = "/api/volumes/{0}/delete_volume_from_recycle_bin.json".format(
        volume_id)

    return session.delete_api(path=path, return_type=return_type, **kwargs)


def detach_snapshot_policy(session, volume_id, snaprule,
                           delete_snapshots="Yes", return_type=None, **kwargs):
    """
    Detach a Snapshot Policy from a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type snaprule: str
    :param snaprule: A snap rule ID.
    (found in /consistency_groups/{volume_cg_id}/snapshot_policies API).
      For example: 'snaprule-00000001'.  Required.

    :type delete_snapshots: str
    :param delete_snapshots: True iff delete snapshots after detach

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_snaprule_id(snaprule)
    delete_snapshots = verify_boolean(delete_snapshots, "delete_snapshots")

    path = '/api/volumes/{0}/detach_snapshot_policy.json'.format(volume_id)
    body_values = {"id": volume_id, "snaprule": snaprule,
                   "delete_snapshots": delete_snapshots}
    return session.post_api(path=path, body=body_values,
                            return_type=return_type, **kwargs)


def update_protection(session, volume_id, alertmode=None, emergencymode=None,
                      capacityhistory=None, autoexpand=None,
                      maxcapacity=None, autoexpandby=None,
                      return_type=None, **kwargs):
    """
    Sets volume capacity thresholds. A support ticket will be created when your
     Volume reaches specified capacity thresholds.

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type alertmode: int
    :param alertmode: Alert me when it is estimated that the Volume will be at
    full capacity in X minutes.

    :type emergencymode: int
    :param emergencymode: Capacity threshold to trigger auto expand in GB

    :type capacityhistory: int
    :param capacityhistory: Window size in minutes which is used to calculate
    the rate of which free Volume capacity is consumed. This rate is used to
    calculate the estimated time until a Volume is full

    :type autoexpand: bool
    :param autoexpand: Enable capacity auto expand

    :type maxcapacity: int
    :param maxcapacity: Max Capacity to expand in GB.

    :type autoexpandby: int
    :param autoexpandby: Capacity to expand by in GB

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)

    body = {}

    if alertmode is not None:
        body["alertmode"] = alertmode
    if emergencymode is not None:
        body['emergencymode'] = emergencymode
    if capacityhistory is not None:
        body['capacityhistory'] = capacityhistory
    if autoexpand is not None:
        body['autoexpand'] = verify_boolean(autoexpand, 'autoexpand')
    if maxcapacity is not None:
        body['maxcapacity'] = maxcapacity
    if autoexpandby is not None:
        body['autoexpandby'] = autoexpandby

    if not body:
        raise ValueError('At least one of the following must be set: '
                         '"alertmode", "emergencymode", "capacityhistory", '
                         '"autoexpand", "maxcapacityexpand", "autoexpandby" ')

    path = "/api/volumes/{0}/update_protection.json".format(volume_id)

    return session.post_api(path=path, body=body, return_type=return_type,
                            **kwargs)


def update_antivirus_policy(session, volume_id, enable_on_demand_scan, file_types_to_scan,
                            exclude_file_types=None, include_file_types=None, exclude_path=None,
                            return_type=None, **kwargs):
    """
    Update Antivirus Policy in a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type enable_on_demand_scan: bool
    :param enable_on_demand_scan: Should enable on demand scan on AV.

    :type file_types_to_scan: str
    :param file_types_to_scan: Types of file to scan - can be 'all' or 'onlyspecified'
                               (available only if enable_on_demand_scan is true)

    :type exclude_file_types: str
    :param exclude_file_types: Comma separated file types to exclude e.g png,jpg
                               (available only if file_types_to_scan is all and enable_on_demand_scan is true)

    :type include_file_types: str
    :param include_file_types: Comma separated file types to include e.g png,jpg
                               (available only if file_types_to_scan is onlyspecified
                               and enable_on_demand_scan is true)

    :type exclude_path: str
    :param exclude_path: Comma separated file types e.g /tmp,/Documents
                         (available only if enable_on_demand_scan is true)

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_volume_av_parameters(enable_on_demand_scan, file_types_to_scan, exclude_file_types,
                                include_file_types, exclude_path)

    path = '/api/volumes/{0}/update_antivirus_policy.json'.format(volume_id)
    body = {}
    if enable_on_demand_scan:
        body["enableods"] = "true"
        body['filetypestoscan'] = file_types_to_scan
        if file_types_to_scan == "all":
            if exclude_file_types is not None:
                body['excludefiletypes'] = exclude_file_types
        else:
            if include_file_types is not None:
                body['includefiletypes'] = include_file_types
        if exclude_path is not None:
            body['excludepath'] = exclude_path
    else:
        body["enableods"] = "false"

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def fetch_volume_quotas(session, volume_id, scope, return_type=None, **kwargs):
    """
    Fetch quotas of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type scope: str
    :param scope: Quota's type, can be only user, group or project.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_volume_type(scope)

    path = 'api/volumes/{0}/quotas.json?scope={1}'.format(volume_id, scope)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def add_volume_quotas(session, volume_id, source_id, source_type, nas_type, limit, return_type=None, **kwargs):
    """
    Add quotas to a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type source_id: int
    :param source_id: Source to the groups/user/project ID.  Required.

    :type source_type: str
    :param source_type: Source type, can be only user, group or project.  Required.

    :type nas_type: str
    :param nas_type: NAS type, can be only ad, uid or nas.  Required.

    :type limit: str
    :param limit: Quota limit in MB.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_volume_type(source_type)
    verify_nas_type(nas_type)

    path = '/api/volumes/{0}/quotas.json'.format(volume_id)
    quotas = {"quotas": [{"source_id": source_id, "source_type": source_type, "nas_type": nas_type, "limit": limit}]}

    return session.post_api(secure=False, path=path, body=quotas, return_type=return_type, **kwargs)


def update_volume_quotas_state(session, volume_id, uquota, gquota, pquota, force, return_type=None, **kwargs):
    """
    Update quotas state of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type uquota: str
    :param uquota: Set user quota state.  Possible values on/off.  Required.

    :type gquota: str
    :param gquota: Set group quota state.  Possible values on/off.  Required.

    :type pquota: str
    :param pquota: Set group quota state.  Possible values on/off.  Required.

    :type force: str
    :param force: Force quota state change (skip warnings).  Possible values YES/NO.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    uquota = verify_on_off(uquota)
    gquota = verify_on_off(gquota)
    pquota = verify_on_off(pquota)

    verify_group_project_polarity(gquota, pquota)

    force = verify_bool(force)

    path = '/api/volumes/{0}/quotas_state.json'.format(volume_id)
    body = {"uquota": uquota, "gquota": gquota, "pquota": pquota, "force": force}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def get_volume_quota(session, volume_id, scope, quota_id, quota_nas=None, quota_ad=None, return_type=None, **kwargs):
    """
    Get quota of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type scope: str
    :param scope: Quota's type, can be only user, group or project.

    :type quota_id: int
    :param quota_id: NFS id / Project Id.

    :type quota_nas: str
    :param quota_nas: NAS name.

    :type quota_ad: str
    :param quota_ad: Active directory name.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_volume_type(scope)

    path = '/api/volumes/{0}/quota.json?scope={1}'.format(volume_id, scope)

    if quota_id:
        path += '&quota_id={0}'.format(quota_id)
    if quota_nas:
        path += '&quota_nas={0}'.format(quota_nas)
    if quota_ad:
        path += '&quota_ad={0}'.format(quota_ad)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def get_quota_projects(session, volume_id, return_type=None, **kwargs):
    """
    Get quotas projects of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)

    path = '/api/volumes/{0}/quota_projects.json'.format(volume_id)

    return session.get_api(path=path, return_type=return_type, **kwargs)


def create_quota_project(session, volume_id, display_name, directories, return_type=None, **kwargs):
    """
    Create a project for a quota in a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type display_name: str
    :param display_name: Display name for quota project.  Required.

    :type directories: List['str']
    :param directories: List of directories to create in quota project.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)

    path = '/api/volumes/{0}/quota_projects.json'.format(volume_id)
    body = {"name": display_name, "directories": directories}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def delete_quota_project(session, volume_id, project_id, force, return_type=None, **kwargs):
    """
    Delete quota project of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type project_id: str
    :param project_id: ID of the project.  e.g. proj-00000001.  Required.

    :type force: str
    :param force: Force quota state change (skip warnings).  Possible values YES/NO.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_project_id(project_id)
    verify_bool(force)

    path = '/api/volumes/{0}/quota_projects.json'.format(volume_id)
    body = {"project_id": project_id, "force": force}

    return session.delete_api(path=path, body=body, return_type=return_type, **kwargs)


def add_directories_to_quota_project(session, volume_id, project_id, path_param, return_type=None, **kwargs):
    """
    Add directories from quota project of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type project_id: str
    :param project_id: ID of the project.  e.g. proj-00000001.  Required.

    :type path_param: str
    :param path_param: Path to directory.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_project_id(project_id)

    path = '/api/volumes/{0}/quota_project_directories.json'.format(volume_id)
    body = {"project_id": project_id, "path": path_param}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def remove_directories_from_quota_project(session, volume_id, project_id, path_param, return_type=None, **kwargs):
    """
    Remove directories from quota project of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type project_id: str
    :param project_id: ID of the project.  e.g. proj-00000001.  Required.

    :type path_param: str
    :param path_param: Path to directory.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    verify_project_id(project_id)

    path = '/api/volumes/{0}/quota_project_directories.json'.format(volume_id)
    body = {"project_id": project_id, "path": path_param}

    return session.delete_api(path=path, body=body, return_type=return_type, **kwargs)


def dump_quotas_file(session, volume_id, scope, create_file=True, clear_file=True, force_refresh=True, return_type=None, **kwargs):
    """
    Remove directories from quota project of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type scope: str
    :param scope: Quota's type, can be only user, group or project.  Required.

    :type create_file: bool
    :param create_file: Should it create a new file.

    :type clear_file: bool
    :param clear_file: Should it clear the file.

    :type force_refresh: bool
    :param force_refresh: Force refresh.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)
    create_file = verify_bool_parameter(create_file)
    clear_file = verify_bool_parameter(clear_file)
    force_refresh = verify_bool_parameter(force_refresh)

    path = '/api/volumes/{0}/dump_quota_to_file.json'.format(volume_id)
    body = {"scope": scope, "create_file": create_file, "clear_file": clear_file, "force_refresh": force_refresh}

    return session.post_api(path=path, body=body, return_type=return_type, **kwargs)


def dump_quotas_state(session, volume_id, scope, return_type=None, **kwargs):
    """
    Remove directories from quota project of a Volume

    :type session: zadarapy.session.Session
    :param session: A valid zadarapy.session.Session object.  Required.

    :type volume_id: str
    :param volume_id: The volume ID 'name' value as returned by
        get_all_volumes.  For example: 'volume-00000001'.  Required.

    :type scope: str
    :param scope: Quota's type, can be only user, group or project.  Required.

    :type return_type: str
    :param return_type: If this is set to the string 'json', this function
        will return a JSON string.  Otherwise, it will return a Python
        dictionary.  Optional (will return a Python dictionary by default).

    :rtype: dict, str
    :returns: A dictionary or JSON data set as a string depending on
        return_type parameter.
    """
    verify_volume_id(volume_id)

    path = '/api/volumes/{0}/quotas_dump_state.json'.format(volume_id)
    body = {"scope": scope}

    return session.get_api(path=path, body=body, return_type=return_type, **kwargs)
