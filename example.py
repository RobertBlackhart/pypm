def f():
    adam = 3
    beta = 4
    theta = lambda x: x**2
    delta = range(10)
    epsilon = {'a': [1,2,3,4]}
    raise ValueError('hey')

if __name__ == '__main__':
    from pypm import pypm

    try:
        f()
    except Exception as ex:
        pypm.save_dump('test.dump')
        raise ex