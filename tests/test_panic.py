# -*- coding: utf-8 -*-

from gopy import(
    golang,
    defer,
    panic,
    recover
)

import unittest


class TestPanic(unittest.TestCase):

    def test_throw_panic(self):

        @golang
        def throw_panic():
            panic(RuntimeError)
            assert 1 == 2

        try:
            throw_panic()
        except BaseException as ex:
            assert isinstance(ex, RuntimeError)
        else:
            assert 1 == 2

    def test_recover_panic1(self):
        def panic_handler():
            assert recover() is None

        @golang
        def not_throw_panic():
            defer(panic_handler)
            pass

        not_throw_panic()

    def test_recover_panic2(self):
        error = RuntimeError('error')

        def panic_handler(error):
            assert error == recover()

        @golang
        def throw_panic():
            defer(panic_handler, error)
            panic(error)
            assert 1 == 2

        throw_panic()

    def test_recover_panic3(self):
        error = ValueError('error')

        def panic_handler(error):
            assert error == recover()
            panic(error)

        @golang
        def throw_panic():
            defer(panic_handler, error)
            panic(error)

        try:
            throw_panic()
        except BaseException as ex:
            assert ex == error
        else:
            assert 1 == 2

if __name__ == '__main__':
    unittest.main()
