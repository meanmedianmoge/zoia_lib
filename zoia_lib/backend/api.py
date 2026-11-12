import json
import io
import zipfile
import rarfile
import math
import os
import re

import certifi
import urllib3
from furl import furl

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED", ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=5, read=30),
    retries=urllib3.Retry(total=2, backoff_factor=0.5,
                         allowed_methods=frozenset(['GET', 'HEAD']),
                         status_forcelist=(500, 502, 503, 504)),
)


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
        self.licenses = self._get_license_data()
        self.categories = self._get_categories_data()
        self.patch_count = None
        # Resolve the count on first use; importing backend modules is offline.

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

        if r.status != 200:
            raise urllib3.exceptions.HTTPError(f"Patch search returned HTTP {r.status}")
        result = json.loads(r.data)
        if not isinstance(result, list):
            raise ValueError("PatchStorage returned an invalid patch list.")
        return result

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
            response = http.request("GET", str(body["files"][0]["url"]))
            if response.status != 200:
                raise urllib3.exceptions.HTTPError(f"Patch download returned HTTP {response.status}")
            return response.data, body
        except (KeyError, IndexError):
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
            artwork_types = {
                ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".png": "image/png", ".bmp": "image/bmp",
            }
            content_type = artwork_types.get(os.path.splitext(path)[1].lower())
            if content_type is None:
                raise ValueError("Unsupported artwork format")
        elif file_type == 1:
            content_type = "application/octet-stream"
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
            # Avoid MIME guessing, which reads system files inaccessible
            # inside the macOS app sandbox (including /etc/apache2/mime.types).
            fields={"file": (os.path.basename(path), data, content_type)},
            timeout=urllib3.Timeout(connect=10, read=60),
            retries=False,
            headers={
                'Authorization': 'Bearer ' + self.api_token,
            }
        )

        return r
        # if r.status == 201:
        #     idx = json.loads(r.data)['id']
        #     return idx

    @staticmethod
    def next_revision(revision):
        """Increment the final numeric component without float conversion."""
        match = re.fullmatch(r"(v?)([0-9]+(?:\.[0-9]+)*)", str(revision).strip())
        if not match:
            raise ValueError(f"Cannot increment revision {revision!r}; use a numeric dotted revision.")
        parts = match[2].split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return match[1] + '.'.join(parts)

    @staticmethod
    def _editable_metadata(meta):
        return (
            meta.get('title', '').strip(), meta.get('content', '').strip(),
            sorted(x['name'] for x in meta.get('categories', [])),
            sorted(x['name'].lower().replace(' ', '-') for x in meta.get('tags', [])),
            meta.get('license', {}).get('id') if meta.get('license') else None,
        )

    def prepare_patch_update(self, idx, path):
        """Compare local data with the current server version without writing."""
        remote = self.get_patch_meta(idx)
        with open(path + '.json', 'r') as source:
            local = json.load(source)
        with open(path + '.bin', 'rb') as source:
            binary = source.read()
        filename = os.path.basename(local['files'][0]['filename'])
        files = remote['files']
        matches = [f for f in files if os.path.basename(f['filename']) == filename]
        if len(matches) == 1:
            remote_file = matches[0]
        elif len(files) == 1:
            remote_file = files[0]
        else:
            raise ValueError("Cannot identify the published file to compare.")
        response = http.request(
            "GET", remote_file['url'],
            timeout=urllib3.Timeout(connect=10, read=60), retries=False,
        )
        if response.status != 200:
            raise ValueError(f"Could not check published binary (HTTP {response.status}).")
        extension = os.path.splitext(remote_file['filename'])[1].lower()
        bundled_binaries = 1
        if extension == '.bin':
            published = response.data
        elif extension in ('.zip', '.rar'):
            archive_type = zipfile.ZipFile if extension == '.zip' else rarfile.RarFile
            with archive_type(io.BytesIO(response.data)) as archive:
                candidates = [info for info in archive.infolist()
                              if info.filename.lower().endswith('.bin')]
                bundled_binaries = len(candidates)
                matching = [info for info in candidates
                            if os.path.basename(info.filename) == filename]
                if len(matching) == 1:
                    candidate = matching[0]
                elif len(candidates) == 1:
                    candidate = candidates[0]
                else:
                    raise ValueError("Cannot identify the patch binary inside the published archive.")
                if candidate.file_size > 64 * 1024 * 1024:
                    raise ValueError("Published patch binary exceeds the comparison size limit.")
                published = archive.read(candidate)
        else:
            raise ValueError("Unsupported published patch file format.")
        if binary != published and (len(files) > 1 or bundled_binaries > 1):
            raise ValueError("This patch contains multiple published files or binaries. Update the complete bundle on PatchStorage to preserve its other files.")
        return {
            'remote': remote,
            'binary_changed': binary != published,
            'metadata_changed': self._editable_metadata(local) != self._editable_metadata(remote),
        }

    def patch_binary_changed(self, idx, path):
        return self.prepare_patch_update(idx, path)['binary_changed']

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
        # if r.status == 201:
        #     return json.loads(r.data)['id']
        # else:
        #     return vars(r)

    def update_patch(self, idx: str, path: str, artwork_id=None, patch_id=None, license_id=None, remote_meta=None):

        if self.api_token is None:
            raise ValueError('Not authenticated')

        with open(path + '.json', 'rb') as f:
            meta = json.load(f)

        # Assign category ID if it's not there
        for cat in meta['categories']:
            if "id" not in cat.keys():
                cat['id'] = [x['id'] for x in self.categories if x['name'] == cat['name']][0]

        remote = remote_meta if remote_meta is not None else self.get_patch_meta(idx)
        new_ver = self.next_revision(remote['revision']) if patch_id is not None else remote['revision']

        # Get list of id's to update with
        art_id = artwork_id if 'id' not in meta['artwork'] else meta['artwork']['id']
        pch_id = [patch_id] if patch_id is not None else [f['id'] for f in remote['files']]
        lic_id = license_id if not meta['license'] else meta['license']['id']

        # Patch upload, combines previous POSTs into final request
        r = http.request(
            "PUT",
            self.url + 'patches/{}'.format(idx),
            timeout=urllib3.Timeout(connect=10, read=60),
            retries=False,
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
        per_page = self.refresh_patch_count() - pch_num
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
