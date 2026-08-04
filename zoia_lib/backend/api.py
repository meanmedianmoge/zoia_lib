import json
import math
import re

import certifi
import urllib3
from furl import furl

# Fail fast instead of blocking the UI indefinitely when PatchStorage
# is slow or unreachable; transient 5xx responses are retried with a
# short backoff.
http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=5.0, read=30.0),
    retries=urllib3.Retry(total=2, backoff_factor=0.5, status_forcelist=(502, 503, 504)),
)

# The licenses and categories lists are resolved on first use, which happens on
# the UI thread the first time an upload dialog is opened, and a bundled
# snapshot takes over whenever the request does not work out. Nothing waits on
# them, so they do not inherit the pool's generous timeout or its two retries:
# unreachable, they would otherwise freeze the interface for well over a minute
# before falling back.
TAXONOMY_TIMEOUT = urllib3.Timeout(connect=2.0, read=3.0)


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
        self.platform = 3003  # 3003 ZOIA 8271 H90
        self.api_token = None
        self.api_usr = None
        # None signals that PatchStorage could not be reached; callers
        # use refresh_patch_count() to retry once connectivity returns.
        self.patch_count = None
        try:
            self.patch_count = self._patch_count()
        except Exception:
            # No internet connection.
            pass
        # Resolved on first use so startup makes one request, not three.
        self._licenses = None
        self._categories = None

    @property
    def licenses(self):
        """The list of licenses, fetched once on first use."""

        if self._licenses is None:
            self._licenses = self._get_license_data()
        return self._licenses

    @property
    def categories(self):
        """The list of categories, fetched once on first use."""

        if self._categories is None:
            self._categories = self._get_categories_data()
        return self._categories

    @staticmethod
    def _is_valid_taxonomy(data):
        """Checks that a live licenses/categories payload carries the
        id/name pairs the rest of the application indexes by. Without
        this the bundled snapshot would be replaced by data of an
        unknown shape and the failure would only surface later, when a
        patch is uploaded.

        return: True if the payload is safe to use, False otherwise.
        """

        return (
            isinstance(data, list)
            and bool(data)
            and all(
                isinstance(x, dict) and "id" in x and "name" in x for x in data
            )
        )

    def refresh_patch_count(self):
        """Returns the number of ZOIA patches on PatchStorage,
        querying the API again if the count could not be retrieved
        previously (e.g., the application started while offline).

        raise: urllib3.exceptions.HTTPError if PatchStorage cannot
               be reached.

        return: The patch count as an int.
        """

        if self.patch_count is None:
            self.patch_count = self._patch_count()
        return self.patch_count

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
        endpoint = self.url + "patches/"

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
        endpoint = self.url + "patches/{}/".format(idx)

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
            r = http.request("GET", str(body["files"][0]["url"]))
            if r.status != 200:
                return None
            return r.data, body
        except KeyError:
            # No patch with the supplied id was found.
            return None

    def _get_license_data(self):
        """Get list of licenses, preferring the live PS API and
        falling back to a bundled snapshot when it is unreachable or
        answers with an unexpected shape."""

        try:
            r = http.request(
                "GET",
                self.url + "licenses/?per_page=100",
                timeout=TAXONOMY_TIMEOUT,
                retries=False,
            )
            if r.status == 200:
                data = json.loads(r.data)
                if self._is_valid_taxonomy(data):
                    return data
        except Exception:
            pass

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
        """Get list of categories, preferring the live PS API and
        falling back to a bundled snapshot when it is unreachable or
        answers with an unexpected shape."""

        try:
            r = http.request(
                "GET",
                self.url + "categories/?per_page=100",
                timeout=TAXONOMY_TIMEOUT,
                retries=False,
            )
            if r.status == 200:
                data = json.loads(r.data)
                if self._is_valid_taxonomy(data):
                    return data
        except Exception:
            pass

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
        """Authentication process for PS API upload access.

        return: True if a token was successfully generated,
                False otherwise.
        """
        r = http.request(
            "POST",
            self.url + 'auth/token',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({'username': username, 'password': password})
        )
        if r.status == 200:
            self.api_token = json.loads(r.data)['token']
            self.api_usr = username
            return True
        return False

    def auth_token(self):
        """Checks if current token is still valid."""
        if self.api_token is None:
            raise ValueError('Not authenticated')

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
            if not path.endswith((".jpg", ".jpeg", ".gif", ".png", ".bmp")):
                raise ValueError("Unsupported artwork format: {}".format(path))
        elif file_type == 1:
            # Need a ZOIA-readable filename
            with open(path + '.json', 'rb') as f:
                meta = json.load(f)
            name = meta['files'][0]['filename']
            path = path + ".bin"
        else:
            raise ValueError("Unknown file_type: {}".format(file_type))

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
                "title": meta['title'].ljust(5),
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

    def update_patch(self, idx: str, path: str, artwork_id=None, patch_id=None, license_id=None):

        if self.api_token is None:
            raise ValueError('Not authenticated')

        with open(path + '.json', 'rb') as f:
            meta = json.load(f)

        # Assign category ID if it's not there
        for cat in meta['categories']:
            if "id" not in cat.keys():
                cat['id'] = [x['id'] for x in self.categories if x['name'] == cat['name']][0]

        # Bump the revision for the updated upload.
        new_ver = self._next_revision(meta['revision'])

        # Get list of id's to update with
        art_id = artwork_id if 'id' not in meta['artwork'] else meta['artwork']['id']
        pch_id = [patch_id] if patch_id else [meta['files'][0]['id']]
        lic_id = license_id if not meta['license'] else meta['license']['id']

        # Patch upload, combines previous POSTs into final request
        r = http.request(
            "PUT",
            self.url + 'patches/{}'.format(idx),
            body=json.dumps({
                "title": meta['title'].ljust(5),
                "content": meta['content'],
                "revision": new_ver,
                "files": pch_id,
                "artwork": art_id,
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

    @staticmethod
    def _next_revision(revision):
        """Computes the next revision string with a modest increment,
        e.g. "2.3" -> "2.31". Revisions carrying three or more
        components increment their last component instead, e.g.
        "1.2.3" -> "1.2.4", so that no component is dropped. Defaults
        to "1.01" when the current revision contains no number.

        revision: The current revision string of the patch.

        return: The bumped revision string.
        """

        parts = re.findall(r"\d+", revision or "")
        if not parts:
            return "1.01"
        if len(parts) > 2:
            return ".".join(parts[:-1] + [str(int(parts[-1]) + 1)])
        return "{:.2f}".format(float(".".join(parts)) + 0.01)

    def get_all_patch_data_init(self):
        """Retrieves the initial amount of information needed for
        display purposes once the user starts the application.

        return: A list of data, where each item contains the
                 information outlined above.
        """

        per_page = 100
        search = {"per_page": per_page}

        all_patches = []

        for page in range(1, math.ceil(self.refresh_patch_count() / per_page) + 1):
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
        patch_count = self.refresh_patch_count()
        per_page = patch_count - pch_num
        if per_page > 100:
            per_page = 100
        search = {"per_page": per_page}

        new_patches = []
        pages = 2
        # Find out how many pages of patches there are.
        if per_page == 100:
            pages = math.ceil((patch_count - pch_num) / 100) + 1

        # Query for each page of patches we need to retrieve.
        if pages == 2:
            return self._search({**search, **{"page": 1}})
        else:
            for i in range(1, pages):
                new_patches.extend(self._search({**search, **{"page": i}}))
            return new_patches

    def _patch_count(self):
        """Queries the PS API for the number of ZOIA patches it hosts.

        raise: urllib3.exceptions.HTTPError if PatchStorage did not
               answer with a usable count.

        return: The patch count as an int.
        """

        endpoint = self.url + "patches/"

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

        # A 5xx page, a login redirect or any other non-patch response
        # completes the request but carries no count. Report that as an
        # HTTP failure rather than letting a KeyError escape, so callers
        # can treat every unreachable-API case the same way.
        if r.status != 200:
            raise urllib3.exceptions.HTTPError(
                "PatchStorage returned HTTP {}".format(r.status)
            )
        try:
            # int(r.headers['X-WP-TotalPages'])
            return int(r.headers["X-WP-Total"])
        except (KeyError, TypeError, ValueError):
            raise urllib3.exceptions.HTTPError(
                "PatchStorage response carried no usable patch count"
            )
