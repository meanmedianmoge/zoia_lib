# -*- coding: utf-8 -*-
"""
Created: 9:45 PM on 2/23/20
Author: Mike Moger
Usage: 
"""

import os
import psutil
import struct
import zipfile
from zoia_lib.common import errors


class ZoiaPatch:

    def __init__(self,
                 filename: str):
        """Initializes ZoiaPatch class"""

        self.path = os.path.dirname(filename)

        # Read single bin file
        if filename.endswith('.bin'):
            self.number, self.name = self.strip_header(filename)
            """binary format requires specialized unpacking, waiting on Empress"""
            # data = open(filename, 'rb').read()
            # self.tag, self.version = struct.unpack('h1123b', data)
            self.notes = self.patch_notes(self.name)

        # Read compressed dir
        elif filename.endswith('.zip'):
            self.name = []
            self.number = []
            self.notes = []
            data = zipfile.ZipFile(filename, "r")
            for fl in data.namelist():
                if fl.endswith('.bin'):
                    self.number.append(self.strip_header(fl)[0])
                    self.name.append(self.strip_header(fl)[1])
                elif fl.endswith('.txt'):
                    """read text file and add notes to object"""
                    with data.open(fl) as f:
                        for line in f:
                            self.notes.append(line)
                else:
                    """create a note if the zip dir does not include one"""
                    self.notes = self.patch_notes(self.name[0])

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if os.path.isdir(path):
            self._path = os.path.abspath(path)
            return
        root_path = os.path.dirname(__file__)
        _path = os.path.join(root_path, path)
        if os.path.isdir(_path):
            self._path = _path
            return
        else:
            raise errors.BadPathError(
                f'Supplied path {path} is not a child of '
                f'current directory.'
            )

    @staticmethod
    def strip_header(name: str):
        """remove header ***_zoia_ from files"""

        return name.split('_zoia_')[0].split('/')[-1], \
            name[3:].split('_zoia_')[1].replace('.bin', '')

    def add_tags(self,
                 primary: list,
                 secondary: list):
        """Add primary and secondary tags to Patch class"""

        self.tag += [primary, secondary]

    def remove_tags(self,
                    to_remove: list):
        """Remove tags from Patch class"""

        self.tag.remove([t for t in to_remove])

    def patch_notes(self,
                    name: str,
                    action: str = 'pop',
                    command: str = 'v 1.0'):
        """Add or edit patch notes"""

        # options = {'add': self.add_notes,
        #            'remove': self.remove_notes,
        #            'update': self.update_notes}
        if action == 'add':
            with open('{}/{} patch notes.txt'.format(self.path, name), 'w') as fl:
                fl.write('{}'.format(command))

            return fl

        else:
            return ''


def check_sd_status():
    """Check if SD card is inserted"""

    for disk in psutil.disk_partitions():
        if 'FAT32' in disk.fstype or 'msdos' in disk.fstype:
            mnt = disk.mountpoint
            break
        else:
            mnt = ''

    return None if mnt == '' else mnt


def GetPatchesFromSD(path: str):
    """Create list of ZoiaPatch objects from SD card"""

    mnt = check_sd_status()
    if not mnt:
        raise ValueError('No SD card inserted')

    pth = os.path.join(mnt, path)

    fls = []
    for alg in os.listdir(pth):
        if alg.startswith('.'):
            continue
        patch = ZoiaPatch(os.path.join(pth, alg))
        fls.append(patch)

    return fls


def MakeDictFromSD():
    """Create dictionary of ZoiaPatch sub-dirs from SD card"""

    mnt = check_sd_status()
    if not mnt:
        raise ValueError('No SD card inserted')

    dct = {}
    for pth in os.listdir(mnt):
        if pth.startswith('.'):
            continue
        dct[pth] = {}
        dct[pth] = GetPatchesFromSD(os.path.join(mnt, pth))

    return dct


def GetPatchesFromDir(path: str):
    """Create list of ZoiaPatch objects from local directory path"""

    fls = []
    for alg in os.listdir(path):
        if alg.startswith('.'):
            continue
        patch = ZoiaPatch(os.path.join(path, alg))
        fls.append(patch)

    return fls


def MakeDictFromDir(drv: str):
    """Create dictionary of ZoiaPatch sub-dirs from directory path"""

    dct = {}
    for pth in os.listdir(drv):
        if pth.startswith('.') or not os.path.isdir(os.path.join(drv, pth)) \
                or pth.startswith('_'):
            continue
        dct[pth] = {}
        dct[pth] = GetPatchesFromDir(os.path.join(drv, pth))

    return dct
