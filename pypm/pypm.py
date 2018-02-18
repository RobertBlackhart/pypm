"""
The MIT License (MIT)
Copyright (C) 2018 Jordi Masip <jordi@masip.cat>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import sys
import pdb
import gzip
import pickle
import linecache
import inspect
import dill
import time
import builtins as __builtin__

__version__ = "2.0"

DUMP_VERSION = 1
exceptions_to_trigger = []


# Public functions
# ================


def set_dump_on_exceptions(*exceptions):
    """
    Set one or more exceptions that will save the dump automatically
    """
    _monkeypatch_sys_excepthook()

    global exceptions_to_trigger
    exceptions_to_trigger = exceptions


def save_dump(filename, tb=None):
    """
    Saves a Python traceback in a pickled file. This function will usually be called from
    an except block to allow post-mortem debugging of a failed process.

    The saved file can be loaded with load_dump which creates a fake traceback
    object that can be passed to any reasonable Python debugger.
    """
    if not tb:
        tb = sys.exc_info()[2]
    fake_tb = FakeTraceback(tb)
    dump = {
        'traceback': fake_tb,
        'files': _get_traceback_files(fake_tb),
        'dump_version': DUMP_VERSION
    }
    
    _monkeypatch_pickle_save()

    with gzip.open(filename, 'wb') as f:
        dill.dump(dump, f)

def load_dump(filename):
    # ugly hack to handle running non-install pydump
    if 'pypm.pypm' not in sys.modules:
        sys.modules['pypm.pypm'] = sys.modules[__name__]
    with gzip.open(filename, 'rb') as f:
        try:
            return dill.load(f)
        except IOError:
            with open(filename, 'rb') as f:
                return dill.load(f)


def debug_dump(dump_filename, post_mortem_func=pdb.post_mortem):
    dump = load_dump(dump_filename)
    _cache_files(dump['files'])
    tb = dump['traceback']
    _old_checkcache = linecache.checkcache
    _old_isframe = inspect.isframe
    _old_iscode = inspect.iscode
    _old_istraceback = inspect.istraceback

    linecache.checkcache = lambda filename=None: None
    inspect.isframe = lambda o: _old_isframe(o) or isinstance(o, FakeFrame)
    inspect.iscode = lambda o: _old_iscode(o) or isinstance(o, FakeCode)
    inspect.istraceback = lambda o: _old_istraceback(o) or isinstance(o, FakeTraceback)

    post_mortem_func(tb)

    inspect.isframe = _old_isframe
    inspect.iscode = _old_iscode
    inspect.istraceback = _old_istraceback
    linecache.checkcache = _old_checkcache


# Private classes and functions
# =============================


class NotPickled(object):

    def __init__(self, txt):
        self.__str__ = lambda x: f'<NotPickled: {txt}>'


class FakeCode(object):
    def __init__(self, code):
        self.co_filename = os.path.abspath(code.co_filename)
        self.co_name = code.co_name
        self.co_argcount = code.co_argcount
        self.co_consts = tuple(
            FakeCode(c) if hasattr(c, 'co_filename') else c
            for c in code.co_consts
        )
        self.co_firstlineno = code.co_firstlineno
        self.co_lnotab = code.co_lnotab
        self.co_varnames = code.co_varnames
        self.co_flags = code.co_flags


class FakeFrame():
    def __init__(self, frame):
        self.f_code = FakeCode(frame.f_code)
        self.f_locals = frame.f_locals
        self.f_globals = frame.f_globals
        self.f_lineno = frame.f_lineno
        self.f_back = FakeFrame(frame.f_back) if frame.f_back else None


class FakeTraceback(object):
    def __init__(self, traceback):
        self.tb_frame = FakeFrame(traceback.tb_frame)
        self.tb_lineno = traceback.tb_lineno
        self.tb_next = FakeTraceback(traceback.tb_next) if traceback.tb_next else None
        self.tb_lasti = 0


def _get_traceback_files(traceback):
    files = {}
    while traceback:
        frame = traceback.tb_frame
        while frame:
            filename = os.path.abspath(frame.f_code.co_filename)
            if filename not in files:
                try:
                    files[filename] = open(filename).read()
                except IOError:
                    files[filename] = "couldn't locate '%s' during dump" % frame.f_code.co_filename
            frame = frame.f_back
        traceback = traceback.tb_next
    return files


def _cache_files(files):
    for name, data in files.items():
        lines = [line+'\n' for line in data.splitlines()]
        linecache.cache[name] = (len(data), None, lines, name)


def _pickle_save(f):
    def _save(self, obj, save_persistent_id=True):
        try:
            f(self, obj, save_persistent_id)
        except Exception:
            obj = NotPickled(obj.__repr__())
            f(self, obj, save_persistent_id)
    return _save


def _excepthook(f):
    def _dump_exception(_type, value, tb):
        for exc in exceptions_to_trigger:
            if isinstance(tb, exc):
                filename = f'{__file__}.{time.time()}.dump'
                save_dump(filename, tb=tb)
                break
        else:
            f(_type, value, tb)
    return _dump_exception


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def _monkeypatch_pickle_save():
    pickle._Pickler.save = _pickle_save(pickle._Pickler.save)


@run_once
def _monkeypatch_sys_excepthook():
    sys.excepthook = _excepthook(sys.excepthook)
