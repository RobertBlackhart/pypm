# pypm
I got this idea of saving interpreter state after exception
so I can interactively debug my long running programs.

Most often, this happens when wrangling some data and such.

In this fork, I am using argparse and did some light refactoring.

# Installation

Just run `pip install pm.py`

# Usage
You have to call `pypm.freeze_traceback()` in an `except` block.
This function returns a `FrozenTraceback` object that can be
saved to a file using `pypm.dump(frozen_traceback, file)`.

You can reraise your exception again. See `example.py` for
an, well, example...

When the dump file is saved, you can use `$ pypm my.dump`
to get into an interactive post mortem debugging. See
`pypm --help` for options.
