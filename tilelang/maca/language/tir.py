"""MACA-specific low-level TIR language operators."""

from __future__ import annotations

import tvm.tirx.op as _tvm_op

from tilelang.language.tir.exports import MACA_ONLY_TIR_EXPORTS
from tilelang.language.tir.ir import (
    _dtype_forward,
)

from tilelang.language.tir.op import call_intrin as _call_intrin


@_dtype_forward
def maca_mma(
    dtype,
    shape,
    A_layout,
    B_layout,
    A_dtype,
    B_dtype,
    C_dtype,
    multiplicand_a,
    a_index,
    multiplicand_b,
    b_index,
    accumulator,
    c_index,
):
    """TVM intrinsic for amd matrix core mfma instructions
    https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-for-mma

    Parameters
    ----------
    dtype : str
        The data type of the result.

    shape : str
        The shape of mma fragment.

    A_layout : Literal["row", "col"]
        The layout of multiplicand fragment A.

    B_layout : Literal["row", "col"]
        The layout of multiplicand fragment B.

    A_dtype : str
        The data type of multiplicand fragment A.

    B_dtype : str
        The data type of multiplicand fragment B.

    C_dtype : str
        The data type of accumulator fragment C.

    multiplicand_a : Var
        The multiplicand fragment A variable.

    a_index : Expr
        The index of multiplicand fragment A.

    multiplicand_b : Var
        The multiplicand fragment B variable.

    b_index : Expr
        The index of multiplicand fragment A.

    accumulator : Var
        The accumulator fragment C variable.

    c_index : Expr
        The index of accumulator fragment C.

    Returns
    -------
    call : PrimExpr
        The call expression.
    """
    return _call_intrin(
        dtype,
        _tvm_op.Op.get("tl.maca_mma"),
        shape,
        A_layout,
        B_layout,
        A_dtype,
        B_dtype,
        C_dtype,
        multiplicand_a,
        a_index,
        multiplicand_b,
        b_index,
        accumulator,
        c_index,
    )


__all__ = tuple(sorted(MACA_ONLY_TIR_EXPORTS))
