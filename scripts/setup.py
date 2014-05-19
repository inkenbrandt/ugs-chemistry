from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

import dbseeder


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='dbseeder',
    version=dbseeder.__version__,
    url='https://github.com/agrc/ugs-chemistry',
    license='MIT',
    author='Steve Gourley',
    tests_require=['pytest', 'mock'],
    install_requires=['requests>=2.3.0'],
    cmdclass={'test': PyTest},
    author_email='sgourley@utah.gov',
    description='build and seed a file geodatabase',
    long_description='',
    packages=['dbseeder'],
    include_package_data=True,
    platforms='any',
    test_suite='dbseeder.test.test_dbseeder',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: Windows'
    ],
    extras_require={
        'testing': ['pytest'],
    }
)
