# zoia-lib
Patch manager for Empress Effects ZOIA pedal  
If you'd like to assist in development for this project, join our Discord here:
`https://discordapp.com/invite/HG5GesY` and PM me for a dev role.
Discussion for the project will take place in the #library-app channel.
While working on modules, please make feature branches and submit to master via PR/MR. Thanks!

## Dependencies
- Patchstorage API https://patchstorage.com/docs/

## Status: WIP
API
- more methods around searching and downloading
- create ZoiaPatch objects from search outputs

Renumber class
- re-arranges input directory of patches
- `alpha` and `random` work as intended
- `by_tag` is dependent on tagging capabilities and definitions

ZoiaPatch class
- constructor for patch object with version-ing and custom tagging
- `zip` is the preferred format, can store multiple patch files and patch notes
- `bin` files need additional metadata on the binary structure

## Known bugs

## Other modules left to be claimed
UI  
Drag and drop via file system (SD card is our I/O source)  
Unit tests  

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

***A note about version control and patch notes: an issue I have with patch uploads
is when/how things get altered on Patchstorage. There is no proper VCS software
(something like Git or Mercurial) to identify WHAT changed, unless the user tells
you in the patch notes.

My suggested solution would allow the app to create a .txt file (either from the
Patchstorage description or from scratch) and “attach” it to the .bin file.
This would change the format from singular .bins to zip files, which I think is
probably for the best since you can dump multiple versions of the patch + the patch
notes in a zip. It makes things a bit cleaner. We’d have to come up with a way for
the app to parse the zip into .bins and .txts so the renumbering and drag/drop works,
but that shouldn’t be too difficult.

## Todo
Another set of tasks could easily be built around exploring how we
build and read our data from a ZIP file like what does ZIP_to_ZOIA() and the reverse look like?
cuz I dont think we want to show .zips in the library, so when we build
the library we should be converting the zips over

What is a library? Is it a single object in memory that contains all of 
the zoia objects from all the directories?
again I think we should follow the leads empress has been giving.
you have an individual patch 01_name_zoia.bin
you have a collection of 64 patches that live in a directory on an sd card
so we have a patch object. we should have a group which may be a custom collection of patches
well for one a directory is filenamed based, and in the case of your local PS storage will
contain way more than 64 patches
if in the object model the patch has both a slot number property and a filename
property, sorting them and ordering them becomes really easy
