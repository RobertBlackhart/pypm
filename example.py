from pypm import dump, freeze_traceback


def f():
    adam = 3
    beta = 4
    theta = lambda x: x**2
    delta = range(10)
    epsilon = {'a': [1,2,3,4]}
    raise ValueError('hey')


if __name__ == '__main__':
    try:
        f()
    except Exception as ex:
        dump_file = 'test.dump'
        with open(dump_file, 'wb') as f:
            print("Exception caught, writing dump to %s" % dump_file)
            dump(freeze_traceback(), f)
            print("Run 'python -m pypm [--debugger <pdb|pudb|ipdb>] %s' to debug" % (dump_file))
