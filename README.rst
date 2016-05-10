===================
Gopy
===================

在Python中模拟Golang的一些语法糖.

----------------
安装
----------------

.. code:: sh
  
  pip install gopy
  
---------------
使用
----------------

1. **defer**

.. code:: python

  from gopy import (
    golang,
    defer
  )
  
  @golang
  def read_file(src):
    f = open(src)
    defer(f.close)
    
    # dosometing
    
  
