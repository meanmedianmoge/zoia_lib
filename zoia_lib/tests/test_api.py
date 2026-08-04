import json
import os
import unittest
import unittest.mock as mock

import urllib3

import zoia_lib.backend.api as api


def _make_patch_storage(patch_count=b"2500"):
    """Constructs a PatchStorage instance without touching the network
    so the test suite can run offline.
    """

    with mock.patch("urllib3.PoolManager.request") as request:
        request.return_value = mock.Mock(
            status=200, data=b"[]", headers={"X-WP-Total": patch_count}
        )
        return api.PatchStorage()


def _make_offline_patch_storage():
    """Constructs a PatchStorage instance as if PatchStorage could not
    be reached at startup.
    """

    with mock.patch("urllib3.PoolManager.request") as request:
        request.side_effect = urllib3.exceptions.MaxRetryError(None, "patches/")
        return api.PatchStorage()


ps = _make_patch_storage()


class TestAPI(unittest.TestCase):
    """This class is responsible for testing the various PS API
    queries that need to be made by the application in order to
    function correctly. Currently, it covers the retrieval of patches
    once the application starts and the downloading of patches.

    All HTTP traffic is mocked; the tests never contact PatchStorage.
    """

    def test_api_download_bin(self):
        """Query the PS API for a patch with the .bin extension,
        and ensure that it is in the correct format as dictated by the
        MetadataSchema.json schema.
        """

        # Mock HTTP requests
        with mock.patch('urllib3.PoolManager.request') as mock_request:
            # For invalid IDs, return 404
            mock_request.return_value = mock.Mock(data=b'{"error": "not found"}', status=404)

            # Try to download something that doesn't exist.
            f = ps.download("1111111111")
            self.assertIsNone(f)

            f = ps.download("900000")
            self.assertIsNone(f)

            # Try to pass in None.
            f = ps.download(None)
            self.assertIsNone(f)

            # Mock successful download
            mock_request.side_effect = [
                mock.Mock(data=b'{"files": [{"url": "http://fake.bin"}], "id": 105634, "title": "Test", "author": {"name": "Test"}, "created_at": "2020-01-01", "updated_at": "2020-01-01", "tags": [], "categories": [], "state": "published", "license": {"name": "CC0"}, "custom_license_text": "", "link": "", "content": "", "preview_url": "", "revision": 1, "view_count": 0, "like_count": 0, "download_count": 0}', status=200),
                mock.Mock(data=b'fake bin data', status=200)
            ]

            # Try to actually download a .bin file.
            f = ps.download("105634")
            self.assertIsNotNone(f)
            self.assertTrue(isinstance(f[0], bytes))
            self.assertTrue(isinstance(f[1], dict))

            expected_keys = ["id", "title", "author", "created_at", "updated_at", "tags", "categories", "state", "license", "files", "preview_url", "revision", "view_count", "like_count", "download_count"]
            for key in expected_keys:
                self.assertIn(key, f[1])

    def test_api_download_failed_file_request(self):
        """Ensure that an error response for the binary itself is not
        returned as patch data.
        """

        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.side_effect = [
                mock.Mock(data=b'{"files": [{"url": "http://fake.bin"}], "id": 105634}', status=200),
                mock.Mock(data=b'<html>Service Unavailable</html>', status=503),
            ]

            f = ps.download("105634")
            self.assertIsNone(f)

    def test_api_download_compressed(self):
        """Query the PS API for a compressed patch, and ensure that it is in
        the correct format as dictated by the MetadataSchema.json schema.
        """

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        test_dir = os.path.join(root_dir, "zoia_lib", "tests", "sample_files")
        with open(os.path.join(test_dir, "sampleJSONZIP.json"), "r") as f_json:
            sample_json = json.loads(f_json.read())
        with open(os.path.join(test_dir, "sampleZIPBytes.bin"), "rb") as f_bin:
            sample_bytes = f_bin.read()

        # Mock HTTP requests
        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.side_effect = [
                mock.Mock(data=json.dumps(sample_json).encode("utf-8"), status=200),
                mock.Mock(data=sample_bytes, status=200),
            ]

            # Try to download a zip file.
            f = ps.download("124436")
        self.assertIsNotNone(
            f,
            "Did not retrieve patch data despite the patch "
            "id existing in PatchStorage.",
        )
        self.assertTrue(
            isinstance(f[0], bytes),
            "Returned tuple did not contain binary data in the " "first element.",
        )
        try:
            json.dumps(f[1])
        except ValueError:
            self.fail(
                "Returned tuple did not contain valid json data in the second "
                "element."
            )

        required_keys = [
            "id",
            "link",
            "content",
            "files",
            "preview_url",
            "revision",
            "view_count",
            "like_count",
            "download_count",
            "author",
            "title",
            "created_at",
            "updated_at",
            "tags",
            "categories",
            "state",
            "license",
            "custom_license_text",
        ]
        for key in required_keys:
            self.assertIn(key, f[1], f"Returned data missing '{key}'.")

    def test_next_revision(self):
        """The revision bump should apply a modest numeric increment,
        not a lexicographic jump.
        """

        self.assertEqual(api.PatchStorage._next_revision("2.3"), "2.31")
        self.assertEqual(api.PatchStorage._next_revision("1.0"), "1.01")
        self.assertEqual(api.PatchStorage._next_revision("1.10"), "1.11")
        self.assertEqual(api.PatchStorage._next_revision("3"), "3.01")
        self.assertEqual(api.PatchStorage._next_revision("v2.1"), "2.11")
        self.assertEqual(api.PatchStorage._next_revision(""), "1.01")
        self.assertEqual(api.PatchStorage._next_revision(None), "1.01")
        self.assertEqual(api.PatchStorage._next_revision("beta"), "1.01")

    def test_next_revision_keeps_every_component(self):
        """A three-part revision must not lose its last component to
        the two-part decimal bump.
        """

        self.assertEqual(api.PatchStorage._next_revision("1.2.3"), "1.2.4")
        self.assertEqual(api.PatchStorage._next_revision("v1.2.3"), "1.2.4")
        self.assertEqual(api.PatchStorage._next_revision("1.2.9"), "1.2.10")

    def test_patch_count_reports_http_failure(self):
        """A response that completes but carries no count (a 5xx page,
        an error page, a garbled header) must surface as an HTTP error
        so the UI can treat it like any other unreachable-API case.
        """

        fresh = _make_patch_storage()
        fresh.patch_count = None
        exc = urllib3.exceptions.HTTPError

        responses = [
            mock.Mock(status=500, data=b"<html>error</html>", headers={}),
            mock.Mock(status=200, data=b"[]", headers={}),
            mock.Mock(status=200, data=b"[]", headers={"X-WP-Total": "lots"}),
        ]
        for response in responses:
            with mock.patch("urllib3.PoolManager.request") as mock_request:
                mock_request.return_value = response
                self.assertRaises(exc, fresh.refresh_patch_count)
            self.assertIsNone(fresh.patch_count)

    def test_taxonomy_lists_are_lazy(self):
        """Constructing PatchStorage should make a single request; the
        license/category lists resolve on first use.
        """

        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.return_value = mock.Mock(
                status=200, data=b"[]", headers={"X-WP-Total": "2500"}
            )
            fresh = api.PatchStorage()
            self.assertEqual(mock_request.call_count, 1)

        live = [{"id": 1, "slug": "live", "name": "Live"}]
        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.return_value = mock.Mock(
                status=200, data=json.dumps(live).encode("utf-8")
            )
            self.assertEqual(fresh.licenses, live)
            self.assertEqual(mock_request.call_count, 1)
            # Resolved once, then cached.
            self.assertEqual(fresh.licenses, live)
            self.assertEqual(mock_request.call_count, 1)

    def test_taxonomy_rejects_unexpected_shape(self):
        """A live payload without the id/name pairs the application
        indexes by must fall back to the bundled snapshot instead of
        failing later, at upload time.
        """

        fresh = _make_patch_storage()

        for payload in (b'["effect", "utility"]', b'{"error": "nope"}', b"[]"):
            fresh._categories = None
            with mock.patch("urllib3.PoolManager.request") as mock_request:
                mock_request.return_value = mock.Mock(status=200, data=payload)
                categories = fresh.categories
            self.assertTrue(any(x["slug"] == "effect" for x in categories))
            # The bundled snapshot is what update_patch() indexes into.
            self.assertTrue(all("id" in x and "name" in x for x in categories))

    def test_offline_start_falls_back_to_bundled_data(self):
        """When PatchStorage cannot be reached at startup, the patch
        count is None and the bundled license/category snapshots are
        used.
        """

        offline_ps = _make_offline_patch_storage()

        self.assertIsNone(offline_ps.patch_count)
        self.assertTrue(any(x["slug"] == "mit" for x in offline_ps.licenses))
        self.assertTrue(any(x["slug"] == "effect" for x in offline_ps.categories))

    def test_refresh_patch_count_recovers_after_offline_start(self):
        """An instance created while offline should pick up the patch
        count once connectivity returns.
        """

        offline_ps = _make_offline_patch_storage()
        self.assertIsNone(offline_ps.patch_count)

        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.return_value = mock.Mock(
                status=200, data=b"[]", headers={"X-WP-Total": "1234"}
            )
            self.assertEqual(offline_ps.refresh_patch_count(), 1234)
        self.assertEqual(offline_ps.patch_count, 1234)

    def test_generate_token_reports_success(self):
        """generate_token should signal whether authentication worked
        instead of failing silently.
        """

        fresh = _make_patch_storage()

        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.return_value = mock.Mock(status=403, data=b"{}")
            self.assertFalse(fresh.generate_token("usr", "bad-password"))
        self.assertIsNone(fresh.api_token)

        with mock.patch("urllib3.PoolManager.request") as mock_request:
            mock_request.return_value = mock.Mock(
                status=200, data=b'{"token": "abc123"}'
            )
            self.assertTrue(fresh.generate_token("usr", "good-password"))
        self.assertEqual(fresh.api_token, "abc123")
        self.assertEqual(fresh.api_usr, "usr")

    def test_auth_token_requires_authentication(self):
        """Validating a token without having generated one is an
        error, not an assert.
        """

        fresh = _make_patch_storage()
        self.assertRaises(ValueError, fresh.auth_token)

    def test_upload_file_input_validation(self):
        """upload_file should reject unsupported artwork formats and
        unknown file types with a ValueError.
        """

        fresh = _make_patch_storage()
        fresh.api_token = "token"

        self.assertRaises(ValueError, fresh.upload_file, "artwork.txt", 0)
        self.assertRaises(ValueError, fresh.upload_file, "artwork.png", 7)

    def test_check_for_updates(self):
        pass


class TaxonomyRequestBoundsTest(unittest.TestCase):
    """The licenses and categories lists must never freeze the interface.

    They are resolved on first use, which happens on the UI thread when an
    upload dialog is opened, and a bundled snapshot takes over whenever the
    request does not work out. Inheriting the pool's 30s read timeout and its
    two retries would stall that dialog for well over a minute before the
    fallback was reached.
    """

    def _captured_kwargs(self, attribute):
        fresh = _make_patch_storage()
        with mock.patch("urllib3.PoolManager.request") as request:
            request.return_value = mock.Mock(status=200, data=b"[]")
            getattr(fresh, attribute)
            self.assertEqual(request.call_count, 1)
            return request.call_args.kwargs

    def test_licenses_request_is_bounded(self):
        kwargs = self._captured_kwargs("licenses")
        self.assertIs(kwargs["timeout"], api.TAXONOMY_TIMEOUT)
        self.assertIs(kwargs["retries"], False)

    def test_categories_request_is_bounded(self):
        kwargs = self._captured_kwargs("categories")
        self.assertIs(kwargs["timeout"], api.TAXONOMY_TIMEOUT)
        self.assertIs(kwargs["retries"], False)

    def test_the_bound_is_small_enough_to_be_worth_having(self):
        self.assertLessEqual(api.TAXONOMY_TIMEOUT.connect_timeout, 5)
        self.assertLessEqual(api.TAXONOMY_TIMEOUT.read_timeout, 5)

    def test_an_unreachable_api_still_yields_the_bundled_snapshot(self):
        fresh = _make_patch_storage()
        with mock.patch("urllib3.PoolManager.request") as request:
            request.side_effect = urllib3.exceptions.MaxRetryError(None, "licenses/")
            licenses = fresh.licenses
        self.assertTrue(licenses)
        self.assertTrue(all("id" in x and "name" in x for x in licenses))
