from pypm.pypm import *

if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    parser = OptionParser(usage="%prog <filename.dump> [options]", description="pydump v%s: post-mortem debugging for Python programs" % __version__)
    parser.add_option("--pdb",  action="append_const", const="pdb",  dest="debuggers", help="Use builtin pdb or pdb++")
    parser.add_option("--pudb", action="append_const", const="pudb", dest="debuggers", help="Use pudb visual debugger")
    parser.add_option("--ipdb", action="append_const", const="ipdb", dest="debuggers", help="Use ipdb IPython debugger")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    if not options.debuggers:
        options.debuggers = ["pdb"]

    for debugger in options.debuggers:
        try:
            dbg = __import__(debugger)
        except ImportError as e:
            print(str(e))
            continue
        else:
            print("Starting %s..." % debugger)
            if debugger == "pudb":
                post_mortem = dbg.post_mortem
            else:
                import pdb
                post_mortem = pdb.post_mortem

            break

    with open(args[0], 'rb') as f:
        frozen_traceback = load(f)

    with debug(frozen_traceback) as tb:
        post_mortem(tb)
