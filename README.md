# zoia-lib
Patch manager/librarian for the Empress Effects ZOIA pedal-format modular effects unit.

To learn more about ZOIA and its community, join our [Discord chat server](https://discordapp.com/invite/HG5GesY),
[Subreddit](https://reddit.com/r/zoia), and/or [Facebook group](https://facebook.com/groups/EmpressZOIAUsers).

If you would like to leave a tip, we are accepting donations here
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=UUQ3SW5VMV3X4&currency_code=USD&source=url).
Thank you for your support!

This project depends heavily on the PatchStorage API, developed by Blokas: https://patchstorage.com/docs/

This software is distributed under GNU General Public License 3.0.
Please familiarize yourself with the Terms & Conditions of copyleft licenses like GPL (and others) here:
https://www.gnu.org/licenses/gpl-3.0.en.html.
ZOIA and its patch binary format are a trademark of Empress Effects, Inc. and are used with permission.

Neither the developers nor Empress Effects, Inc. are liable for any issues caused or raised by the use or
modification of this application. By installing the application you agree to these terms.

## How to Install
Application can be installed in one of two ways:
- (For general users) - Use the pre-bundled build, available on Windows, Mac, and Linux (Ubuntu) here:
https://github.com/meanmedianmoge/zoia_lib/releases.

- (For developers/contributors) - Build from source; requires Python 3.7+.
```
# Download source code from Github (either directly from the site or cloning the repo)
git clone https://github.com/meanmedianmoge/zoia_lib.git
# Make sure you're in the right directory
cd Downloads/zoia_lib
# Install Python 3.7+, make sure you have pip
pip help
# Install the dependencies that allow the app to run
pip install -r requirements.txt
# Load the application
python -m zoia_lib.backend.startup
```

## Documentation
- Overview video and tutorial: https://www.youtube.com/watch?v=JLOUrWtG1Pk
- Supplemental 1.1 video: coming soon!
- The current version of the manual can be found in `/User Manual`
- Changelog of the various improvements, bug fixes, and known issues are in `/Changelog`
- Initial app frameworks and discussions among the dev team and Empress can be found in `/Backend Implementation`, 
`/Design Document`, and `/Testing Plan`
- HTML versions of the featured documentation (available in the Help toolbar) are in `/Resources`

## Features
- Browse PatchStorage uploads and local patches within the UI
- Search for specific patches, authors, tags, and more
- Sort the results by author, title, date modified, likes, views, or downloads
- Download patches from PatchStorage
- Import patches from local storage or SD card
- Version control and local/PS patch merging
- Preview patches with the patch visualizer
- View and edit patch notes
- Customized category and tag labels for all patches
- Manage your SD card folders quickly
- Drag & drop patches into folders, configured automatically into a ZOIA-readable format
- Help toolbar for app documentation and ZOIA resources
- Dark and light themes

## Contributing
We welcome all contributions! If you want to see something added, 
either fork or clone the repo to get started. Some useful tools include:
- QtDesigner - https://build-system.fman.io/qt-designer-download
- PyCharm Community Edition - https://www.jetbrains.com/pycharm/download
- Python 3.9.X - https://www.python.org/downloads/release/python-394/

## Authors
- Mike Moger - app owner, primary dev after Beta 3 release, initial Python implementation
- John Breton - primary dev, designer, and documentation creator up to Beta 3 release
- djigneo/apparent1 - C# binary decoder and testing
- Matthew Allen - initial UI frames and app planning
- Special thanks to Steve Bragg and the entire Empress Effects team for supporting this work
- Additional thanks to our beta testers and those who submitted user stories
