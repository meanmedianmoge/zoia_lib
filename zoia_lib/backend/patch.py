# -*- coding: utf-8 -*-
"""
Created: 9:45 PM on 2/23/20
Author: Mike Moger
Usage:
"""

import json
import os
import subprocess
# import struct
import zipfile

import numpy as np
import psutil

from zoia_lib.backend.api import PatchStorage
from zoia_lib.backend.renumber import Renumber

ps = PatchStorage()

with open('zoia_lib/common/tags.json', 'r') as tags_file:
    tags = json.load(tags_file)


class ZoiaPatch:

    def __init__(self,
                 fname: str = None,
                 obj=None):
        """Initializes ZoiaPatch class
        fname: used when files exist in local dir
        obj: used when files are being imported from PS
        """

        if obj is None:
            obj = {}
        if fname:
            self.path = os.path.dirname(fname)
            self.fname = fname

            # Read single bin file
            if fname.endswith('.bin'):
                self.number, self.name = self.strip_header(fname)
                """binary format requires specialized unpacking, waiting on Empress"""
                # data = open(fname, 'rb').read()
                # self.tags, self.version = struct.unpack('h1123b', data)

            # Read compressed dir
            elif fname.endswith('.zip'):
                self.name = []
                self.number = []
                self.notes = []
                data = zipfile.ZipFile(fname, "r")
                for fl in data.namelist():
                    if fl.endswith('.bin'):
                        self.number.append(self.strip_header(fl)[0])
                        self.name.append(self.strip_header(fl)[1])
                    elif fl.endswith('.txt'):
                        """read text file and add notes to object"""
                        with data.open(fl) as f:
                            for line in f:
                                self.notes.append(line)

        if obj:
            # get top-level attribs
            self.path = obj['self']
            self.name = obj['title']
            self.views = obj['view_count']
            self.likes = obj['like_count']
            self.downloads = obj['download_count']

            # get patch endpoint attribs
            patch = ps.get_patch(obj['id'])
            self.fname = patch['files'][0]['filename']
            if self.fname.endswith('.bin'):
                self.number, self.name = self.strip_header(self.fname)
            elif self.fname.endswith('.zip'):
                self.name = []
                self.number = []
                ps.download(obj['id'])
                data = zipfile.ZipFile(self.fname)
                for fl in data.namelist():
                    if fl.endswith('.bin'):
                        self.number.append(self.strip_header(fl)[0])
                        self.name.append(self.strip_header(fl)[1])
                os.remove(self.fname)

            self.notes = patch['content']
            self.categories = {s['id']: s['slug'] for s in patch['categories']}
            self.tags = {s['id']: s['slug'] for s in patch['tags']}

    @staticmethod
    def strip_header(name: str):
        """remove header ***_zoia_ from files"""

        return name.split('_zoia_')[0].split('/')[-1], name[3:].split('_zoia_')[1].replace('.bin', '')

    def add_tags(self,
                 to_add: list):
        """Add tags to Patch class"""

        keys = [{v: k for k, v in tags.items()}[s] for s in to_add]
        more_tags = dict(zip(keys, to_add))
        self.tags = {**self.tags, **more_tags}

    def remove_tags(self,
                    to_remove: list):
        """Remove tags from Patch class"""

        reverse = {v: k for k, v in self.tags.items()}
        for tag in to_remove:
            self.tags.pop(reverse[tag], None)

    def patch_notes(self,
                    text: str = None,
                    file: str = None):
        """Add or edit patch notes"""

        if file:
            with open(file, 'r') as f:
                for line in f:
                    self.notes.join(line)

        if text:
            self.notes = text

    def rating(self,
               rating: float,
               scale=None):
        """Assign rating to Patch"""

        if scale is None:
            scale = list(np.linspace(0, 5, 11))
        if rating not in scale:
            raise ValueError('Either define a new scale or score  '
                             'within {}'.format(str(scale)))
        self.rating = rating


def check_sd_status():
    """Check if SD card is inserted"""
    mnt = ''

    for disk in psutil.disk_partitions():
        if 'FAT32' in disk.fstype or 'msdos' in disk.fstype:
            mnt = disk.mountpoint
            break

    return None if mnt == '' else mnt


def get_patches_from_sd(path: str):
    """Create list of ZoiaPatch objects from SD card"""

    mnt = check_sd_status()
    if not mnt:
        raise ValueError('No SD card inserted')

    pth = os.path.join(mnt, path)

    fls = []
    for alg in os.listdir(pth):
        if alg.startswith('.'):
            continue
        patch = ZoiaPatch(fname=os.path.join(pth, alg))
        fls.append(patch)

    return fls


def make_dict_from_sd():
    """Create dictionary of ZoiaPatch sub-dirs from SD card"""

    mnt = check_sd_status()
    if not mnt:
        raise ValueError('No SD card inserted')

    dct = {}
    for pth in os.listdir(mnt):
        if pth.startswith('.'):
            continue
        dct[pth] = {}
        dct[pth] = get_patches_from_sd(os.path.join(mnt, pth))

    return dct


def get_patches_from_dir(path: str):
    """Create list of ZoiaPatch objects from local directory path"""

    fls = []
    for alg in os.listdir(path):
        if alg.startswith('.'):
            continue
        patch = ZoiaPatch(fname=os.path.join(path, alg))
        fls.append(patch)

    return fls


def make_dict_from_dir(drv: str):
    """Create dictionary of ZoiaPatch sub-dirs from directory path"""

    dct = {}
    for pth in os.listdir(drv):
        if pth.startswith('.') or not os.path.isdir(os.path.join(drv, pth)) \
                or pth.startswith('_'):
            continue
        dct[pth] = {}
        dct[pth] = get_patches_from_dir(os.path.join(drv, pth))

    return dct


def make_sorted_dirs_from_master(mstr: str):
    """Create directories of 64 ZoiaPatches from master directory path"""

    subprocess.call(['split_master.sh'])

    for dr in os.listdir(mstr):
        if dr.startswith('.') or not os.path.isdir(os.path.join(mstr, dr)) \
                or dr.startswith('_'):
            continue
        rn = Renumber(os.path.join(os.path.join(mstr, dr)))
        rn.renumber(sort='alpha')


def zoia_patch_from_api(body):
    """Create ZoiaPatch objects from PS returns"""

    dct = {}
    for patch in body:
        dct[patch['id']] = ZoiaPatch(obj=patch)

    return dct


def zoia_to_zip(pch: ZoiaPatch):
    """Create zipped file from ZoiaPatch object(s)"""

    reconstructed_name = pch.number + '_zoia_' + pch.name + '.bin'
    out_name = os.path.join(pch.path, pch.name + '.zip')

    zf = zipfile.ZipFile(out_name, "w", zipfile.ZIP_DEFLATED)

    try:
        print('adding binary patch file(s)')
        zf.write(pch.fname,
                 os.path.join(pch.name, reconstructed_name))

        print('adding patch notes')
        txt = reconstructed_name.replace('.bin', '')
        pch.patch_notes(txt, 'add')
        zf.write(pch.fname.replace('.bin', '.txt'),
                 os.path.join(pch.name, txt + '.txt'))
    finally:
        print('closing')
        zf.close()

    return zf
