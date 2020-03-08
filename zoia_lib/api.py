# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage: https://patchstorage.com/docs/
"""

import os
import requests


class PatchStorage:

    def __init__(self):
        """initializes PatchStorage class"""

        # set defaults for query params
        self.url = 'https://patchstorage.com/api/alpha'
        self.platform = 'zoia'  # PS stores platforms with an integer, unsure which one maps to zoia

    def endpoint(self,
                 endpoint: str):
        """specify endpoint for query"""

        return os.path.join(self.url, endpoint)

    def get_patch(self,
                  download: bool = True):
        """get Patch object"""

        endpoint = self.endpoint('patches')

        patch = requests.get(url=endpoint,
                             params=[('platform', self.platform)]
                             ).json()
        idx = str(patch.id)

        if download:
            return requests.get(url=os.path.join(endpoint, idx)).json().files[0].url
        else:
            return idx


def get_patch():

    base_url = 'https://patchstorage.com/api/alpha/patches/'
    res = requests.get(
        url=base_url,
        params=[('author', 'Christopher H. M. Jacques')],
    )

    return res
