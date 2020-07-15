# -*- coding: utf-8 -*-
"""
// this is the structure of the preset
// these are all based on int sizes

// PRESET
//  size of whole preset including this 32-bit integer (int)       [0]
#define LOCATION_OF_PRESET_SIZE 0
//  preset name (SCREEN_LIST_MAX_SIZE string) (16 bytes)           [1]
#define LOCATION_OF_PRESET_NAME 1
//  MODULE_UIS
//    number of module_uis (int)                                   [5]
#define LOCATION_OF_NUMBER_OF_MODULES 5
//    MODULE_UI   0
#define LOCATION_OF_START_OF_MODULES 6
// then a bunch of modules
#define PRESET_MINIMUM_SIZE (LOCATION_OF_NUMBER_OF_MODULES + 2)
// up to the number of modules, and then the number of connections is in the int after that.
#define LOCATION_OF_NUMBER_OF_CONNECTIONS (PRESET_MINIMUM_SIZE + 1)
// then a bunch of connections
//
// then optionally, the number of page names
// then a bunch of page names
// each one is SCREEN_ELEMENT_MAX_STRING_SIZE long, which is 16 bytes, so each one will be 4 ints
//
// along with the page names there is the starred settings
// we start with the number of starred settings then a bunch of starred settings
// we'll treat these like signed numbers:
// if the number is zero or positive, it's a jack.
// If it's a jack, the bottom 16 bits specify the module index in the ordered module list,
// and the upper 16 bits specify the jack index.
// If it's negative, it's a connection. We multiply by -1 and subtract 1 to get the connection.


"""

import struct


def formatter(byt: bytes):
    """Patch format to decode binaries"""

    s = struct.Struct('I 16s I')
    size, name, n_mod = s.unpack(byt[:24])

    return size, name.rstrip(b'\x00').decode(), n_mod


def formatter_extended(byt: bytes,
                       n_mod: int = 32):
    """Additional decoding, EXPERIMENTAL"""

    # anything past this point is experimental
    s = struct.Struct('{}I I'.format(n_mod))
    mods = s.unpack(byt[24:24+n_mod*4+4])
    n_conn = mods[-1]
    mods = mods[:n_mod]

    s = struct.Struct('{}I'.format(n_conn))
    conn = s.unpack(byt[24+n_mod*4+4:24+n_mod*4+4+n_conn*4])

    s = struct.Struct('I')
    pages = s.unpack(byt[24+n_mod*4+4+n_conn*4:24+n_mod*4+4+n_conn*4+4])

    s = struct.Struct('16s')
    pg_names = s.unpack(byt[24+n_mod*4+4+n_conn*4+4:24+n_mod*4+4+n_conn*4+4+16])

    return mods, conn, pages, pg_names
