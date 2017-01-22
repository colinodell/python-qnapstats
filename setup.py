#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name='qnapstats',
    description='Python API for obtaining QNAP NAS system stats',
    version='0.1.0',
    license='MIT',
    author='Colin O\'Dell',
    author_email='colinodell@gmail.com',
    url='https://github.com/colinodell/python-qnapstats',
    packages=['qnapstats'],
    keywords=['qnap'],
    classifiers=[
        'Home Automation',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Monitoring'
    ],
    install_requires=['requests>=1.0.0', 'lxml']
)
