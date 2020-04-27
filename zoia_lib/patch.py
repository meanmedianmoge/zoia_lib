# -*- coding: utf-8 -*-
"""
Created: 9:45 PM on 2/23/20
Author: Mike Moger
Usage: 
"""

import os
import psutil
import subprocess
# import struct
import zipfile
from zoia_lib.renumber import Renumber


class ZoiaPatch:

    def __init__(self,
                 filename: str):
        """Initializes ZoiaPatch class"""

        self.path = os.path.dirname(filename)
        self.filename = filename

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
            with open('{}/{}.txt'.format(self.path, name), 'w') as fl:
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


def MakeSortedDirsFromMaster(mstr: str):
    """Create directories of 64 ZoiaPatches from master directory path"""

    subprocess.call(['split_master.sh'])

    for dr in os.listdir(mstr):
        if dr.startswith('.') or not os.path.isdir(os.path.join(mstr, dr)) \
                or dr.startswith('_'):
            continue
        rn = Renumber(os.path.join(os.path.join(mstr, dr)))
        rn.renumber(sort='alpha')


def zoia_to_zip(pch: ZoiaPatch):
    """Create zipped file from ZoiaPatch object(s)"""

    reconstructed_name = pch.number + '_zoia_' + pch.name + '.bin'
    outname = os.path.join(pch.path, pch.name + '.zip')

    zf = zipfile.ZipFile(outname, "w", zipfile.ZIP_DEFLATED)

    try:
        print('adding binary patch file(s)')
        zf.write(pch.filename,
                 os.path.join(pch.name, reconstructed_name))

        print('adding patch notes')
        txt = reconstructed_name.replace('.bin', '')
        pch.patch_notes(txt, 'add')
        zf.write(pch.filename.replace('.bin', '.txt'),
                 os.path.join(pch.name, txt + '.txt'))
    finally:
        print('closing')
        zf.close()

    return zf
