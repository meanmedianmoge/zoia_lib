import copy
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from zoia_lib.backend.patch_save import PatchSave
from zoia_lib.common import errors


class TestArchiveRouting(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.save = PatchSave.__new__(PatchSave)
        self.save.back_path = str(self.root)
        self.meta = {'id': 123456, 'title': 'Bundle', 'revision': '1.0',
                     'files': [{'filename': 'bundle.zip'}]}

    def archive(self, entries):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            for name, data in entries:
                archive.writestr(name, data)
        return stream.getvalue(), copy.deepcopy(self.meta)

    def test_archive_order_and_samples_survive_initial_import_and_update(self):
        # Deliberately differs from alphabetic order; duplicate patch basenames
        # in separate folders must remain separate ordered versions.
        entries = [('z/patch.bin', b'first'), ('samples/drum.WAV', b'drum'),
                   ('a/patch.bin', b'second'), ('nested/voice.wav', b'voice')]
        self.save.save_to_backend(self.archive(entries))
        folder = self.root / '123456'
        for number, binary in ((1, b'first'), (2, b'second')):
            self.assertEqual((folder / f'123456_v{number}.bin').read_bytes(), binary)
            metadata = json.loads((folder / f'123456_v{number}.json').read_text())
            self.assertEqual(metadata['files'][0]['filename'], 'patch.bin')
            self.assertEqual(metadata['revision'], number)
        self.assertEqual((self.root / 'Samples/123456/drum.wav').read_bytes(), b'drum')
        self.assertEqual((self.root / 'Samples/123456/voice.wav').read_bytes(), b'voice')
        self.save.save_to_backend(self.archive(entries + [('new.bin', b'third')]))
        self.assertEqual((folder / '123456_v3.bin').read_bytes(), b'third')
        with self.assertRaises(errors.SavingError):
            self.save.save_to_backend(self.archive(entries + [('new.bin', b'third')]))
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['123456', 'Samples'])

    def test_single_patch_and_sample_only_archive(self):
        self.save.save_to_backend(self.archive([('nested/one.bin', b'one')]))
        self.assertEqual((self.root / '123456/123456.bin').read_bytes(), b'one')
        self.save.save_to_backend(self.archive([('deep/sample.wav', b'sample')]))
        self.assertEqual((self.root / 'Samples/123456/sample.wav').read_bytes(), b'sample')
        self.assertEqual((self.root / '123456/123456.bin').read_bytes(), b'one')

    def test_unsafe_paths_do_not_write_or_remove_library_files(self):
        sentinel = self.root / 'keep.bin'
        sentinel.write_bytes(b'keep')
        for name in ('../keep.bin', '/outside.bin', 'C:/outside.bin', '..\\keep.bin'):
            with self.subTest(name=name):
                with self.assertRaises(errors.SavingError):
                    self.save.save_to_backend(self.archive([('good.bin', b'good'), (name, b'bad')]))
                self.assertEqual(sentinel.read_bytes(), b'keep')
                self.assertFalse((self.root / '123456').exists())

    def test_duplicate_sample_names_rejected_before_saving(self):
        with self.assertRaises(errors.SavingError):
            self.save.save_to_backend(self.archive([('patch.bin', b'patch'),
                                                    ('a/drum.wav', b'one'), ('b/DRUM.WAV', b'two')]))
        self.assertFalse((self.root / '123456').exists())
