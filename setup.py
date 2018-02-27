from setuptools import setup

DESCRIPTION = """
pypm allows post-mortem debugging for Python programs.

It writes the traceback of an exception into a file and can later load
it in a Python debugger.

Works with the built-in pdb and with other popular debuggers
(pudb, ipdb and pdbpp).
"""

# get version without importing
__version__ = 'unknown'
for line in open('pypm/pypm.py'):
    if line.startswith('__version__ = '):
        exec(line)
        break

setup(
    name='pm.py',
    version=__version__,
    description='Post-mortem debugging for Python programs',
    long_description=DESCRIPTION,
    author='Jordi Masip',
    license='MIT',
    author_email='jordi.masip@onna.com',
    url='https://github.com/onna/pypm',
    package_dir={'pypm': 'pypm'},
    packages=['pypm'],
    install_requires=['dill'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Debuggers'
    ]
)
