/*!
 * \file tl/maca/op/builtin.cc
 * \brief Registration of MACA-specific TileLang intrinsic Ops.
 */

#include "builtin.h"

#include <tvm/ir/transform.h>

#include "op/builtin_registry.h"

namespace tvm {
namespace tl {

using namespace tirx;

// maca_memcpy_async(dst_ptr, src_ptr, bytes) -> barrier_handle
// MACA memory async copy
TIR_DEFINE_TL_BUILTIN(maca_memcpy_async)
    .set_num_inputs(-1)
    .set_attr<TCallEffectKind>("TCallEffectKind",
                               Integer(CallEffectKind::kOpaque));

// maca_barrier_arrive_and_wait(barrier)
// MACA barrier arrive and wait operation
TIR_DEFINE_TL_BUILTIN(maca_barrier_arrive_and_wait)
    .set_num_inputs(-1)
    .set_attr<TCallEffectKind>("TCallEffectKind",
                               Integer(CallEffectKind::kOpaque));

TIR_DEFINE_TL_BUILTIN(maca_mma).set_num_inputs(12).set_attr<TCallEffectKind>(
    "TCallEffectKind", Integer(CallEffectKind::kOpaque));
} // namespace tl
} // namespace tvm

#undef TIR_DEFINE_TL_BUILTIN
