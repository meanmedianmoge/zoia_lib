import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import requests
from PySide6.QtWidgets import QMessageBox

from zoia_lib.interface.ZOIALibrarian_main import ZOIALibrarianMain


class TestAppUpdates(unittest.TestCase):
    def setUp(self):
        self.window = SimpleNamespace(ui=Mock(), msg=Mock(), _version='2.2')

    def test_connection_failures_stop_check_without_crashing(self):
        for error in (requests.ConnectionError('offline'), requests.Timeout('timed out')):
            with self.subTest(error=error):
                self.window.msg.reset_mock()
                with patch('zoia_lib.interface.ZOIALibrarian_main.requests.get',
                           side_effect=error) as get:
                    ZOIALibrarianMain.check_for_updates(self.window)
                get.assert_called_once_with(
                    'https://github.com/meanmedianmoge/zoia_lib/releases/latest', timeout=5)
                self.window.msg.setWindowTitle.assert_called_once_with('Github Error')
                self.window.msg.exec_.assert_called_once_with()

    def test_failed_or_invalid_release_response_stops_check(self):
        for response in (
            Mock(url='https://github.com/meanmedianmoge/zoia_lib/releases/latest',
                 raise_for_status=Mock(side_effect=requests.HTTPError('503'))),
            Mock(url='https://github.com/meanmedianmoge/zoia_lib/releases/latest'),
        ):
            with self.subTest(response=response):
                self.window.msg.reset_mock()
                with patch('zoia_lib.interface.ZOIALibrarian_main.requests.get',
                           return_value=response):
                    ZOIALibrarianMain.check_for_updates(self.window)
                self.window.msg.setWindowTitle.assert_called_once_with('Github Error')

    def test_successful_checks_still_compare_versions(self):
        for version in ('2.2', '2.3'):
            with self.subTest(version=version):
                self.window.ui.reset_mock()
                self.window.msg.reset_mock()
                self.window.msg.exec_.return_value = QMessageBox.No
                response = Mock(url=f'https://github.com/meanmedianmoge/zoia_lib/releases/tag/{version}')
                with patch('zoia_lib.interface.ZOIALibrarian_main.requests.get',
                           return_value=response) as get:
                    ZOIALibrarianMain.check_for_updates(self.window)
                self.assertEqual(get.call_count, 1)
                response.raise_for_status.assert_called_once_with()
                if version == '2.2':
                    self.window.msg.exec_.assert_not_called()
                    self.window.ui.statusbar.showMessage.assert_called_once_with(
                        'You are already using the latest version!', timeout=5000)
                else:
                    self.window.msg.setWindowTitle.assert_called_once_with('App Update')
                    self.window.msg.exec_.assert_called_once_with()
