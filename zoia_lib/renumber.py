# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage:
"""

import os
import random
import uuid
from zoia_lib.common import errors
from zoia_lib.api import PatchStorage

ps = PatchStorage()


# TODO: figure out how to handle zip dirs from PS
# best case would be to dl immediately and treat as separate patch objects


class Renumber:

    def __init__(self,
                 path: str = None,
                 obj: dict = None):
        """initializes Renumber class"""

        if path:
            # get absolute path to files
            self.path = path
            # record original state of files so we can revert if needed
            self.original_files = self.get_files(self.path)

        if obj:
            # get absolute path to files
            self.path = os.getcwd()
            # record original state of files so we can revert if needed
            self.original_files = [obj[s].fname for s in obj.keys()]

        self.sort_counts = {
            'alpha': 0,
            'alpha_invert': 0,
            'by_tag': 0,
            'random': 0
        }

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
            raise errors.BadPathError(path)

    @staticmethod
    def get_files(path: str):
        raw_files = os.listdir(path)
        return [f for f in raw_files if not f.startswith('.')]

    @staticmethod
    def strip_header(fls: list):
        """Remove header ***_zoia_ from files for better lists.

        Returns dictionary mapping current file name
        to file name with headers stripped.
        """

        return {s: s[3:].split('_zoia_')[1] for s in fls}

    def loop_it(self,
                fls: dict):
        """do the loop"""
        dupes = {}
        start = 0
        for src, fname in fls.items():
            if start < 10:
                dst = "00" + str(start) + '_zoia_' + fname
            else:
                dst = "0" + str(start) + '_zoia_' + fname

            source_path = os.path.join(self.path, src)
            dest_path = os.path.join(self.path, dst)

            if os.path.isfile(dest_path) and source_path != dest_path:
                uuid_str = str(uuid.uuid4())
                temp_name = f'{dst}_{uuid_str}'
                dest_path = os.path.join(self.path, temp_name)
                dupes[temp_name] = fname
            os.rename(source_path, dest_path)
            start += 1

        if dupes:
            return self.loop_it(dupes)

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
        self.file_mapping = self.strip_header(self.files)
        self.sorted_mapping = sort_options.get(sort)()
        # Added this because it might be useful to track
        self.sort_counts[sort] += 1
        return self.loop_it(self.sorted_mapping)

    def alpha(self):
        """renumbers self.files alphabetically"""

        # sort alpha, ignore case
        return {k: v for k, v in sorted(
            self.file_mapping.items(),
            key=lambda item: item[1])
                }

    def alpha_invert(self):
        """renumbers self.files alphabetically in reverse"""

        # sort alpha invert, ignore case
        return {k: v for k, v in sorted(
            self.file_mapping.items(),
            key=lambda item: item[1],
            reverse=True)
                }

    def by_tag(self,
               how: str = 'category',
               sort: str = 'alpha',
               tags: list = None):
        """renumbers self.files by tag"""

        return self.file_mapping

    def random(self):
        """renumbers self.files randomly"""

        sorted_files = self.alpha()
        # can't random.shuffle dict.items(). Using sample instead:
        # https://docs.python.org/3/library/random.html#random.shuffle
        shuffled = random.sample(
            sorted_files.items(),
            k=len(sorted_files.items())
        )

        return dict(shuffled)
