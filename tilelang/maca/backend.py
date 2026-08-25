from __future__ import annotations

import re

from tvm import tirx

from tilelang.backend.device_codegen import DeviceCodegen
from tilelang.backend.host_codegen import STANDARD_HOST_CODEGENS
from tilelang.backend.module import BackendModule, register_backend
from tilelang.contrib import mxcc
from tilelang.env import TILELANG_TEMPLATE_PATH
from tilelang.transform import PassConfigKey

from . import codegen, execution_backend, pipeline

_MACA_GLOBAL_KERNEL_PATTERN = re.compile(r'(?:extern\s+"C"\s+)?__global__\s+void\s+(?:__launch_bounds__\([^\)]*\)\s+)?(\w+)')


def _collect_external_maca_kernel_names(source: str) -> list[str]:
    kernel_names: list[str] = []
    seen_names: set[str] = set()
    for match in _MACA_GLOBAL_KERNEL_PATTERN.finditer(source):
        kernel_name = match.group(1)
        if kernel_name not in seen_names:
            kernel_names.append(kernel_name)
            seen_names.add(kernel_name)
    return kernel_names


def tilelang_callback_maca_validate(device_mod):
    for _, base_func in device_mod.functions.items():
        if not isinstance(base_func, tirx.PrimFunc) or not base_func.attrs:
            continue

        code_block_source = base_func.attrs.get("code_block_source")
        if code_block_source is None:
            continue

        global_symbol = base_func.attrs.get("global_symbol")
        if global_symbol is None:
            raise ValueError("CodeGenTileLangMACA expects source-kernel PrimFunc to have the global_symbol attribute")

        expected_name = str(global_symbol)
        code_block_entry_name = base_func.attrs.get("code_block_entry_name")
        if code_block_entry_name is not None and str(code_block_entry_name) != expected_name:
            raise ValueError("T.MACASourceCodeKernel expects the lowered device global_symbol to match entry_name")

        kernel_names = _collect_external_maca_kernel_names(str(code_block_source))
        if not kernel_names:
            raise ValueError("T.MACASourceCodeKernel expects external MACA source to declare at least one __global__ kernel")
        if expected_name not in kernel_names:
            raise ValueError(
                "T.MACASourceCodeKernel expected device global_symbol "
                f"`{expected_name}` to match a __global__ kernel in the provided MACA source. "
                f"Available entries: {', '.join(kernel_names)}"
            )


def tilelang_callback_maca_compile(code, target, pass_config=None):
    target_arch = mxcc.get_target_arch(mxcc.get_target_compute_version(target))

    arch = [f"--offload-arch={target_arch}"]
    compile_format = "mcbin"

    # Read pass-config keys (string-valued) like in jit.adapter.libgen.compile_lib
    cfg = pass_config or {}
    enable_fast_math = bool(cfg.get(PassConfigKey.TL_ENABLE_FAST_MATH, False))

    options = [
        "-std=c++17",
        "-I" + TILELANG_TEMPLATE_PATH,
    ]

    # Merge extra device compiler flags from pass config, if provided
    extra_flags = cfg.get(PassConfigKey.TL_DEVICE_COMPILE_FLAGS, None)
    if extra_flags:
        import shlex

        if isinstance(extra_flags, str):
            tokens = shlex.split(extra_flags)
        else:
            tokens = []
            for flag in extra_flags:
                if isinstance(flag, str):
                    tokens.extend(shlex.split(flag))
                else:
                    tokens.append(str(flag))
        options += tokens

    if enable_fast_math:
        options.append("-use-fast-math")

    if "--use_fast_math" in options:
        options.remove("--use_fast_math")

    fatbin = mxcc.compile_maca(
        code,
        compile_format,
        arch,
        options=options,
        verbose=False,
    )

    return fatbin


BACKEND = register_backend(
    BackendModule(
        name="maca",
        target_kinds=("maca",),
        supports_target=codegen._is_plain_maca_target,
        pipelines={"maca": pipeline.MACA_PIPELINE},
        device_codegens={
            "maca": DeviceCodegen(
                "maca",
                build=codegen.build_maca,
                build_without_compile=codegen.build_maca_without_compile,
            )
        },
        execution_backends=execution_backend.MACA_EXECUTION_BACKENDS,
        host_codegens=STANDARD_HOST_CODEGENS,
        callbacks={
            "tilelang_callback_maca_validate": tilelang_callback_maca_validate,
            "tilelang_callback_maca_compile": tilelang_callback_maca_compile,
        },
    )
)
