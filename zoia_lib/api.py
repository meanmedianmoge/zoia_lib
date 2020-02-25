# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage: 
"""

import os
import requests


class PatchStorage:

    def __init__(self):
        """initializes PatchStorage class"""

        # set defaults for query params
        self.url = 'https://patchstorage.com/api/alpha'
        self.platform = 'zoia'

    def endpoint(self,
                 endpoint: str):
        """specify endpoint for query"""

        return os.path.join(self.url, endpoint)

    def get_patch(self,
                  **kwargs):
        """get Patch object"""

        patch = requests.get(url=self.endpoint('patches'),
                             params=[('platform', self.platform)],
                             **kwargs).json()

        idx = str(patch.id)

        mn = self.endpoint('patches')
        dl = requests.get(url=os.path.join(mn, idx)).json().files.url

        return dl

# https://patchstorage.com/docs/


def get_patch():

    base_url = 'https://patchstorage.com/api/alpha/patches/'
    res = requests.get(
        url=base_url,
        params=[('author', 'Christopher H. M. Jacques')],
    )

    return res
