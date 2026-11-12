import ntpath
import os
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from zoia_lib.backend.utilities import meipass, path_basename
from zoia_lib.interface.ZOIALibrarian_sd import ZOIALibrarianSD


class TestPaths(unittest.TestCase):
    def test_filename_accepts_qt_native_and_network_paths(self):
        for path in (r'C:\Users\Me\patch.bin', 'C:/Users/Me/patch.bin',
                     r'\\server\share\patch.bin', '/home/me/patch.bin'):
            self.assertEqual(path_basename(path), 'patch.bin')

    def test_packaged_resource_discards_windows_source_directory(self):
        with patch('zoia_lib.backend.utilities.sys._MEIPASS', '/bundle', create=True):
            for source in (r'C:\repo\resources\splash.png', 'C:/repo/resources/splash.png'):
                self.assertEqual(meipass(source, is_ui=True), os.path.abspath('/bundle/splash.png'))

    def test_sd_selection_keeps_complete_windows_paths(self):
        for selected in ('E:/', 'E:/patches/bank', r'E:\patches\bank', '//server/share/bank'):
            with self.subTest(selected=selected):
                sd = SimpleNamespace(ui=Mock())
                with patch('zoia_lib.interface.ZOIALibrarian_sd.QFileDialog.getExistingDirectory', return_value=selected), patch(
                    'zoia_lib.interface.ZOIALibrarian_sd.os.path.isdir', return_value=True
                ), patch('zoia_lib.interface.ZOIALibrarian_sd.os.path.normpath', side_effect=ntpath.normpath), patch(
                    'zoia_lib.interface.ZOIALibrarian_sd.os.path.join', side_effect=ntpath.join
                ), patch('zoia_lib.interface.ZOIALibrarian_sd.QFileSystemModel'):
                    ZOIALibrarianSD.sd_path(sd, False, 1000)
                self.assertEqual(sd.sd_root, ntpath.normpath(selected))
                self.assertEqual(sd.export_dir, ntpath.join(ntpath.normpath(selected), 'to_zoia'))

    def test_tree_selection_uses_model_path(self):
        sd = SimpleNamespace(ui=Mock(), _set_data_sd=Mock(), _has_item=Mock())
        sd.ui.sd_tree.model.return_value.filePath.return_value = r'E:\banks\bank 1'
        ZOIALibrarianSD.prepare_sd_view(sd)
        self.assertEqual(sd.sd_path_full, r'E:\banks\bank 1')
        sd._set_data_sd.assert_called_once_with()
