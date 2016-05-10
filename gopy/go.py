# -*- coding: utf-8 -*-

import functools
import inspect

__all__ = ("golang", "defer", "panic", "recover")


class GolangContext(object):
    """Golang context"""

    def __init__(self):
        self.defers = []
        self.panic = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.do_defers()
        # just throw the last uncatched panic
        panic(self.panic)

    def do_defers(self):
        """Call all defered functions in a reverse order. So, the \
        function which called firstly in parent function will called\
        lastly in this function"""
        __golang_context__ = self
        for defer in __golang_context__.defers:
            try:
                fn, args, kwargs, filename, lineno = defer
                fn(*args, **kwargs)
            except BaseException as ex:
                __golang_context__.panic = ex

        ex = __golang_context__.panic


def golang(func):
    """Golang context that allow python function to use\
    some properties in golang. Usually, just use it as a
    decorator.

    :param func: function that wants to use golang properties.
    :type func: function

    """
    @functools.wraps(func)
    def _golang_wrapper(*args, **kwargs):
        ret = None
        with GolangContext() as __golang_context__:
            try:
                ret = func(*args, **kwargs)
            except Exception as ex:
                __golang_context__.panic = ex
        return ret
    return _golang_wrapper


def defer(fn, *args, **kwargs):
    """Defer calling the specific function to the end of \
    parent function anyway.

    :param fn: function to call.
    :type fn: function
    :param \*args: args that pass to fn.
    :type \*args: list
    :param \*\*kwargs: kwargs that pass to fn.
    :type \*\*kwargs: dict

    :rtype: None
    """
    frames = inspect.stack()
    parent_frame = frames[1][0]

    golang_frame = None
    golang_context = None

    try:
        for frame in frames:
            if '_golang_wrapper' in frame:
                golang_frame = frame[0]
                golang_context = golang_frame.f_locals.get('__golang_context__')
                break
        if not golang_frame or not golang_context:
            raise RuntimeError('no golang context found.')

        golang_context.defers.insert(
            0, (fn, args, kwargs, parent_frame.f_code.co_filename, parent_frame.f_lineno))
    finally:
        del parent_frame
        del golang_frame
        del frames


def panic(ex):
    """Throw a panic

    :param ex: panic is exception.
    :type ex: exception
    """
    if ex:
        raise ex


def recover():
    """Recover from a panic in a golang context.

    :rtype: exception. if there has no panic, return `None`.
    """
    frames = inspect.stack()
    defer_frame = None
    golang_context = None

    for frame in frames:
        if 'do_defers' in frame:
            defer_frame = frame[0]
            golang_context = defer_frame.f_locals.get('__golang_context__')
            break
    if not defer_frame or not golang_context:
        return None

    panic = golang_context.panic
    golang_context.panic = None

    return panic
