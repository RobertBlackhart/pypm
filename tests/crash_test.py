import requests
import asyncio

if __name__ == '__main__':
    def foo():
        foovar = 7
        bar()

    def bar():
        barvar = "hello"
        list_sample = [1,2,3,4]
        dict_sample = {'a':1, 'b':2}
        baz()

    async def my_coroutine(seconds_to_sleep=3):
        print('my_coroutine sleeping for: {0} seconds'.format(seconds_to_sleep))
        await asyncio.sleep(seconds_to_sleep)
        raise Exception('hi')

    def baz():
        momo = Momo()
        momo.raiser()

    class Momo(object):
        def __init__(self):
            self.momodata = "Some data"
            self.r = requests.get('http://www.google.com')

        def raiser(self):
            raise Exception("BOOM!")

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(my_coroutine())
        )
        loop.close()
        foo()
    except:
        from pypm import pypm
        filename = __file__ + '.dump'
        print("Exception caught, writing %s" % filename)
        pypm.save_dump(filename)
        print("Run 'pypm %s' to debug" % (filename))
