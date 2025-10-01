# 2025 - Modified by MetaX Integrated Circuits (Shanghai) Co., Ltd. All Rights Reserved.

from .arch_base import TileDevice
from .cuda import CUDA
from .cpu import CPU
from .cdna import CDNA
from .maca import MACA
from typing import Union
from tvm import device as tvm_device
from tvm.target import Target
from tvm.runtime import Device


def get_arch(target: Union[str, Target] = "cuda") -> TileDevice:
    if isinstance(target, str):
        target = Target(target)

    if target.kind.name == "cuda":
        return CUDA(target)
    elif target.kind.name == "llvm":
        return CPU(target)
    elif target.kind.name == "hip":
        return CDNA(target)
    elif target.kind.name == "maca":
        return MACA(target)
    else:
        raise ValueError(f"Unsupported target: {target.kind.name}")

AUTO_DETECT_DEVICES = ["maca", "cuda", "rocm", "llvm"]

def auto_infer_current_arch() -> TileDevice:
    # TODO(lei): This is a temporary solution to infer the current architecture
    # Can be replaced by a more sophisticated method in the future
    def _check_device(device: Device) -> bool:
        try:
            return bool(device.exist)
        except:
            return False
    for dev_name in AUTO_DETECT_DEVICES:
        if _check_device(tvm_device(dev_name)):
            return get_arch(dev_name)
    else:
        raise ValueError(f"No device found, supported devices: {AUTO_DETECT_DEVICES}")

from .cpu import is_cpu_arch  # noqa: F401
from .cuda import (
    is_cuda_arch,  # noqa: F401
    is_volta_arch,  # noqa: F401
    is_ampere_arch,  # noqa: F401
    is_ada_arch,  # noqa: F401
    is_hopper_arch,  # noqa: F401
    is_tensorcore_supported_precision,  # noqa: F401
    has_mma_support,  # noqa: F401
)
from .cdna import is_cdna_arch  # noqa: F401
from .maca import is_maca_arch
