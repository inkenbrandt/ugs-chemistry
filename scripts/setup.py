from __future__ import print_function
from setuptools import setup
import dbseeder


setup(
    name='dbseeder',
    version=dbseeder.__version__,
    url='https://github.com/agrc/ugs-chemistry',
    license='MIT',
    author='Steve Gourley',
    tests_require=['nose>=1.0', 'mock>=1.0'],
    install_requires=['requests>=2.3.0', 'pyproj>=1.9.0'],
    # setup_requires=['nose>=1.0'],
    author_email='sgourley@utah.gov',
    description='build and seed a file geodatabase',
    long_description='',
    packages=['dbseeder'],
    include_package_data=True,
    platforms='any',
    test_suite='nose.collector',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: Windows'
    ],
    extras_require={
        'testing': ['nose'],
    }
)
