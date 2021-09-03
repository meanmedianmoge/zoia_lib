import math
import struct

from zoia_lib.backend.patch import Patch
from zoia_lib.common import errors


class PatchBinEncoder(Patch):
    """The PatchBinEncoder class is a child of the Patch class. It is
    responsible for ZOIA patch binary re-encoding.
    """

    def __init__(self):
        """"""
        super().__init__()

    def encode(self, pch):
        """
        pch: parsed .bin using PatchBinary
        ================================================================
        Patch Structure:

        bytes 0-4 - Preset Size (indicates number of 4-byte chunks in file)
        bytes 5-21 - Preset Name
        bytes 22-25 - Number of Modules
        [] - List of modules
        bytes x-y - Number of connections
        [] - List of connections
        bytes x-y - Number of pages
        [] - List of page names (each is 16 bytes)
        bytes x-y Number of starred parameters
        [] - List of starred parameters
        [] - List of module colors (follows same order as list of modules)

        ================================================================
        """

        file = open(r"output_test.bin", "w+b")
        color_dict = {
            "Blue": 1,
            "Green": 2,
            "Red": 3,
            "Yellow": 4,
            "Aqua": 5,
            "Magenta": 6,
            "White": 7,
            "Orange": 8,
            "Lima": 9,
            "Surf": 10,
            "Sky": 11,
            "Purple": 12,
            "Pink": 13,
            "Peach": 14,
            "Mango": 15
        }

        file_array = bytearray()
        farray = bytearray()

        patch_size = self.encode_value(pch["size"], 4)
        patch_name = self.encode_text(pch["name"], 16)
        module_count = self.encode_value(pch["meta"]["n_modules"], 4)

        modules_array = bytearray()
        colors_array = bytearray()

        for module in pch["modules"]:

            module_array = bytearray()

            # Determine module size (in 4-byte words)
            module_size = self.encode_value(module["size"], 4)
            module_type = self.encode_value(module["mod_idx"], 4)
            module_version = self.encode_value(module["version"], 4)
            module_page = self.encode_value(module["page"], 4)
            module_color = self.encode_value(color_dict[module["color"]], 4)
            module_position = self.encode_value(min(module["position"]), 4)
            module_params_count = self.encode_value(len(module["parameters"]), 4)
            module_size_bytes = self.encode_value(module["size_of_saveable_data"], 4)

            module_options = bytearray()
            options_padding = 8 - len(module["options_binary"])
            for option in module["options_binary"]:
                module_options.extend(self.encode_byte(module["options_binary"][option], 1))

            if options_padding == 0:
                pass
            elif options_padding > 0:
                module_options.extend(self.encode_byte(0, options_padding))

            module_params = bytearray()
            for param in module["parameters"]:
                if module["parameters"][param] is None:
                    module_params.extend(self.encode_value(0, 4))
                else:
                    param_value = int(round(module["parameters"][param] * 65535, 0))
                    module_params.extend(self.encode_value(param_value, 4))

            for i in range(module["params"] - len(module["parameters"])):
                module_params.extend(self.encode_value(0, 4))

            module_saved_data = bytearray()
            nearest_int = self.round_up_to_nearest_int(module["size_of_saveable_data"])
            if nearest_int == 0:
                pass
            else:
                module_saved_data.extend(self.encode_value(0, nearest_int))

            module_name = self.encode_text(module["name"], 16)

            module_array.extend(module_size)
            module_array.extend(module_type)
            module_array.extend(module_version)
            module_array.extend(module_page)
            module_array.extend(module_color)
            module_array.extend(module_position)
            module_array.extend(module_params_count)
            module_array.extend(module_size_bytes)
            module_array.extend(module_options)
            module_array.extend(module_params)
            module_array.extend(module_saved_data)
            module_array.extend(module_name)

            # Add the module byte array to the modules byte array, by first
            # appending the size of the module, then the module pch
            modules_array.extend(module_array)

            color_array = self.encode_value(color_dict[module["color"]], 4)
            colors_array.extend(color_array)

        # Connections Encoding Section
        connections_array = bytearray()
        connection_count_array = self.encode_value(pch["meta"]["n_connections"], 4)
        connections_array.extend(connection_count_array)

        for connection in pch["connections"]:
            connection_array = bytearray()

            source_values = connection["source"].split(".")
            dest_values = connection["destination"].split(".")

            source_module_number_array = self.encode_value(int(source_values[0]), 4)
            source_output_number_array = self.encode_value(int(source_values[1]), 4)
            dest_module_number_array = self.encode_value(int(dest_values[0]), 4)
            dest_input_number_array = self.encode_value(int(dest_values[1]), 4)
            strength_value = int(round(connection["strength"] * 100, 0))
            connection_strength = self.encode_value(strength_value, 4)

            connection_array.extend(source_module_number_array)
            connection_array.extend(source_output_number_array)
            connection_array.extend(dest_module_number_array)
            connection_array.extend(dest_input_number_array)
            connection_array.extend(connection_strength)

            connections_array.extend(connection_array)

        # Build out the byte array for the pages by first calculating the number of pages,
        # then looping over them and pulling out the names
        pages_array = bytearray()
        pages_count_array = self.encode_value((pch["meta"]["n_pages"]), 4)
        pages_array.extend(pages_count_array)
        for page in pch["pages"]:
            if len(page) > 0:
                page_array = self.encode_text(page, 16)
                pages_array.extend(page_array)

        # Build out the byte array for starred params by first calculating the number
        # of starred params, then looping over them and pulling out the values to be
        # encoded per parameter
        starred_params_array = bytearray()
        starred_params_count_array = self.encode_value(pch["meta"]["n_starred"], 4)
        starred_params_array.extend(starred_params_count_array)
        for starred_param in pch["starred"]:
            starred_module_array = self.encode_value(starred_param["module"], 2)

            if starred_param["midi_cc"] == "None":
                starred_block_midi_array = self.encode_value(starred_param["block"], 2)
            else:
                cc = 128 * (starred_param["midi_cc"]+1) + starred_param["block"]
                starred_block_midi_array = self.encode_value(cc, 2)

            starred_params_array.extend(starred_module_array)
            starred_params_array.extend(starred_block_midi_array)

        # Now we stitch together the byte arrays into one large one which will be
        # analyzed for size, then written out to the binary file
        farray.extend(patch_name)
        farray.extend(module_count)
        farray.extend(modules_array)
        farray.extend(connections_array)
        farray.extend(pages_array)
        farray.extend(starred_params_array)
        farray.extend(colors_array)

        # Patch Size includes itself in the calculation!
        patch_size_array = self.encode_value(int(len(farray) / 4 + 1), 4)

        file_array.extend(patch_size_array)
        file_array.extend(farray)

        # Need some padding to fill the 32kB
        padding_length = 32764 - len(farray)
        padding = bytearray(b"\x00" * int(padding_length))
        file_array.extend(padding)

        file.write(file_array)
        file.close()

        return file_array

    @staticmethod
    def round_up_to_nearest_int(n):
        return n + (4 - n) % 4

    @staticmethod
    def encode_text(text, byte_array_length):
        # Helper function used to handle text encoding,
        # which is sequential and left-aligned
        format_string = "{}B{}x".format(len(text), byte_array_length - len(text))
        data = list(text.encode())

        return bytearray(struct.pack(format_string, *data))

    @staticmethod
    def encode_value(value, byte_array_length):
        # Helper function used to handle non-text encoding, which is little-endian
        # and left-aligned

        # Determine the number of bits required to encode the value
        # log of 0 is undefined, so account for the edge case
        if value == 0:
            value_bytes = 2
        else:
            value_bytes = int(math.ceil(math.log(value, 2)) / 8)

        # Determine the data type string to use when requesting the struct library
        # to encode our value in a byte array
        if value_bytes > 8:
            raise errors.BinaryError(None)

        elif value_bytes > 4:
            # long long
            byte_array_format = "Q"
            used_bytes = 8

        elif value_bytes > 2:
            # Unsigned Int
            byte_array_format = "I"
            used_bytes = 4

        else:
            # Unsigned Short
            byte_array_format = "H"
            used_bytes = 2

        # Little-endian encoding is enforced to allow for cross-platform consistency
        format_string = "<{}{}x".format(byte_array_format, byte_array_length - used_bytes)

        return bytearray(struct.pack(format_string, value))

    @staticmethod
    def encode_byte(byte, byte_array_length):
        # Helper function used to handle text encoding,
        # which is sequential and left-aligned
        format_string = "B{}x".format(byte_array_length - 1)

        return bytearray(struct.pack(format_string, byte))

    @staticmethod
    def encode_bool(bool, byte_array_length):
        # Helper function used to handle text encoding,
        # which is sequential and left-aligned
        format_string = "?{}x".format(byte_array_length - 1)

        return bytearray(struct.pack(format_string, bool))
