#!/usr/bin/env python
# -*- coding:utf-8 -*-

import io

from setuptools import setup

setup(
    name='qnapstats',
    description='Python API for obtaining QNAP NAS system stats',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    version='0.3.0',
    license='MIT',
    author='Colin O\'Dell',
    author_email='colinodell@gmail.com',
    url='https://github.com/colinodell/python-qnapstats',
    packages=['qnapstats'],
    keywords=['qnap'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Home Automation',
        'Topic :: System :: Monitoring'
    ],
    install_requires=['requests>=1.0.0', 'xmltodict>=0.10.0']
)
