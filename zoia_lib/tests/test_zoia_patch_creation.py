from zoia_lib.backend.zoia_patch import ZoiaPatch

test_patch = ZoiaPatch()
test_patch.set_patch_binary_file_path(r"C:\Share\zoia_lib\105188.bin")
test_patch.decode_patch_binary()

for module in test_patch.modules:
    print(module.__dict__)

for connection in test_patch.connections:
    print(connection)
    print(test_patch.connections[connection])

for page in test_patch.pages:
    print(page)

test_patch.add_module(0, 0, 0)
