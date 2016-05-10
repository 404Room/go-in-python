# -*- coding: utf-8 -*-
from gopy import (
    golang,
    defer
)

import unittest
import os


class TestFunctionDefer(unittest.TestCase):

    def test_close_file(self):

        @golang
        def read_file(src):
            f = open(src, 'r')
            defer(f.close)
            assert f.read()
            return f

        src = os.path.abspath(__file__)
        f = read_file(src)
        assert f.closed is True

    def test_reverse_order(self):

        @golang
        def append_to_list(order):
            defer(order.append, 1)
            defer(order.append, 2)
            order.append(3)

        order = []
        append_to_list(order)
        assert [3, 2, 1] == order

if __name__ == '__main__':
    unittest.main()
