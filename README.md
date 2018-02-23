# pypm-fork
I got this idea of saving interpreter state after exception
so I can interactively debug my long running programs.

Most often, this happens when wrangling some data and such.

In this fork, I am using argparse and did some light refactoring.

# Installation
1. clone this repository
2. `cd pypm`
3. `pip install -e .`

# Usage
You have to call `pypm.save_dump` in an `except` block. 
You can reraise your exception again. See example.py for
an, well, example...

When the dump file is saved, you can use `pypm my.dump`
to get into an interactive post mortem debugging. See
`pypm --help` for options.

