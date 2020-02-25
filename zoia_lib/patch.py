# -*- coding: utf-8 -*-
"""
Created: 9:45 PM on 2/23/20
Author: Mike Moger
Usage: 
"""

import os
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

        return name.split('_zoia_')[0], name[3:].split('_zoia_')[1].replace('.bin', '')

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
                    action: str = 'add',
                    command: str = 'v 1.0'):
        """Add or edit patch notes"""

        # options = {'add': self.add_notes,
        #            'remove': self.remove_notes,
        #            'update': self.update_notes}
        if action == 'add':
            with open('{}/{} patch notes.txt'.format(self.path, name), 'w') as fl:
                fl.write('{}'.format(command))

        return fl
