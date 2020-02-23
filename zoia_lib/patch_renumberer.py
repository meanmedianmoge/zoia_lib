"""Renumbers patches in a directory path

So, to go back to that _is_ vs _has_ idea:

What I was trying to suggest is two sortings.
The first would occur by default category,
but the second would sort tags based on popularity
only as they applied within that default category.

So, for the example of "delay," I would imagine this
would rank high in the "effects" default (along with
"reverb" and "looper"). So, for an effect, delay would
appear early in the tag list, as per my example above.

However, since synthesizer would sort tags within that
category according to popularity as it applied to synthesizer
patches, delay, while likely to come up, would be less likely
to precede tags like "generative" or "polyphonic" or "MIDI."

"Delay" might be a more popular tag overall than any of
these, but it is not as popular as these in the category
of "synthesizer" tag patches.

I have zero idea how difficult that would be to code,
but yeah, basically: first sort, by default categories;
second sort, by popularity, but only the popularity of
that tag within that specific default category, rather
than in patches overall.

That won't eliminate the _is_/_has_ problem, but it
would likely help a lot.
"""

import os
import random
import struct
import zipfile

import requests

from zoia_lib.common import errors

# https://patchstorage.com/docs/
def get_patch():
    base_url = 'https://patchstorage.com/api/alpha/patches/'
    res = requests.get(
        url=base_url,
        params=[('author', 'Christopher H. M. Jacques')],
    )

    return res


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


class Renumber:

    def __init__(self,
                 path: str,
                 invert: bool = False):
        """initializes Renumber class"""

        # get absolute path to files
        self.path = path
        self.files = self.get_files()
        # set class attributes
        self.start = 0
        self.invert = invert

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

    def get_files(self):
        raw_files = os.listdir(self.path)
        return [f for f in raw_files if not f.startswith('.')]

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

    @staticmethod
    def strip_header(fls: list):
        """remove header ***_zoia_ from files for better lists"""

        return zip([s.split('_zoia_')[0] for s in fls],
                   [s[3:].split('_zoia_')[1] for s in fls])

    def renumber(self,
                 sort: str):
        """applies the renumbering"""

        sort_options = {
            'alpha': self.alpha,
            'by_tag': self.by_tag,
            'random': self.random
        }
        sorted_files = sort_options.get(sort)()
        self.loop_it(sorted_files)

    def alpha(self):
        """renumbers self.files alphabetically"""

        # sort alpha, ignore case
        sorted_files = sorted(self.strip_header(self.files), key=lambda x: x[1])

        # invert if desired
        if self.invert:
            zip(*sorted(sorted_files, reverse=True))

        return sorted_files

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

        sorted_files = sorted(
            self.strip_header(self.files),
            key=lambda x: x[1]
        )
        return random.shuffle(sorted_files)
