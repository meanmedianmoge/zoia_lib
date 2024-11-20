import json
import math
import os

import certifi
import urllib3
# from bs4 import BeautifulSoup
from furl import furl
# from numpy.compat import unicode

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())


class PatchStorage:
    """The PatchStorage class is responsible for all API calls to the
    PatchStorage API. This includes the querying of metadata, the
    downloading of patches binaries, and determining the number of
    ZOIA patches currently stored on PatchStorage.
    Documentation for the PatchStorage API can be found at:
        https://patchstorage.com/docs/
    """

    def __init__(self):
        """Initializes the PatchStorage class."""

        # Set defaults for query params
        self.url = "https://patchstorage.com/api/beta/"
        self.platform = 3003  # ZOIA
        self.api_token = None
        self.licenses = self._get_license_data()
        self.categories = self._get_categories_data()
        try:
            self.patch_count = self._patch_count()
        except:
            # No internet connection.
            pass

    def _search(self, more_params=None):
        """Make a query to the PS API.
        Default args:
            - page (int): current page, default 1
            - per_page (int): max number to return, default 10
            - order (str enum): [asc, desc], order sort, default desc
            - orderby (str enum): [author, date, id, modified, slug,
                                   title relevance
                                   (must include search term)],
                                    order sort by, default date
        Optional args:
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
            - categories_exclude (int []): exclude specific
                                           category(ies)
            - tags (int []): search for items with tag(s)
            - tags_exclude (int []): exclude specific tag(s)
            - platforms (int []): search for items within a platform
            - platforms_exclude (int []): exclude specific platform(s)
            - states (int []): search for items with a given state
            - states_exclude (int []); exclude specific state(s)

        Please note that the use of optional args is deprecated as of
        Beta 3 of the ZOIA Librarian. Should the implementation be
        needed, please consult the repo for the previous implementation.

        return: The retrieved metadata in JSON form.
        """

        if more_params is None:
            more_params = {}
        endpoint = os.path.join(self.url, "patches/")

        # get param dict
        default_params = {
            "page": 1,
            "per_page": 25,
            "order": "desc",
            "orderby": "date",
            "platforms": self.platform,
        }

        params = {**default_params, **more_params}

        # make request
        url = str(furl(endpoint).add(params))
        r = http.request("GET", url)

        return json.loads(r.data) if r.status == 200 else []

    def get_patch_meta(self, idx: str):
        """Get the metadata associated with a specific
        patch ID.

        idx: The id that the metadata will be retrieved for.

        return: The metadata for the patch, in a MetadataSchema
                 compliant form.
        """
        endpoint = os.path.join(self.url, "patches/{}/".format(idx))

        # Make the request
        raw_data = json.loads(http.request("GET", endpoint).data)

        # Return the metadata
        return raw_data

    def download(self, idx: str):
        """Download a file using patch id

        Returns: The raw binary data for the patch if it was found,
                 None otherwise.
        """

        # Patches stored on PS use a 6-digit unique id number.
        # If an idx is not 6 digits long, it isn't a patch on PS.
        if idx is None or len(idx) != 6:
            return None

        try:
            body = self.get_patch_meta(idx)
            f = http.request("GET", str(body["files"][0]["url"])).data, body
            return f
        except KeyError:
            # No patch with the supplied id was found.
            return None

    def _get_license_data(self):
        """Get list of licenses."""
        # r = http.request(
        #     "GET",
        #     self.url + 'licenses?per_page=100',
        #     headers={
        #         'Content-Type': 'application/json'
        #     }
        # )
        # if r.status == 200:
        #     return json.loads(r.data)

        return [
            {
                "id": 4184,
                "description": "",
                "slug": "afl-3-0",
                "name": "Academic Free License v3.0"
            },
            {
                "id": 4173,
                "description": "",
                "slug": "apache-2-0",
                "name": "Apache License 2.0"
            },
            {
                "id": 4185,
                "description": "",
                "slug": "artistic-2-0",
                "name": "Artistic license 2.0"
            },
            {
                "id": 4186,
                "description": "",
                "slug": "bsl-1-0",
                "name": "Boost Software License 1.0"
            },
            {
                "id": 4174,
                "description": "",
                "slug": "bsd-2-clause",
                "name": "BSD 2-Clause \"Simplified\" License"
            },
            {
                "id": 4175,
                "description": "",
                "slug": "bsd-3-clause",
                "name": "BSD 3-Clause \"New\" or \"Revised\" License"
            },
            {
                "id": 4187,
                "description": "",
                "slug": "bsd-3-clause-clear",
                "name": "BSD 3-clause Clear license"
            },
            {
                "id": 4190,
                "description": "",
                "slug": "cc-by-4-0",
                "name": "Creative Commons Attribution 4.0"
            },
            {
                "id": 4191,
                "description": "",
                "slug": "cc-by-sa-4-0",
                "name": "Creative Commons Attribution Share Alike 4.0"
            },
            {
                "id": 4188,
                "description": "",
                "slug": "cc",
                "name": "Creative Commons license family"
            },
            {
                "id": 4189,
                "description": "",
                "slug": "cc0-1-0",
                "name": "Creative Commons Zero v1.0 Universal"
            },
            {
                "id": 4201,
                "description": "",
                "slug": "custom",
                "name": "Custom License"
            },
            {
                "id": 4192,
                "description": "",
                "slug": "wtfpl",
                "name": "Do What The F*ck You Want To Public License"
            },
            {
                "id": 4176,
                "description": "",
                "slug": "epl-2-0",
                "name": "Eclipse Public License 2.0"
            },
            {
                "id": 4193,
                "description": "",
                "slug": "ecl-2-0",
                "name": "Educational Community License v2.0"
            },
            {
                "id": 4194,
                "description": "",
                "slug": "eupl-1-1",
                "name": "European Union Public License 1.1"
            },
            {
                "id": 4172,
                "description": "",
                "slug": "agpl-3-0",
                "name": "GNU Affero General Public License v3.0"
            },
            {
                "id": 4195,
                "description": "",
                "slug": "gpl",
                "name": "GNU General Public License family"
            },
            {
                "id": 4177,
                "description": "",
                "slug": "gpl-2-0",
                "name": "GNU General Public License v2.0"
            },
            {
                "id": 4178,
                "description": "",
                "slug": "gpl-3-0",
                "name": "GNU General Public License v3.0"
            },
            {
                "id": 4196,
                "description": "",
                "slug": "lgpl",
                "name": "GNU Lesser General Public License family"
            },
            {
                "id": 4179,
                "description": "",
                "slug": "lgpl-2-1",
                "name": "GNU Lesser General Public License v2.1"
            },
            {
                "id": 4180,
                "description": "",
                "slug": "lgpl-3-0",
                "name": "GNU Lesser General Public License v3.0"
            },
            {
                "id": 4197,
                "description": "",
                "slug": "isc",
                "name": "ISC"
            },
            {
                "id": 4199,
                "description": "",
                "slug": "ms-pl",
                "name": "Microsoft Public License"
            },
            {
                "id": 4181,
                "description": "",
                "slug": "mit",
                "name": "MIT License"
            },
            {
                "id": 4182,
                "description": "",
                "slug": "mpl-2-0",
                "name": "Mozilla Public License 2.0"
            },
            {
                "id": 4200,
                "description": "",
                "slug": "osl-3-0",
                "name": "Open Software License 3.0"
            },
            {
                "id": 4183,
                "description": "",
                "slug": "unlicense",
                "name": "The Unlicense"
            }
        ]

    def _get_categories_data(self):
        """Get list of categories."""
        # r = http.request(
        #     "GET",
        #     self.url + 'categories',
        #     headers={
        #         'Content-Type': 'application/json'
        #     }
        # )
        # if r.status == 200:
        #     return json.loads(r.data)

        return [
            {
                "id": 378,
                "description": "",
                "slug": "composition",
                "name": "Composition"
            },
            {
                "id": 77,
                "description": "",
                "slug": "effect",
                "name": "Effect"
            },
            {
                "id": 3317,
                "description": "",
                "slug": "game",
                "name": "Game"
            },
            {
                "id": 1,
                "description": "",
                "slug": "other",
                "name": "Other"
            },
            {
                "id": 75,
                "description": "",
                "slug": "sampler",
                "name": "Sampler"
            },
            {
                "id": 76,
                "description": "",
                "slug": "sequencer",
                "name": "Sequencer"
            },
            {
                "id": 372,
                "description": "",
                "slug": "sound",
                "name": "Sound"
            },
            {
                "id": 74,
                "description": "",
                "slug": "synthesizer",
                "name": "Synthesizer"
            },
            {
                "id": 117,
                "description": "",
                "slug": "utility",
                "name": "Utility"
            },
            {
                "id": 91,
                "description": "",
                "slug": "video",
                "name": "Video"
            }
        ]

    def generate_token(self, username: str, password: str):
        """Authentication process for PS API upload access."""
        r = http.request(
            "POST",
            self.url + 'auth/token',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({'username': username, 'password': password})
        )
        if r.status == 200:
            self.api_token = json.loads(r.data)['token']

    def auth_token(self):
        """Checks if current token is still valid."""
        assert self.api_token is not None

        r = http.request(
            "POST",
            self.url + 'auth/token/validate',
            headers={
                'Authorization': 'Bearer ' + self.api_token,
                'Content-Type': 'application/json'
            }
        )

        return r.status

    def upload_file(self, path: str, file_type=0):
        """Attempts to upload a file to the PS API.
        Used as a reference input for the patch upload."""

        if file_type == 0:
            assert path.endswith(tuple([".jpg", ".jpeg", ".gif", ".png", ".bmp"]))
        elif file_type == 1:
            # Need a ZOIA-readable filename
            with open(path + '.json', 'rb') as f:
                meta = json.load(f)
            name = meta['files'][0]['filename']
            path = path + ".bin"
        else:
            raise ValueError

        with open(path, 'rb') as f:
            data = f.read()

        if file_type == 1:
            path = name

        # Upload and save the ID
        r = http.request(
            "POST",
            self.url + 'files',
            fields={"file": (path, data)},
            headers={
                'Authorization': 'Bearer ' + self.api_token,
            }
        )

        return r
        # if r.status == 201:
        #     idx = json.loads(r.data)['id']
        #     return idx

    def upload_patch(self, path: str, artwork_file_id: int, patch_file_id: int, lic_id: int):

        if self.api_token is None:
            raise ValueError('Not authenticated')

        with open(path + '.json', 'rb') as f:
            meta = json.load(f)

        # Assign category ID if it's not there
        for cat in meta['categories']:
            if "id" not in cat.keys():
                cat['id'] = [x['id'] for x in self.categories if x['name'] == cat['name']][0]

        # Patch upload, combines previous POSTs into final request
        r = http.request(
            "POST",
            self.url + 'patches',
            body=json.dumps({
                "title": meta['title'],
                "content": meta['content'],
                "revision": "1.0",
                "files": [patch_file_id],
                "artwork": artwork_file_id,
                "categories": [x['id'] for x in meta['categories']],
                "tags": [x['name'].replace(' ', '-') for x in meta['tags']],
                "license": lic_id,
                "platform": 3003,
                "state": 151,
            }),
            headers={
              'Authorization': 'Bearer ' + self.api_token,
              'Content-Type': 'application/json'
            }
        )

        return r
        # if r.status == 201:
        #     return json.loads(r.data)['id']
        # else:
        #     return vars(r)

    def get_all_patch_data_init(self):
        """Retrieves the initial amount of information needed for
        display purposes once the user starts the application.

        return: A list of data, where each item contains the
                 information outlined above.
        """

        per_page = 100
        search = {"per_page": per_page}

        all_patches = []

        for page in range(1, math.ceil(self.patch_count / per_page) + 1):
            # Get all the patches on the current page.
            all_patches.extend(self._search({**search, **{"page": page}}))

        return all_patches

    def get_potential_updates(self, meta):
        """Queries the PS API for all patches that have an updated_at
        attribute that is more recent than the one present for patches
        that have been previously downloaded.

        meta: An array containing the id and updated_at attributes for
              patches that may need to be updated.

        return: An array containing the metadata and binaries for all
                 patches that had been updated.
        """

        new_bin = []

        for entry in meta:
            idx = str(entry["id"])
            curr_meta = self.get_patch_meta(idx)
            # Check to see if the patch has been updated by comparing
            # the dates.
            if curr_meta["updated_at"] > entry["updated_at"]:
                new_bin.append((self.download(idx), curr_meta))

        return new_bin

    def get_newest_patches(self, pch_num):
        """Queries the PS API for the latest patches that have not been
        stored in data.json previously. This is only called after the
        initial launch of the application and only if new patches have
        been uploaded to PS since that initial launch.

        pch_num: The number of patches currently stored in data.json

        return: A list of patch metadata that was not present in the
                data.json file.
        """

        # Max on per_page is 100, so we can't go over that.
        per_page = self.patch_count - pch_num
        if per_page > 100:
            per_page = 100
        search = {"per_page": per_page}

        new_patches = []
        pages = 2
        # Find out how many pages of patches there are.
        if per_page == 100:
            pages = math.ceil((self.patch_count - pch_num) / 100) + 1

        # Query for each page of patches we need to retrieve.
        if pages == 2:
            return self._search({**search, **{"page": 1}})
        else:
            for i in range(1, pages):
                new_patches.extend(self._search({**search, **{"page": i}}))
            return new_patches

    def _patch_count(self):
        endpoint = os.path.join(self.url, "patches/")

        # get param dict
        params = {
            "page": 1,
            "per_page": 1,
            "order": "desc",
            "orderby": "date",
            "platforms": self.platform,
        }

        # make request
        url = str(furl(endpoint).add(params))
        r = http.request("GET", url)

        # int(r.headers['X-WP-TotalPages'])
        return int(r.headers['X-WP-Total'])

    # @staticmethod
    # def _determine_patch_count():
    #     """
    #     Deprecated, see _patch_count function above for new method.
    #
    #     Determines the number of ZOIA patches that
    #     are currently being stored on PS.
    #     Does not count questions as patches.
    #
    #     return: An integer representing the total of ZOIA patches.
    #     """
    #
    #     # Hi PS, yes we are a normal Firefox browser and not a program.
    #     soup_patch = BeautifulSoup(
    #         http.request(
    #             "GET",
    #             "https://patchstorage.com/",
    #             headers={"User-Agent": "Mozilla/5.0"}
    #         ).data,
    #         features="html.parser",
    #     )
    #     found_pedals = soup_patch.find_all(
    #         class_="d-flex flex-column " "justify-content-center"
    #     )
    #
    #     """ Convert the ResultSet to a string so we can split on what we are
    #     looking for. The PS website does not have unique div names, so this
    #     is to workaround that.
    #     """
    #     zoia = (
    #         unicode.join(u"\n", map(unicode, found_pedals))
    #         .split("ZOIA", 1)[1]
    #         .split("<strong>", 1)[1]
    #     )
    #
    #     # For some reason, questions posted on PS count as "patches",
    #     # so we need to figure out the # of questions.
    #     soup_ques = BeautifulSoup(
    #         http.request(
    #             "GET",
    #             "https://patchstorage.com/platform/zoia/?search_query=&ptype"
    #             "%5B%5D=question&tax_platform=zoia&tax_post_tag=&orderby"
    #             "=modified&wpas_id=search_form&wpas_submit=1",
    #             headers={"User-Agent": "Mozilla/5.0"},
    #         ).data,
    #         features="html.parser",
    #     )
    #
    #     # Return the total minus the number of questions found.
    #     return int(zoia.split("<")[0]) - len(soup_ques.find_all(class_="card"))
