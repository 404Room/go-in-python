===================
Gopy
===================

在Python中模拟Golang的一些语法糖.

安装
----

::
  
    pip  install gopy
    
使用
----

**1. defer**

.. code:: python

    from gopy import (
        golang,
        defer
    )
    
    @golang
    def read_file(src):
        f = open(src, 'r')
        defer(f.close)
        # others

**2. panic和recover**

.. code:: python
    
    from __future__ import print_function
    from gopy import (
        golang,
        defer,
        panic,
        recover
    )
    
    def error_handler(a, b):
        error = recover()
        if error:
            pass
        else:
            pass
        print(a + b)
    
    @golang
    def some_func():
        defer(error_handler, a, b)
            # just throw some panic
            # panic is exception
            # also, like this
            # raise RuntimeError
            panic(RuntimeError)
          
            # unreachable code
            assert 1 == 2
            defer(print, 'Never print this')


说明
----
最近在学习和使用Golang， 觉得还挺不错的。所以就想把Golang中的一些语法糖和特性在python中模拟一下，虽然很蹩脚，但是有助于自己的巩固。随着学习的继续，可以回尝试将更多的东西模拟过来的。
