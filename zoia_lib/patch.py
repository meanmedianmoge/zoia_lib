# -*- coding: utf-8 -*-
"""
Created: 9:45 PM on 2/23/20
Author: Mike Moger
Usage: 
"""

import struct
import zipfile


class ZoiaPatch:

    def __init__(self,
                 filename: str):
        """Initializes ZoiaPatch class"""

        # Read single bin file
        if filename.endswith('bin'):
            data = open(filename, "rb").read()
            self.name, self.number = struct.unpack('@II', data)
            self.tag, self.version = struct.unpack('h1123b', data)
            self.notes = self.patch_notes()

        # Read compressed dir
        elif filename.endswith('zip'):
            data = zipfile.ZipFile(filename, "rb")
            for fls in data.filelist:
                if fls.filename.endswith('bin'):
                    self.name, self.number = fls
                if fls.filename.endswith('txt'):
                    self.notes = fls

    def add_tags(self,
                 primary: list,
                 secondary: list):
        """Add primary and secondary tags to Patch class"""

        self.tag += [primary, secondary]

    def remove_tags(self,
                    to_remove: list):
        """Remove tags from Patch class"""

        self.tag.remove([t for t in tag])

    def patch_notes(self,
                    action: str = 'add',
                    command: str = 'v 1.0'):
        """Add or edit patch notes"""

        with open('{}_patch_notes.txt'.format(self.name), 'wb') as fl:
            fl.write('{}'.format(command))

        return fl
