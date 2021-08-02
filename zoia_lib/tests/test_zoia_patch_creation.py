from zoia_lib.backend.zoia_patch import ZoiaPatch

test_patch = ZoiaPatch()
test_patch.set_patch_binary_file_path(r"C:\Share\zoia_lib\105188.bin")
test_patch.decode_patch_binary()

print(test_patch.size)
print(test_patch.name)
test_patch.add_module(0, 0, 0)
