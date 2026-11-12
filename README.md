# ZOIA Librarian
Patch manager/librarian for the Empress Effects ZOIA pedal-format modular effects unit.

To learn more about ZOIA and its community, join our [Discord](https://discordapp.com/invite/HG5GesY),
[Subreddit](https://reddit.com/r/zoia), and/or [Facebook group](https://facebook.com/groups/EmpressZOIAUsers).

If you would like to leave a tip, we are accepting donations here
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=UUQ3SW5VMV3X4&currency_code=USD&source=url).
Thank you for your support!

This project depends heavily on the PatchStorage API, developed by Blokas: https://patchstorage.com/docs/api/beta/.

This software is distributed under GNU General Public License 3.0.
Please familiarize yourself with the Terms & Conditions of copyleft licenses like GPL (and others) here:
https://www.gnu.org/licenses/gpl-3.0.en.html.
ZOIA and its patch binary format are a trademark of Empress Effects, Inc. and are used with permission.

This app does not collect or transmit personal data or usage information to its developers. The developers do not receive data from your use of the app.

Neither the developers nor Empress Effects, Inc. are liable for any issues caused or raised by the use or
modification of this application. By installing the application you agree to these terms.

## How to Install
Application can be installed in one of two ways:
- For general users - Use the pre-bundled build; available on Mac and Windows here:
https://github.com/meanmedianmoge/zoia_lib/releases/latest.

- For developers/contributors - Build from source; requires Python 3.11+.
    ```
    # Download source code
    git clone https://github.com/meanmedianmoge/zoia_lib.git
    cd zoia_lib

    # Install dependencies
    sh tools/env.sh

    # Load the application
    python -m zoia_lib.backend.startup
    ```

## Documentation
- Version 1.0 video: https://www.youtube.com/watch?v=JLOUrWtG1Pk
- Version 1.1 video: https://www.youtube.com/watch?v=nP9oRLtXMUE
- Version 1.2 video: https://www.youtube.com/watch?v=zR8XSI_Unlk
- Version 1.3 video: https://www.youtube.com/watch?v=Y4ILhtxdIvs
- Version 1.4 video: https://www.youtube.com/watch?v=ymLvRhC1GmI
- Version 2.0 video: https://www.youtube.com/watch?v=j6mz4DIdEpU
- Version 2.1 video: https://www.youtube.com/watch?v=VkhidyALOXM
- Version 2.2 video: 
- You'll find the following in `documentation`: <br>
    - Current version of the user manual
    - Overall changelog - lists new features, bug fixes, and known issues for each release
    - Initial app frameworks and discussions among the dev team
    - Binary format (updated by marcuslupinus, thanks!)

## Features
- Browse PatchStorage uploads and local patches
- Search for specific patches, authors, tags, and more
- Sort the results by author, title, date modified, likes, views, or downloads
- Download & upload patches from/to PatchStorage
- Import patches from local storage or SD card
- Version control and patch merging
- Create and modify patches with the patch editor
- Preview patches with the patch visualizer
- Expose the internal routing and connections with the patch expander
- View and edit patch notes
- Customized category and tag labels for all patches
- Manage your SD card folders quickly
- Drag & drop patches into folders, configured automatically into a ZOIA-readable format
- Organize sample files for patches using the Sampler module
- Help toolbar for app documentation and ZOIA resources
- Dark and light themes

## Contributing
We welcome all contributions! If you want to see something added, 
either fork or clone the repo to get started. Some useful tools include:
- Python - https://www.python.org/downloads/
- VS Code - https://code.visualstudio.com/download
- QtDesigner - https://build-system.fman.io/qt-designer-download

## Authors
- Mike Moger - app owner, primary dev
- John Breton - primary dev up to Beta 3 release
- djigneo/apparent1 - binary decoding and testing
- Sranderley - binary encoding
- Matthew Allen - initial UI frames and app planning
- Special thanks to Steve Bragg and the entire Empress Effects team for supporting this work!
- Additional thanks to our beta testers, bug reporters, and user story writers
