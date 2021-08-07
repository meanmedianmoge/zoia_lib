from zoia_lib.backend.zoia_patch import ZoiaPatch

test_patch = ZoiaPatch()
test_patch.set_patch_binary_file_path(r"105188.bin")
test_patch.decode_patch_binary()

for module in test_patch.modules:
    # print(module.__dict__)
    print(module.module_id)
    print(module.get_blocks())
    pass

for connection in test_patch.connections:
    # print(connection)
    # print(test_patch.connections[connection])
    pass

for page in test_patch.pages:
    # print(page)
    pass



test_patch.add_module(0, 0, 0)
