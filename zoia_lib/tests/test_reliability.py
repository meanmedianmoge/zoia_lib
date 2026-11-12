import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import urllib3
from zoia_lib.backend.api import PatchStorage
from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.backend.utilities import merge_patch_metadata, search_patches
from zoia_lib.common.errors import SavingError
from zoia_lib.interface.ZOIALibrarian_local import ZOIALibrarianLocal
from zoia_lib.interface.ZOIALibrarian_ps import ReloadPSWorker, DownloadAllWorker
from zoia_lib.interface.ZOIALibrarian_sd import ZOIALibrarianSD
from PySide6.QtWidgets import QMessageBox


class TestReliability(unittest.TestCase):
    def test_cv_mixer_accepts_all_supported_channel_counts(self):
        binary = PatchBinary.__new__(PatchBinary)
        for channels in range(1, 9):
            with self.subTest(channels=channels):
                blocks = binary._calc_blocks({
                    'mod_idx': 104, 'version': 0,
                    'options': {'num_channels': channels, 'levels': 'summing'},
                })
                self.assertEqual(len(blocks), channels * 2 + 1)
                self.assertIn('cv_output', blocks)

    def test_clear_visualizer_discards_previous_patch_and_page_controls(self):
        local = SimpleNamespace(ui=Mock(), curr_viz={'old': 'patch'},
                                curr_page_viz=4, viz_disable=Mock())
        ZOIALibrarianLocal.clear_viz(local)
        self.assertIsNone(local.curr_viz)
        self.assertEqual(local.curr_page_viz, 0)
        for name in ('back_btn', 'btn_next_page', 'btn_prev_page', 'btn_show_routing'):
            getattr(local.ui, name).setEnabled.assert_called_once_with(False)
        local.viz_disable.assert_called_once_with()

    def test_split_refreshes_parent_without_leaving_remaining_history(self):
        for remaining in (0, 1, 3):
            with self.subTest(remaining=remaining):
                patch = {'title': 'Split patch'}
                local = SimpleNamespace(
                    ui=Mock(), msg=Mock(), window=Mock(), curr_ver='123456',
                    prev_search='split', data_local=[patch],
                    _select_versions_to_split=Mock(return_value=['123456_v2']),
                    _count_version_files=Mock(side_effect=[5, remaining]),
                    get_version_patches=Mock(), get_local_patches=Mock(), go_back=Mock(),
                    clear_viz=Mock(),
                )
                local.msg.exec_.return_value = QMessageBox.Yes
                with unittest.mock.patch(
                    'zoia_lib.interface.ZOIALibrarian_local.update.split_version_history'
                ) as split:
                    ZOIALibrarianLocal.split_version_history(local)
                split.assert_called_once_with('123456', ['123456_v2'])
                local.get_local_patches.assert_called_once_with(render=False)
                self.assertEqual(local.window.search_data_local, [patch])
                self.assertEqual(local.prev_search, 'split')
                if remaining <= 1:
                    local.go_back.assert_called_once_with()
                    local.get_version_patches.assert_not_called()
                else:
                    local.go_back.assert_not_called()
                    local.get_version_patches.assert_called_once_with(True, '123456')

    def test_cancel_sd_selection_preserves_existing_root(self):
        sd = SimpleNamespace(sd_root='/existing', ui=Mock())
        with patch('zoia_lib.interface.ZOIALibrarian_sd.QFileDialog.getExistingDirectory', return_value=''):
            ZOIALibrarianSD.sd_path(sd, False, 1000)
        self.assertEqual(sd.sd_root, '/existing')
        sd.ui.tab_sd.setEnabled.assert_not_called()

    def test_error_has_readable_message_and_context(self):
        error = SavingError('Arithmetic', 503)
        self.assertIn('already', str(error))
        self.assertEqual(error.info, 'Arithmetic')
        self.assertEqual(error.error_code, 503)

    def test_download_rejects_error_body(self):
        api = PatchStorage.__new__(PatchStorage)
        api.get_patch_meta = Mock(return_value={'files': [{'url': 'https://example.invalid/file'}]})
        with patch('zoia_lib.backend.api.http.request', return_value=SimpleNamespace(status=503, data=b'error')):
            with self.assertRaises(urllib3.exceptions.HTTPError):
                api.download('123456')

    def test_offline_count_can_recover(self):
        api = PatchStorage.__new__(PatchStorage)
        api.patch_count = None
        api._patch_count = Mock(side_effect=[urllib3.exceptions.HTTPError('offline'), 23])
        with self.assertRaises(urllib3.exceptions.HTTPError):
            api.refresh_patch_count()
        self.assertIsNone(api.patch_count)
        self.assertEqual(api.refresh_patch_count(), 23)

    def test_merge_deduplicates_fresh_and_cached_entries(self):
        self.assertEqual(merge_patch_metadata([{'id': 1, 'title': 'fresh'}, {'id': 1}],
                                             [{'id': 1}, {'id': 2}]),
                         [{'id': 1, 'title': 'fresh'}, {'id': 2}])

    def test_search_with_empty_files_still_matches_author(self):
        entry = {'title': 'Patch', 'files': [], 'author': {'name': 'Alice'}}
        self.assertEqual(search_patches([entry], 'alice'), [entry])

    def test_cancelled_authentication_stops_upload_and_update(self):
        local = SimpleNamespace(local_selected='10000', usr_pwd=Mock(return_value=None))
        ZOIALibrarianLocal.upload_patch(local)
        ZOIALibrarianLocal.update_patch(local)

    def test_refresh_failure_preserves_cache_and_emits_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / 'data.json'
            cache.write_text('[{"id": 1}]')
            worker = SimpleNamespace(path=directory, api=Mock(), signal=Mock(), failed=Mock())
            worker.api.get_all_patch_data_init.side_effect = ValueError('offline')
            ReloadPSWorker.run(worker)
            self.assertEqual(json.loads(cache.read_text()), [{'id': 1}])
            worker.signal.emit.assert_not_called()
            worker.failed.emit.assert_called_once_with('offline')

    def test_batch_continues_after_failure_and_reports_counts(self):
        worker = SimpleNamespace(jobs=[(0, '123456'), (1, '234567')], api=Mock(),
                                 save=Mock(), signal=Mock(), signal_2=Mock(), downloaded=Mock())
        worker.api.download.side_effect = [urllib3.exceptions.HTTPError('offline'), (b'patch', {})]
        DownloadAllWorker.run(worker)
        worker.signal.emit.assert_called_once_with(1, 1)
        worker.downloaded.emit.assert_called_once_with(1)

    def test_cancel_sd_delete_leaves_file_alone(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'patch.bin'
            path.write_bytes(b'patch')
            sd = SimpleNamespace(sd_path_full=str(path), msg=Mock(), delete=Mock(), ui=Mock())
            sd.msg.exec_.return_value = QMessageBox.No
            ZOIALibrarianSD.delete_sd_item(sd)
            sd.delete.delete_file.assert_not_called()
            self.assertEqual(path.read_bytes(), b'patch')
