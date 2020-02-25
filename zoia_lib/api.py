# -*- coding: utf-8 -*-
"""
Created: 9:47 PM on 2/23/20
Author: Mike Moger
Usage: 
"""

import requests


# https://patchstorage.com/docs/
def get_patch():

    base_url = 'https://patchstorage.com/api/alpha/patches/'
    res = requests.get(
        url=base_url,
        params=[('author', 'Christopher H. M. Jacques')],
    )

    return res
