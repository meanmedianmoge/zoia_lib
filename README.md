# zoia-lib
Patch manager for Empress Effects ZOIA pedal  
If you'd like to assist in development for this project, join our Discord here https://discordapp.com/invite/HG5GesY and PM me for a `dev` role. Discussion for the project will take place in the #library-app channel. While working on modules, please make feature branches and submit to master via merge requests. Thanks!

## Dependencies
- Patchstorage API https://patchstorage.com/docs/

## Status: WIP
API
- The API is read-only and in alpha, so many desired features are missing

Renumber class
- re-arranges input directory of patches
- `alpha` and `random` work as intended
- `by_tag` is dependent on tagging capabilities and definitions

ZoiaPatch class
- constructor for patch object with versioning and custom tagging
- `zip` is the preffered format, can store multiple patch files and patch notes
- `bin` files need additional metadata on the binary structure

## Known bugs
Renumber will drop duplicate names from the list of patches, meaning that if you have a stack of empty patches in your directory, it will drop some (but not all?) of those empties.

## Other modules left to be claimed
UI
Drag and drop via file system (SD card is our I/O source)

## Features
EXTRACT (extract from Librarian)
- pull the latest uploads (bin/zip) files directly from Patchstorage
- drag and drop patches into to_zoia directories

TRANSFORM (transform with Librarian)
- tagging (Patchstorage and custom)
- renumbering (with options.. alpha, by tag, random, none)
- version control/view and edit patch notes***

LOAD (load to Librarian)
- drag and drop patches into from_zoia directories
- user upload to Patchstorage
- general storage for your WIP/secret patches

***A note about version control and patch notes: an issue I have with patch uploads is when/how things get altered on Patchstorage. There is no proper VCS software (something like Git or Mercurial) to identify WHAT changed, unless the user tells you in the patch notes.

My suggested solution would allow the app to create a .txt file (either from the Patchstorage description or from scratch) and “attach” it to the .bin file. This would change the format from singular .bins to zip files, which I think is probably for the best since you can dump multiple versions of the patch + the patch notes in a zip. It makes things a bit cleaner. We’d have to come up with a way for the app to parse the zip into .bins and .txts so the renumbering and drag/drop works, but that shouldn’t be too difficult.
