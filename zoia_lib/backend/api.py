# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage: https://patchstorage.com/docs/
"""

import datetime
import json
import math
import os
from urllib.request import urlopen, Request

import certifi
import urllib3
from bs4 import BeautifulSoup
from furl import furl
from numpy import unicode

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


class PatchStorage:

    def __init__(self):
        """initializes PatchStorage class"""

        # set defaults for query params
        self.url = 'https://patchstorage.com/api/alpha/'
        self.platform = 3003  # ZOIA
        self.patch_count = self.determine_patch_count()

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
    def _validate_date(date: str):
        """ Ensures a date follows the format YYYY-MM-DD

        date: The date to check the format of.
        Returns the date in the correct format.
        Raises a ValueError on incorrect format.
        """
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            return date.isoformat()
        except ValueError:
            raise ValueError('Incorrect date format, should be YYYY-MM-DD')

    def search(self, more_params=None):
        """make query and output json body
        default args:
            - page (int): current page, default 1
            - per_page (int): max number to return, default 10
            - order (str enum): [asc, desc], order sort, default desc
            - orderby (str enum): [author, date, id, modified, slug,
                                   title relevance
                                   (must include search term)],
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
        endpoint = os.path.join(self.url, 'patches/')

        # get param dict
        default_params = {
            'page': 1,
            'per_page': 25,
            'order': 'desc',
            'orderby': 'date',
            'platforms': self.platform
        }

        # check type of optional args
        for key in list(more_params.keys()):
            # date
            if key in ['before', 'after']:
                more_params[key] = self._validate_date(more_params[key])
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

    def get_patch_meta(self, idx: str):
        """ Get the metadata associated with a specific
        patch ID.

        idx: The id that the metadata will be retrieved for.
        return: The metadata for the patch, in a MetadataSchema
                compliant form.
        """
        endpoint = os.path.join(self.url, 'patches/{}/'.format(idx))

        # Make the request
        raw_data = json.loads(http.request('GET', endpoint).data)
        # Remove the data that is not apart
        # of the MetadataSchema.json schema
        raw_data.pop("slug", None)
        raw_data.pop("excerpt", None)
        raw_data.pop("comment_count", None)
        raw_data.pop("platform", None)
        raw_data.pop("code", None)
        raw_data.pop("artwork", None)
        raw_data.pop("source_code_url", None)

        # Return the metadata
        return raw_data

    def download(self, idx: str):
        """ Download a file using patch id

        Raises a KeyError should no patch with the supplied id is found.
        """

        # Patches stored on PS use a 6-digit unique id number.
        # If an idx is not 6 digits long, it isn't a patch on PS.
        if idx is None or len(idx) != 6:
            return None

        try:
            body = self.get_patch_meta(idx)
            path = str(body['files'][0]['url'])
            f = http.request('GET', path).data, body
            return f
        except KeyError:
            # No patch with the supplied id was found.
            return None

    def get_all_patch_data_init(self):
        """ Returns the initial amount of information
        needed for display purposes once the user starts
        the application.

        return: A list of data, where each item contains the
                information outlined above.
        """

        per_page = 100
        search = {
            'per_page': per_page
        }

        all_patches = []
        for page in range(1, math.ceil(self.patch_count / per_page) + 1):
            # Get all the patches on the current page.
            all_patches += self.search({**search, **{'page': page}})

        return all_patches

    @staticmethod
    def determine_patch_count():
        """ Determines the number of ZOIA patches that
        are currently being stored on PS.

        return: An integer representing the total of ZOIA patches.
        """
        soup_patch = BeautifulSoup(urlopen(Request("https://patchstorage.com/",
                                                   headers={"User-Agent":
                                                                "Mozilla/5.0"})
                                           ).read(), "html.parser")
        found_pedals = soup_patch.find_all(class_="d-flex flex-column "
                                                  "justify-content-center")

        """ Convert the ResultSet to a string so we can split on what we are 
        looking for. The PS website does not have unique div names, so this
        is to workaround that. 
        """
        zoia = unicode.join(u'\n', map(unicode, found_pedals)
                            ).split("ZOIA", 1)[1].split("<strong>", 1)[1]

        # For some reason, questions posted on PS count as "patches",
        # so we need to figure out the # of questions.
        soup_ques = BeautifulSoup(
            urlopen(Request(
                "https://patchstorage.com/platform/zoia/?search_query=&ptype"
                "%5B%5D=question&tax_platform=zoia&tax_post_tag=&orderby"
                "=modified&wpas_id=search_form&wpas_submit=1",
                headers={"User-Agent": "Mozilla/5.0"})).read(), "html.parser")

        # Return the total minus the number of questions found.
        return int(zoia[:3]) - len(soup_ques.find_all(class_="card"))

    def get_potential_updates(self, meta):
        """ Queries the PS API for all patches that have an updated_at
        attribute that is more recent than the one present for patches
        that have been previously downloaded.

        meta: An array containing the id and updated_at attributes for
              patches that may need to be updated.
        """
        new_bin = []

        for entry in meta:
            idx = entry["id"]

            # Check to see if the patch has been updated by comparing the dates
            curr_meta = self.get_patch_meta(idx)
            if curr_meta["updated_at"] > meta["updated_at"]:
                new_bin.append((self.download(meta["id"]), curr_meta))

        return new_bin

    def get_newest_patches(self, pch_num):
        """ Queries the PS API for the latest patches that have not been
        stored in data.json previously. This is only called after the
        initial launch of the application and only if new patches have
        been uploaded to PS since that initial launch.

        pch_num: The number of patches currently stored in data.json
        """
        per_page = self.patch_count - pch_num
        if per_page > 100:
            per_page = 100
        search = {
            'per_page': per_page
        }

        new_patches = []
        pages = 2
        if per_page == 100:
            pages = math.ceil((self.patch_count - pch_num) / 100) + 1
        if pages == 2:
            return self.search({**search, **{'page': 1}})
        else:
            for i in range(1, pages):
                new_patches += self.search({**search, **{'page': 1}})
            return new_patches
