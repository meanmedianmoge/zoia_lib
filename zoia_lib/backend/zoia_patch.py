import struct

from zoia_lib.backend.patch import Patch
from zoia_lib.backend.zoia_module_factory import ZoiaModuleFactory
from zoia_lib.backend.patch_bin_encoder import PatchBinEncoder


class ZoiaPatch(Patch):
   
    def __init__(self):
        super(ZoiaPatch, self).__init__()

        self.module_factory = ZoiaModuleFactory()
        self.bin_encoder = PatchBinEncoder()

        self.bin_file_path = ""
        self.bin_array = []

        self.size = 0
        self.name = ""
        self.modules = []
        self.connections = {}
        self.pages = []
        self.starred_params = []

    # ===========================================================================================
    #   Patch Functions Exposed to User
    # ===========================================================================================
    def set_patch_binary_file_path(self, file_path):
        self.bin_file_path = file_path

    def decode_patch_binary(self):
        self.bin_array = open(self.bin_file_path, "rb").read()

        # Unpack the binary data.
        self.size = self.convert_bin_to_int(self.bin_array[0:4])
        self.name = self.convert_bin_to_text(self.bin_array[4:20])
        # Get Size
        # Get Name
        # Get Modules
        # Get Connections
        # Get Pages
        # Get Starred Params
        # Get Colors
        pass

    def set_patch_size(self, patch_size):
        self.size = patch_size

    def set_patch_name(self, patch_name):
        self.name = patch_name

    def encode_patch_binary(self):
        return self.bin_encoder.encode(self)

    # ===========================================================================================
    #   Module Functions Exposed to User
    # ===========================================================================================
    def add_module(self, position, id, version):
        new_module = self.module_factory.create_module(id, version)
        self.modules.insert(position, new_module)

    def remove_module(self, position):
        self.modules.pop(position)

    def replace_module(self, position, id, version):
        new_module = self.module_factory.create_module(id, version)
        self.modules.insert(position, new_module)

    def clear_modules(self):
        self.modules.clear()

    # ===========================================================================================
    #   Connection Functions Exposed to User
    # ===========================================================================================
    def add_connection(self, source_module, source_output, dest_module, dest_input, strength):
        # Create a unique ID for the connection which can be used by the application to lookup
        # and modify the existing connection's details

        connection_id = str(source_module) + str(source_output) + str(dest_module) + str(dest_input)
        connection = {
            "source_module": source_module,
            "source_output": source_output,
            "dest_module": dest_module,
            "dest_input": dest_input,
            "strength": strength
        }
        self.connections[connection_id] = connection

    def remove_connection(self, connection_id):
        del self.connections[connection_id]

    def update_connection(self, source_module, source_output, dest_module, dest_input, strength):
        connection_id = str(source_module) + str(source_output) + str(dest_module) + str(dest_input)
        self.connections[connection_id] = {
            "source_module": source_module,
            "source_output": source_output,
            "dest_module": dest_module,
            "dest_input": dest_input,
            "strength": strength
        }

    def clear_connections(self):
        self.connections = {}

    # ===========================================================================================
    #   Starred Params Functions Exposed to User
    # ===========================================================================================

    def add_starred_param(self):
        pass

    def remove_starred_param(self):
        pass

    def clear_starred_params(self):
        pass

    # ===========================================================================================
    #   Helper Functions used in module
    # ===========================================================================================
    @staticmethod
    def convert_bin_to_int(byte_string):
        return int.from_bytes(byte_string[0:4], "little")

    @staticmethod
    def convert_bin_to_text(string_tuple):
        string = ''
        for item in string_tuple:
            string += chr(item)
        return string
