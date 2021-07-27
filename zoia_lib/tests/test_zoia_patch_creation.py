from zoia_lib.backend.zoia_module_factory import ZoiaModuleFactory
from zoia_lib.backend.patch_bin_encoder import PatchBinEncoder
from zoia_lib.backend.zoia_patch import ZoiaPatch

module_factory = ZoiaModuleFactory()
bin_encoder = PatchBinEncoder()

test_patch = ZoiaPatch(module_factory, bin_encoder, "test_patch")

test_patch.add_module(0, 0, 0)

print(test_patch)