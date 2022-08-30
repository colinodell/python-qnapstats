================
python-qnapstats
================

.. image:: https://img.shields.io/github/workflow/status/colinodell/python-qnapstats/Test/master.svg?style=flat-square
   :target: https://github.com/colinodell/python-qnapstats/actions?query=workflow%3ATest+branch%3Amaster
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
    pprint(qnap.get_download_station_status())

**Note:** The user you connect with must be in the admin group. It doesn't necessarily
need to be THE "administrator" account, but you do need to use some account in the
administrators group.

Device Support
==============

This library has been tested against the following devices and firmwares:

+--------------+-----------------------+---------------------------------------+
| Model        | QTS Firmware Versions | Notes                                 |
+==============+=======================+=======================================+
| D4 Pro       | 4.5.1                 | User-reported: no automated tests     |
+--------------+-----------------------+---------------------------------------+
| TS-110       | 4.2.4                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-210       | 4.2.6                 | This device does not report CPU temps |
+--------------+-----------------------+---------------------------------------+
| TS-219P II   | 4.3.3                 | User-reported: no automated tests     |
+--------------+-----------------------+---------------------------------------+
| TS-251B      | 4.4.3                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-251+      | 4.5.1                 | No information on dnsInfo             |
+--------------+-----------------------+---------------------------------------+
| TS-253 Pro   | 4.5.2                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-253D      | 4.5.3                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-332       | 5.0.0                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-269L      | 4.3.3                 | User-reported: no automated tests     |
+--------------+-----------------------+---------------------------------------+
| TS-410       | 4.2.3                 | This device does not report CPU temps |
+--------------+-----------------------+---------------------------------------+
| TS-412       | 4.3.3                 | This device does not report CPU temps |
+--------------+-----------------------+---------------------------------------+
| TS-431P      | 4.3.4                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-451       | 4.2.2 - 4.2.4         |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-453A      | 4.3.4                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-453Be     | 4.2.3                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-639       | 4.2.3                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-659       | 4.2.6                 | May report `None` for some disk temps |
+--------------+-----------------------+---------------------------------------+
| TS-853 Pro   | 4.5.4                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-869 Pro   | 4.3.4                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-1677XU-RP | 4.5.2                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-EC1280U   | 4.5.2                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-X53       | 4.5.4                 |                                       |
+--------------+-----------------------+---------------------------------------+
| TS-231+      | 5.0.0                 |                                       |
+--------------+-----------------------+---------------------------------------+

Other QNAP devices using these firmwares should probably work fine, as should the devices listed above on newer firmwares.
If you encounter any compatibility issues, please let us know (or better yet, contribute a patch!)
