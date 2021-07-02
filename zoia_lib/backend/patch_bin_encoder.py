import math
import struct

from zoia_lib.backend.patch_binary import PatchBinary
from zoia_lib.common import errors

class PatchBinEncoder():
    def __init__(self, source_binary_path):
        self.bin_path = source_binary_path

        self.bin_data = open(self.bin_path, "rb").read()

        self.patch = PatchBinary()
        self.data = self.patch.parse_data(self.bin_data)

        self.file = open(r"output_test.bin", "w+b")
        self.color_dict = {
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

    def encode(self):
        """
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
        file_array = bytearray()

        patch_name = self.encode_text(self.data["name"], 16)
        module_count = self.encode_value(len(self.data["modules"]), 4)

        modules_array = bytearray()
        colors_array = bytearray()

        for module in self.data["modules"]:

            module_array = bytearray()

            module_type = self.encode_value(module["mod_idx"], 8)
            module_page = self.encode_value(module["page"], 8)
            module_position = self.encode_value(min(module["position"]), 4)
            module_params_count = self.encode_value(len(module["parameters"]), 8)

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

            module_name = self.encode_text(module["name"], 16)

            module_array.extend(module_type)
            module_array.extend(module_page)
            module_array.extend(module_position)
            module_array.extend(module_params_count)
            module_array.extend(module_options)
            module_array.extend(module_params)
            module_array.extend(module_name)

            # Determine module size (in 4-byte words)
            module_size = self.encode_value(int(len(module_array) / 4 + 1), 4)

            # Add the module byte array to the modules byte array, by first
            # appending the size of the module, then the module data
            modules_array.extend(module_size)
            modules_array.extend(module_array)

            color_array = self.encode_value(self.color_dict[module["color"]], 4)
            colors_array.extend(color_array)

        # Connections Encoding Section
        connections_array = bytearray()
        connection_count_array = self.encode_value(len(self.data["connections"]), 4)
        connections_array.extend(connection_count_array)

        for connection in self.data["connections"]:
            connection_array = bytearray()

            source_values = connection["source"].split(".")
            dest_values = connection["destination"].split(".")

            source_module_number_array = self.encode_value(int(source_values[0]), 4)
            source_output_number_array = self.encode_value(int(source_values[1]), 4)
            dest_module_number_array = self.encode_value(int(dest_values[0]), 4)
            dest_input_number_array = self.encode_value(int(dest_values[1]), 4)
            connection_strength = self.encode_value(connection["strength"], 4)

            connection_array.extend(source_module_number_array)
            connection_array.extend(source_output_number_array)
            connection_array.extend(dest_module_number_array)
            connection_array.extend(dest_input_number_array)
            connection_array.extend(connection_strength)

            connections_array.extend(connection_array)

        # Build out the byte array for the pages by first calculating the number of pages,
        # then looping over them and pulling out the names
        pages_array = bytearray()
        pages_count_array = self.encode_value(len(self.data["pages"]), 4)
        pages_array.extend(pages_count_array)
        for page in self.data["pages"]:
            if len(page) > 0:
                page_array = self.encode_text(page, 16)
                pages_array.extend(page_array)

        # Build out the byte array for starred params by first calculating the number
        # of starred params, then looping over them and pulling out the values to be
        # encoded per parameter
        starred_params_array = bytearray()
        starred_params_count_array = self.encode_value(len(self.data["starred"]), 4)
        starred_params_array.extend(starred_params_count_array)
        for starred_param in self.data["starred"]:
            starred_module_array = self.encode_value(starred_param["module"], 2)
            starred_block_array = self.encode_byte(starred_param["block"], 1)

            if starred_param["midi_cc"] == "None":
                starred_midi_cc_array = self.encode_byte(0, 1)
            else:
                starred_midi_cc_array = self.encode_byte(starred_param["midi_cc"], 1)

            starred_params_array.extend(starred_module_array)
            starred_params_array.extend(starred_block_array)
            starred_params_array.extend(starred_midi_cc_array)

        # Now we stitch together the byte arrays into one large one which will be
        # analyzed for size, then written out to the binary file
        file_array.extend(patch_name)
        file_array.extend(module_count)
        file_array.extend(modules_array)
        file_array.extend(connections_array)
        file_array.extend(pages_array)
        file_array.extend(starred_params_array)
        file_array.extend(colors_array)

        # Patch Size includes itself in the calculation!
        patch_size_array = self.encode_value(int(len(file_array) / 4 + 1), 4)
        self.file.write(patch_size_array)
        self.file.write(file_array)
        self.file.close()

    def encode_text(self, text, byte_array_length):
        # Helper function used to handle text encoding,
        # which is sequential and left-aligned
        format_string = "{}B{}x".format(len(text), byte_array_length - len(text))
        data = list(text.encode())

        return bytearray(struct.pack(format_string, *data))

    def encode_value(self, value, byte_array_length):
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

    def encode_byte(self, byte, byte_array_length):
        # Helper function used to handle text encoding,
        # which is sequential and left-aligned
        format_string = "B{}x".format(byte_array_length - 1)

        return bytearray(struct.pack(format_string, byte))

    def encode_bool(self, bool, byte_array_length):
        # Helper function used to handle text encoding,
        # which is sequential and left-aligned
        format_string = "?{}x".format(byte_array_length - 1)

        return bytearray(struct.pack(format_string, bool))