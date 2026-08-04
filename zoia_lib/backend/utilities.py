import json
import os
import re
import sys
import _thread as thread
import threading

from zoia_lib.common import errors


def merge_patch_metadata(new_patches, known):
    """Merges freshly retrieved PS metadata into the metadata already
    cached in data.json.

    Pages are retrieved in blocks of 100, so the newest block can
    overlap with patches that are already cached. Where both carry the
    same patch the freshly retrieved copy wins; resolving the other way
    would pin the cached copy and a patch updated on PatchStorage could
    never refresh its metadata.

    new_patches: The metadata just retrieved from PatchStorage.
    known: The metadata previously stored in data.json.

    return: A list holding the new metadata followed by the cached
            metadata it did not supersede.
    """

    fresh = {x["id"] for x in new_patches}
    return new_patches + [x for x in known if x["id"] not in fresh]


def sort_metadata(mode, data, rev):
    """Sort an array of metadata based on the passed parameters.

    mode: The method in which the data will be sorted. Valid modes are:
          - 1 -> Sort by title
          - 2 -> Sort by author
          - 3 -> Sort by like count
          - 4 -> Sort by download count
          - 5 -> Sort by view count
          - 6 -> Sort by date modified
          - 7 -> Sort by revision
          - 8 -> Sort by rating (local and folder tabs only)
          - 9 -> Sort by category
          - 10 -> Sort by tag
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
        raise errors.SortingError(mode, 903)
    if mode < 1 or mode > 10:
        raise errors.SortingError(mode, 901)
    if not isinstance(data, list):
        raise errors.SortingError(data, 902)

    if mode == 1:
        # Sort by title
        data.sort(key=lambda x: x["title"].upper(), reverse=rev)
    elif mode == 2:
        # Sort by author
        data.sort(
            key=lambda x: x["author"]["name"].upper() if "author" in x else "",
            reverse=rev,
        )
    elif mode == 3:
        # Sort by like count.
        data.sort(
            key=lambda x: x["like_count"] if "like_count" in x else 0, reverse=rev
        )
    elif mode == 4:
        # Sort by download count.
        data.sort(
            key=lambda x: x["download_count"] if "download_count" in x else 0,
            reverse=rev,
        )
    elif mode == 5:
        # Sort by view count.
        data.sort(
            key=lambda x: x["view_count"] if "view_count" in x else 0, reverse=rev
        )
    elif mode == 6:
        # Sort by date modified. Local metadata carries downloaded_at,
        # PS metadata carries updated_at; a mixed list is sorted on
        # whichever each entry has, instead of aborting mid-sort on
        # the first entry that lacks the key.
        data.sort(
            key=lambda x: x.get("downloaded_at", x.get("updated_at", "")),
            reverse=rev,
        )
    elif mode == 7:
        # Sort by revision #
        data.sort(key=lambda x: x["revision"] if "revision" in x else 0, reverse=rev)
    elif mode == 8:
        # Sort by rating (local and folder tabs only)
        data.sort(key=lambda x: x["rating"] if "rating" in x else 0, reverse=rev)
    elif mode == 9:
        # Sort by category
        data.sort(
            key=lambda x: ", ".join(y["name"] for y in x["categories"]), reverse=rev
        )
    elif mode == 10:
        # Sort by tag
        data.sort(
            key=lambda x: ", ".join(
                y["name"].lower().replace("#", "") for y in x["tags"]
            ),
            reverse=rev,
        )


def search_patches(data, query):
    """Search an array of metadata based on the passed parameters. The
    search will attempt to match results using a wildcard regex system.

    data: An array of metadata that is to be searched through.
    query: The search term for the current search.

    raise: SearchingError if the parameters are None or data is
           not of type list.

    return: An array of metadata containing the data that matches the
            search query.
    """

    # Input checking.
    if query is None or data is None:
        raise errors.SearchingError(query, 1002)
    if not isinstance(data, list):
        raise errors.SearchingError(query, 1001)

    query = query.lower()

    if not query:
        # Every patch matches an empty query, so there is nothing to
        # rank; return them in their existing order.
        return list(data)

    hits = []
    # Track hits by object identity; comparing whole metadata dicts
    # against the hit list made the search quadratic.
    seen = set()

    def add_hit(entry):
        hits.append(entry)
        seen.add(id(entry))

    # Category matches are prioritized. Note the direction of the
    # match: the category has to start with the query, so "synt" ranks
    # Synthesizer patches first, but a query merely contained in a
    # category name (e.g. "o") no longer reorders the results. The
    # names are read from the patches themselves, so a category added
    # on PatchStorage is picked up without editing this file.
    for curr in data:
        # Check category tag.
        for category in curr.get("categories", []):
            if category["name"].lower().startswith(query):
                add_hit(curr)
                break

    for curr in data:
        if id(curr) in seen:
            continue
        # Check the patch title.
        if query in curr["title"].lower():
            add_hit(curr)
            continue
        # Check the version title (local and folders tab only).
        if "files" in curr:
            try:
                version = (
                    curr["files"][0]["filename"]
                    .split(".")[0]
                    .split("_zoia_")[-1]
                    .replace("_", " ")
                    .lower()
                )
            except (KeyError, IndexError):
                version = None
            if version is not None and query in version:
                add_hit(curr)
                continue
        # Check the author.
        if "author" in curr and query in curr["author"]["name"].lower():
            add_hit(curr)
            continue
        # Check every tag.
        if any(query in tag["name"].lower() for tag in curr.get("tags", [])):
            add_hit(curr)
            continue
        # Check dates.
        if "updated_at" in curr and query in curr["updated_at"].lower():
            add_hit(curr)
            continue
        if "created_at" in curr and query in curr["created_at"].lower():
            add_hit(curr)

    return hits


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", string_)]


def hide_dotted_files(path, sd: bool = False):
    """Removes hidden files from a list of files in a directory.

    directory: List of files.
    sd: Option to exclude preceding path in list of files.

    return: List of files without hidden files.
    """

    files = []
    for item in sorted(os.listdir(path)):
        if not item.startswith(".") and os.path.isfile(os.path.join(path, item)):
            if not sd:
                files.append(os.path.join(path, item))
            else:
                files.append(item)

    if not sd:
        return files[::-1]
    else:
        return sorted(files[::-1])


def remove_empty_patches(path):
    """Removes empty ZOIA patches from a list of files in a directory.

    directory: List of files.
    sd: Option to exclude preceding path in list of files.

    return: List of files without empty patches.
    """

    files = []
    for item in sorted(path):
        if not item.endswith('_zoia_.bin'):
            files.append(item)

    return files[::-1]


def generate_blank_patch():
    """Creates a blank patch to be used in the export process
    to fill any empty slots.

    return: Bytes data.
    """

    return b"\t" + b"\x00" * 32767


def meipass(resource, is_ui=False):
    """Helper function for the UI to find resource files."""

    if is_ui:
        resource = str(resource).split("/")[-1]
        bundle_dir = getattr(
            sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__))
        )
        file_path = os.path.abspath(os.path.join(bundle_dir, resource))
        return file_path
    else:
        return resource


def add_test_patch(name, idx, path):
    """Note: This method is for testing purposes only.
    Adds a test patch that can be used for unit testing purposes.

    name: The name of the patch, to be used for the title attribute
          in the JSON metadata.
    idx: The id number to be used for the patch.
    path: The path where the test patch will be located.
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


def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    print("{0} took too long".format(fn_name), file=sys.stderr)
    sys.stderr.flush()  # Python 3 stderr is likely buffered.
    thread.interrupt_main()  # raises KeyboardInterrupt


def exit_after(s):
    """Use as decorator to exit process if
    function takes longer than s seconds.
    """

    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer
