def f():
    adam = 3
    beta = 4
    theta = lambda x: x**2
    delta = range(10)
    epsilon = {'a': [1,2,3,4]}
    raise ValueError('hey')

if __name__ == '__main__':
    from pypm import dump, freeze_traceback

    try:
        f()
    except Exception as ex:
        with open('test.dump', 'wb') as f:
            dump(freeze_traceback(), f)

        raise ex
