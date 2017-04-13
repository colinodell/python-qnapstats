================
python-qnapstats
================

.. image:: https://img.shields.io/travis/colinodell/python-qnapstats/master.svg?style=flat-square
   :target: https://travis-ci.org/colinodell/python-qnapstats
   :alt: Build Status
.. image:: https://img.shields.io/pypi/pyversions/qnapstats.svg?style=flat-square
   :target: https://pypi.python.org/pypi/qnapstats
   :alt: Supported Python Versions

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

    #!/usr/bin/env python3
    from qnapstats import QNAPStats
    from pprint import pprint
    
    qnap = QNAPStats('192.168.1.3', 8080, 'admin', 'correcthorsebatterystaple')
    
    pprint(qnap.get_system_stats())
    pprint(qnap.get_system_health())
    pprint(qnap.get_smart_disk_health())
    pprint(qnap.get_volumes())
    pprint(qnap.get_bandwidth())

Device Support
==============

This library has been tested against the following devices and firmwares:

+--------+-----------------------+---------------------------------------+
| Model  | QTS Firmware Versions | Notes                                 |
+========+=======================+=======================================+
| TS-110 | 4.2.4                 |                                       |
+--------+-----------------------+---------------------------------------+
| TS-410 | 4.2.3                 | This device does not report CPU temps |
+--------+-----------------------+---------------------------------------+
| TS-451 | 4.2.2, 4.2.3, 4.2.4   |                                       |
+--------+-----------------------+---------------------------------------+
| TS-639 | 4.2.3                 |                                       |
+--------+-----------------------+---------------------------------------+

Other devices using these firmwares should probably work fine.
If you encounter any compatibility issues, please let us know (or better yet, contribute a patch!)
