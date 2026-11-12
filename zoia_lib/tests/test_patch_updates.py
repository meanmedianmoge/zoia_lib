import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import urllib3
from zoia_lib.backend.api import PatchStorage
from zoia_lib.interface.ZOIALibrarian_local import ZOIALibrarianLocal


class TestPatchUpdates(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        folder = Path(self.directory.name) / '123456'
        folder.mkdir()
        self.path = str(folder / '123456')
        self.metadata = {
            'title': 'Arithmetic', 'content': 'A useful description.', 'revision': '0.1',
            'files': [{'id': 42, 'filename': 'patch.bin', 'url': 'https://example.invalid/patch.bin'}],
            'categories': [{'id': 5, 'name': 'Utility'}], 'tags': [],
            'artwork': {'id': 4}, 'license': {'id': 1},
        }
        self.remote = dict(self.metadata, revision='1.10')
        self.save()
        Path(self.path + '.bin').write_bytes(b'patch')
        self.client = PatchStorage.__new__(PatchStorage)
        self.client.url = 'https://example.invalid/'
        self.client.api_token = 'test-token'
        self.client.get_patch_meta = Mock(return_value=self.remote)

    def save(self):
        Path(self.path + '.json').write_text(json.dumps(self.metadata))

    def test_revision_components(self):
        for revision, expected in [('1', '2'), ('1.10', '1.11'), ('1.2.9', '1.2.10'), ('v2.9', 'v2.10')]:
            self.assertEqual(self.client.next_revision(revision), expected)
        with self.assertRaises(ValueError):
            self.client.next_revision('release candidate')

    def test_comparison_binary_and_metadata(self):
        for binary, content, expected in [(b'patch', self.remote['content'], (False, False)),
                                           (b'changed', self.remote['content'], (True, False)),
                                           (b'patch', 'Updated notes.', (False, True))]:
            Path(self.path + '.bin').write_bytes(binary)
            self.metadata['content'] = content
            self.save()
            with patch('zoia_lib.backend.api.http.request', return_value=SimpleNamespace(status=200, data=b'patch')):
                plan = self.client.prepare_patch_update('123456', self.path)
            self.assertEqual((plan['binary_changed'], plan['metadata_changed']), expected)

    def test_archive_comparison_and_ambiguity(self):
        for filenames in [('nested/patch.bin',), ('one.bin', 'two.bin')]:
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as archive:
                for filename in filenames:
                    archive.writestr(filename, b'patch')
            self.remote['files'] = [{'id': 42, 'filename': 'patch.zip', 'url': 'https://example.invalid/patch.zip'}]
            with patch('zoia_lib.backend.api.http.request', return_value=SimpleNamespace(status=200, data=buffer.getvalue())):
                if len(filenames) == 1:
                    self.assertFalse(self.client.prepare_patch_update('123456', self.path)['binary_changed'])
                else:
                    with self.assertRaisesRegex(ValueError, 'Cannot identify'):
                        self.client.prepare_patch_update('123456', self.path)

    def test_payload_preserves_or_increments_live_revision(self):
        for patch_id, revision in [(None, '1.10'), (99, '1.11')]:
            with patch('zoia_lib.backend.api.http.request') as request:
                self.client.update_patch('123456', self.path, patch_id=patch_id, remote_meta=self.remote)
            payload = json.loads(request.call_args.kwargs['body'])
            self.assertEqual(payload['revision'], revision)
            self.assertEqual(payload['files'], [42] if patch_id is None else [99])
            self.assertFalse(request.call_args.kwargs['retries'])

    def test_rar_comparison_reads_without_extracting(self):
        self.remote['files'] = [{'id': 42, 'filename': 'patch.rar', 'url': 'https://example.invalid/patch.rar'}]
        archive = Mock()
        archive.infolist.return_value = [SimpleNamespace(filename='nested/patch.bin', file_size=5)]
        archive.read.return_value = b'patch'
        with patch('zoia_lib.backend.api.http.request', return_value=SimpleNamespace(status=200, data=b'rar')), patch(
            'zoia_lib.backend.api.rarfile.RarFile'
        ) as rar:
            rar.return_value.__enter__.return_value = archive
            self.assertFalse(self.client.prepare_patch_update('123456', self.path)['binary_changed'])
        archive.extractall.assert_not_called()

    def test_changed_binary_does_not_replace_multiple_published_files(self):
        self.remote['files'] = [self.metadata['files'][0], {'id': 99, 'filename': 'other.bin'}]
        with patch('zoia_lib.backend.api.http.request', return_value=SimpleNamespace(status=200, data=b'old')):
            with self.assertRaisesRegex(ValueError, 'multiple published files'):
                self.client.prepare_patch_update('123456', self.path)

    def test_http_error_is_not_compared_as_binary(self):
        with patch('zoia_lib.backend.api.http.request', return_value=SimpleNamespace(status=503, data=b'error')):
            with self.assertRaisesRegex(ValueError, 'HTTP 503'):
                self.client.prepare_patch_update('123456', self.path)

    def ui_local(self):
        api = Mock()
        api.prepare_patch_update.return_value = {'binary_changed': False, 'metadata_changed': True, 'remote': self.remote}
        return SimpleNamespace(path=self.directory.name, local_selected='123456', api=api,
                               usr_pwd=Mock(), ui=Mock(), msg=Mock(), _upload_patch_file=Mock())

    def test_metadata_only_skips_binary_upload(self):
        local = self.ui_local()
        local.api.update_patch.return_value = SimpleNamespace(status=200)
        local.api.get_patch_meta.return_value = self.remote
        ZOIALibrarianLocal.update_patch(local)
        local._upload_patch_file.assert_not_called()
        local.api.update_patch.assert_called_once_with('123456', self.path, None, None, None, remote_meta=self.remote)
        local.ui.statusbar.showMessage.assert_called_with('Update complete.', timeout=5000)

    def test_retry_error_never_reports_success(self):
        local = self.ui_local()
        local.api.update_patch.side_effect = urllib3.exceptions.MaxRetryError(None, '/patch')
        ZOIALibrarianLocal.update_patch(local)
        local.msg.setWindowTitle.assert_called_once_with('Update Not Confirmed')
        local.api.get_patch_meta.assert_not_called()

    def test_refresh_error_does_not_retry_successful_write(self):
        local = self.ui_local()
        local.api.update_patch.return_value = SimpleNamespace(status=200)
        local.api.get_patch_meta.side_effect = ValueError('refresh failed')
        ZOIALibrarianLocal.update_patch(local)
        local.api.update_patch.assert_called_once()
        local.msg.exec_.assert_not_called()
        local.ui.statusbar.showMessage.assert_called_with(
            'PatchStorage update succeeded; local metadata could not be refreshed.', timeout=5000)
