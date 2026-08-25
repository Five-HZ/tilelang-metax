from __future__ import annotations

from tvm.target import Target

from tilelang.backend.device_codegen import global_func_device_codegen


def _is_plain_maca_target(target: Target) -> bool:
    return target.kind.name == "maca"


build_maca = global_func_device_codegen("target.build.tilelang_maca")
build_maca_without_compile = global_func_device_codegen("target.build.tilelang_maca_without_compile")
