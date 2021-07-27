from zoia_lib.backend.patch import Patch


class ZoiaPatch(Patch):
   
    def __init__(self, module_factory, bin_encoder, patch_name):
        super(ZoiaPatch, self).__init__()

        self.module_factory = module_factory
        self.bin_encoder = bin_encoder

        self.name = patch_name
        self.modules = []
        self.connections = {}
        self.pages = []
        self.starred_params = []

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
