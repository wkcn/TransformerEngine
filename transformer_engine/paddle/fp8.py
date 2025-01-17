# Copyright (c) 2022-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# See LICENSE for license information.
"""FP8 utilities for TransformerEngine"""

from typing import Tuple

import paddle
import transformer_engine_paddle as tex

_is_fp8_available = None
_reason_for_no_fp8 = ""


def _check_fp8_support() -> Tuple[bool, str]:
    """Return if fp8 support is available"""

    # Check GPU arch
    arch = paddle.device.cuda.get_device_capability()
    if arch >= (9, 0):    # hopper and above
        return True, ""
    if arch < (8, 9):    # pre-ada
        return False, "Device compute capability 8.9 or higher required for FP8 execution."

    # Special handling for Ada
    if tex.get_cublasLt_version() < 120103:
        return False, "CublasLt version 12.1.3.x or higher required for FP8 execution on Ada."
    if not paddle.version.cuda():
        return False, "Cuda version 12.1 or higher required for FP8 execution on Ada."
    if tuple(int(v) for v in paddle.version.cuda().split(".")) < (12, 1):
        return False, "Cuda version 12.1 or higher required for FP8 execution on Ada."
    return True, ""


def is_fp8_available() -> Tuple[bool, str]:
    """Return if fp8 support is available"""
    global _is_fp8_available, _reason_for_no_fp8
    if _is_fp8_available is None:
        _is_fp8_available, _reason_for_no_fp8 = _check_fp8_support()
    return _is_fp8_available, _reason_for_no_fp8
