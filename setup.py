# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


try:
    long_description = open('README.md').read()
except:
    long_description = u'Street address parser and formatter'


CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ]

setup( 
        name='street-address',
        version='0.4.0',
        description='Street address parser and formatter',
        long_description=long_description,
        author='PN',
        author_email='pn.appdev@gmail.com',
        url='https://github.com/pnpnpn/street-address',
        packages=['streetaddress'],
        install_requires=[],
        test_suite='tests',
        classifiers=CLASSIFIERS)


