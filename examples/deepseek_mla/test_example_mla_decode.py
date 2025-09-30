# 2025 - Modified by MetaX Integrated Circuits (Shanghai) Co., Ltd. All Rights Reserved.

import tilelang.testing

import example_mla_decode
from unittest import mock
import sys

def test_example_mla_decode():
    with mock.patch.object(sys, 'argv', ["example_mla_decode.py"]):
        example_mla_decode.main()


if __name__ == "__main__":
    tilelang.testing.main()
