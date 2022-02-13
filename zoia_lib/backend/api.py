import json
import math
import os

import certifi
import urllib3
from bs4 import BeautifulSoup
from furl import furl
from numpy.compat import unicode

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
        self.url = "https://patchstorage.com/api/alpha/"
        self.platform = 3003  # ZOIA
        try:
            self.patch_count = self._determine_patch_count()
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

        return json.loads(r.data)

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

    @staticmethod
    def _determine_patch_count():
        """Determines the number of ZOIA patches that
        are currently being stored on PS.
        Does not count questions as patches.

        return: An integer representing the total of ZOIA patches.
        """

        # Hi PS, yes we are a normal Firefox browser and not a program.
        soup_patch = BeautifulSoup(
            http.request(
                "GET",
                "https://patchstorage.com/",
                headers={"User-Agent": "Mozilla/5.0"}
            ).data,
            features="html.parser",
        )
        found_pedals = soup_patch.find_all(
            class_="d-flex flex-column " "justify-content-center"
        )

        """ Convert the ResultSet to a string so we can split on what we are 
        looking for. The PS website does not have unique div names, so this
        is to workaround that.
        """
        zoia = (
            unicode.join(u"\n", map(unicode, found_pedals))
            .split("ZOIA", 1)[1]
            .split("<strong>", 1)[1]
        )

        # For some reason, questions posted on PS count as "patches",
        # so we need to figure out the # of questions.
        soup_ques = BeautifulSoup(
            http.request(
                "GET",
                "https://patchstorage.com/platform/zoia/?search_query=&ptype"
                "%5B%5D=question&tax_platform=zoia&tax_post_tag=&orderby"
                "=modified&wpas_id=search_form&wpas_submit=1",
                headers={"User-Agent": "Mozilla/5.0"},
            ).data,
            features="html.parser",
        )

        # Return the total minus the number of questions found.
        return int(zoia.split("<")[0]) - len(soup_ques.find_all(class_="card"))
