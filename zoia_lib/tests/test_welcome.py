from pathlib import Path
import unittest

from zoia_lib.interface.ZOIALibrarian_util import ZOIALibrarianUtil

welcome_html = ZOIALibrarianUtil.welcome_html


class TestWelcome(unittest.TestCase):
    def test_current_changelog_excludes_earlier_versions(self):
        changelog = (Path(__file__).resolve().parents[2] / 'documentation' / 'resources' / 'welcome-changelog.html').read_text()
        html = welcome_html(changelog, '2.2', 'file:///app/splash.png')
        self.assertIn('Welcome to ZOIA Librarian!', html)
        self.assertIn('Version 2.2', html)
        self.assertIn('Metadata-only edits', html)
        self.assertNotIn('Version 2.1', html)
        self.assertNotIn('version 2.1', html)

    def test_content_is_escaped_and_missing_release_is_usable(self):
        html = welcome_html('<section id="version-2.2"><h3>Fixes</h3><p>A &lt; B &amp; C</p></section><section id="version-2.1">Old note</section>', '2.2', 'file:///app/image.png')
        self.assertIn('A &lt; B &amp; C', html)
        self.assertNotIn('Old note', html)
        self.assertIn('Select a patch', welcome_html('', '2.3', 'file:///app/image.png'))
