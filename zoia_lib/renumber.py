# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage:
"""

import os
import random
from zoia_lib.common import errors


class Renumber:

    def __init__(self,
                 path: str):
        """initializes Renumber class"""

        # get absolute path to files
        self.path = path
        # set class attributes
        self.start = 0

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
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
    def get_files(path: str):
        raw_files = os.listdir(path)
        return [f for f in raw_files if not f.startswith('.')]

    @staticmethod
    def strip_header(fls: list):
        """remove header ***_zoia_ from files for better lists"""

        return zip([s.split('_zoia_')[0] for s in fls],
                   [s[3:].split('_zoia_')[1] for s in fls])

    def loop_it(self,
                fls: list):
        """do the loop"""

        for num, fname in fls:
            if self.start < 10:
                dst = "00" + str(self.start) + '_zoia_' + fname
            else:
                dst = "0" + str(self.start) + '_zoia_' + fname

            src = num + '_zoia_' + fname
            os.rename(os.path.join(self.path, src),
                      os.path.join(self.path, dst))
            self.start += 1

    def renumber(self,
                 sort: str):
        """applies the renumbering"""

        # Get a fresh list of files from path on each call of renumber.
        self.files = self.get_files(self.path)

        sort_options = {
            'alpha': self.alpha,
            'alpha_invert': self.alpha_invert,
            'by_tag': self.by_tag,
            'random': self.random
        }
        self.files = sort_options.get(sort)()
        return self.loop_it(self.files)

    def alpha(self):
        """renumbers self.files alphabetically"""

        # sort alpha, ignore case
        self.files = sorted(self.strip_header(self.files),
                            key=lambda x: x[1])

        return self.files

    def alpha_invert(self):
        """renumbers self.files alphabetically in reverse"""

        # sort alpha, ignore case
        self.files = sorted(self.strip_header(self.files),
                            key=lambda x: x[1],
                            reverse=True)

        return self.files

    def by_tag(self):
        """renumbers self.files by tag"""

        _type = [
            'Patches',
            'Questions',
            'Tutorials'
        ]

        primary = [
            'Composition',
            'Effect',
            'Game',
            'Other',
            'Sampler',
            'Sequencer',
            'Sound',
            'Synthesizer',
            'Utility',
            'Video'
        ]

        secondary = [
            'delay',
            'glitch',
            'granular',
            ''
        ]

        state = [
            'Help Needed',
            'Inactive',
            'Ready to Go',
            'Work in Progress'
        ]

        sort_by = [
            'Date',
            'Views',
            'Likes',
            'Downloads'
        ]

        return self.files

    def random(self):
        """renumbers self.files randomly"""

        self.files = sorted(self.strip_header(self.files),
                            key=lambda x: x[1])
        random.shuffle(self.files)

        return self.files
