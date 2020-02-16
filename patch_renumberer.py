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
import struct
import random
import zipfile
import requests


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

        # get starting path and folder
        os.chdir(path)
        folder = path
        files = os.listdir(folder)

        # set class attributes
        self.path = folder
        self.files = files
        self.start = 0
        self.invert = invert

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

    def strip_header(self,
                     fls: list):
        """remove header ***_zoia_ from files for better lists"""

        self.files = zip([s.split('_zoia_')[0] for s in fls],
                         [s[3:].split('_zoia_')[1] for s in fls])

        return self.files

    def renumber(self,
                 sort: str):
        """applies the renumbering"""

        if sort == 'alpha':
            self.files = self.alpha()
            return self.loop_it(self.files)
        if sort == 'by_tag':
            self.files = self.by_tag()
            return self.loop_it(self.files)
        if sort == 'random':
            self.files = self.random()
            return self.loop_it(self.files)

    def alpha(self):
        """renumbers files alphabetically"""

        # sort alpha, ignore case
        self.files = sorted(self.strip_header(self.files), key=lambda x: x[1])

        # invert if desired
        if self.invert:
            zip(*sorted(self.files, reverse=True))

        return self.files

    def by_tag(self):
        """renumbers files by tag"""

        type = ['Patches',
                'Questions',
                'Tutorials']

        primary = ['Composition',
                    'Effect',
                    'Game',
                    'Other',
                    'Sampler',
                    'Sequencer',
                    'Sound',
                    'Synthesizer',
                    'Utility',
                    'Video']

        secondary = ['delay',
                     'glitch',
                     'granular',
                     '']

        state = ['Help Needed',
                 'Inactive',
                 'Ready to Go',
                 'Work in Progress']

        sort_by = ['Date',
                   'Views',
                   'Likes',
                   'Downloads']

        return self.files

    def random(self):
        """renumbers files randomly"""

        self.files = sorted(self.strip_header(self.files), key=lambda x: x[1])
        random.shuffle(self.files)

        return self.files
