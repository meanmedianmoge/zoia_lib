import json
import os

from zoia_lib.common import errors


def sort_metadata(mode, data, rev):
    """ Sort an array of metadata based on the passed parameters.

    mode: The method in which the data will be sorted. Valid modes are:
          - 1 -> Sort by title
          - 2 -> Sort by author
          - 3 -> Sort by like count
          - 4 -> Sort by download count
          - 5 -> Sort by view count
          - 6 -> Sort by date modified (updated_at attribute)
          - 7 -> Sort by revision
    data: An array of metadata that is to be sorted.
    inc: True if the data should be sorted in reverse,
         false otherwise.
    """

    """ The use of .upper() is to prevent sorting of lower case names 
    before their uppercase counterparts, especially when they share the 
    same initial letter. In a list, you would want all the "d" titles 
    grouped together.
    """
    # Input checking.
    if mode is None or data is None or rev is None:
        # TODO replace with an error.
        return None
    if mode < 1 or mode > 7:
        raise errors.SortingError(mode, 901)
    if not isinstance(data, list):
        raise errors.SortingError(data, 902)

    if mode == 1:
        # Sort by title
        data.sort(key=lambda x: x["title"].upper(), reverse=rev)
    elif mode == 2:
        # Sort by author
        data.sort(key=lambda x: x["author"]["name"].upper()
        if "author" in x else "", reverse=rev)
    elif mode == 3:
        # Sort by like count.
        data.sort(key=lambda x: x["like_count"] if "like_count" in x else 0,
                  reverse=rev)
    elif mode == 4:
        # Sort by download count.
        data.sort(key=lambda x: x["download_count"]
        if "download_count" in x else 0, reverse=rev)
    elif mode == 5:
        # Sort by view count.
        data.sort(key=lambda x: x["view_count"] if "view_count" in x else 0,
                  reverse=rev)
    elif mode == 6:
        # Sort by date modified
        data.sort(key=lambda x: x["updated_at"].upper(), reverse=rev)
    elif mode == 7:
        # Sort by revision #
        data.sort(key=lambda x: x["revision"] if "revision" in x else 0,
                  reverse=rev)


def search_patches(data, query):
    """ Search an array of metadata based on the passed parameters. The
    search will attempt to match results using a wildcard regex system.

    data: An array of metadata that is to be searched through.
    query: The search term for the current search.
    Returns an array of metadata containing the data that matches the
    search query.
    """

    query = query.lower()

    # Input checking.
    if query is None or data is None:
        # TODO replace with an error.
        return None
    if not isinstance(data, list):
        raise errors.SearchingError(query, 1001)

    hits = []

    # Special case, searching for a category. Since there are a known # of
    # categories, we prioritize these first.
    if query in "composition" or query in "effect" or query in "game" or \
            query in "other" or query in "sampler" or query in "sequencer" or \
            query in "sound" or query in "synthesizer" or query in "utility" \
            or query in "video":
        for curr in data:
            if "categories" in curr:
                # Check category tag.
                for category in curr["categories"]:
                    if query in category["name"].lower():
                        hits.insert(0, curr)
                        break

    for curr in data:
        # Check the patch title.
        if query in curr["title"].lower():
            if curr not in hits:
                hits.append(curr)
            continue
        if "author" in curr:
            # Check the author name.
            if query in curr["author"]["name"].lower():
                if curr not in hits:
                    hits.append(curr)
                continue
        if "tags" in curr:
            # Check every tag.
            for tag in curr["tags"]:
                if query in tag["name"].lower():
                    if curr not in hits:
                        hits.append(curr)
                    continue
        if query in curr["updated_at"].lower():
            if curr not in hits:
                hits.append(curr)
            continue
        if query in curr["created_at"].lower():
            if curr not in hits:
                hits.append(curr)
            continue

    return hits


def add_test_patch(name, idx, path):
    """Note: This method is for testing purposes
    and will be deleted once a release candidate
    is prepared.
    Adds a test patch that can be used for unit
    testing purposes.
    name: The name of the patch, to be used for the title attribute
          in the JSON metadata.
    idx: The id number to be used for the patch.
    """

    if os.path.sep in name:
        dr, name = name.split(os.path.sep)
        pch = os.path.join(path, "{}".format(dr))
    else:
        pch = os.path.join(path, "{}".format(name))

    if not os.path.isdir(pch):
        os.mkdir(pch)

    name_bin = os.path.join(pch, "{}.bin".format(name))
    with open(name_bin, "wb") as f:
        f.write(b"Test")
    name_json = os.path.join(pch, "{}.json".format(name))
    with open(name_json, "w") as jf:
        json.dump({"id": idx, "title": "Test", "created_at": "test"}, jf)
