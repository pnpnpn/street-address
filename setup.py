# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ]

setup( 
        name='street-address',
        version='0.1.1',
        description='Street address parser and formatter',
        long_description = open('README.rst').read(),
        author='PN',
        author_email='pn.appdev@gmail.com',
        url='https://github.com/pnpnpn/street-address',
        packages=['streetaddress'],
        install_requires=[],
        test_suite='tests',
        classifiers=CLASSIFIERS)


