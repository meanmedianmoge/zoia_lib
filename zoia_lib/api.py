# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage: https://patchstorage.com/docs/
"""

import datetime
import json
import os

import certifi
import urllib3
from furl import furl

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())


class PatchStorage:

    def __init__(self):
        """initializes PatchStorage class"""

        # set defaults for query params
        self.url = 'https://patchstorage.com/api/alpha/'
        self.platform = 3003  # ZOIA
        self.state = 151  # Ready-to-Go
        # self.author = '2825'  # MMM, '2953' CHMJ
        self.manifest = {
            'platforms': [
                {704: 'aleph',
                 3074: 'audiokit-synth-one',
                 215: 'audulus',
                 4751: 'beatmaker-3',
                 400: 'bela',
                 295: 'cabbage',
                 1146: 'camomile',
                 2017: 'chuck',
                 3540: 'digit',
                 4890: 'drambo',
                 1525: 'echosystem',
                 662: 'etc',
                 4296: 'groove-rider',
                 354: 'max-for-live',
                 288: 'maxmsp',
                 3201: 'midiboy',
                 3830: 'midihub',
                 3989: 'mirack',
                 4242: 'moog-model-15',
                 3341: 'mozaic',
                 3501: 'nanostudio',
                 3073: 'nebulae',
                 3371: 'orac',
                 3226: 'orca',
                 154: 'organelle',
                 289: 'owl',
                 89: 'pd-extended',
                 163: 'pd-pulp',
                 90: 'pd-vanilla',
                 1558: 'pisound',
                 3270: 'medusa',
                 1993: 'purr-data',
                 4538: 'reaktor',
                 1524: 'reverb',
                 4690: 'roland-aira-modular-customizer',
                 922: 'softube-modular',
                 921: 'solorack',
                 371: 'supercollider',
                 3019: 'synthstrom-deluge',
                 745: 'vcv-rack',
                 3003: 'zoia'}
            ],
            'categories': [
                {378: 'composition',
                 77: 'effect',
                 3317: 'game',
                 1: 'other',
                 75: 'sampler',
                 76: 'sequencer',
                 372: 'sound',
                 74: 'synthesizer',
                 117: 'utility',
                 91: 'video'}
            ],
            'states': [
                {149: 'help-needed',
                 1098: 'inactive',
                 151: 'ready-to-go',
                 150: 'work-in-progress'}
            ],
            'licenses': [
                {4184: 'afl-3-0',
                 4173: 'apache-2-0',
                 4185: 'artistic-2-0',
                 4186: 'bsl-1-0',
                 4174: 'bsd-2-clause',
                 4175: 'bsd-3-clause',
                 4187: 'bsd-3-clause-clear',
                 4190: 'cc-by-4-0',
                 4191: 'cc-by-sa-4-0',
                 4188: 'cc'}
            ]
        }

    @staticmethod
    def _validate_intlist(lst: list):
        """ Forces all items in a list to take on the type int

        lst: The list of items to convert to ints
        Returns the converted list.
        """
        return [int(v) for v in lst]

    @staticmethod
    def _validate_strlist(lst: list):
        """ Forces all items in a list to take on the type str

        lst: The list of items to convert to strings
        Returns the converted list.
        """
        return [str(s) for s in lst]

    @staticmethod
    def validate_date(date: str):
        """ Ensures a date follows the format YYYY-MM-DD

        date: The date to check the format of.
        Returns the date in the correct format.
        On incorrect format a ValueError is raised.
        """
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            return date.isoformat()
        except ValueError:
            raise ValueError('Incorrect data format, should be YYYY-MM-DD')

    def endpoint(self,
                 endpoint: str):
        """specify endpoint for query"""

        return os.path.join(self.url, endpoint)

    def search(self,
               more_params=None):
        """make query and output json body
        default args:
            - page (int): current page, default 1
            - per_page (int): max number to return, default 10
            - order (str enum): [asc, desc], order sort, default desc
            - orderby (str enum): [author, date, id, modified, slug, title
                                   relevance (must include search term)],
                                        order sort by, default date
        optional args:
            - search (str): search for given string
            - before (str): published before given ISO8601 date
            - after (str): published after given ISO8601 date
            - exclude (str): exclude specific id(s)
            - include (str): include specific id(s)
            - offset (int): offset by number of items
            - slug (str []): search for given slug(s)
            - author (str): search for items by an author(s)
            - author_exclude (str): exclude specific author(s)
            - categories (int []): search for items with a category(ies)
            - categories_exclude (int []): exclude specific category(ies)
            - tags (int []): search for items with tag(s)
            - tags_exclude (int []): exclude specific tag(s)
            - platforms (int []): search for items within a platform
            - platforms_exclude (int []): exclude specific platform(s)
            - states (int []): search for items with a given state
            - states_exclude (int []); exclude specific state(s)
        """

        if more_params is None:
            more_params = {}
        endpoint = self.endpoint('patches?/')

        # get param dict
        default_params = {
            'page': 1,
            'per_page': 25,
            'order': 'desc',
            'orderby': 'date',
            'platforms': self.platform,
            'states': self.state,
        }

        # check type of optional args
        for key in list(more_params.keys()):
            # date
            if key in ['before', 'after']:
                more_params[key] = self.validate_date(more_params[key])
            # str
            if key in ['search', 'exclude', 'include', 'order',
                       'orderby', 'slug', 'author', 'author_exclude'] and \
                    type(more_params[key]) != list:
                more_params[key] = str(more_params[key])
            # int
            if key in ['offset', 'categories', 'categories_exclude',
                       'tags', 'tags_exclude', 'page', 'platforms',
                       'platforms_exclude', 'states', 'states_exclude'] and \
                    type(more_params[key]) != list:
                more_params[key] = int(more_params[key])
            # str list
            if key in ['slug'] and type(more_params[key]) == list:
                more_params[key] = self._validate_strlist(more_params[key])
            # int list
            if key in ['categories', 'categories_exclude', 'tags',
                       'tags_exclude', 'platforms', 'platforms_exclude',
                       'states', 'states_exclude'] and \
                    type(more_params[key]) == list:
                more_params[key] = self._validate_intlist(more_params[key])

        params = {**default_params, **more_params}

        # make request
        url = str(furl(endpoint).add(params))
        r = http.request('GET', url)

        return json.loads(r.data)

    def get_list(self,
                 more_params=None):
        """get list of returned objects"""

        if more_params is None:
            more_params = {}
        body = self.search(more_params)

        return dict(zip([str(x['title']) for x in body],
                        [str(x['self'] + '?/') for x in body]))

    def get_tags(self,
                 more_params=None):
        """get list of tags"""

        if more_params is None:
            more_params = {}
        body = self.search(more_params)

        return dict(zip([str(x['title']) for x in body],
                        [str(x['tags']) for x in body]))

    def get_patch(self,
                  idx: str):
        """get Patch object"""

        endpoint = self.endpoint('patches/{}?/'.format(idx))

        # make request
        r = http.request('GET', endpoint)

        return json.loads(r.data)

    def download(self,
                 idx: str):
        """download file using patch id"""

        body = self.get_patch(idx)

        path = str(body['files'][0]['url'])
        fname = str(body['files'][0]['filename'])

        with open(fname, 'wb') as out:
            rr = http.request('GET', path)
            data = rr.data
            out.write(data)


def get_all_tags():
    """get master dict of all tag id's and slugs"""

    ps = PatchStorage()
    search = {'orderby': 'title',
              'order': 'asc',
              'per_page': 100}

    tags = {}
    for page in range(1, 6):
        body = ps.search({**search, **{'page': page}})
        for patch in body:
            more = dict(zip([s['id'] for s in patch['tags']],
                            [s['slug'] for s in patch['tags']]))

            # remove any duplicate tags
            for idx in set(more).intersection(set(tags)):
                more.pop(idx, None)
            tags = {**tags, **more}

    with open('zoia_lib/common/tags.json', 'w') as f:
        json.dump(tags, f)



