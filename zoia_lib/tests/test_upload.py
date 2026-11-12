import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, mock_open, patch

from zoia_lib.interface.ZOIALibrarian_local import ZOIALibrarianLocal


class TestUploadOwnership(unittest.TestCase):
    def setUp(self):
        self.local = SimpleNamespace(
            local_selected="10000",
            path=os.path.abspath("library"),
            usr_pwd=Mock(return_value="patchstorage-user"),
            update_patch=Mock(),
            ui=Mock(),
            msg=Mock(),
        )

    def test_new_upload_allows_empty_or_different_local_author(self):
        for author in ("", "local-author"):
            with self.subTest(author=author):
                metadata = json.dumps({"author": {"name": author}, "content": "Test patch", "categories": [{"name": "Utility"}]})
                # Stop at artwork selection, before any network uploads.
                with patch("builtins.open", mock_open(read_data=metadata)), patch(
                    "zoia_lib.interface.ZOIALibrarian_local.QFileDialog.getOpenFileName",
                    side_effect=InterruptedError("artwork selection reached"),
                ):
                    with self.assertRaisesRegex(InterruptedError, "artwork selection reached"):
                        ZOIALibrarianLocal.upload_patch(self.local)
                self.local.msg.exec_.assert_not_called()
        self.assertEqual(self.local.usr_pwd.call_count, 2)

    def test_existing_patch_routes_to_update(self):
        self.local.local_selected = "123456"
        ZOIALibrarianLocal.upload_patch(self.local)
        self.local.update_patch.assert_called_once_with()
        self.local.usr_pwd.assert_not_called()

    def test_update_allows_display_name_different_from_login(self):
        self.local.local_selected = "123456"
        self.local.api = Mock()
        self.local.api.prepare_patch_update.return_value = {'binary_changed': True, 'metadata_changed': False, 'remote': {'revision': '1.0'}}
        self.local._upload_patch_file = lambda *args, **kwargs: ZOIALibrarianLocal._upload_patch_file(self.local, *args, **kwargs)
        self.local.api.upload_file.return_value = SimpleNamespace(status=201, data=b'{"id": 42}')
        self.local.api.update_patch.side_effect = RuntimeError("update reached")
        metadata = json.dumps({"author": {"name": "Display Name"}, "artwork": {"id": 41}, "license": {"id": 1}})
        with patch("builtins.open", mock_open(read_data=metadata)):
            with self.assertRaisesRegex(RuntimeError, "update reached"):
                ZOIALibrarianLocal.update_patch(self.local)
        self.local.usr_pwd.assert_called_once_with()
        expected_path = os.path.join(self.local.path, "123456", "123456")
        self.local.api.upload_file.assert_called_once_with(expected_path, file_type=1)
        self.local.api.update_patch.assert_called_once_with(
            "123456", expected_path, None, 42, None, remote_meta={"revision": "1.0"}
        )
        self.local.msg.exec_.assert_not_called()

    def test_unchanged_binary_does_not_publish_update(self):
        self.local.api = Mock()
        self.local.api.prepare_patch_update.return_value = {'binary_changed': False, 'metadata_changed': False}
        with patch("builtins.open", mock_open(read_data='{}')):
            ZOIALibrarianLocal.update_patch(self.local)
        self.local.api.upload_file.assert_not_called()
        self.local.api.update_patch.assert_not_called()

    def test_failed_binary_comparison_does_not_publish_update(self):
        self.local.api = Mock()
        self.local.api.prepare_patch_update.side_effect = ValueError("HTTP 503")
        with patch("builtins.open", mock_open(read_data='{}')):
            ZOIALibrarianLocal.update_patch(self.local)
        self.local.api.upload_file.assert_not_called()
        self.local.api.update_patch.assert_not_called()
        self.local.msg.exec_.assert_called_once_with()

    def test_upload_reaches_license_after_both_files(self):
        self.local._upload_patch_file = Mock(side_effect=[41, 42])
        self.local.license = Mock(side_effect=InterruptedError("license reached"))
        with patch("builtins.open", mock_open(read_data='{"content": "Test patch", "categories": [{"name": "Utility"}]}')), patch(
            "zoia_lib.interface.ZOIALibrarian_local.QFileDialog.getOpenFileName",
            return_value=("/art.JPG", "Images"),
        ):
            with self.assertRaisesRegex(InterruptedError, "license reached"):
                ZOIALibrarianLocal.upload_patch(self.local)
        self.assertEqual(self.local._upload_patch_file.call_args_list, [
            unittest.mock.call("/art.JPG", file_type=0),
            unittest.mock.call(os.path.join(self.local.path, "10000", "10000"), file_type=1),
        ])

    def test_file_errors_show_dialog(self):
        self.local.api = Mock()
        for failure in (FileNotFoundError("missing binary"), ValueError("bad metadata")):
            with self.subTest(failure=failure):
                self.local.api.upload_file.side_effect = failure
                result = ZOIALibrarianLocal._upload_patch_file(self.local, "/patch", 1)
                self.assertIsNone(result)
                self.local.msg.setDetailedText.assert_any_call(str(failure))

    def test_non_json_server_error_shows_dialog(self):
        self.local.api = Mock()
        self.local.api.upload_file.return_value = SimpleNamespace(status=502, data=b"Bad Gateway")
        self.assertIsNone(ZOIALibrarianLocal._upload_patch_file(self.local, "/art", 0))
        self.local.msg.exec_.assert_called_once_with()

    def test_missing_details_stop_before_uploading_artwork(self):
        with patch("builtins.open", mock_open(read_data='{}')), patch(
            "zoia_lib.interface.ZOIALibrarian_local.QFileDialog.getOpenFileName"
        ) as artwork:
            ZOIALibrarianLocal.upload_patch(self.local)
        artwork.assert_not_called()
        self.local.msg.setText.assert_called_once_with(
            "Before uploading, add a description and at least one category to the patch."
        )

    def test_patch_rejection_preserves_field_specific_error(self):
        self.local._upload_patch_file = Mock(side_effect=[41, 42])
        self.local.license = Mock(return_value="CC0")
        error = {"message": "Invalid parameter(s): content", "data": {
            "params": {"content": "Server validation explanation"}
        }}
        self.local.api = Mock()
        self.local.api.licenses = [{"name": "CC0", "id": 1}]
        self.local.api.upload_patch.return_value = SimpleNamespace(
            status=400, data=json.dumps(error).encode()
        )
        metadata = {"content": "My saved notes", "categories": [{"name": "Utility"}]}
        with patch("builtins.open", mock_open(read_data=json.dumps(metadata))), patch(
            "zoia_lib.interface.ZOIALibrarian_local.QFileDialog.getOpenFileName",
            return_value=("/art.jpeg", "Images"),
        ):
            ZOIALibrarianLocal.upload_patch(self.local)
        self.local.msg.setDetailedText.assert_any_call(json.dumps(error))
