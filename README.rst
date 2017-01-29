================
python-qnapstats
================

.. image:: https://img.shields.io/travis/colinodell/python-qnapstats/master.svg?style=flat-square
   :target: https://travis-ci.org/colinodell/python-qnapstats
   :alt: Build Status

Library from obtaining system information from QNAP NAS devices.

Installation
============

This library requires `xmltodict`, so make sure you have that installed:

.. code-block:: bash

    pip3 install xmltodict>=0.10.0

Then install this Python module:

.. code-block:: bash

    pip3 install qnapstats

Usage Example
=============

.. code-block:: python

    from from qnapstats import QNAPStats
    from pprint import pprint
    
    qnap = QNAPStats('192.168.1.3', 8080, 'admin', 'correcthorsebatterystaple')
    
    pprint(qnap.get_system_stats())
    pprint(qnap.get_system_health())
    pprint(qnap.get_smart_disk_health())
    pprint(qnap.get_volumes())
    pprint(qnap.get_bandwidth())

Device Support
==============

This library has been tested against the latest QTS 4.2.2 firmware on a QNAP TS-451.  Other devices using this firmware should work fine.
If you encounter any compatibility issues, please let us know (or better yet, contribute a patch!)
