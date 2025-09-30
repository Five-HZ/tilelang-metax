# 2025 - Modified by MetaX Integrated Circuits (Shanghai) Co., Ltd. All Rights Reserved.

from typing import Callable, Union
from tvm import register_func
from tvm.target import Target


def register_cuda_postproc(func: Callable[[str, Target], str], override: bool = True):
    """Register a post-processing function for CUDA code generation.
    
    Args:
        func: A callable that takes generated code (str) and target (Target) as input,
             and returns the processed code (str).
        override: Whether to override existing registered function. Defaults to True.
    """
    register_func("tilelang_callback_cuda_postproc", f=func, override=override)

def register_hip_postproc(func: Callable[[str, Target], str], override: bool = True):
    """Register a post-processing function for HIP code generation.
    
    Args:
        func: A callable that takes generated code (str) and target (Target) as input,
             and returns the processed code (str).
        override: Whether to override existing registered function. Defaults to True.
    """
    register_func("tilelang_callback_hip_postproc", f=func, override=override)

def register_maca_postproc(func: Callable[[str, Target], str], override: bool = True):
    """Register a post-processing function for MACA code generation.
    
    Args:
        func: A callable that takes generated code (str) and target (Target) as input,
             and returns the processed code (str).
        override: Whether to override existing registered function. Defaults to True.
    """
    register_func("tilelang_callback_maca_postproc", f=func, override=override)

def register_cuda_postproc_callback(func: Union[Callable, bool] = None, override: bool = True):
    """Decorator for registering CUDA post-processing callback function.
    
    Can be used with or without parentheses:
        @register_cuda_postproc_callback
        def func(code, target): ...
        
        @register_cuda_postproc_callback()
        def func(code, target): ...
        
        @register_cuda_postproc_callback(override=False)
        def func(code, target): ...
    
    Args:
        func: The function to be decorated or a boolean override flag
        override: Whether to override existing registered function. Defaults to True.
    """
    if callable(func):
        register_cuda_postproc(func, override)
        return func

    if func is None or isinstance(func, bool):
        _override = func if isinstance(func, bool) else override

        def _register(fn: Callable[[str, Target], str]):
            register_cuda_postproc(fn, _override)
            return fn

        return _register

    raise TypeError("Invalid decorator usage")

def register_hip_postproc_callback(func: Union[Callable, bool] = None, override: bool = True):
    """Decorator for registering HIP post-processing callback function.
    
    Can be used with or without parentheses:
        @register_hip_postproc_callback
        def func(code, target): ...
        
        @register_hip_postproc_callback()
        def func(code, target): ...
        
        @register_hip_postproc_callback(override=False)
        def func(code, target): ...
    
    Args:
        func: The function to be decorated or a boolean override flag
        override: Whether to override existing registered function. Defaults to True.
    """
    if callable(func):
        register_hip_postproc(func, override)
        return func

    if func is None or isinstance(func, bool):
        _override = func if isinstance(func, bool) else override

        def _register(fn: Callable[[str, Target], str]):
            register_hip_postproc(fn, _override)
            return fn

        return _register

    raise TypeError("Invalid decorator usage")

def register_maca_postproc_callback(func: Union[Callable, bool] = None, override: bool = True):
    """Decorator for registering MACA post-processing callback function.
    
    Can be used with or without parentheses:
        @register_maca_postproc_callback
        def func(code, target): ...
        
        @register_maca_postproc_callback()
        def func(code, target): ...
        
        @register_maca_postproc_callback(override=False)
        def func(code, target): ...
    
    Args:
        func: The function to be decorated or a boolean override flag
        override: Whether to override existing registered function. Defaults to True.
    """
    if callable(func):
        register_maca_postproc(func, override)
        return func

    if func is None or isinstance(func, bool):
        _override = func if isinstance(func, bool) else override

        def _register(fn: Callable[[str, Target], str]):
            register_maca_postproc(fn, _override)
            return fn

        return _register

    raise TypeError("Invalid decorator usage")

def register_target_postproc_callback(target: str = "auto"):
    from tilelang.utils.target import determine_target
    target = determine_target(target)
    if target == "maca":
        return register_maca_postproc_callback
    elif target == "cuda":
        return register_cuda_postproc_callback
    elif target == "hip":
        return register_hip_postproc_callback
    else:
        raise ValueError(f"Unsupported target: {target}")
