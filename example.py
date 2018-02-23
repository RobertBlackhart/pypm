import pandas as pd
def f():

    a = 3
    b = 4
    t = lambda x: x**2
    d = range(10)
    e = t(2)
    df = pd.DataFrame({'a': [1,2,3,4]}, index=[2,4,1,2])
    raise ValueError('hey')

if __name__ == '__main__':
    from pypm import pypm


    try:
        f()
    except Exception as ex:
        pypm.save_dump('test.dump')
        raise ex
