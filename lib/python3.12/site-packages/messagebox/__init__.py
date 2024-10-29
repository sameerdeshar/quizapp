# -*- coding=utf-8 -*-
r"""
MIT License

Copyright (c) 2021 PlayerG9

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = "PlayerG9"
__copyright__ = "Copyright 2021, PlayerG9"
__credits__ = ["PlayerG9"]
__license__ = "MIT"
__version_info__ = (0,1,0)
__version__ = '.'.join(str(_) for _ in __version_info__)
__maintainer__ = "PlayerG9"
__email__ = None
__status__ = "Prototype"  # Prototype, Development, Production


from ._dummy import *  # contains descriptions and help for IDE or reading of package
from ._dummy import __all__


try:  # this block updates the functions corresponding to the operating system
    import sys as __sys
    import importlib as __il
    import functools as __ft
    __module = __il.import_module('._{}'.format(__sys.platform), __package__)
    globals().update(  # update the functions but keep the help/documentation from _dummy.py
        {
            k: __ft.wraps(globals()[k])(getattr(__module, k))
            for k in __all__
            if hasattr(__module, k)  # this line is for test-purposes only (implementing a new os)
        }
    )
except ImportError:
    raise ImportError('this platform is not supported: {}'.format(__sys.platform))
